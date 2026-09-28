# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestDemoData(TransactionCase):

    def test_01_verify_demo_vendors(self):
        """SPEC-10.2.1: Verificar existencia de proveedores de demostración"""
        vijosa = self.env.ref("caryvil_erp.vendor_vijosa", raise_if_not_found=False)
        self.assertIsNotNone(vijosa)
        self.assertIn("Vijosa", vijosa.name)

    def test_02_verify_demo_customers(self):
        """SPEC-10.2.1: Verificar existencia de clientes de demostración con DUI"""
        maria = self.env.ref("caryvil_erp.customer_maria_lopez", raise_if_not_found=False)
        self.assertIsNotNone(maria)
        self.assertEqual(maria.dui, "04589632-1")

    def test_03_verify_demo_medicines_count(self):
        """SPEC-10.2.1: Verificar existencia de medicamentos en catálogo"""
        amoxicilina = self.env.ref("caryvil_erp.med_amoxicilina_500", raise_if_not_found=False)
        self.assertIsNotNone(amoxicilina)
        self.assertEqual(amoxicilina.barcode, "7410001000012")

    def test_04_verify_demo_stock_lots(self):
        """SPEC-10.2.1: Verificar existencia de lotes de prueba"""
        lot_critico = self.env.ref("caryvil_erp.lot_amoxicilina_critico", raise_if_not_found=False)
        self.assertIsNotNone(lot_critico)
        self.assertEqual(lot_critico.name, "LOT-AMX-CRITICO")

    def test_05_verify_demo_reordering_rules(self):
        """SPEC-7.2.2: Verificar existencia de reglas de reabastecimiento de demostración"""
        op = self.env.ref("caryvil_erp.demo_orderpoint_amoxicilina_500", raise_if_not_found=False)
        self.assertIsNotNone(op)
        self.assertEqual(op.name, "OP/AMX500")

    def test_06_verify_quant_update_on_module_upgrade(self):
        """Verificar actualización sin errores de stock.quant en recarga de datos demo"""
        quant = self.env.ref("caryvil_erp.quant_amoxicilina_largo", raise_if_not_found=False)
        if quant:
            # Simular actualización de registro XML mediante _load_records_write
            vals = {
                "product_id": quant.product_id.id,
                "location_id": quant.location_id.id,
                "lot_id": quant.lot_id.id if quant.lot_id else False,
                "quantity": 100.0,
            }
            quant._load_records_write(vals)
            self.assertEqual(quant.quantity, 100.0)

