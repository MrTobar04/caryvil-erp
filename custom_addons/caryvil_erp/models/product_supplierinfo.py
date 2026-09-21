# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductSupplierinfoCaryvil(models.Model):
    _inherit = "product.supplierinfo"

    product_presentation = fields.Char(
        string="Presentación Proveedor",
        help="Ej: Caja con 100 tabletas, Frasco 120ml",
    )
    gross_price = fields.Monetary(
        string="Precio Lista / Bruto",
        currency_field="currency_id",
        help="Precio de lista oficial del laboratorio antes de aplicar descuentos comerciales.",
    )
    discount_percentage = fields.Float(
        string="% Descuento Comercial",
        default=0.0,
        help="Porcentaje de descuento comercial otorgado por el laboratorio (0 a 100%).",
    )

    @api.onchange("gross_price", "discount_percentage")
    def _onchange_pricing_caryvil(self):
        """Calcula el precio neto unitario (price) sin degradación compuesta."""
        for record in self:
            if record.gross_price > 0:
                discount = max(0.0, min(record.discount_percentage, 100.0))
                record.price = record.gross_price * (1.0 - (discount / 100.0))
            elif record.price > 0 and not record.gross_price:
                record.gross_price = record.price

    @api.onchange("price")
    def _onchange_price_sync_gross(self):
        """Sincroniza el precio bruto si el usuario digita directamente el precio neto sin descuento."""
        for record in self:
            if record.price > 0 and record.discount_percentage == 0.0 and not record.gross_price:
                record.gross_price = record.price
