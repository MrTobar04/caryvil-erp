# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from psycopg2 import IntegrityError

class TestResPartnerCustomer(TransactionCase):

    def setUp(self):
        super(TestResPartnerCustomer, self).setUp()
        self.partner_model = self.env['res.partner']

    def test_01_create_valid_customer(self):
        """Scenario 1: Crear cliente exitosamente con DUI válido"""
        customer = self.partner_model.create({
            'first_name': 'María Elena',
            'last_name': 'López Rivas',
            'dui': '04589632-1',
            'phone': '7845-1234',
            'street': 'Col. San Antonio, Soyapango',
            'is_pharmacy_customer': True,
        })
        self.assertEqual(customer.name, 'María Elena López Rivas')
        self.assertEqual(customer.dui, '04589632-1')
        self.assertTrue(customer.is_pharmacy_customer)

    def test_02_autocorrect_dui_without_hyphen(self):
        """Scenario 2: Autocorrección de DUI de 9 dígitos sin guion"""
        customer = self.partner_model.create({
            'first_name': 'Carlos',
            'last_name': 'Pérez',
            'dui': '012345678',
        })
        self.assertEqual(customer.dui, '01234567-8')

    def test_03_invalid_dui_format_raises_error(self):
        """Scenario 3: Rechazo de DUI con formato inválido"""
        with self.assertRaises(ValidationError):
            self.partner_model.create({
                'first_name': 'Juan',
                'last_name': 'Gómez',
                'dui': '0458A-1',
            })

        with self.assertRaises(ValidationError):
            self.partner_model.create({
                'first_name': 'Ana',
                'last_name': 'Martínez',
                'dui': '12345',
            })

    def test_04_duplicate_dui_raises_error(self):
        """Scenario 4: Bloqueo de cliente duplicado por DUI"""
        self.partner_model.create({
            'first_name': 'Pedro',
            'last_name': 'Ramírez',
            'dui': '09876543-2',
        })
        with self.assertRaises((ValidationError, IntegrityError)):
            with self.cr.savepoint():
                self.partner_model.create({
                    'first_name': 'Pedro Segundo',
                    'last_name': 'Ramírez',
                    'dui': '09876543-2',
                })

    def test_05_display_name_formatting(self):
        """SPEC-5.2.1: Formato de display_name [DUI] Nombre - Tel: XXXXXXXX"""
        customer = self.partner_model.create({
            'first_name': 'María Elena',
            'last_name': 'López Rivas',
            'dui': '04589632-1',
            'phone': '7845-1234',
            'is_pharmacy_customer': True,
        })
        self.assertEqual(customer.display_name, '[04589632-1] María Elena López Rivas - Tel: 7845-1234')

    def test_06_name_search_by_dui(self):
        """SPEC-5.2.1 Scenario 1: Búsqueda rápida por DUI con y sin guion y parcial"""
        customer = self.partner_model.create({
            'first_name': 'María Elena',
            'last_name': 'López Rivas',
            'dui': '04589632-1',
            'phone': '7845-1234',
            'is_pharmacy_customer': True,
        })
        # Búsqueda por DUI completo con guion
        res1 = self.partner_model.name_search('04589632-1')
        res1_ids = [r[0] for r in res1]
        self.assertIn(customer.id, res1_ids)

        # Búsqueda por DUI sin guion (digitando 9 números seguidos)
        res2 = self.partner_model.name_search('045896321')
        res2_ids = [r[0] for r in res2]
        self.assertIn(customer.id, res2_ids)

        # Búsqueda por fragmento de DUI
        res3 = self.partner_model.name_search('0458')
        res3_ids = [r[0] for r in res3]
        self.assertIn(customer.id, res3_ids)

    def test_07_name_search_by_phone(self):
        """SPEC-5.2.1 Scenario 2: Búsqueda rápida por teléfono o celular"""
        customer = self.partner_model.create({
            'first_name': 'Roberto',
            'last_name': 'Gómez',
            'dui': '01122334-5',
            'phone': '7845-1234',
            'is_pharmacy_customer': True,
        })
        res = self.partner_model.name_search('7845-1234')
        res_ids = [r[0] for r in res]
        self.assertIn(customer.id, res_ids)

    def test_08_name_search_by_names(self):
        """SPEC-5.2.1: Búsqueda rápida por nombres o apellidos"""
        customer = self.partner_model.create({
            'first_name': 'Sofía',
            'last_name': 'Alvarado',
            'dui': '05544332-1',
            'is_pharmacy_customer': True,
        })
        res = self.partner_model.name_search('Alvarado')
        res_ids = [r[0] for r in res]
        self.assertIn(customer.id, res_ids)

