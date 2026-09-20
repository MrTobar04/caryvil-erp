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
        self.producto = self.env["product.template"].create(
            {
                "name": "Amoxicilina 500mg (Caja x 50)",
            }
        )

    # Se puede registrar un proveedor para un medicamento, con presentación y precio propios.
    def test_crear_supplierinfo_con_presentacion(self):
        supplierinfo = self.env["product.supplierinfo"].create(
            {
                "partner_id": self.laboratorio.id,
                "product_tmpl_id": self.producto.id,
                "product_presentation": "Caja con 50 tabletas",
                "price": 4.50,
            }
        )
        self.assertEqual(supplierinfo.product_presentation, "Caja con 50 tabletas")
        self.assertEqual(supplierinfo.price, 4.50)

    # Un medicamento puede tener más de un proveedor, para comparar precios.
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
                "product_tmpl_id": self.producto.id,
                "price": 4.50,
            }
        )
        self.env["product.supplierinfo"].create(
            {
                "partner_id": laboratorio_2.id,
                "product_tmpl_id": self.producto.id,
                "price": 4.80,
            }
        )
        self.assertEqual(len(self.producto.seller_ids), 2)

    # El % de descuento debe recalcular el precio unitario automáticamente (onchange).
    def test_onchange_descuento_recalcula_precio(self):
        supplierinfo = self.env["product.supplierinfo"].new(
            {
                "partner_id": self.laboratorio.id,
                "product_tmpl_id": self.producto.id,
                "price": 10.0,
                "discount_percentage": 10.0,
            }
        )
        supplierinfo._onchange_discount_percentage()
        self.assertEqual(supplierinfo.price, 9.0)
