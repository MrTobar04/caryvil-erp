# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from num2words import num2words


class AccountMoveInvoice(models.Model):
    _inherit = "account.move"

    simple_invoice_number = fields.Char(
        string="N° Factura",
        readonly=True,
        index=True,
        copy=False,
    )

    payment_method_display = fields.Char(
        string="Método de Pago",
        compute="_compute_payment_method_display",
        readonly=True,
    )

    amount_in_words = fields.Char(
        string="Monto en Letras",
        compute="_compute_amount_in_words",
        readonly=True,
    )

    @api.depends(
        "invoice_line_ids.sale_line_ids.order_id.payment_method",
    )
    def _compute_payment_method_display(self):
        payment_labels = {
            "efectivo": "Efectivo",
            "tarjeta_debito_credito": "Tarjeta",
            "transferencia_qr": "Transferencia",
        }

        for move in self:
            orders = move.invoice_line_ids.sale_line_ids.order_id

            if orders:
                payment_method = orders[:1].payment_method
                move.payment_method_display = payment_labels.get(
                    payment_method,
                    payment_method or "",
                )
            else:
                move.payment_method_display = ""

    @api.depends("amount_total")
    def _compute_amount_in_words(self):
        for move in self:
            if not move.amount_total or not move.currency_id:
                move.amount_in_words = "CERO DÓLARES CON 00/100 USD"
                continue

            amount = move.currency_id.round(move.amount_total)

            entero = int(amount)

            decimales = int(
                round((amount - entero) * 100)
            )

            if decimales == 100:
                entero += 1
                decimales = 0

            texto = num2words(
                entero,
                lang="es",
            ).upper()

            move.amount_in_words = (
                f"{texto} DÓLARES CON "
                f"{decimales:02d}/100 USD"
            )

    def _caryvil_get_discount_total(self):
        self.ensure_one()

        discount_total = 0.0

        invoice_lines = self.invoice_line_ids.filtered(
            lambda line: line.display_type == "product"
        )

        for invoice_line in invoice_lines:
            sale_line = invoice_line.sale_line_ids[:1]

            if not sale_line:
                continue

            discount = sale_line.discount or 0.0

            discount_total += (
                invoice_line.price_unit
                * invoice_line.quantity
                * discount
                / 100.0
            )

        return self.currency_id.round(discount_total)

    def action_post(self):
        result = super().action_post()

        invoice_sequence = self.env["ir.sequence"]

        for move in self.filtered(
            lambda move: (
                move.move_type == "out_invoice"
                and move.state == "posted"
            )
        ):
            if not move.simple_invoice_number or move.simple_invoice_number == "/":
                move.simple_invoice_number = (
                    invoice_sequence.with_company(
                        move.company_id
                    ).next_by_code(
                        "caryvil.simple.invoice.sequence",
                        sequence_date=move.invoice_date or move.date,
                    )
                    or "/"
                )

        return result

class ProductTemplateCaryvilAccounting(models.Model):
    _inherit = "product.template"

    def _get_product_accounts(self):
        accounts = super()._get_product_accounts()

        if len(self) != 1 or not self.active_ingredient_id:
            return accounts

        sales_account = self.env.ref(
            "caryvil_erp.account_caryvil_ventas_medicamentos",
            raise_if_not_found=False,
        )

        if not sales_account:
            return accounts

        if sales_account.company_id == self.env.company:
            accounts["income"] = sales_account

        return accounts

class SaleOrderLineCaryvilInvoice(models.Model):
    _inherit = "sale.order.line"

    def _prepare_invoice_line(self, **optional_values):
        values = super()._prepare_invoice_line(
            **optional_values
        )

        account = self.env.ref(
            "caryvil_erp.account_caryvil_ventas_medicamentos",
            raise_if_not_found=False,
        )

        if account:
            for line in self:
                if (
                    line.product_id
                    and line.product_id.active_ingredient_id
                ):
                    values["account_id"] = account.id

        return values


class SaleOrderCaryvilInvoice(models.Model):
    _inherit = "sale.order"

    def action_confirm_and_invoice(self):
        #Mantiene el flujo de SPEC-9.1.1

        result = super().action_confirm_and_invoice()

        for order in self:
            invoices = order.invoice_ids.filtered(
                lambda move: (
                    move.move_type == "out_invoice"
                    and move.state == "posted"
                )
            )

            for invoice in invoices.filtered(
                lambda move: move.payment_state != "paid"
            ):
                invoice._register_caryvil_payment(
                    order.payment_method
                )

        return result


class AccountMoveCaryvilPayment(models.Model):
    _inherit = "account.move"

    def _register_caryvil_payment(self, payment_method):
        #Registra automáticamente el pago completo de la factura utilizando el diario de caja o banco.

        self.ensure_one()

        if self.move_type != "out_invoice":
            return False

        if self.state != "posted":
            raise UserError(
                _(
                    "La factura debe estar publicada antes "
                    "de registrar el pago."
                )
            )

        if self.payment_state == "paid":
            return True

        if payment_method == "efectivo":
            journal_ref = (
                "caryvil_erp.journal_caryvil_cash"
            )
        else:
            journal_ref = (
                "caryvil_erp.journal_caryvil_bank"
            )

        journal = self.env.ref(
            journal_ref,
            raise_if_not_found=False,
        )

        if not journal:
            raise UserError(
                _(
                    "No está configurado el diario "
                    "de cobro de Caryvil."
                )
            )

        if self.amount_residual <= 0:
            return True

        payment_register = (
            self.env["account.payment.register"]
            .with_context(
                active_model="account.move",
                active_ids=self.ids,
            )
            .sudo()
            .create(
                {
                    "journal_id": journal.id,
                    "amount": self.amount_residual,
                    "payment_date": fields.Date.context_today(
                        self
                    ),
                }
            )
        )

        payment_register._create_payments()

        return True