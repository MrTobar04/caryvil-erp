# -*- coding: utf-8 -*-
from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPurchaseOrderMedicine(TransactionCase):

    def setUp(self):
        super().setUp()
        self.laboratorio = self.env["res.partner"].create(
            {
                "name": "Laboratorios Vijosa",
                "is_company": True,
                "is_pharmacy_vendor": True,
                "vendor_type": "laboratorio",
                "nit": "0614-123456-001-2",
                "nrc": "12345-6",
            }
        )
        self.vendedor = self.env["res.partner"].create(
            {
                "name": "Carlos Méndez",
                "is_pharmacy_vendor": True,
                "parent_id": self.laboratorio.id,
            }
        )
        self.producto = self.env["product.product"].create(
            {
                "name": "Amoxicilina 500mg",
                "purchase_method": "purchase",
            }
        )

    # El campo laboratory_id debe derivarse automáticamente de la empresa del vendedor seleccionado.
    def test_laboratory_id_derivado_del_vendedor(self):
        orden = self.env["purchase.order"].create(
            {
                "partner_id": self.vendedor.id,
            }
        )
        self.assertEqual(orden.laboratory_id, self.laboratorio)

    # Cálculo de subtotal, IVA y total sobre una línea de compra. El 13% se calcula sobre el
    # total de la orden (no depende de ningún impuesto configurado en el producto/línea).
    def test_calculo_subtotal_iva_total(self):
        orden = self.env["purchase.order"].create(
            {
                "partner_id": self.vendedor.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.producto.id,
                            "name": self.producto.name,
                            "product_qty": 10,
                            "price_unit": 4.50,
                        },
                    )
                ],
            }
        )
        self.assertAlmostEqual(orden.amount_untaxed, 45.0, places=2)
        self.assertAlmostEqual(orden.amount_tax, 5.85, places=2)
        self.assertAlmostEqual(orden.amount_total_final, 50.85, places=2)

    # El IVA Percibido (1%) solo se calcula si el check está activo y el total supera $100.
    def test_iva_percibido_requiere_check_y_supera_100(self):
        orden = self.env["purchase.order"].create(
            {
                "partner_id": self.vendedor.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.producto.id,
                            "name": self.producto.name,
                            "product_qty": 30,
                            "price_unit": 4.50,
                        },
                    )
                ],
            }
        )
        # total sin percibido = 135 * 1.13 = 152.55 > 100, pero el check sigue apagado por defecto.
        total_sin_percibido = orden.amount_total
        self.assertGreater(total_sin_percibido, 100)
        self.assertFalse(orden.iva_percibido_check)
        self.assertEqual(orden.amount_iva_percibido, 0.0)
        self.assertAlmostEqual(orden.amount_total_final, total_sin_percibido, places=2)

        orden.iva_percibido_check = True
        self.assertAlmostEqual(orden.amount_iva_percibido, total_sin_percibido * 0.01, places=2)
        self.assertAlmostEqual(orden.amount_total_final, total_sin_percibido * 1.01, places=2)

    # Aunque el check esté activo, si la factura no supera $100 no se cobra IVA Percibido.
    def test_iva_percibido_no_aplica_bajo_100(self):
        orden = self.env["purchase.order"].create(
            {
                "partner_id": self.vendedor.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.producto.id,
                            "name": self.producto.name,
                            "product_qty": 1,
                            "price_unit": 4.50,
                        },
                    )
                ],
                "iva_percibido_check": True,
            }
        )
        total_sin_percibido = orden.amount_total
        self.assertLess(total_sin_percibido, 100)
        self.assertEqual(orden.amount_iva_percibido, 0.0)

    # SPEC-8.1.2: el estado de pago refleja los abonos parciales registrados contra la factura.
    def test_abonos_parciales_actualizan_estado_de_pago(self):
        orden = self.env["purchase.order"].create(
            {
                "partner_id": self.vendedor.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.producto.id,
                            "name": self.producto.name,
                            "product_qty": 10,
                            "price_unit": 50.0,
                        },
                    )
                ],
            }
        )
        orden.button_confirm()
        self.assertEqual(orden.payment_status_label, "sin_facturar")

        orden.action_create_invoice()
        factura = orden.invoice_ids
        factura.invoice_date = fields.Date.today()
        factura.action_post()
        self.assertEqual(orden.payment_status_label, "pendiente")
        # 10 x $50 + IVA 13% automático = $565.00
        self.assertAlmostEqual(orden.amount_residual_total, 565.0, places=2)

        pago_1 = (
            self.env["account.payment.register"]
            .with_context(active_model="account.move", active_ids=factura.ids)
            .create({"amount": 200.0})
        )
        pago_1._create_payments()
        self.assertEqual(orden.payment_status_label, "parcial")
        self.assertAlmostEqual(orden.amount_residual_total, 365.0, places=2)

        pago_2 = (
            self.env["account.payment.register"]
            .with_context(active_model="account.move", active_ids=factura.ids)
            .create({"amount": 365.0})
        )
        pago_2._create_payments()
        self.assertEqual(orden.payment_status_label, "pagado")
        self.assertAlmostEqual(orden.amount_residual_total, 0.0, places=2)

    # No se puede confirmar una orden sin líneas.
    def test_bloqueo_confirmacion_sin_lineas(self):
        orden = self.env["purchase.order"].create(
            {
                "partner_id": self.vendedor.id,
            }
        )
        with self.assertRaises(ValidationError):
            orden.button_confirm()

    # No se puede confirmar una orden con una línea en cantidad cero.
    def test_bloqueo_confirmacion_cantidad_cero(self):
        orden = self.env["purchase.order"].create(
            {
                "partner_id": self.vendedor.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.producto.id,
                            "name": self.producto.name,
                            "product_qty": 0,
                            "price_unit": 4.50,
                        },
                    )
                ],
            }
        )
        with self.assertRaises(ValidationError):
            orden.button_confirm()

    # button_confirm() debe generar el albarán de recepción (stock.picking) al confirmar.
    def test_confirmacion_genera_albaran_recepcion(self):
        orden = self.env["purchase.order"].create(
            {
                "partner_id": self.vendedor.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.producto.id,
                            "name": self.producto.name,
                            "product_qty": 10,
                            "price_unit": 4.50,
                        },
                    )
                ],
            }
        )
        orden.button_confirm()
        self.assertEqual(orden.state, "purchase")
        self.assertTrue(orden.picking_ids)
        self.assertEqual(orden.picking_ids[0].state, "assigned")

    # Un proveedor no catalogado como farmacéutico no puede usarse en una orden de compra.
    def test_proveedor_no_farmaceutico_bloqueado(self):
        proveedor_generico = self.env["res.partner"].create(
            {
                "name": "Proveedor de Oficina",
            }
        )
        with self.assertRaises(ValidationError):
            self.env["purchase.order"].create(
                {
                    "partner_id": proveedor_generico.id,
                }
            )
