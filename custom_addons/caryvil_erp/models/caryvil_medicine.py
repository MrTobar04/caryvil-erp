# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CaryvilTherapeuticCategory(models.Model):
    _name = "caryvil.therapeutic.category"
    _description = "Categoría Terapéutica Farmacéutica"

    name = fields.Char(string="Categoría", required=True, index=True)
    code = fields.Char(string="Código ATC / Clave", size=10)
    description = fields.Text(string="Descripción / Uso Terapéutico")


class CaryvilActiveIngredient(models.Model):
    _name = "caryvil.active.ingredient"
    _description = "Principio Activo"

    name = fields.Char(string="Nombre del Principio Activo", required=True, index=True)
    description = fields.Text(string="Acción Farmacológica")


class ProductTemplateMedicine(models.Model):
    _inherit = "product.template"

    detailed_type = fields.Selection(default="product")

    tracking = fields.Selection(default="lot")

    active_ingredient_id = fields.Many2one(
        "caryvil.active.ingredient",
        string="Principio Activo",
        index=True,
    )

    therapeutic_category_id = fields.Many2one(
        "caryvil.therapeutic.category",
        string="Categoría Terapéutica",
        index=True,
    )

    dosage_form = fields.Selection(
        [
            ("tableta", "Tableta / Comprimido"),
            ("capsula", "Cápsula"),
            ("jarabe", "Jarabe"),
            ("suspension", "Suspensión Oral"),
            ("inyectable", "Inyectable / Ampolla"),
            ("crema_unguento", "Crema / Ungüento / Pomada"),
            ("gotas_oftalmicas", "Gotas Oftálmicas / Óticas"),
            ("otro", "Otro"),
        ],
        string="Forma Farmacéutica",
        default="tableta",
    )

    concentration = fields.Char(string="Concentración", help="Ej: 500 mg, 10 mg/ml")

    prescription_required = fields.Boolean(string="Requiere Receta Médica", default=False)

    orderpoint_min_qty = fields.Float(
        string="Stock Mínimo de Seguridad",
        compute="_compute_orderpoint_min_qty",
        search="_search_orderpoint_min_qty",
        help="Cantidad mínima de existencia de seguridad configurada en las reglas de reabastecimiento.",
    )

    @api.depends("product_variant_ids.orderpoint_min_qty")
    def _compute_orderpoint_min_qty(self):
        for tmpl in self:
            tmpl.orderpoint_min_qty = sum(tmpl.product_variant_ids.mapped("orderpoint_min_qty"))

    def _search_orderpoint_min_qty(self, operator, value):
        orderpoints = self.env["stock.warehouse.orderpoint"].search([("product_min_qty", operator, value)])
        return [("product_tmpl_id", "in", orderpoints.mapped("product_tmpl_id").ids)]


class ProductProductMedicine(models.Model):
    _inherit = "product.product"

    _sql_constraints = [
        (
            "barcode_unique",
            "unique(barcode)",
            "El código de barras debe ser único por producto.",
        )
    ]

    orderpoint_min_qty = fields.Float(
        string="Stock Mínimo de Seguridad",
        compute="_compute_orderpoint_min_qty",
        search="_search_orderpoint_min_qty",
        help="Cantidad mínima de existencia de seguridad configurada en las reglas de reabastecimiento.",
    )

    @api.depends("orderpoint_ids.product_min_qty")
    def _compute_orderpoint_min_qty(self):
        for prod in self:
            prod.orderpoint_min_qty = sum(prod.orderpoint_ids.mapped("product_min_qty"))

    def _search_orderpoint_min_qty(self, operator, value):
        orderpoints = self.env["stock.warehouse.orderpoint"].search([
            ("product_min_qty", operator, value)
        ])
        return [("id", "in", orderpoints.mapped("product_id").ids)]
