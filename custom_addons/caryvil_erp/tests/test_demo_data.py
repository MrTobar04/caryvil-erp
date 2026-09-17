# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestDemoData(TransactionCase):

    def test_01_verify_demo_vendors(self):
        """SPEC-10.2.1: Verificar existencia de proveedores de demostración"""
        vijosa = self.env.ref('caryvil_erp.vendor_vijosa', raise_if_not_found=False)
        self.assertIsNotNone(vijosa)
        self.assertIn('Vijosa', vijosa.name)

    def test_02_verify_demo_customers(self):
        """SPEC-10.2.1: Verificar existencia de clientes de demostración con DUI"""
        maria = self.env.ref('caryvil_erp.customer_maria_lopez', raise_if_not_found=False)
        self.assertIsNotNone(maria)
        self.assertEqual(maria.dui, '04589632-1')

    def test_03_verify_demo_medicines_count(self):
        """SPEC-10.2.1: Verificar existencia de medicamentos en catálogo"""
        amoxicilina = self.env.ref('caryvil_erp.med_amoxicilina_500', raise_if_not_found=False)
        self.assertIsNotNone(amoxicilina)
        self.assertEqual(amoxicilina.barcode, '7410001000012')

    def test_04_verify_demo_stock_lots(self):
        """SPEC-10.2.1: Verificar existencia de lotes de prueba"""
        lot_critico = self.env.ref('caryvil_erp.lot_amoxicilina_critico', raise_if_not_found=False)
        self.assertIsNotNone(lot_critico)
        self.assertEqual(lot_critico.name, 'LOT-AMX-CRITICO')
