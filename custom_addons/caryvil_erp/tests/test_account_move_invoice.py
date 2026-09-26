# -*- coding: utf-8 -*-

from odoo import Command
from odoo.tests.common import TransactionCase


class TestAccountMoveInvoice(TransactionCase):

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

        cls.tax_account = cls.env.ref(
            "caryvil_erp.account_caryvil_iva_debito_fiscal"
        )

        cls.sale_journal = cls.env["account.journal"].search(
            [
                ("type", "=", "sale"),
                ("company_id", "=", cls.company.id),
            ],
            limit=1,
        )

        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Consumidor Final Test",
                "customer_rank": 1,
                "is_pharmacy_customer": True,
            }
        )

        cls.product = cls.env["product.product"].create(
            {
                "name": "Medicamento Factura Test",
                "detailed_type": "product",
                "sale_ok": True,
                "list_price": 10.00,
                "taxes_id": [
                    Command.set([cls.tax.id]),
                ],
            }
        )

    def _create_invoice(self):
        """
        Crea una factura de cliente por $10.00 netos más IVA 13%, para obtener un total de $11.30.
        """

        return self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.partner.id,
                "company_id": self.company.id,
                "currency_id": self.company.currency_id.id,
                "journal_id": self.sale_journal.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "name": self.product.display_name,
                            "quantity": 1.0,
                            "price_unit": 10.00,
                            "account_id": self.sales_account.id,
                            "tax_ids": [
                                Command.set([self.tax.id]),
                            ],
                        }
                    ),
                ],
            }
        )

    def test_01_invoice_is_posted_and_has_number(self):
        """
        SPEC-9.2.1:
        La factura debe quedar publicada y recibir un número correlativo FAC-YYYY-XXXXX.
        """

        invoice = self._create_invoice()

        invoice.action_post()

        self.assertEqual(
            invoice.state,
            "posted",
        )

        self.assertTrue(
            invoice.simple_invoice_number,
        )

        self.assertRegex(
            invoice.simple_invoice_number,
            r"^FAC-\d{4}-\d{5}$",
        )

    def test_02_invoice_sequence_increments_by_one(self):
        """
        SPEC-9.2.1:
        Dos facturas consecutivas deben incrementar la secuencia exactamente en 1.
        """

        invoice_1 = self._create_invoice()
        invoice_1.action_post()

        invoice_2 = self._create_invoice()
        invoice_2.action_post()

        number_1 = int(
            invoice_1.simple_invoice_number[-5:]
        )

        number_2 = int(
            invoice_2.simple_invoice_number[-5:]
        )

        self.assertEqual(
            number_2,
            number_1 + 1,
        )

    def test_03_amount_in_words(self):
        """
        SPEC-9.2.1:
        Una factura de $11.30 debe generar correctamente el monto en letras.
        """

        invoice = self._create_invoice()

        invoice.action_post()

        self.assertAlmostEqual(
            invoice.amount_untaxed,
            10.00,
            places=2,
        )

        self.assertAlmostEqual(
            invoice.amount_tax,
            1.30,
            places=2,
        )

        self.assertAlmostEqual(
            invoice.amount_total,
            11.30,
            places=2,
        )

        self.assertEqual(
            invoice.amount_in_words,
            "ONCE DÓLARES CON 30/100 USD",
        )

    def test_04_invoice_uses_caryvil_accounts(self):
        """
        SPEC-9.2.1:
        La factura debe utilizar: 4101 para ingresos y 2107 para IVA.
        """

        invoice = self._create_invoice()

        invoice.action_post()

        income_lines = invoice.invoice_line_ids.filtered(
            lambda line: line.display_type == "product"
        )

        self.assertIn(
            self.sales_account.id,
            income_lines.mapped("account_id").ids,
        )

        tax_lines = invoice.line_ids.filtered(
            lambda line: line.tax_line_id == self.tax
        )

        self.assertTrue(
            tax_lines,
        )

        self.assertIn(
            self.tax_account.id,
            tax_lines.mapped("account_id").ids,
        )

    def test_05_invoice_registers_cash_payment(self):
        """
        SPEC-9.2.1:
        El cobro en efectivo debe registrarse automáticamente y dejar la factura pagada.
        """

        invoice = self._create_invoice()

        invoice.action_post()

        invoice._register_caryvil_payment(
            "efectivo"
        )

        invoice.invalidate_recordset()

        self.assertEqual(
            invoice.payment_state,
            "paid",
        )