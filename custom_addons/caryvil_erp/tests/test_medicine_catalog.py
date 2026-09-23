# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from psycopg2 import IntegrityError

class TestMedicineCatalog(TransactionCase):

    def setUp(self):
        super().setUp()

        self.category = self.env['caryvil.therapeutic.category'].create({
            'name': 'Categoría de Prueba',
            'code': 'TEST',
            'description': 'Categoría para pruebas de SPEC-7.1.1',
        })

        self.ingredient = self.env['caryvil.active.ingredient'].create({
            'name': 'Principio Activo de Prueba',
            'description': 'Principio activo para pruebas de SPEC-7.1.1',
        })

    def test_01_create_therapeutic_category(self):
        """SPEC-7.1.1: Verificar creación de categoría terapéutica."""
        self.assertEqual(self.category.name, 'Categoría de Prueba')
        self.assertEqual(self.category.code, 'TEST')

    def test_02_create_active_ingredient(self):
        """SPEC-7.1.1: Verificar creación de principio activo."""
        self.assertEqual(
            self.ingredient.name,
            'Principio Activo de Prueba'
        )

    def test_03_create_medicine_with_pharma_data(self):
        """SPEC-7.1.1: Verificar producto farmacéutico y sus relaciones."""
        product = self.env['product.template'].create({
            'name': 'Medicamento de Prueba',
            'active_ingredient_id': self.ingredient.id,
            'therapeutic_category_id': self.category.id,
            'dosage_form': 'capsula',
            'concentration': '500 mg',
            'prescription_required': False,
            'barcode': '9999999999999',
            'list_price': 0.25,
        })

        self.assertEqual(
            product.active_ingredient_id,
            self.ingredient
        )
        self.assertEqual(
            product.therapeutic_category_id,
            self.category
        )
        self.assertEqual(product.dosage_form, 'capsula')
        self.assertEqual(product.concentration, '500 mg')
        self.assertFalse(product.prescription_required)
        self.assertEqual(product.barcode, '9999999999999')
        self.assertEqual(product.list_price, 0.25)

    def test_04_medicine_defaults(self):
        """SPEC-7.1.1: Verificar producto almacenable y tracking por lotes."""
        product = self.env['product.template'].create({
            'name': 'Medicamento Default Test',
            'active_ingredient_id': self.ingredient.id,
            'therapeutic_category_id': self.category.id,
            'barcode': '9999999999998',
        })

        self.assertEqual(product.detailed_type, 'product')
        self.assertEqual(product.tracking, 'lot')

    def test_05_prescription_required(self):
        """SPEC-7.1.1: Verificar campo de receta médica."""
        product = self.env['product.template'].create({
            'name': 'Medicamento con Receta Test',
            'active_ingredient_id': self.ingredient.id,
            'therapeutic_category_id': self.category.id,
            'prescription_required': True,
            'barcode': '9999999999997',
        })

        self.assertTrue(product.prescription_required)

def test_06_barcode_unique(self):
    """SPEC-7.1.1: Verificar unicidad del código de barras."""

    # Crear dos productos sin código de barras
    product_1 = self.env['product.template'].create({
        'name': 'Medicamento Barcode 1',
    })

    product_2 = self.env['product.template'].create({
        'name': 'Medicamento Barcode 2',
    })

    # Generar un código EAN-13 único para la prueba
    base = f"20000000{product_1.id:04d}"[:12]

    def calculate_ean13(base12):
        total = 0

        for i, digit in enumerate(base12):
            value = int(digit)
            total += value if i % 2 == 0 else value * 3

        check_digit = (10 - (total % 10)) % 10

        return base12 + str(check_digit)

    barcode = calculate_ean13(base)

    # Buscar un código que no exista actualmente
    while self.env['product.product'].search_count([
        ('barcode', '=', barcode)
    ]):
        base = str(int(base) + 1).zfill(12)
        barcode = calculate_ean13(base)

    # Asignar el código al primer producto
    product_1.product_variant_id.write({
        'barcode': barcode
    })

    # El segundo producto no puede utilizar el mismo código
    with self.assertRaises(IntegrityError):
        with self.env.cr.savepoint():
            product_2.product_variant_id.write({
                'barcode': barcode
            })