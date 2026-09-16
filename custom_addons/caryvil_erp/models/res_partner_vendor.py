# -*- coding: utf-8 -*-
import re

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

NIT_RE = re.compile(r'^\d{4}-\d{6}-\d{3}-\d{1}$')
PHONE_RE = re.compile(r'^\d{4}-\d{4}$')


class ResPartnerVendor(models.Model):
    _inherit = 'res.partner'

    is_pharmacy_vendor = fields.Boolean(string='Es Proveedor Farmacéutico', default=False)
    vendor_code = fields.Char(string='Código', readonly=True, copy=False)
    vendor_type = fields.Selection([
        ('laboratorio', 'Laboratorio'),
        ('distribuidora', 'Distribuidora'),
        ('drogueria', 'Droguería'),
    ], string='Tipo de Proveedor', default='laboratorio')
    nit = fields.Char(string='NIT', size=17, help='Formato: 0000-000000-000-0')
    nrc = fields.Char(string='NRC', size=10, help='Formato: 00000-0')
    purchase_order_ids = fields.One2many(
        'purchase.order', 'partner_id',
        string='Historial de Compras',
        help='Órdenes de compra hechas directamente a este vendedor.',
    )

    # Asigna el código autogenerado (P0001, P0002...) a proveedores/vendedores nuevos.
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('is_pharmacy_vendor') and not vals.get('vendor_code'):
                vals['vendor_code'] = self.env['ir.sequence'].next_by_code('caryvil.vendor.code') or 'Nuevo'
        return super().create(vals_list)

    # Fuerza que al abrir un Laboratorio existente se use el formulario simplificado, no el de contactos genérico.
    def get_formview_id(self, access_uid=None):
        if self.is_pharmacy_vendor and self.is_company:
            return self.env.ref('caryvil_erp.view_res_partner_laboratorio_quick_form').id
        return super().get_formview_id(access_uid=access_uid)

    # Hace que ese formulario simplificado se abra en ventana emergente, igual que al crear.
    def get_formview_action(self, access_uid=None):
        action = super().get_formview_action(access_uid=access_uid)
        if self.is_pharmacy_vendor and self.is_company:
            action['target'] = 'new'
        return action

    # Valida que el NIT, si se llena, tenga el formato 0000-000000-000-0.
    @api.constrains('nit', 'is_pharmacy_vendor')
    def _check_nit_format(self):
        for partner in self:
            if partner.is_pharmacy_vendor and partner.nit and not NIT_RE.match(partner.nit):
                raise ValidationError(_(
                    'El NIT de "%s" debe tener el formato 0000-000000-000-0.'
                ) % partner.name)

    # Obliga a llenar el NRC en todo Laboratorio/Proveedor (sin exigir un formato fijo).
    @api.constrains('nrc', 'is_pharmacy_vendor', 'is_company')
    def _check_nrc_required(self):
        for partner in self:
            if partner.is_pharmacy_vendor and partner.is_company and not partner.nrc:
                raise ValidationError(_(
                    'El NRC de "%s" es obligatorio.'
                ) % partner.name)

    # Valida que el teléfono, si se llena, tenga el formato 0000-0000.
    @api.constrains('phone', 'is_pharmacy_vendor')
    def _check_phone_format(self):
        for partner in self:
            if partner.is_pharmacy_vendor and partner.phone and not PHONE_RE.match(partner.phone):
                raise ValidationError(_(
                    'El teléfono de "%s" debe tener el formato 0000-0000.'
                ) % partner.name)
