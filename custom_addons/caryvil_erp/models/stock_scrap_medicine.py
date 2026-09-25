# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class StockScrapMedicine(models.Model):
    _inherit = "stock.scrap"

    scrap_reason = fields.Selection(
        [
            ("medicamento_vencido", "Medicamento Caducado / Vencido"),
            ("rotura_frasco_ampolla", "Rotura de Frasco / Ampolla"),
            ("empaque_deteriorado_humedad", "Deterioro de Empaque / Humedad"),
            ("retiro_sanitario_laboratorio", "Retiro Sanitario por Laboratorio"),
            ("otro", "Otra Causa"),
        ],
        string="Causa de la Merma",
        required=True,
        default="medicamento_vencido",
    )

    scrap_unit_cost = fields.Monetary(
        string="Costo Unitario ($)",
        currency_field="currency_id",
        compute="_compute_scrap_costs",
        store=True,
    )

    scrap_total_loss = fields.Monetary(
        string="Pérdida Total ($)",
        currency_field="currency_id",
        compute="_compute_scrap_costs",
        store=True,
    )

    currency_id = fields.Many2one(
        "res.currency",
        string="Moneda",
        default=lambda self: self.env.company.currency_id,
    )

    justification_notes = fields.Text(
        string="Justificación / Observaciones",
    )

    authorized_by_id = fields.Many2one(
        "res.users",
        string="Autorizado por",
        readonly=True,
    )

    authorization_date = fields.Datetime(
        string="Fecha de Autorización",
        readonly=True,
    )

    @api.depends("product_id", "scrap_qty", "product_uom_id")
    def _compute_scrap_costs(self):
        for scrap in self:
            if not scrap.product_id:
                scrap.scrap_unit_cost = 0.0
                scrap.scrap_total_loss = 0.0
                continue

            base_cost = scrap.product_id.standard_price or 0.0
            if (
                scrap.product_uom_id
                and scrap.product_id.uom_id
                and scrap.product_uom_id != scrap.product_id.uom_id
            ):
                unit_cost = scrap.product_id.uom_id._compute_price(
                    base_cost, scrap.product_uom_id
                )
            else:
                unit_cost = base_cost

            scrap.scrap_unit_cost = unit_cost
            scrap.scrap_total_loss = unit_cost * (scrap.scrap_qty or 0.0)

    @api.depends("company_id", "location_id")
    def _compute_scrap_location_id(self):
        super()._compute_scrap_location_id()

        caryvil_location = self.env.ref(
            "caryvil_erp.stock_location_scrap_caryvil",
            raise_if_not_found=False,
        )

        if not caryvil_location:
            return

        for scrap in self:
            if not caryvil_location.company_id or scrap.company_id == caryvil_location.company_id:
                scrap.scrap_location_id = caryvil_location

    def _check_scrap_prerequisites(self):
        precision = self.env["decimal.precision"].precision_get("Product Unit of Measure")
        for scrap in self:
            if not self.env.user.has_group("caryvil_erp.group_caryvil_manager"):
                raise UserError(
                    _("Solo el Administrador / Propietario puede autorizar la baja del medicamento.")
                )

            if scrap.product_id.tracking in ("lot", "serial") and not scrap.lot_id:
                raise ValidationError(
                    _("Debe especificar el número de lote para dar de baja el medicamento %s.")
                    % scrap.product_id.display_name
                )

            if scrap.scrap_qty <= 0:
                raise ValidationError(_("La cantidad a dar de baja debe ser mayor a cero."))

            if scrap.product_id.detailed_type == "product" and scrap.location_id.usage == "internal":
                available_qty = self.env["stock.quant"]._get_available_quantity(
                    scrap.product_id,
                    scrap.location_id,
                    lot_id=scrap.lot_id,
                    strict=True,
                )
                scrap_qty_in_prod_uom = scrap.product_uom_id._compute_quantity(
                    scrap.scrap_qty, scrap.product_id.uom_id
                )
                if float_compare(scrap_qty_in_prod_uom, available_qty, precision_digits=precision) > 0:
                    lot_name = scrap.lot_id.name if scrap.lot_id else _("Sin lote")
                    raise ValidationError(
                        _(
                            "No se puede dar de baja una cantidad superior a la existencia física disponible "
                            "en el lote seleccionado.\n"
                            "- Medicamento: %s\n"
                            "- Lote: %s\n"
                            "- Cantidad solicitada: %s %s\n"
                            "- Existencia física disponible: %s %s"
                        )
                        % (
                            scrap.product_id.display_name,
                            lot_name,
                            scrap.scrap_qty,
                            scrap.product_uom_id.name,
                            scrap.product_id.uom_id._compute_quantity(available_qty, scrap.product_uom_id),
                            scrap.product_uom_id.name,
                        )
                    )

    def action_validate(self):
        self._check_scrap_prerequisites()
        return super().action_validate()

    def do_scrap(self):
        self._check_scrap_prerequisites()
        for scrap in self:
            scrap.authorized_by_id = self.env.user
            scrap.authorization_date = fields.Datetime.now()
        return super().do_scrap()

    def write(self, vals):
        protected_fields = {
            "scrap_reason",
            "justification_notes",
            "scrap_qty",
            "lot_id",
            "product_id",
            "location_id",
            "scrap_location_id",
        }
        for scrap in self:
            if scrap.state == "done" and any(field in vals for field in protected_fields):
                raise UserError(
                    _(
                        "No se pueden modificar los datos de una merma farmacéutica "
                        "que ya ha sido autorizada y procesada."
                    )
                )
        return super().write(vals)

    def unlink(self):
        for scrap in self:
            if scrap.state == "done":
                raise UserError(
                    _("No se puede eliminar un registro de merma y baja farmacéutica que ya ha sido procesado.")
                )
        return super().unlink()
