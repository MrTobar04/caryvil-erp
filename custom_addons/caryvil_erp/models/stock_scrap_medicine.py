# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


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

    @api.depends("product_id", "scrap_qty")
    def _compute_scrap_costs(self):
        for scrap in self:
            cost = scrap.product_id.standard_price or 0.0
            scrap.scrap_unit_cost = cost
            scrap.scrap_total_loss = cost * scrap.scrap_qty

    @api.depends("company_id", "location_id")
    def _compute_scrap_location_id(self):
        super()._compute_scrap_location_id()

        caryvil_location = self.env.ref(
            "caryvil_erp.stock_location_scrap_caryvil",
            raise_if_not_found=False,
        )

        if not caryvil_location:
            return

        for scrap in self.filtered(lambda record: record.company_id == caryvil_location.company_id):
            scrap.scrap_location_id = caryvil_location

    def action_validate(self):
        for scrap in self:
            if scrap.product_id.tracking in ("lot", "serial") and not scrap.lot_id:
                raise ValidationError(
                    _("Debe especificar el número de lote " "para dar de baja el medicamento %s.")
                    % scrap.product_id.display_name
                )

            if not self.env.user.has_group("caryvil_erp.group_caryvil_manager"):
                raise UserError(_("Solo el Administrador / Propietario " "puede autorizar la baja del medicamento."))

            scrap.authorized_by_id = self.env.user

        return super().action_validate()
