# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.osv import expression


class StockQuantFEFO(models.Model):
    _inherit = "stock.quant"

    @api.model
    def _get_removal_strategy_domain_order(
        self,
        domain,
        removal_strategy,
        qty,
    ):
        domain, order = super()._get_removal_strategy_domain_order(
            domain,
            removal_strategy,
            qty,
        )

        if removal_strategy != "fefo":
            return domain, order

        # Un lote vencido no puede participar en la reserva FEFO.
        now = fields.Datetime.now()

        domain = expression.AND(
            [
                domain,
                [
                    ("expiration_date", ">", now),
                ],
            ]
        )

        # Prioridad FEFO por fecha de vencimiento. Se mantienen in_date e id como desempates.
        return domain, "expiration_date ASC, in_date ASC, id ASC"
