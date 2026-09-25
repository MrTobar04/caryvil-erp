# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
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
        readonly=True,
        copy=False,
        help="Usuario que registró el conteo físico en estantería.",
    )

    validated_by_user_id = fields.Many2one(
        "res.users",
        string="Validado por",
        readonly=True,
        copy=False,
        help="Administrador que aprobó y aplicó el ajuste.",
    )

    @api.constrains("inventory_quantity", "inventory_quantity_set")
    def _check_inventory_quantity_non_negative(self):
        for quant in self:
            if quant.inventory_quantity_set and quant.inventory_quantity < 0:
                raise ValidationError(
                    _(
                        "La cantidad física contada no puede ser negativa (%s) "
                        "para el producto %s."
                    )
                    % (quant.inventory_quantity, quant.product_id.display_name)
                )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "inventory_quantity" in vals and "counted_by_user_id" not in vals:
                vals["counted_by_user_id"] = self.env.user.id
                if "user_id" not in vals:
                    vals["user_id"] = self.env.user.id
        return super().create(vals_list)

    def write(self, vals):
        if "inventory_quantity" in vals and "counted_by_user_id" not in vals:
            vals["counted_by_user_id"] = self.env.user.id
            if "user_id" not in vals:
                vals["user_id"] = self.env.user.id
        return super().write(vals)

    @api.onchange("inventory_quantity")
    def _onchange_inventory_quantity(self):
        if hasattr(super(), "_onchange_inventory_quantity"):
            super()._onchange_inventory_quantity()
        if self.inventory_quantity_set or self.inventory_quantity is not False:
            self.counted_by_user_id = self.env.user
            self.user_id = self.env.user

    def action_apply_inventory(self):
        if not self.env.user.has_group("caryvil_erp.group_caryvil_manager"):
            raise UserError(
                _("Solo el Administrador / Propietario puede aplicar ajustes de inventario.")
            )

        for quant in self:
            if quant.inventory_quantity_set:
                if quant.inventory_quantity < 0:
                    raise ValidationError(
                        _(
                            "La cantidad física contada no puede ser negativa (%s) "
                            "para el producto %s."
                        )
                        % (quant.inventory_quantity, quant.product_id.display_name)
                    )

                if not fields.Float.is_zero(
                    quant.inventory_diff_quantity,
                    precision_rounding=quant.product_uom_id.rounding,
                ):
                    if not quant.adjustment_reason:
                        raise ValidationError(
                            _(
                                "Debe especificar el Motivo del Ajuste "
                                "para el producto %s."
                            )
                            % quant.product_id.display_name
                        )

                    if quant.product_id.tracking in ("lot", "serial") and not quant.lot_id:
                        raise ValidationError(
                            _(
                                "Debe especificar el lote para el producto "
                                "con seguimiento: %s."
                            )
                            % quant.product_id.display_name
                        )

                quant.validated_by_user_id = self.env.user

        return super().action_apply_inventory()

    def _get_inventory_move_values(
        self, qty, location_id, location_dest_id, package_id=False, package_dest_id=False
    ):
        res = super()._get_inventory_move_values(
            qty,
            location_id,
            location_dest_id,
            package_id=package_id,
            package_dest_id=package_dest_id,
        )
        if self.adjustment_reason:
            reason_label = dict(
                self._fields["adjustment_reason"].selection
            ).get(self.adjustment_reason, self.adjustment_reason)
            res["origin"] = _("Ajuste de Inventario: %s") % reason_label
            notes_str = f" | Notas: {self.adjustment_notes}" if self.adjustment_notes else ""
            counter_str = (
                f" | Contado por: {self.counted_by_user_id.name}"
                if self.counted_by_user_id
                else ""
            )
            res["description_picking"] = (
                _("Motivo: %s%s%s") % (reason_label, notes_str, counter_str)
            )
        return res
