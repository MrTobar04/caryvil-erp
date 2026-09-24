# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from psycopg2 import IntegrityError


class TestMedicineCatalog(TransactionCase):

    def setUp(self):
        super().setUp()

        self.category = self.env["caryvil.therapeutic.category"].create(
            {
                "name": "Categoría de Prueba",
                "code": "TEST",
                "description": "Categoría para pruebas de SPEC-7.1.1",
            }
        )

        self.ingredient = self.env["caryvil.active.ingredient"].create(
            {
                "name": "Principio Activo de Prueba",
                "description": "Principio activo para pruebas de SPEC-7.1.1",
            }
        )

    def test_01_create_therapeutic_category(self):
        """SPEC-7.1.1: Verificar creación de categoría terapéutica."""
        self.assertEqual(self.category.name, "Categoría de Prueba")
        self.assertEqual(self.category.code, "TEST")

    def test_02_create_active_ingredient(self):
        """SPEC-7.1.1: Verificar creación de principio activo."""
        self.assertEqual(self.ingredient.name, "Principio Activo de Prueba")

    def test_03_create_medicine_with_pharma_data(self):
        """SPEC-7.1.1: Verificar producto farmacéutico y sus relaciones."""
        product = self.env["product.template"].create(
            {
                "name": "Medicamento de Prueba",
                "active_ingredient_id": self.ingredient.id,
                "therapeutic_category_id": self.category.id,
                "dosage_form": "capsula",
                "concentration": "500 mg",
                "prescription_required": False,
                "barcode": "9999999999999",
                "list_price": 0.25,
            }
        )

        self.assertEqual(product.active_ingredient_id, self.ingredient)
        self.assertEqual(product.therapeutic_category_id, self.category)
        self.assertEqual(product.dosage_form, "capsula")
        self.assertEqual(product.concentration, "500 mg")
        self.assertFalse(product.prescription_required)
        self.assertEqual(product.barcode, "9999999999999")
        self.assertEqual(product.list_price, 0.25)

    def test_04_medicine_defaults(self):
        """SPEC-7.1.1: Verificar producto almacenable y tracking por lotes."""
        product = self.env["product.template"].create(
            {
                "name": "Medicamento Default Test",
                "active_ingredient_id": self.ingredient.id,
                "therapeutic_category_id": self.category.id,
                "barcode": "9999999999998",
            }
        )

        self.assertEqual(product.detailed_type, "product")
        self.assertEqual(product.tracking, "lot")

    def test_05_prescription_required(self):
        """SPEC-7.1.1: Verificar campo de receta médica."""
        product = self.env["product.template"].create(
            {
                "name": "Medicamento con Receta Test",
                "active_ingredient_id": self.ingredient.id,
                "therapeutic_category_id": self.category.id,
                "prescription_required": True,
                "barcode": "9999999999997",
            }
        )

        self.assertTrue(product.prescription_required)

    def test_06_barcode_unique(self):
        """SPEC-7.1.1: Verificar unicidad del código de barras."""

        # Crear dos productos sin código de barras
        product_1 = self.env["product.template"].create(
            {
                "name": "Medicamento Barcode 1",
            }
        )

        product_2 = self.env["product.template"].create(
            {
                "name": "Medicamento Barcode 2",
            }
        )

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
        while self.env["product.product"].search_count([("barcode", "=", barcode)]):
            base = str(int(base) + 1).zfill(12)
            barcode = calculate_ean13(base)

        # Asignar el código al primer producto
        product_1.product_variant_id.write({"barcode": barcode})

        # El segundo producto no puede utilizar el mismo código
        with self.assertRaises(IntegrityError):
            with self.env.cr.savepoint():
                product_2.product_variant_id.write({"barcode": barcode})

    def test_07_search_by_active_ingredient(self):
        """SPEC-7.1.1: Verificar búsqueda de productos por principio activo (Escenario 2)."""
        product = self.env["product.template"].create(
            {
                "name": "Panadol Extra 500mg",
                "active_ingredient_id": self.ingredient.id,
                "therapeutic_category_id": self.category.id,
                "dosage_form": "tableta",
                "concentration": "500 mg",
            }
        )
        # Búsqueda usando el dominio inyectado en product_medicine_views.xml
        found = self.env["product.template"].search([
            "|", "|", "|", "|",
            ("default_code", "ilike", "Principio Activo de Prueba"),
            ("product_variant_ids.default_code", "ilike", "Principio Activo de Prueba"),
            ("name", "ilike", "Principio Activo de Prueba"),
            ("barcode", "ilike", "Principio Activo de Prueba"),
            ("active_ingredient_id.name", "ilike", "Principio Activo de Prueba"),
        ])
        self.assertIn(product, found)

    def test_08_actions_and_menus_exist(self):
        """SPEC-7.1.1: Verificar existencia de acciones de ventana y menús."""
        action_cat = self.env.ref("caryvil_erp.action_caryvil_therapeutic_category")
        self.assertEqual(action_cat.res_model, "caryvil.therapeutic.category")

        action_act = self.env.ref("caryvil_erp.action_caryvil_active_ingredient")
        self.assertEqual(action_act.res_model, "caryvil.active.ingredient")

        menu_act = self.env.ref("caryvil_erp.menu_caryvil_principios_activos")
        self.assertTrue(menu_act.exists())

        menu_cat = self.env.ref("caryvil_erp.menu_caryvil_categorias_terapeuticas")
        self.assertTrue(menu_cat.exists())

    def test_09_cashier_read_only_access(self):
        """SPEC-7.1.1: Verificar que rol cajero solo tiene lectura en catálogos."""
        group_cashier = self.env.ref("caryvil_erp.group_caryvil_cashier")
        cashier_user = self.env["res.users"].create(
            {
                "name": "Cajero Test",
                "login": "cajero_test@caryvil.com",
                "email": "cajero_test@caryvil.com",
                "groups_id": [(6, 0, [group_cashier.id])],
            }
        )
        # Cajero puede leer
        cats = self.env["caryvil.therapeutic.category"].with_user(cashier_user).search([])
        self.assertTrue(len(cats) >= 1)

        # Cajero no puede crear categoría
        from odoo.exceptions import AccessError
        with self.assertRaises(AccessError):
            self.env["caryvil.therapeutic.category"].with_user(cashier_user).create(
                {"name": "Categoría Prohibida Cajero"}
            )

