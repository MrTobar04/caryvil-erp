# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestReportPurchaseOrder(TransactionCase):

    def setUp(self):
        super().setUp()
        self.laboratorio = self.env['res.partner'].create({
            'name': 'Laboratorios Vijosa',
            'is_company': True,
            'is_pharmacy_vendor': True,
            'vendor_type': 'laboratorio',
            'nit': '0614-123456-001-2',
            'nrc': '12345-6',
        })
        self.vendedor = self.env['res.partner'].create({
            'name': 'Carlos Méndez',
            'is_pharmacy_vendor': True,
            'parent_id': self.laboratorio.id,
        })
        self.producto = self.env['product.product'].create({
            'name': 'Amoxicilina 500mg',
            'default_code': 'AMX-500',
        })

    # Escenario 1 (SPEC-3.3.2): genera un PDF válido para una orden de compra confirmada.
    def test_genera_pdf_orden_de_compra(self):
        orden = self.env['purchase.order'].create({
            'partner_id': self.vendedor.id,
            'order_line': [(0, 0, {
                'product_id': self.producto.id,
                'name': self.producto.name,
                'product_qty': 10,
                'price_unit': 4.50,
            })],
        })
        # En modo test, Odoo omite la conversión real a PDF (wkhtmltopdf) y devuelve el HTML
        # renderizado — igual sirve para detectar errores de sintaxis QWeb en la plantilla.
        content, report_type = self.env['ir.actions.report']._render_qweb_pdf(
            'caryvil_erp.report_purchase_order_template', orden.ids
        )
        self.assertIn(report_type, ('pdf', 'html'))
        self.assertGreater(len(content), 1000)
        self.assertIn(b'Amoxicilina 500mg', content)
