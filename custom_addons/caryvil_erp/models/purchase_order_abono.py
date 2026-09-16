# -*- coding: utf-8 -*-
from odoo import models, fields


class PurchaseOrderAbono(models.Model):
    _name = 'purchase.order.abono'
    _description = 'Abono a Orden de Compra'
    _order = 'fecha desc, id desc'

    order_id = fields.Many2one(
        'purchase.order', string='Orden de Compra', required=True, ondelete='cascade',
    )
    fecha = fields.Date(string='Fecha', default=fields.Date.context_today, required=True)
    monto = fields.Monetary(string='Monto Abonado', required=True, currency_field='currency_id')
    nota = fields.Char(string='Nota')
    currency_id = fields.Many2one(related='order_id.currency_id', store=True, readonly=True)
