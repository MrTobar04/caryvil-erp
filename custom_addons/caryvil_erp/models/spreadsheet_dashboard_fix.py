# -*- coding: utf-8 -*-
"""Extensión y resguardo para el modelo nativo `spreadsheet.dashboard`.

Solución para el error TypeError en Odoo Core cuando `spreadsheet_data` es nulo o `False`:
`TypeError: the JSON object must be str, bytes or bytearray, not bool`
"""

import json
from odoo import models


class SpreadsheetDashboardFix(models.Model):
    _inherit = "spreadsheet.dashboard"

    def get_readonly_dashboard(self):
        """Retorna los datos del dashboard en modo lectura.
        Resguarda ejecuciones donde `spreadsheet_data` sea False o nulo para prevenir
        excepciones TypeError en json.loads(False).
        """
        self.ensure_one()
        if not self.spreadsheet_data:
            return {
                "snapshot": {
                    "version": 1,
                    "sheets": [],
                },
                "revisions": [],
            }
        try:
            return super().get_readonly_dashboard()
        except TypeError:
            is_valid_type = isinstance(self.spreadsheet_data, (str, bytes, bytearray))
            snapshot = json.loads(self.spreadsheet_data) if is_valid_type else {"version": 1, "sheets": []}
            return {
                "snapshot": snapshot,
                "revisions": [],
            }
