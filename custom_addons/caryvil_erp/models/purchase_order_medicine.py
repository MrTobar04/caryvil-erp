# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PurchaseOrderMedicine(models.Model):
    _inherit = 'purchase.order'

    laboratory_id = fields.Many2one(
        'res.partner',
        string='Proveedor',
        related='partner_id.commercial_partner_id',
        store=True,
        readonly=True,
        help='Empresa (laboratorio/droguería) a la que pertenece el vendedor (Nombre Vendedor) seleccionado.',
    )
    commercial_terms_id = fields.Selection([
        ('contado', 'Contado'),
        ('credito_15', 'Crédito 15 días'),
        ('credito_30', 'Crédito 30 días'),
        ('credito_45', 'Crédito 45 días'),
        ('credito_60', 'Crédito 60 días'),
    ], string='Condiciones de Pago', default='contado')
    expected_delivery_date = fields.Date(string='Fecha Límite de Entrega')
    notes_reception = fields.Text(
        string='Requerimientos de Recepción',
        default='Requerir lotes con fecha de caducidad mayor a 18 meses.',
    )
    state_label = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('recibido', 'Recibido'),
        ('cancelado', 'Cancelado'),
    ], string='Estado', compute='_compute_state_label', store=True)
    amount_subtotal_gross = fields.Monetary(
        string='Subtotal (sin descuento)',
        compute='_compute_amount_discount_summary',
        store=True,
        currency_field='currency_id',
    )
    amount_discount_total = fields.Monetary(
        string='Descuento',
        compute='_compute_amount_discount_summary',
        store=True,
        currency_field='currency_id',
    )
    iva_percibido_check = fields.Boolean(
        string='Aplicar IVA Percibido (1%)',
        help='El IVA Percibido (1%) aplica a facturas de $100.00 o más, cuando el proveedor es Gran Contribuyente. '
             'Se sugiere automáticamente al superar $100, pero puede desactivarse manualmente.',
    )
    amount_iva_percibido = fields.Monetary(
        string='IVA Percibido (1%)',
        compute='_compute_amount_iva_percibido',
        store=True,
        currency_field='currency_id',
    )
    amount_total_final = fields.Monetary(
        string='Total Final (con IVA Percibido)',
        compute='_compute_amount_iva_percibido',
        store=True,
        currency_field='currency_id',
    )

    # Sugiere activar el IVA Percibido cuando la factura (con IVA incluido) supera los $100.
    @api.onchange('amount_total')
    def _onchange_amount_total_iva_percibido(self):
        for order in self:
            order.iva_percibido_check = order.amount_total > 100

    # El 1% de IVA Percibido solo se cobra si la factura supera $100 y el check está activo.
    @api.depends('amount_total', 'iva_percibido_check')
    def _compute_amount_iva_percibido(self):
        for order in self:
            if order.iva_percibido_check and order.amount_total > 100:
                order.amount_iva_percibido = order.amount_total * 0.01
            else:
                order.amount_iva_percibido = 0.0
            order.amount_total_final = order.amount_total + order.amount_iva_percibido

    # Simplifica los 6 estados nativos de Odoo a los 3 que maneja el negocio: Pendiente, Recibido, Cancelado.
    @api.depends('state')
    def _compute_state_label(self):
        for order in self:
            if order.state == 'cancel':
                order.state_label = 'cancelado'
            elif order.state == 'done':
                order.state_label = 'recibido'
            else:
                order.state_label = 'pendiente'

    # Subtotal bruto (cantidad x precio unitario, sin descuento) y el monto total descontado.
    @api.depends('order_line.product_qty', 'order_line.price_unit', 'order_line.price_subtotal')
    def _compute_amount_discount_summary(self):
        for order in self:
            gross = sum(line.product_qty * line.price_unit for line in order.order_line)
            order.amount_subtotal_gross = gross
            order.amount_discount_total = gross - order.amount_untaxed

    # Asigna el código autogenerado (PE0001, PE0002...) a las nuevas órdenes de compra.
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('caryvil.purchase.order') or 'New'
        return super().create(vals_list)

    # El proveedor (vendedor o su empresa/laboratorio) debe estar catalogado como proveedor farmacéutico.
    @api.constrains('partner_id')
    def _check_pharmacy_vendor(self):
        for order in self:
            partner = order.partner_id
            if partner and not (partner.is_pharmacy_vendor or partner.commercial_partner_id.is_pharmacy_vendor):
                raise ValidationError(_(
                    'El proveedor "%s" no está catalogado como proveedor farmacéutico.'
                ) % partner.name)

    def button_confirm(self):
        for order in self:
            if not order.order_line:
                raise ValidationError(_('No puede confirmar una orden de compra sin líneas de medicamentos.'))
            for line in order.order_line:
                if line.product_qty <= 0:
                    raise ValidationError(_('La cantidad del medicamento %s debe ser mayor a 0.') % line.product_id.name)
        return super().button_confirm()
