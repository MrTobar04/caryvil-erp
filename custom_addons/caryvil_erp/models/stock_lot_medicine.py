# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class StockLotMedicine(models.Model):
    _inherit = "stock.lot"

    is_expired = fields.Boolean(
        string="Lote Vencido",
        compute="_compute_is_expired",
        store=True,
        index=True,
    )

    @api.depends("expiration_date")
    def _compute_is_expired(self):
        now = fields.Datetime.now()

        for lot in self:
            lot.is_expired = bool(
                lot.expiration_date
                and lot.expiration_date < now
            )

    @api.constrains("expiration_date")
    def _check_expiration_date(self):
        return

    def write(self, vals):
        if "expiration_date" not in vals:
            return super().write(vals)

        if not self.env.user.has_group("base.group_system"):
            raise ValidationError(
                _(
                    "Solo un Administrador puede modificar "
                    "la fecha de vencimiento de un lote."
                )
            )

        old_dates = {
            lot.id: lot.expiration_date
            for lot in self
        }

        result = super().write(vals)

        for lot in self:
            if old_dates[lot.id] != lot.expiration_date:
                lot.message_post(
                    body=_(
                        "Fecha de vencimiento modificada: "
                        "<b>%s</b> → <b>%s</b>."
                    )
                    % (
                        old_dates[lot.id] or _("Sin fecha"),
                        lot.expiration_date or _("Sin fecha"),
                    )
                )

        return result