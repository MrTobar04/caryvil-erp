# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestSeedData(TransactionCase):

    def test_01_verify_therapeutic_categories(self):
        """SPEC-10.1.1: Verificar existencia de las familias terapéuticas base"""
        cat_analgesicos = self.env.ref('caryvil_erp.cat_analgesicos', raise_if_not_found=False)
        self.assertIsNotNone(cat_analgesicos)
        self.assertEqual(cat_analgesicos.name, 'Analgésicos y Antiinflamatorios')

        cat_antibioticos = self.env.ref('caryvil_erp.cat_antibioticos', raise_if_not_found=False)
        self.assertIsNotNone(cat_antibioticos)

    def test_02_verify_tax_data(self):
        """SPEC-10.1.1: Verificar existencia del impuesto IVA 13% de ventas"""
        tax_sales = self.env.ref('caryvil_erp.tax_caryvil_iva_ventas_13', raise_if_not_found=False)
        self.assertIsNotNone(tax_sales)
        self.assertEqual(tax_sales.amount, 13.0)
        self.assertEqual(tax_sales.type_tax_use, 'sale')

    def test_03_verify_active_ingredients(self):
        """SPEC-10.1.1: Verificar existencia de principios activos normalizados"""
        paracetamol = self.env.ref('caryvil_erp.active_paracetamol', raise_if_not_found=False)
        self.assertIsNotNone(paracetamol)
        self.assertIn('Paracetamol', paracetamol.name)

    def test_04_verify_demo_users(self):
        """SPEC-10.1.1: Verificar la carga de usuarios semilla por rol"""
        user_cajero = self.env.ref('caryvil_erp.user_cajero_demo', raise_if_not_found=False)
        self.assertIsNotNone(user_cajero)
        self.assertEqual(user_cajero.login, 'cajero')
