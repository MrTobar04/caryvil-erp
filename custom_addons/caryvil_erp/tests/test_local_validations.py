# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError, AccessError
from psycopg2 import IntegrityError
from odoo.tools import mute_logger


class TestLocalValidations(TransactionCase):
    """Suite de pruebas unitarias para SPEC-11.1.3: Pruebas Unitarias de Validaciones Locales y Reglas de Negocio.

    Valida:
    1. Formatos válidos de DUI salvadoreño y autocorrección de digitación continua (9 dígitos sin guion).
    2. Rechazo con ValidationError ante formatos de DUI inválidos (letras, longitud incorrecta, caracteres especiales).
    3. Restricción de unicidad de DUI a nivel de base de datos / modelo.
    4. Búsqueda rápida multicampo (_name_search) por DUI (con/sin guion), teléfono y nombres/apellidos.
    5. Restricciones de seguridad por rol RBAC (Cajero sin permisos para
       modificar facturas publicadas o eliminar medicamentos).
    """

    def setUp(self):
        super(TestLocalValidations, self).setUp()
        self.partner_model = self.env["res.partner"]
        self.product_model = self.env["product.template"]
        self.invoice_model = self.env["account.move"]

        # Cargar o crear roles y usuarios para pruebas de seguridad RBAC
        self.group_cashier = self.env.ref("caryvil_erp.group_caryvil_cashier")
        self.group_manager = self.env.ref("caryvil_erp.group_caryvil_manager")

        self.user_cashier = self.env["res.users"].create(
            {
                "name": "Cajero Validaciones Local",
                "login": "cashier_local_test",
                "email": "cashier_local@caryvil.test",
                "groups_id": [(6, 0, [self.group_cashier.id])],
            }
        )

        self.user_manager = self.env["res.users"].create(
            {
                "name": "Manager Validaciones Local",
                "login": "mgr_local_test",
                "email": "mgr_local@caryvil.test",
                "groups_id": [(6, 0, [self.group_manager.id])],
            }
        )

    def test_dui_valid_formats_and_autocorrection(self):
        """Test 1: Validación de DUI con formato estándar y autocorrección de digitación continua de 9 dígitos."""
        # Caso 1: DUI formateado estándar con guion
        client1 = self.partner_model.create(
            {
                "first_name": "Carlos",
                "last_name": "Rivas",
                "dui": "04589632-1",
                "is_pharmacy_customer": True,
            }
        )
        self.assertEqual(client1.dui, "04589632-1")
        self.assertEqual(client1.name, "Carlos Rivas")

        # Caso 2: DUI sin guion (9 dígitos continuos) -> Debe autocorregirse a 09876543-2
        client2 = self.partner_model.create(
            {
                "first_name": "Ana",
                "last_name": "García",
                "dui": "098765432",
                "is_pharmacy_customer": True,
            }
        )
        self.assertEqual(client2.dui, "09876543-2")
        self.assertEqual(client2.name, "Ana García")

    def test_dui_invalid_formats_raise_validation_error(self):
        """Test 2: Comprobación de que cadenas inválidas (longitud corta, letras,
        caracteres especiales) disparen ValidationError."""
        # Longitud corta (< 9 dígitos)
        with self.assertRaises(ValidationError):
            self.partner_model.create(
                {
                    "first_name": "Test",
                    "last_name": "Corto",
                    "dui": "12345",
                    "is_pharmacy_customer": True,
                }
            )

        # Longitud larga (> 10 caracteres)
        with self.assertRaises(ValidationError):
            self.partner_model.create(
                {
                    "first_name": "Test",
                    "last_name": "Largo",
                    "dui": "0123456789-0",
                    "is_pharmacy_customer": True,
                }
            )

        # Caracteres alfabéticos en el DUI
        with self.assertRaises(ValidationError):
            self.partner_model.create(
                {
                    "first_name": "Test",
                    "last_name": "Letras",
                    "dui": "0458A632-1",
                    "is_pharmacy_customer": True,
                }
            )

        # Caracteres especiales
        with self.assertRaises(ValidationError):
            self.partner_model.create(
                {
                    "first_name": "Test",
                    "last_name": "Especial",
                    "dui": "04589632#1",
                    "is_pharmacy_customer": True,
                }
            )

    @mute_logger("odoo.sql_db")
    def test_dui_uniqueness_sql_constraint(self):
        """Test 3: Creación de un segundo cliente con un DUI ya existente ->
        Comprobación de bloqueo por violación de unicidad."""
        self.partner_model.create(
            {
                "first_name": "Cliente",
                "last_name": "Uno",
                "dui": "01122334-5",
                "is_pharmacy_customer": True,
            }
        )

        # Intentar crear segundo cliente con el mismo DUI
        with self.assertRaises((ValidationError, IntegrityError)):
            with self.cr.savepoint():
                self.partner_model.create(
                    {
                        "first_name": "Cliente",
                        "last_name": "Dos",
                        "dui": "01122334-5",
                        "is_pharmacy_customer": True,
                    }
                )

    def test_customer_name_search_multicampo(self):
        """Test 4: Verificación de que el método _name_search retorne el registro correcto
        al buscar por fragmentos de DUI, teléfono o apellidos."""
        client = self.partner_model.create(
            {
                "first_name": "Roberto",
                "last_name": "Menjívar",
                "dui": "05544332-9",
                "phone": "7890-1234",
                "is_pharmacy_customer": True,
            }
        )

        # Buscar por DUI parcial con guion
        results_dui = self.partner_model.name_search("05544332")
        self.assertIn(client.id, [r[0] for r in results_dui])

        # Buscar por DUI de 9 dígitos sin guion
        results_dui_clean = self.partner_model.name_search("055443329")
        self.assertIn(client.id, [r[0] for r in results_dui_clean])

        # Buscar por número de teléfono
        results_phone = self.partner_model.name_search("7890-1234")
        self.assertIn(client.id, [r[0] for r in results_phone])

        # Buscar por apellido
        results_lastname = self.partner_model.name_search("Menjívar")
        self.assertIn(client.id, [r[0] for r in results_lastname])

    def test_security_rbac_restrictions(self):
        """Test 5: Verificación de privilegios por rol (Cajero no puede eliminar medicamentos
        ni modificar facturas emitidas)."""
        category = self.env["product.category"].create({"name": "Categoría Validaciones Local"})

        medicine = self.product_model.create(
            {
                "name": "Acetaminofén 500mg Test Validations",
                "categ_id": category.id,
                "type": "consu",
                "list_price": 2.50,
            }
        )

        customer = self.partner_model.create(
            {
                "first_name": "Juan",
                "last_name": "Pérez",
                "dui": "03344556-7",
                "is_pharmacy_customer": True,
            }
        )

        # 1. El Cajero intenta eliminar un medicamento del catálogo -> AccessError
        med_cashier = medicine.with_user(self.user_cashier)
        with self.assertRaises(AccessError):
            med_cashier.unlink()

        # 2. El Cajero intenta modificar una factura publicada (posted) -> AccessError
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        if not journal:
            journal = self.env["account.journal"].create(
                {
                    "name": "Ventas Test Validations",
                    "code": "VTVAL",
                    "type": "sale",
                }
            )

        invoice = self.invoice_model.create(
            {
                "partner_id": customer.id,
                "move_type": "out_invoice",
                "journal_id": journal.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Acetaminofén 500mg",
                            "quantity": 1,
                            "price_unit": 2.50,
                        },
                    )
                ],
            }
        )
        invoice.action_post()
        self.assertEqual(invoice.state, "posted")

        inv_cashier = invoice.with_user(self.user_cashier)
        with self.assertRaises(AccessError):
            inv_cashier.write({"ref": "Intento de Modificación Ilegal"})
