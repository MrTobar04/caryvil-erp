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
