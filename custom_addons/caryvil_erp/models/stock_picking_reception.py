# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StockMoveLineReception(models.Model):
    _inherit = "stock.move.line"

    expiration_date = fields.Datetime(string="Fecha de Vencimiento")


class StockPickingReception(models.Model):
    _inherit = "stock.picking"

    has_discrepancy = fields.Boolean(
        string="Presenta Discrepancia",
        compute="_compute_has_discrepancy",
        store=True,
    )
    discrepancy_notes = fields.Text(string="Detalle de Discrepancia / Daños")

    # SPEC-8.2.1: exige lote y fecha de vencimiento antes de validar una recepción de medicamentos.
    def _check_expired_lots_on_outgoing(self, picking):
        if picking.picking_type_code != "outgoing":
            return

        now = fields.Datetime.now()
        for line in picking.move_line_ids:
            if line.quantity > 0 and line.lot_id:
                lot = line.lot_id
                if lot.is_expired or (lot.expiration_date and lot.expiration_date < now):
                    raise ValidationError(
                        _("No es posible dispensar el lote %s porque se encuentra vencido.") % lot.name
                    )

    def _find_expiration_date_from_siblings_or_db(self, line):
        """Busca fecha de vencimiento en líneas hermanas, backorders o lotes existentes."""
        siblings = (line.move_id.move_line_ids | line.picking_id.move_line_ids).filtered(
            lambda ml: ml.expiration_date
        )
        if siblings:
            return siblings[0].expiration_date

        if line.picking_id.backorder_id:
            backorder_lines = line.picking_id.backorder_id.move_line_ids
            bo_siblings = backorder_lines.filtered(
                lambda ml: (
                    ml.lot_name == line.lot_name
                    or (ml.lot_id and ml.lot_id.name == line.lot_name)
                )
                and ml.expiration_date
            )
            if bo_siblings:
                return bo_siblings[0].expiration_date

        existing_lot = self.env["stock.lot"].search(
            [
                ("name", "=", line.lot_name),
                ("product_id", "=", line.product_id.id),
                ("expiration_date", "!=", False),
            ],
            limit=1,
        )
        return existing_lot.expiration_date if existing_lot else False

    def _process_incoming_line_lot_expiration(self, line, today):
        """Procesa la asignación y validación de fecha de vencimiento para una línea de recepción."""
        product = line.product_id
        if product.tracking != "lot" or line.quantity <= 0:
            return

        if not line.lot_id and not line.lot_name:
            raise ValidationError(
                _("Debe asignar el Número de Lote ") + _("para el medicamento %s en la recepción.") % product.name
            )

        exp_date = line.expiration_date or (line.lot_id.expiration_date if line.lot_id else False)
        if not exp_date and line.lot_name:
            exp_date = self._find_expiration_date_from_siblings_or_db(line)
            if exp_date:
                line.expiration_date = exp_date

        ctx = self.env.context
        if line.lot_name and not exp_date:
            if ctx.get("skip_backorder") or ctx.get("picking_ids_not_to_backorder"):
                return
            raise ValidationError(
                _("Debe especificar la Fecha de Vencimiento ")
                + _("para el lote %s del producto %s.") % (line.lot_name, product.name)
            )

        if exp_date and exp_date < today:
            raise ValidationError(
                _(
                    "La fecha de vencimiento (%s) del lote %s "
                    "ya está caducada. No se puede recibir "
                    "mercadería vencida."
                )
                % (line.expiration_date, line.lot_name)
            )

    def button_validate(self):
        today = fields.Datetime.now()
        for picking in self:
            if picking.picking_type_code == "incoming":
                for line in picking.move_line_ids:
                    self._process_incoming_line_lot_expiration(line, today)

            self._check_expired_lots_on_outgoing(picking)

        result = super().button_validate()
        self._caryvil_notify_discrepancy()
        self._caryvil_lock_fully_received_purchase_orders()
        return result

    # SPEC-8.2.3: detecta discrepancias (cantidad recibida menor a la ordenada) al validar la recepción.
    @api.depends("move_ids.quantity", "move_ids.product_uom_qty", "state")
    def _compute_has_discrepancy(self):
        for picking in self:
            discrepancy = False
            if picking.picking_type_code == "incoming" and picking.state == "done":
                for move in picking.move_ids:
                    if move.quantity < move.product_uom_qty:
                        discrepancy = True
                        break
            picking.has_discrepancy = discrepancy

    # SPEC-8.2.3: notifica al Encargado de Compras en el chatter cuando hay discrepancia.
    def _caryvil_notify_discrepancy(self):
        for picking in self:
            if picking.has_discrepancy:
                picking.message_post(
                    body=_(
                        "Discrepancia detectada en la recepción %s: la cantidad recibida es menor "
                        "a la ordenada. %s"
                    )
                    % (picking.name, picking.discrepancy_notes or "Sin notas adicionales.")
                )

    # SPEC-8.2.2: bloquea (Lock) automáticamente la Orden de Compra cuando ya se recibió todo lo pedido.
    def _caryvil_lock_fully_received_purchase_orders(self):
        orders = self.mapped("move_ids.purchase_line_id.order_id")
        for order in orders:
            if (
                order.state == "purchase"
                and order.order_line
                and all(line.qty_received >= line.product_qty for line in order.order_line)
            ):
                order.button_done()
