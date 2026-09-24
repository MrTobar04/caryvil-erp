# -*- coding: utf-8 -*-

from odoo import _, fields, models
from odoo.exceptions import UserError, ValidationError


class StockQuantAdjustment(models.Model):
    _inherit = "stock.quant"

    adjustment_reason = fields.Selection(
        [
            ("ajuste_inicial", "Carga de Inventario Inicial"),
            ("conteo_ciclico_periodico", "Conteo Cíclico Periódico"),
            ("error_conteo_previo", "Corrección de Conteo Previo"),
            ("diferencia_despacho", "Diferencia en Despacho"),
            ("otro", "Otro Motivo"),
        ],
        string="Motivo del Ajuste",
        default="conteo_ciclico_periodico",
    )

    adjustment_notes = fields.Text(
        string="Observaciones / Justificación",
    )

    counted_by_user_id = fields.Many2one(
        "res.users",
        string="Contado por",
        related="user_id",
        store=True,
        readonly=True,
    )

    validated_by_user_id = fields.Many2one(
        "res.users",
        string="Validado por",
        readonly=True,
    )

    def action_apply_inventory(self):
        for quant in self:
            if quant.inventory_quantity_set and not fields.Float.is_zero(
                quant.inventory_diff_quantity,
                precision_rounding=quant.product_uom_id.rounding,
            ):
                if not quant.adjustment_reason:
                    raise ValidationError(
                        _("Debe especificar el Motivo del Ajuste " "para el producto %s.")
                        % quant.product_id.display_name
                    )

                if quant.product_id.tracking in ("lot", "serial") and not quant.lot_id:
                    raise ValidationError(
                        _("Debe especificar el lote para el producto " "con seguimiento: %s.")
                        % quant.product_id.display_name
                    )

            if not self.env.user.has_group("caryvil_erp.group_caryvil_manager"):
                raise UserError(_("Solo el Administrador / Propietario " "puede aplicar ajustes de inventario."))

            if quant.inventory_quantity_set:
                quant.validated_by_user_id = self.env.user

        return super().action_apply_inventory()
