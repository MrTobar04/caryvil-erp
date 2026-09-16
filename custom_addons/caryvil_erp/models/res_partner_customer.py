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

    # Indexación B-Tree de campos adicionales para optimización de búsqueda (<200ms)
    name = fields.Char(index=True)
    phone = fields.Char(index=True)
    mobile = fields.Char(index=True)

    _sql_constraints = [
        ('dui_unique', 'unique(dui)', 'Ya existe un cliente registrado con este número de DUI.')
    ]

    @api.depends('name', 'dui', 'phone', 'is_pharmacy_customer')
    def _compute_display_name(self):
        for partner in self:
            if partner.is_pharmacy_customer and partner.dui:
                phone_part = f" - Tel: {partner.phone}" if partner.phone else ""
                partner.display_name = f"[{partner.dui}] {partner.name or ''}{phone_part}"
            else:
                super(ResPartnerCustomer, partner)._compute_display_name()

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = list(args or [])
        if name:
            clean_term = name.replace('-', '').strip()
            domain = [
                '|', '|', '|', '|', '|', '|',
                ('name', operator, name),
                ('first_name', operator, name),
                ('last_name', operator, name),
                ('dui', operator, name),
                ('dui', operator, clean_term),
                ('phone', operator, name),
                ('mobile', operator, name)
            ]
            if len(clean_term) == 9 and clean_term.isdigit():
                formatted_dui = f"{clean_term[:8]}-{clean_term[8]}"
                domain = ['|'] + domain + [('dui', operator, formatted_dui)]

            return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
        return super(ResPartnerCustomer, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

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

