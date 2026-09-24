# -*- coding: utf-8 -*-
from odoo import models, fields


class CaryvilTherapeuticCategory(models.Model):
    _name = 'caryvil.therapeutic.category'
    _description = 'Categoría Terapéutica Farmacéutica'

    name = fields.Char(
        string='Categoría',
        required=True,
        index=True
    )
    code = fields.Char(
        string='Código ATC / Clave',
        size=10
    )
    description = fields.Text(
        string='Descripción / Uso Terapéutico'
    )


class CaryvilActiveIngredient(models.Model):
    _name = 'caryvil.active.ingredient'
    _description = 'Principio Activo'

    name = fields.Char(
        string='Nombre del Principio Activo',
        required=True,
        index=True
    )
    description = fields.Text(
        string='Acción Farmacológica'
    )


class ProductTemplateMedicine(models.Model):
    _inherit = 'product.template'

    detailed_type = fields.Selection(
        default='product'
    )

    tracking = fields.Selection(
        default='lot'
    )

    active_ingredient_id = fields.Many2one(
        'caryvil.active.ingredient',
        string='Principio Activo',
        index=True,
    )

    therapeutic_category_id = fields.Many2one(
        'caryvil.therapeutic.category',
        string='Categoría Terapéutica',
        index=True,
    )

    dosage_form = fields.Selection([
        ('tableta', 'Tableta / Comprimido'),
        ('capsula', 'Cápsula'),
        ('jarabe', 'Jarabe'),
        ('suspension', 'Suspensión Oral'),
        ('inyectable', 'Inyectable / Ampolla'),
        ('crema_unguento', 'Crema / Ungüento / Pomada'),
        ('gotas_oftalmicas', 'Gotas Oftálmicas / Óticas'),
        ('otro', 'Otro')
    ], string='Forma Farmacéutica', default='tableta')

    concentration = fields.Char(
        string='Concentración',
        help='Ej: 500 mg, 10 mg/ml'
    )

    prescription_required = fields.Boolean(
        string='Requiere Receta Médica',
        default=False
    )


class ProductProductMedicine(models.Model):
    _inherit = 'product.product'

    _sql_constraints = [
        (
            'barcode_unique',
            'unique(barcode)',
            'El código de barras debe ser único por producto.'
        )
    ]
