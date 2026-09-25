# -*- coding: utf-8 -*-
"""Suite de pruebas automatizadas para el Dashboard de KPIs de Ventas (SPEC-4.1.1).

Cubre:
- Escenario 1: Agregación exacta de ventas del día, conteo de transacciones y ticket promedio.
- Escenario 2: Actualización de métricas en tiempo real tras la emisión de una nueva factura.
- Escenario 3: Restricción de acceso estricta para usuarios no autorizados (rol Cajero).
- Casos adicionales: Tendencia temporal de 7 días, ranking Top 5 de medicamentos y manejo de 0 ventas.
"""

from datetime import timedelta
from odoo import fields
from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install", "caryvil", "caryvil_dashboard")
class TestCaryvilDashboardSales(TransactionCase):
    """Pruebas funcionales y de seguridad para el modelo caryvil.dashboard.sales."""

    def setUp(self):
        super(TestCaryvilDashboardSales, self).setUp()

        self.group_manager = self.env.ref("caryvil_erp.group_caryvil_manager")
        self.group_cashier = self.env.ref("caryvil_erp.group_caryvil_cashier")

        # Usuario Administrador
        self.user_manager = self.env["res.users"].create(
            {
                "name": "Administradora Test Dashboard",
                "login": "admin_test_dashboard",
                "email": "admin_dashboard@caryvil.test",
                "groups_id": [(6, 0, [self.group_manager.id])],
            }
        )

        # Usuario Cajero sin permisos gerenciales
        self.user_cashier = self.env["res.users"].create(
            {
                "name": "Cajero Test Mostrador",
                "login": "cashier_test_dashboard",
                "email": "cashier_dashboard@caryvil.test",
                "groups_id": [(6, 0, [self.group_cashier.id])],
            }
        )

        # Cliente farmacéutico
        self.customer = self.env["res.partner"].create(
            {
                "name": "Cliente Caryvil Prueba",
                "first_name": "Ana",
                "last_name": "Rivas",
                "dui": "01234567-9",
                "is_pharmacy_customer": True,
            }
        )

        # Productos farmacéuticos para pruebas
        self.product_a = self.env["product.product"].create(
            {
                "name": "Amoxicilina 500mg",
                "default_code": "MED-AMX-500",
                "list_price": 10.0,
            }
        )
        self.product_b = self.env["product.product"].create(
            {
                "name": "Ibuprofeno 400mg",
                "default_code": "MED-IBU-400",
                "list_price": 5.0,
            }
        )

        # Asegurar un diario de ventas para facturas
        self.journal_sale = self.env["account.journal"].search(
            [("type", "=", "sale"), ("company_id", "=", self.env.company.id)], limit=1
        )

    def _create_posted_invoice(self, date_inv, amount, product=None, qty=1):
        """Helper para crear y publicar una factura de venta con monto exacto."""
        prod = product or self.product_a
        invoice = self.env["account.move"].create(
            {
                "partner_id": self.customer.id,
                "move_type": "out_invoice",
                "invoice_date": date_inv,
                "journal_id": self.journal_sale.id if self.journal_sale else False,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": prod.name,
                            "product_id": prod.id,
                            "quantity": qty,
                            "price_unit": amount / qty if qty else amount,
                            "tax_ids": [(6, 0, [])],
                        },
                    )
                ],
            }
        )
        invoice.action_post()
        return invoice

    def test_01_scenario_1_sales_today_kpis(self):
        """Escenario 1: Tres ventas hoy por $10.00, $25.50 y $14.50.

        Total = $50.00, Transacciones = 3, Ticket Promedio = $16.67.
        """
        today = fields.Date.today()

        self._create_posted_invoice(today, 10.00)
        self._create_posted_invoice(today, 25.50)
        self._create_posted_invoice(today, 14.50)

        dashboard_service = self.env["caryvil.dashboard.sales"].with_user(self.user_manager)
        kpis = dashboard_service.get_sales_kpis()

        self.assertEqual(kpis["total_sales_today"], 50.00, "Ventas del Día deben ser exactamente $50.00")
        self.assertEqual(kpis["tx_count_today"], 3, "Transacciones de Hoy deben ser exactamente 3")
        self.assertEqual(kpis["avg_ticket"], 16.67, "Ticket Promedio debe ser exactamente $16.67")
        self.assertEqual(kpis["currency"], "$ USD", "Moneda debe ser $ USD")

    def test_02_scenario_2_realtime_refresh_after_new_sale(self):
        """Escenario 2: Tras registrar nueva factura por $20.00, se actualiza a $70.00 y 4 transacciones."""
        today = fields.Date.today()

        # Ventas iniciales (suman $50.00 en 3 transacciones)
        self._create_posted_invoice(today, 10.00)
        self._create_posted_invoice(today, 25.50)
        self._create_posted_invoice(today, 14.50)

        dashboard_service = self.env["caryvil.dashboard.sales"].with_user(self.user_manager)
        initial_kpis = dashboard_service.get_sales_kpis()
        self.assertEqual(initial_kpis["total_sales_today"], 50.00)
        self.assertEqual(initial_kpis["tx_count_today"], 3)

        # Se registra y valida nueva venta en mostrador por $20.00
        self._create_posted_invoice(today, 20.00)

        # Refresco de vista
        refreshed_kpis = dashboard_service.get_sales_kpis()
        self.assertEqual(refreshed_kpis["total_sales_today"], 70.00, "Ventas del Día actualizadas a $70.00")
        self.assertEqual(refreshed_kpis["tx_count_today"], 4, "Transacciones actualizadas a 4")
        self.assertEqual(refreshed_kpis["avg_ticket"], 17.50, "Ticket Promedio actualizado a $17.50")

    def test_03_scenario_3_access_restriction_cashier(self):
        """Escenario 3: Acceso denegado con AccessError para usuarios con rol Cajero."""
        dashboard_service_cashier = self.env["caryvil.dashboard.sales"].with_user(self.user_cashier)

        with self.assertRaises(AccessError, msg="El rol Cajero debe ser bloqueado con AccessError"):
            dashboard_service_cashier.get_sales_kpis()

    def test_04_sales_last_7_days_trend_continuity(self):
        """Valida que la serie temporal de 7 días devuelva exactamente 7 días consecutivos."""
        today = fields.Date.today()
        # Venta ayer y hoy
        self._create_posted_invoice(today - timedelta(days=1), 30.00)
        self._create_posted_invoice(today, 15.00)

        dashboard_service = self.env["caryvil.dashboard.sales"].with_user(self.user_manager)
        kpis = dashboard_service.get_sales_kpis()

        trend = kpis["sales_last_7_days"]
        self.assertEqual(len(trend), 7, "La serie temporal debe contener exactamente 7 registros diarios")
        # El último registro debe coincidir con la fecha de hoy
        self.assertEqual(trend[-1]["date"], today.strftime("%Y-%m-%d"))
        self.assertEqual(trend[-1]["total"], 15.00)
        # El penúltimo registro debe coincidir con ayer
        self.assertEqual(trend[-2]["total"], 30.00)

    def test_05_top_5_medicines_ranking(self):
        """Valida el cálculo del Top 5 de medicamentos con mayor rotación en unidades e ingresos."""
        today = fields.Date.today()

        # Venta de 100 unidades de Producto A por $1000.00
        self._create_posted_invoice(today, 1000.00, product=self.product_a, qty=100)
        # Venta de 200 unidades de Producto B por $2000.00
        self._create_posted_invoice(today, 2000.00, product=self.product_b, qty=200)

        dashboard_service = self.env["caryvil.dashboard.sales"].with_user(self.user_manager)
        kpis = dashboard_service.get_sales_kpis()

        top_medicines = kpis["top_5_medicines"]
        self.assertTrue(len(top_medicines) >= 2, "Debe listar al menos los 2 medicamentos con ventas")

        top_ids = [m["product_id"] for m in top_medicines]
        self.assertIn(self.product_b.id, top_ids, "Producto B debe figurar en el ranking")
        self.assertIn(self.product_a.id, top_ids, "Producto A debe figurar en el ranking")
        self.assertLess(
            top_ids.index(self.product_b.id),
            top_ids.index(self.product_a.id),
            "Producto B (200 u) debe tener mejor posición en el ranking que Producto A (100 u)",
        )

    def test_06_zero_sales_boundary_handles_gracefully(self):
        """Valida que ante cero ventas en el día, los valores retornen en 0.0 sin error por división entre cero."""
        dashboard_service = self.env["caryvil.dashboard.sales"].with_user(self.user_manager)
        kpis = dashboard_service.get_sales_kpis()

        self.assertIsInstance(kpis["total_sales_today"], float)
        self.assertIsInstance(kpis["tx_count_today"], int)
        self.assertIsInstance(kpis["avg_ticket"], float)
        if kpis["tx_count_today"] == 0:
            self.assertEqual(kpis["avg_ticket"], 0.0)
