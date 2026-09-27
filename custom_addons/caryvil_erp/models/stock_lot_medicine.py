# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
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
            lot.is_expired = bool(lot.expiration_date and lot.expiration_date < now)

    @api.model
    def _cron_update_expired_lots(self):
        """Cron diario para sincronizar el estado de caducidad de lotes."""
        now = fields.Datetime.now()
        expired_lots = self.search(
            [
                ("expiration_date", "<", now),
                ("is_expired", "=", False),
            ]
        )
        if expired_lots:
            expired_lots.write({"is_expired": True})

        valid_lots = self.search(
            [
                ("expiration_date", ">=", now),
                ("is_expired", "=", True),
            ]
        )
        if valid_lots:
            valid_lots.write({"is_expired": False})

    @api.onchange("expiration_date")
    def _onchange_expiration_date_set_alerts(self):
        """Calcula fechas sugeridas de alerta (60 días) y retiro (15 días) antes de vencer."""
        if self.expiration_date:
            if not self.alert_date:
                self.alert_date = fields.Datetime.subtract(self.expiration_date, days=60)
            if not self.removal_date:
                self.removal_date = fields.Datetime.subtract(self.expiration_date, days=15)

    @api.model_create_multi
    def create(self, vals_list):
        """Asigna alert_date y removal_date por defecto si no fueron especificados."""
        for vals in vals_list:
            exp_date_raw = vals.get("expiration_date")
            if exp_date_raw:
                exp_date = fields.Datetime.to_datetime(exp_date_raw)
                if not vals.get("alert_date"):
                    vals["alert_date"] = fields.Datetime.subtract(exp_date, days=60)
                if not vals.get("removal_date"):
                    vals["removal_date"] = fields.Datetime.subtract(exp_date, days=15)
        return super().create(vals_list)

    @api.constrains("expiration_date")
    def _check_expiration_date(self):
        """Valida que la fecha de caducidad sea coherente y no anterior a creación/recepción."""
        if self.env.context.get("bypass_expiration_check"):
            return

        now = fields.Datetime.now()
        for lot in self:
            if not lot.expiration_date:
                continue

            ref_date = lot.create_date or now
            if lot.expiration_date < ref_date:
                raise ValidationError(
                    _(
                        "La fecha de vencimiento del lote (%s) no puede ser anterior "
                        "a su fecha de creación/recepción."
                    )
                    % lot.name
                )

            max_future = ref_date + relativedelta(years=10)
            if lot.expiration_date > max_future:
                raise ValidationError(
                    _(
                        "La fecha de vencimiento del lote (%s) no puede exceder "
                        "un rango lógico de 10 años en el futuro."
                    )
                    % lot.name
                )

    def write(self, vals):
        if "expiration_date" in vals:
            is_admin = (
                self.env.user.has_group("caryvil_erp.group_caryvil_manager")
                or self.env.user.has_group("stock.group_stock_manager")
                or self.env.user.has_group("base.group_system")
            )
            if not is_admin and not self.env.context.get("install_mode"):
                raise ValidationError(
                    _(
                        "Solo un Administrador de Farmacia Caryvil puede modificar "
                        "la fecha de vencimiento de un lote."
                    )
                )

            exp_date_raw = vals.get("expiration_date")
            if exp_date_raw:
                exp_date = fields.Datetime.to_datetime(exp_date_raw)
                if "alert_date" not in vals:
                    vals["alert_date"] = fields.Datetime.subtract(exp_date, days=60)
                if "removal_date" not in vals:
                    vals["removal_date"] = fields.Datetime.subtract(exp_date, days=15)

            old_dates = {lot.id: lot.expiration_date for lot in self}
            result = super().write(vals)

            for lot in self:
                if old_dates.get(lot.id) != lot.expiration_date:
                    lot.message_post(
                        body=_("Fecha de vencimiento modificada: <b>%s</b> → <b>%s</b>.")
                        % (
                            old_dates.get(lot.id) or _("Sin fecha"),
                            lot.expiration_date or _("Sin fecha"),
                        )
                    )
            return result

        return super().write(vals)
