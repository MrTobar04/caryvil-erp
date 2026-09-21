# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestProductSupplierinfo(TransactionCase):

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
                "name": "Carlos Méndez (Vijosa)",
                "is_pharmacy_vendor": True,
                "parent_id": self.laboratorio.id,
            }
        )
        self.producto_template = self.env["product.template"].create(
            {
                "name": "Amoxicilina 500mg (Caja x 50)",
                "purchase_method": "purchase",
            }
        )
        self.producto = self.producto_template.product_variant_ids[0]

    # CA-1: Se puede registrar un proveedor para un medicamento con presentación y precio propios.
    def test_crear_supplierinfo_con_presentacion(self):
        supplierinfo = self.env["product.supplierinfo"].create(
            {
                "partner_id": self.laboratorio.id,
                "product_tmpl_id": self.producto_template.id,
                "product_presentation": "Caja con 50 tabletas",
                "gross_price": 5.00,
                "discount_percentage": 10.0,
                "price": 4.50,
            }
        )
        self.assertEqual(supplierinfo.product_presentation, "Caja con 50 tabletas")
        self.assertEqual(supplierinfo.gross_price, 5.00)
        self.assertEqual(supplierinfo.discount_percentage, 10.0)
        self.assertEqual(supplierinfo.price, 4.50)

    # CA-1: Un medicamento puede tener múltiples proveedores registrados para comparar costos.
    def test_multiples_proveedores_mismo_medicamento(self):
        laboratorio_2 = self.env["res.partner"].create(
            {
                "name": "Droguería Santa Lucía",
                "is_company": True,
                "is_pharmacy_vendor": True,
                "vendor_type": "drogueria",
                "nrc": "54321-0",
            }
        )
        self.env["product.supplierinfo"].create(
            {
                "partner_id": self.laboratorio.id,
                "product_tmpl_id": self.producto_template.id,
                "price": 4.50,
                "delay": 2,
            }
        )
        self.env["product.supplierinfo"].create(
            {
                "partner_id": laboratorio_2.id,
                "product_tmpl_id": self.producto_template.id,
                "price": 4.80,
                "delay": 1,
            }
        )
        self.assertEqual(len(self.producto_template.seller_ids), 2)
        sellers = self.producto_template.seller_ids
        self.assertIn(self.laboratorio, sellers.mapped("partner_id"))
        self.assertIn(laboratorio_2, sellers.mapped("partner_id"))

    # Validación de cálculo determinista y no acumulativo de descuento.
    def test_onchange_descuento_no_acumulativo(self):
        supplierinfo = self.env["product.supplierinfo"].new(
            {
                "partner_id": self.laboratorio.id,
                "product_tmpl_id": self.producto_template.id,
                "gross_price": 10.0,
                "discount_percentage": 10.0,
            }
        )
        supplierinfo._onchange_pricing_caryvil()
        self.assertEqual(supplierinfo.price, 9.0)

        # Modificación posterior a 20% no debe degradar sobre 9.0 sino sobre 10.0 original
        supplierinfo.discount_percentage = 20.0
        supplierinfo._onchange_pricing_caryvil()
        self.assertEqual(supplierinfo.price, 8.0)

        # Retorno a 0% recupera el precio bruto completo
        supplierinfo.discount_percentage = 0.0
        supplierinfo._onchange_pricing_caryvil()
        self.assertEqual(supplierinfo.price, 10.0)

    # CA-2: Autocompletado de precio pactado en Órdenes de Compra (purchase.order.line).
    def test_autocompletado_precio_orden_compra(self):
        self.env["product.supplierinfo"].create(
            {
                "partner_id": self.laboratorio.id,
                "product_tmpl_id": self.producto_template.id,
                "price": 4.50,
                "min_qty": 1.0,
            }
        )
        # Buscar lista de proveedor según motor de compras
        seller = self.producto._select_seller(
            partner_id=self.laboratorio,
            quantity=5.0,
            uom_id=self.producto.uom_po_id,
        )
        self.assertTrue(seller)
        self.assertEqual(seller.price, 4.50)

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
                            "product_qty": 5.0,
                            "price_unit": seller.price,
                        },
                    )
                ],
            }
        )
        self.assertEqual(orden.order_line[0].price_unit, 4.50)
        self.assertEqual(orden.order_line[0].price_subtotal, 22.50)

    # CA-3: Aplicación automática de precio por escala de volumen (min_qty).
    def test_precio_escala_volumen_min_qty(self):
        # Escala 1: Menos de 10 cajas a $5.00
        self.env["product.supplierinfo"].create(
            {
                "partner_id": self.laboratorio.id,
                "product_tmpl_id": self.producto_template.id,
                "min_qty": 1.0,
                "price": 5.00,
            }
        )
        # Escala 2: 10 o más cajas a $4.20
        self.env["product.supplierinfo"].create(
            {
                "partner_id": self.laboratorio.id,
                "product_tmpl_id": self.producto_template.id,
                "min_qty": 10.0,
                "price": 4.20,
            }
        )

        seller_menor = self.producto._select_seller(
            partner_id=self.laboratorio,
            quantity=5.0,
            uom_id=self.producto.uom_po_id,
        )
        self.assertEqual(seller_menor.price, 5.00)

        seller_mayor = self.producto._select_seller(
            partner_id=self.laboratorio,
            quantity=12.0,
            uom_id=self.producto.uom_po_id,
        )
        self.assertEqual(seller_mayor.price, 4.20)
