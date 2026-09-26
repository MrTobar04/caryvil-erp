# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.fields import Command
from odoo.tools import float_compare


class ProductProductCaryvilSearch(models.Model):

    #Extiende la búsqueda de variantes de productos para que también permita localizar medicamentos mediante su principio activo.

    _inherit = "product.product"

    @api.model
    def _name_search(
        self,
        name="",
        domain=None,
        operator="ilike",
        limit=None,
        order=None,
    ):
        domain = list(domain or [])

        positive_operators = ("=", "ilike", "=ilike", "like", "=like")

        if name and operator in positive_operators:
            ingredient_ids = self.env["caryvil.active.ingredient"]._search(
                [("name", operator, name)],
                limit=limit,
            )

            if ingredient_ids:
                product_ids = self._search(
                    [
                        ("active_ingredient_id", "in", ingredient_ids),
                    ]
                    + domain,
                    limit=limit,
                    order=order,
                )

                if product_ids:
                    return product_ids

        return super()._name_search(
            name=name,
            domain=domain,
            operator=operator,
            limit=limit,
            order=order,
        )

class SaleOrderLineCaryvilTax(models.Model):
    _inherit = "sale.order.line"

    @api.depends("product_id", "company_id", "order_id.fiscal_position_id")
    def _compute_tax_id(self):
        super()._compute_tax_id()

        caryvil_tax = self.env.ref(
            "caryvil_erp.tax_caryvil_iva_ventas_13",
            raise_if_not_found=False,
        )

        if not caryvil_tax:
            return

        for line in self.filtered(
            lambda line: (
                line.product_id
                and line.product_id.active_ingredient_id
                and line.company_id
            )
        ):
            tax = caryvil_tax.filtered(
                lambda tax: (
                    not tax.company_id
                    or tax.company_id == line.company_id
                )
            )

            if not tax:
                continue

            if line.order_id.fiscal_position_id:
                tax = line.order_id.fiscal_position_id.map_tax(tax)

            line.tax_id = tax

class SaleOrderMedicine(models.Model):
    
    # Extensión del flujo estándar de sale.order para la operación de ventas rápidas.

    _inherit = "sale.order"

    payment_method = fields.Selection(
        [
            ("efectivo", "Efectivo"),
            (
                "tarjeta_debito_credito",
                "Tarjeta de Débito / Crédito",
            ),
            (
                "transferencia_qr",
                "Transferencia / Pago QR",
            ),
        ],
        string="Forma de Pago",
        default="efectivo",
        required=True,
    )

    amount_tendered = fields.Monetary(
        string="Efectivo Recibido ($)",
        currency_field="currency_id",
        default=0.0,
    )

    amount_change = fields.Monetary(
        string="Cambio / Vuelto ($)",
        currency_field="currency_id",
        compute="_compute_amount_change",
    )

    caryvil_barcode_input = fields.Char(
        string="Escanear EAN-13",
        copy=False,
        help=(
            "Campo de entrada rápida para lectores de código de barras "
            "compatibles con entrada de teclado."
        ),
    )

    @api.model
    def _default_caryvil_customer(self):
        # Obtiene el cliente genérico de mostrador.
        partner = self.env.ref(
            "caryvil_erp.partner_consumidor_final",
            raise_if_not_found=False,
        )

        if partner:
            return partner.id

        partner = self.env["res.partner"].search(
            [
                ("name", "=", "Consumidor Final"),
            ],
            limit=1,
        )

        return partner.id if partner else False

    # El campo partner_id es requerido por sale.order.
    # Se redefine únicamente el default de Caryvil.
    @api.model
    def default_get(self, fields_list):
        vals = super().default_get(fields_list)

        if "partner_id" in fields_list and not vals.get("partner_id"):
            vals["partner_id"] = self._default_caryvil_customer()

        if "payment_method" in fields_list and not vals.get("payment_method"):
            vals["payment_method"] = "efectivo"

        return vals

    @api.depends(
        "amount_tendered",
        "amount_total",
        "payment_method",
    )
    def _compute_amount_change(self):
        # Calcula el cambio exclusivamente para pagos en efectivo.
        for order in self:
            if order.payment_method != "efectivo":
                order.amount_change = 0.0
                continue

            amount_received = order.amount_tendered or 0.0
            change = max(
                amount_received - (order.amount_total or 0.0),
                0.0,
            )

            order.amount_change = (
                order.currency_id.round(change)
                if order.currency_id
                else change
            )

    def _check_caryvil_payment(self):
        # Valida las reglas del cobro en mostrador.
        self.ensure_one()

        if self.payment_method == "efectivo":
            amount_received = self.amount_tendered or 0.0
            total = self.amount_total or 0.0

            if amount_received < total:
                raise UserError(
                    _(
                        "El monto en efectivo recibido ($%(received).2f) "
                        "es menor al total a pagar ($%(total).2f)."
                    )
                    % {
                        "received": amount_received,
                        "total": total,
                    }
                )

    def _get_caryvil_requested_quantities(self):

        # Agrupa la cantidad solicitada por producto y la convierte a la unidad de medida base del producto.
        self.ensure_one()

        requested = {}

        for line in self.order_line.filtered(
            lambda line: not line.display_type and line.product_id
        ):
            product = line.product_id

            if product.detailed_type != "product":
                continue

            qty = line.product_uom._compute_quantity(
                line.product_uom_qty,
                product.uom_id,
            )

            requested[product.id] = requested.get(product.id, 0.0) + qty

        return requested

    def _check_caryvil_stock_availability(self):
        
        # Validación inicial de existencias.

        self.ensure_one()

        requested_quantities = self._get_caryvil_requested_quantities()

        for product_id, requested_qty in requested_quantities.items():
            product = self.env["product.product"].browse(product_id)
            available_qty = product.qty_available

            if float_compare(
                requested_qty,
                available_qty,
                precision_rounding=product.uom_id.rounding,
            ) > 0:
                raise UserError(
                    _(
                        'Stock insuficiente para "%(product)s".\n'
                        "Cantidad solicitada: %(requested)s %(uom)s\n"
                        "Cantidad disponible: %(available)s %(uom)s"
                    )
                    % {
                        "product": product.display_name,
                        "requested": requested_qty,
                        "available": available_qty,
                        "uom": product.uom_id.name,
                    }
                )

    def _prepare_caryvil_sale_line_values(self, product):
        
        # Prepara una línea de venta.
        
        self.ensure_one()

        if self.pricelist_id:
            price_unit = self.pricelist_id._get_product_price(
                product=product,
                quantity=1.0,
                currency=self.currency_id,
                date=self.date_order,
            )
        else:
            price_unit = product.lst_price

        caryvil_tax = self.env.ref(
            "caryvil_erp.tax_caryvil_iva_ventas_13",
            raise_if_not_found=False,
        )
        
        if not caryvil_tax:
            raise UserError(
                _(
                    "No está configurado el impuesto "
                    "'IVA 13% Ventas Bienes Farmacéuticos'."
                )
            )
        
        taxes = caryvil_tax.filtered(
            lambda tax: (
                not tax.company_id
                or tax.company_id == self.company_id
            )
        )
        
        if self.fiscal_position_id:
            taxes = self.fiscal_position_id.map_tax(taxes)

        return {
            "product_id": product.id,
            "product_uom_qty": 1.0,
            "product_uom": product.uom_id.id,
            "price_unit": price_unit,
            "name": product.display_name,
            "tax_id": [Command.set(taxes.ids)],
        }

    def _add_caryvil_scanned_product(self, product):
        # Agrega el producto escaneado a la venta. Si ya existe, incrementa la cantidad en lugar de crear una línea duplicada.
        
        self.ensure_one()

        existing_line = self.order_line.filtered(
            lambda line: (
                not line.display_type
                and line.product_id == product
                and line.product_uom == product.uom_id
            )
        )[:1]

        if existing_line:
            existing_line.product_uom_qty += 1.0
            return

        line_values = self._prepare_caryvil_sale_line_values(product)

        self.update(
            {
                "order_line": [
                    Command.create(line_values),
                ],
            }
        )

    @api.onchange("caryvil_barcode_input")
    def _onchange_caryvil_barcode_input(self):
        
        # Procesa automáticamente un EAN-13 cuando el lector termina de introducir el código.
        # Los lectores USB configurados como teclado normalmente envían el código seguido de ENTER, lo que dispara el onchange.
        
        if not self.caryvil_barcode_input:
            return

        code = self.caryvil_barcode_input.strip()

        # No hacemos consultas mientras el usuario todavía está escribiendo.
        if len(code) < 13:
            return

        if len(code) != 13 or not code.isdigit():
            return {
                "warning": {
                    "title": _("Código inválido"),
                    "message": _(
                        "El código de barras debe contener exactamente "
                        "13 dígitos (EAN-13)."
                    ),
                }
            }

        product = self.env["product.product"].search(
            [
                ("barcode", "=", code),
                ("sale_ok", "=", True),
                ("active", "=", True),
            ],
            limit=1,
        )

        if not product:
            return {
                "warning": {
                    "title": _("Producto no encontrado"),
                    "message": _(
                        'No se encontró un medicamento activo con el '
                        'código de barras "%s".'
                    )
                    % code,
                }
            }

        self._add_caryvil_scanned_product(product)

        # Limpia el campo para permitir un nuevo escaneo.
        self.caryvil_barcode_input = False

    def _caryvil_get_invoice_action(self, invoices):
        
        # Devuelve la acción de la factura.

        self.ensure_one()

        report = self.env.ref(
            "caryvil_erp.action_report_caryvil_invoice_ticket",
            raise_if_not_found=False,
        )

        if report:
            return report.report_action(invoices[:1])

        invoice = invoices[:1]

        return {
            "type": "ir.actions.act_window",
            "name": _("Factura"),
            "res_model": "account.move",
            "view_mode": "form",
            "res_id": invoice.id,
            "views": [(False, "form")],
        }

    def action_confirm_and_invoice(self):
        
        # Flujo unificado para caja.

        self.ensure_one()

        if self.state not in ("draft", "sent"):
            raise UserError(
                _("Solo se pueden cobrar ventas en estado borrador.")
            )

        if not self.order_line.filtered(
            lambda line: not line.display_type
        ):
            raise UserError(
                _("Debe agregar al menos un medicamento a la venta.")
            )

        self._check_caryvil_payment()
        self._check_caryvil_stock_availability()

        # Flujo nativo de Odoo.
        self.action_confirm()

        invoices = self._create_invoices()

        if not invoices:
            raise UserError(
                _("No se pudo generar la factura de la venta.")
            )

        invoices.action_post()

        return self._caryvil_get_invoice_action(invoices)