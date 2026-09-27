# -*- coding: utf-8 -*-
from odoo import fields
from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPharmacyUom(TransactionCase):

    def setUp(self):
        super().setUp()

        # Unidades sólidas
        self.category_units = self.env.ref("caryvil_erp.uom_category_pharmacy_units")
        self.unit = self.env.ref("caryvil_erp.uom_unit_pill")
        self.blister4 = self.env.ref("caryvil_erp.uom_blister_4")
        self.blister10 = self.env.ref("caryvil_erp.uom_blister_10")
        self.box20 = self.env.ref("caryvil_erp.uom_box_20")
        self.box50 = self.env.ref("caryvil_erp.uom_box_50")
        self.box100 = self.env.ref("caryvil_erp.uom_box_100")

        # Unidades líquidas y semisólidas (Envases)
        self.category_packaging = self.env.ref("caryvil_erp.uom_category_pharmacy_packaging")
        self.unit_container = self.env.ref("caryvil_erp.uom_unit_container")
        self.bottle60 = self.env.ref("caryvil_erp.uom_bottle_60ml")
        self.bottle120 = self.env.ref("caryvil_erp.uom_bottle_120ml")
        self.tube_ointment = self.env.ref("caryvil_erp.uom_tube_ointment")
        self.ampoule_vial = self.env.ref("caryvil_erp.uom_ampoule_vial")
        self.box_ampoules = self.env.ref("caryvil_erp.uom_box_5_ampoules")
        self.box_bottles = self.env.ref("caryvil_erp.uom_box_12_bottles")

        # Proveedor farmacéutico para pruebas
        self.laboratorio = self.env["res.partner"].create(
            {
                "name": "Laboratorios Test Vijosa",
                "is_company": True,
                "is_pharmacy_vendor": True,
                "vendor_type": "laboratorio",
                "nit": "0614-123456-001-2",
                "nrc": "12345-6",
            }
        )

        # Cliente para ventas
        self.cliente = self.env["res.partner"].create(
            {
                "name": "Cliente Mostrador Test",
                "customer_rank": 1,
            }
        )

    # =========================================================================
    # Ratios de Conversión Sólidos
    # =========================================================================
    def test_blister_4_to_unit(self):
        """Un blíster x4 debe convertirse en 4 unidades."""
        result = self.blister4._compute_quantity(1, self.unit)
        self.assertEqual(result, 4, "Un Blíster x4 debe equivaler a 4 unidades.")

    def test_blister_10_to_unit(self):
        """Un blíster x10 debe convertirse en 10 unidades."""
        result = self.blister10._compute_quantity(1, self.unit)
        self.assertEqual(result, 10, "Un Blíster x10 debe equivaler a 10 unidades.")

    def test_box_20_to_unit(self):
        """Una caja x20 debe convertirse en 20 unidades."""
        result = self.box20._compute_quantity(1, self.unit)
        self.assertEqual(result, 20, "Una Caja x20 debe equivaler a 20 unidades.")

    def test_box_50_to_unit(self):
        """Una caja x50 debe convertirse en 50 unidades."""
        result = self.box50._compute_quantity(1, self.unit)
        self.assertEqual(result, 50, "Una Caja x50 debe equivaler a 50 unidades.")

    def test_box_100_to_unit(self):
        """Una caja x100 debe convertirse en 100 unidades."""
        result = self.box100._compute_quantity(1, self.unit)
        self.assertEqual(result, 100, "Una Caja x100 debe equivaler a 100 unidades.")

    # =========================================================================
    # Unidades Líquidas y Semisólidas (Scope 2.1)
    # =========================================================================
    def test_liquid_semisolid_uoms_exist(self):
        """Verifica la existencia y correcta parametrización de unidades líquidas/semisólidas."""
        self.assertIsNotNone(self.category_packaging)
        self.assertEqual(self.unit_container.uom_type, "reference")
        self.assertEqual(self.bottle60.category_id, self.category_packaging)
        self.assertEqual(self.bottle120.category_id, self.category_packaging)
        self.assertEqual(self.tube_ointment.category_id, self.category_packaging)
        self.assertEqual(self.ampoule_vial.category_id, self.category_packaging)

    def test_box_5_ampoules_to_vial(self):
        """Una caja x5 ampollas debe convertirse en 5 ampollas."""
        result = self.box_ampoules._compute_quantity(1, self.ampoule_vial)
        self.assertEqual(result, 5, "Una Caja x5 ampollas debe equivaler a 5 ampollas.")

    def test_box_12_bottles_to_bottle(self):
        """Una caja x12 frascos debe convertirse en 12 frascos."""
        result = self.box_bottles._compute_quantity(1, self.bottle120)
        self.assertEqual(result, 12, "Una Caja x12 frascos debe equivaler a 12 frascos.")

    # =========================================================================
    # Criterio de Aceptación: Escenario 1
    # Configuración de producto con compra en caja y venta en unidad
    # =========================================================================
    def test_scenario_1_product_dual_uom_configuration(self):
        """SPEC-7.1.2 Escenario 1: Configurar medicamento con UoM Compra = Caja x 100 y UoM Venta = Unidad."""
        product = self.env["product.product"].create(
            {
                "name": "Acetaminofén 500mg Test UoM",
                "detailed_type": "product",
                "tracking": "lot",
                "uom_id": self.unit.id,
                "uom_po_id": self.box100.id,
                "list_price": 0.10,
            }
        )

        self.assertEqual(product.uom_id, self.unit)
        self.assertEqual(product.uom_po_id, self.box100)
        self.assertEqual(product.uom_id.category_id, product.uom_po_id.category_id)

    # =========================================================================
    # Criterio de Aceptación: Escenario 2
    # Conversión automática al recibir mercadería (2 Cajas x 100 -> 200 Unidades)
    # =========================================================================
    def test_scenario_2_purchase_reception_stock_conversion(self):
        """SPEC-7.1.2 Escenario 2: 2 Cajas x 100 en orden de compra incrementan 200 pastillas en stock."""
        product = self.env["product.product"].create(
            {
                "name": "Acetaminofén 500mg Recepción Test",
                "detailed_type": "product",
                "tracking": "lot",
                "uom_id": self.unit.id,
                "uom_po_id": self.box100.id,
            }
        )

        # Crear y confirmar Orden de Compra por 2 Cajas x 100
        po = self.env["purchase.order"].create(
            {
                "partner_id": self.laboratorio.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": product.id,
                            "name": product.name,
                            "product_qty": 2.0,
                            "product_uom": self.box100.id,
                            "price_unit": 8.00,
                        },
                    )
                ],
            }
        )
        po.button_confirm()

        # Verificar que se generó el albarán de recepción
        self.assertEqual(len(po.picking_ids), 1)
        picking = po.picking_ids[0]

        # El movimiento interno de stock debe haber convertido 2 Cajas a 200 pastillas
        stock_move = picking.move_ids[0]
        self.assertEqual(stock_move.product_uom, self.unit)
        self.assertEqual(stock_move.product_uom_qty, 200.0)

        # Asignar lote y fecha de vencimiento según SPEC-8.2.1
        lot = self.env["stock.lot"].create(
            {
                "name": "LOT-ACT-TEST-2028",
                "product_id": product.id,
                "company_id": self.env.company.id,
                "expiration_date": fields.Datetime.to_datetime("2028-12-31 23:59:59"),
            }
        )

        picking.move_line_ids.write(
            {
                "quantity": 200.0,
                "lot_id": lot.id,
                "expiration_date": fields.Datetime.to_datetime("2028-12-31 23:59:59"),
            }
        )

        picking.button_validate()
        self.assertEqual(picking.state, "done")

        # Validar incremento exacto en el inventario
        self.assertEqual(product.qty_available, 200.0, "El stock debe reflejar 200 pastillas.")

    # =========================================================================
    # Criterio de Aceptación: Escenario 3
    # Descuento en mostrador por blíster (1 Blíster x 10 deduce 10 unidades)
    # =========================================================================
    def test_scenario_3_sale_blister_stock_deduction(self):
        """SPEC-7.1.2 Escenario 3: Venta de 1 Blíster x 10 descuenta 10 pastillas de 200 disponibles."""
        product = self.env["product.product"].create(
            {
                "name": "Acetaminofén 500mg Venta Test",
                "detailed_type": "product",
                "tracking": "lot",
                "uom_id": self.unit.id,
                "uom_po_id": self.box100.id,
                "list_price": 0.10,
            }
        )

        # Sembrar 200 pastillas en stock con lote
        warehouse = self.env["stock.warehouse"].search([], limit=1)
        stock_loc = warehouse.lot_stock_id
        lot = self.env["stock.lot"].create(
            {
                "name": "LOT-ACT-SALE-2028",
                "product_id": product.id,
                "company_id": self.env.company.id,
                "expiration_date": fields.Datetime.to_datetime("2028-12-31 23:59:59"),
            }
        )
        self.env["stock.quant"]._update_available_quantity(product, stock_loc, 200.0, lot_id=lot)
        self.assertEqual(product.qty_available, 200.0)

        # Crear y confirmar orden de venta por 1 Blíster x 10
        so = self.env["sale.order"].create(
            {
                "partner_id": self.cliente.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": product.id,
                            "product_uom_qty": 1.0,
                            "product_uom": self.blister10.id,
                            "price_unit": 1.50,
                        },
                    )
                ],
            }
        )
        so.action_confirm()

        # Validar albarán de entrega saliente
        out_picking = so.picking_ids[0]
        out_picking.action_assign()
        for ml in out_picking.move_line_ids:
            ml.quantity = 10.0
            ml.lot_id = lot.id

        out_picking.with_context(skip_sms=True).button_validate()
        self.assertEqual(out_picking.state, "done")

        # Validar existencia remanente exacta: 200 - 10 = 190 pastillas
        self.assertEqual(product.qty_available, 190.0, "El stock remanente debe ser exactamente 190 pastillas.")

    # =========================================================================
    # Regla de Redondeo y Restricciones
    # =========================================================================
    def test_rounding_integrity_unit_pill(self):
        """SPEC-7.1.2: La unidad base no permite fracciones menores a 1 unidad entera."""
        self.assertEqual(self.unit.rounding, 1.0, "La unidad base de pastilla debe tener redondeo de 1.0.")

    # =========================================================================
    # Seguridad y Privilegios (Sección 8)
    # =========================================================================
    def test_security_cashier_cannot_modify_uom_factor(self):
        """SPEC-7.1.2 Sección 8: Usuarios con rol Cajero no pueden modificar factores de conversión."""
        group_cashier = self.env.ref("caryvil_erp.group_caryvil_cashier")
        cashier_user = self.env["res.users"].create(
            {
                "name": "Cajero UoM Security Test",
                "login": "cajero_uom_test@caryvil.com",
                "email": "cajero_uom_test@caryvil.com",
                "groups_id": [(6, 0, [group_cashier.id])],
            }
        )

        with self.assertRaises(AccessError):
            self.box100.with_user(cashier_user).write({"factor_inv": 80.0})
