from odoo import models, fields


class ResCompanyCaryvil(models.Model):
    _inherit = "res.company"

    legal_name = fields.Char(
        string="Razón Social",
        help="Nombre legal/razón social de la empresa, distinto del nombre comercial (name). "
        "Aparece en documentos fiscales.",
    )
    economic_activity = fields.Char(string="Actividad Económica")
