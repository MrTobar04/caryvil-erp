# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockWarehouseOrderpointMedicine(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    suggested_replenishment_qty = fields.Float(
        string="Cantidad Sugerida a Comprar",
        compute="_compute_suggested_qty",
    )

    @api.depends(
        "product_id",
        "product_min_qty",
        "product_max_qty",
        "qty_multiple",
    )
    def _compute_suggested_qty(self):
        for rule in self:
            virtual_stock = rule.product_id.virtual_available

            if virtual_stock < rule.product_min_qty:
                needed = rule.product_max_qty - virtual_stock

                if rule.qty_multiple > 1:
                    remainder = needed % rule.qty_multiple
                    if remainder > 0:
                        needed += rule.qty_multiple - remainder

                rule.suggested_replenishment_qty = max(needed, 0.0)
            else:
                rule.suggested_replenishment_qty = 0.0
