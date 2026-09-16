# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ResPartnerCustomer(models.Model):
    _inherit = 'res.partner'

    first_name = fields.Char(string='Nombres', index=True)
    last_name = fields.Char(string='Apellidos', index=True)
    dui = fields.Char(string='DUI', size=10, index=True, help='Formato: 00000000-0')
    is_pharmacy_customer = fields.Boolean(string='Es Cliente de Farmacia', default=True)

    _sql_constraints = [
        ('dui_unique', 'unique(dui)', 'Ya existe un cliente registrado con este número de DUI.')
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('is_pharmacy_customer') and not vals.get('ref'):
                # Autogenerar código secuencial de cliente (CL0001, CL0002, etc.)
                count = self.search_count([('is_pharmacy_customer', '=', True)]) + 1
                vals['ref'] = f"CL{count:04d}"
        return super(ResPartnerCustomer, self).create(vals_list)

    @api.onchange('first_name', 'last_name')
    def _onchange_names(self):
        names = [self.first_name or '', self.last_name or '']
        full_name = ' '.join(filter(None, names)).strip()
        if full_name:
            self.name = full_name

    @api.constrains('dui')
    def _check_dui_format(self):
        for record in self:
            if record.dui:
                clean_dui = record.dui.strip()
                if re.match(r'^\d{9}$', clean_dui):
                    clean_dui = f"{clean_dui[:8]}-{clean_dui[8]}"
                    record.dui = clean_dui
                
                if not re.match(r'^\d{8}-\d{1}$', record.dui):
                    raise ValidationError(_('El DUI ingresado (%s) no es válido. Debe cumplir el formato 00000000-0.') % record.dui)
