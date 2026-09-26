# -*- coding: utf-8 -*-

from odoo import Command
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestReportInvoiceTicket(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.company = cls.env.ref(
            "caryvil_erp.company_farmacia_caryvil"
        )

        cls.tax = cls.env.ref(
            "caryvil_erp.tax_caryvil_iva_ventas_13"
        )

        cls.sales_account = cls.env.ref(
            "caryvil_erp.account_caryvil_ventas_medicamentos"
        )

        cls.sale_journal = cls.env["account.journal"].search(
            [
                ("type", "=", "sale"),
                ("company_id", "=", cls.company.id),
            ],
            limit=1,
        )

        cls.ingredient = cls.env[
            "caryvil.active.ingredient"
        ].create(
            {
                "name": "Principio Activo Reporte Test",
            }
        )

        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Cliente Reporte Test",
                "dui": "06141234-5",
                "customer_rank": 1,
                "is_pharmacy_customer": True,
            }
        )

        cls.consumer = cls.env.ref(
            "caryvil_erp.partner_consumidor_final"
        )

        cls.product_template_1 = cls.env["product.template"].create(
            {
                "name": "Ibuprofeno 600mg",
                "detailed_type": "product",
                "sale_ok": True,
                "list_price": 1.00,
                "active_ingredient_id": cls.ingredient.id,
                "concentration": "600 mg",
                "taxes_id": [
                    Command.set([cls.tax.id]),
                ],
            }
        )

        cls.product_1 = cls.product_template_1.product_variant_id

        cls.product_template_2 = cls.env["product.template"].create(
            {
                "name": "Virogrip AM GelCaps",
                "detailed_type": "product",
                "sale_ok": True,
                "list_price": 0.86,
                "active_ingredient_id": cls.ingredient.id,
                "concentration": "GelCaps",
                "taxes_id": [
                    Command.set([cls.tax.id]),
                ],
            }
        )

        cls.product_2 = cls.product_template_2.product_variant_id

    def _create_invoice_from_sale(
        self,
        partner,
        amount_tendered=0.0,
        price_1=1.00,
        price_2=0.86,
        discount=0.0,
    ):
        order = self.env["sale.order"].create(
            {
                "partner_id": partner.id,
                "company_id": self.company.id,
                "payment_method": "efectivo",
                "amount_tendered": amount_tendered,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product_1.id,
                            "product_uom_qty": 1.0,
                            "product_uom": self.product_1.uom_id.id,
                            "price_unit": price_1,
                            "discount": discount,
                        }
                    ),
                    Command.create(
                        {
                            "product_id": self.product_2.id,
                            "product_uom_qty": 1.0,
                            "product_uom": self.product_2.uom_id.id,
                            "price_unit": price_2,
                            "discount": 0.0,
                        }
                    ),
                ],
            }
        )

        order.action_confirm()

        invoice = order._create_invoices()
        invoice.action_post()

        return order, invoice

    def _render_report(self, invoice):
        return self.env[
            "ir.actions.report"
        ]._render_qweb_pdf(
            "caryvil_erp.report_invoice_ticket_template",
            invoice.ids,
        )

    def test_01_render_ticket_with_change(self):
        """
        SPEC-3.3.1:
        Una venta pagada con $3.00 debe reflejar el cambio en el ticket.
        """

        order, invoice = self._create_invoice_from_sale(
            self.partner,
            amount_tendered=3.00,
        )

        self.assertAlmostEqual(
            invoice.amount_total,
            2.10,
            places=2,
        )

        self.assertAlmostEqual(
            order.amount_change,
            0.90,
            places=2,
        )

        content, report_type = self._render_report(invoice)

        self.assertIn(
            report_type,
            ("pdf", "html"),
        )

        self.assertGreater(
            len(content),
            1000,
        )

        self.assertIn(
            b"Ibuprofeno 600mg",
            content,
        )

        self.assertIn(
            b"Virogrip AM GelCaps",
            content,
        )

        self.assertIn(
            b"IVA (13%)",
            content,
        )

    def test_02_consumer_final_without_dui(self):
        """
        SPEC-3.3.1:
        Consumidor Final debe mostrarse sin error y con DUI N/A.
        """

        _order, invoice = self._create_invoice_from_sale(
            self.consumer,
            amount_tendered=3.00,
        )

        self.assertFalse(
            invoice.partner_id.dui
        )

        content, _report_type = self._render_report(
            invoice
        )

        self.assertIn(
            b"Consumidor Final",
            content,
        )

        self.assertIn(
            b"N/A",
            content,
        )

    def test_03_discount_and_iva_breakdown(self):
        """
        SPEC-3.3.1:
        El reporte debe mostrar descuento e IVA.
        """

        _order, invoice = self._create_invoice_from_sale(
            self.partner,
            amount_tendered=12.00,
            price_1=10.00,
            price_2=0.00,
            discount=10.0,
        )

        self.assertAlmostEqual(
            invoice.amount_untaxed,
            9.00,
            places=2,
        )

        self.assertAlmostEqual(
            invoice.amount_tax,
            1.17,
            places=2,
        )

        self.assertAlmostEqual(
            invoice.amount_total,
            10.17,
            places=2,
        )

        self.assertAlmostEqual(
            invoice._caryvil_get_discount_total(),
            1.00,
            places=2,
        )

        content, _report_type = self._render_report(
            invoice
        )

        self.assertIn(
            b"Descuento",
            content,
        )

        self.assertIn(
            b"IVA (13%)",
            content,
        )