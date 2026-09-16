# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductSupplierinfoCaryvil(models.Model):
    _inherit = 'product.supplierinfo'

    product_presentation = fields.Char(
        string='Presentación Proveedor',
        help='Ej: Caja con 100 tabletas',
    )
    discount_percentage = fields.Float(string='% Descuento Comercial', default=0.0)

    # Si se llena un % de descuento, recalcula el precio unitario en automático.
    @api.onchange('discount_percentage')
    def _onchange_discount_percentage(self):
        if self.discount_percentage > 0 and self.price > 0:
            self.price = self.price * (1 - (self.discount_percentage / 100.0))
