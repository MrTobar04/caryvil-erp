# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductTemplateMedicine(models.Model):
    _inherit = 'product.template'

    # Todo medicamento nuevo nace con seguimiento por lote activado (necesario para capturar
    # lote y fecha de vencimiento al recibir, SPEC-8.2.1). Evita que un producto creado al
    # vuelo desde Compras quede sin esta opción por olvido.
    tracking = fields.Selection(default='lot')
