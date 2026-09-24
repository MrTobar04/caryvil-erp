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
    # NOTA: solo aplica a productos con tracking='lot'. El catálogo de medicamentos de Caryvil
    # aún no tiene ese seguimiento activado (pendiente en SPEC-7.1.1/7.1.2), así que hasta que se
    # active, esta validación no bloqueará ninguna recepción.
    def button_validate(self):
        today = fields.Datetime.now()
        for picking in self:
            if picking.picking_type_code == "incoming":
                for line in picking.move_line_ids:
                    product = line.product_id
                    if product.tracking == "lot" and line.quantity > 0:
                        if not line.lot_id and not line.lot_name:
                            raise ValidationError(
                                _("Debe asignar el Número de Lote para el medicamento %s en la recepción.")
                                % product.name
                            )
                        if line.lot_name and not line.expiration_date:
                            raise ValidationError(
                                _("Debe especificar la Fecha de Vencimiento para el lote %s del producto %s.")
                                % (line.lot_name, product.name)
                            )
                        if line.expiration_date and line.expiration_date < today:
                            raise ValidationError(
                                _(
                                    "La fecha de vencimiento (%s) del lote %s ya está caducada. "
                                    "No se puede recibir mercadería vencida."
                                )
                                % (line.expiration_date, line.lot_name)
                            )
            # Bloquea la dispensación de lotes vencidos.
            if picking.picking_type_code == "outgoing":
                for line in picking.move_line_ids:
                    if line.quantity > 0 and line.lot_id and line.lot_id.is_expired:
                        raise ValidationError(
                            _(
                                "No es posible dispensar el lote %s "
                                "porque se encuentra vencido."
                            )
                            % line.lot_id.name
                        )

        
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
                        "Discrepancia detectada en la recepción %s: la cantidad recibida es menor " "a la ordenada. %s"
                    )
                    % (picking.name, picking.discrepancy_notes or "Sin notas adicionales.")
                )

    # SPEC-8.2.2: bloquea (Lock) automáticamente la Orden de Compra cuando ya se recibió todo lo pedido.
    # El resto de la actualización de stock (stock.quant, balance del lote, qty_received) ya es
    # comportamiento nativo de Odoo (módulo purchase_stock) y no requiere código adicional.
    def _caryvil_lock_fully_received_purchase_orders(self):
        orders = self.mapped("move_ids.purchase_line_id.order_id")
        for order in orders:
            if (
                order.state == "purchase"
                and order.order_line
                and all(line.qty_received >= line.product_qty for line in order.order_line)
            ):
                order.button_done()
