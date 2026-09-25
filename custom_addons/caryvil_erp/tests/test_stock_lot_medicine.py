# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo import fields


class TestStockLotMedicine(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.product = cls.env["product.product"].create(
            {
                "name": "Medicamento Test SPEC-7.2.1",
                "type": "product",
                "tracking": "lot",
            }
        )

        cls.customer = cls.env["res.partner"].create(
            {
                "name": "Cliente Test SPEC-7.2.1",
            }
        )

        cls.stock_location = cls.env.ref("stock.stock_location_stock")
        cls.customer_location = cls.env.ref("stock.stock_location_customers")

        # Usuarios de prueba para verificar seguridad
        cls.cashier_user = cls.env["res.users"].create(
            {
                "name": "Cajero Prueba SPEC-7.2.1",
                "login": "cajero_test_spec721",
                "email": "cajero_test@caryvil.com",
                "groups_id": [(6, 0, [cls.env.ref("caryvil_erp.group_caryvil_cashier").id])],
            }
        )

        cls.manager_user = cls.env["res.users"].create(
            {
                "name": "Gerente Prueba SPEC-7.2.1",
                "login": "gerente_test_spec721",
                "email": "gerente_test@caryvil.com",
                "groups_id": [(6, 0, [cls.env.ref("caryvil_erp.group_caryvil_manager").id])],
            }
        )

    def _create_lot(self, expiration_date, bypass_check=False):
        context = dict(self.env.context)
        if bypass_check:
            context["bypass_expiration_check"] = True

        return (
            self.env["stock.lot"]
            .with_context(context)
            .create(
                {
                    "name": "LOT-TEST-%s" % expiration_date,
                    "product_id": self.product.id,
                    "company_id": self.env.company.id,
                    "expiration_date": expiration_date,
                }
            )
        )

    def _add_stock(self, lot, quantity=10):
        self.env["stock.quant"]._update_available_quantity(
            self.product,
            self.stock_location,
            quantity,
            lot_id=lot,
        )

    def _create_delivery(self, lot, quantity=1):
        picking_type = self.env["stock.picking.type"].search(
            [
                ("code", "=", "outgoing"),
                ("warehouse_id.company_id", "=", self.env.company.id),
            ],
            limit=1,
        )

        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": picking_type.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
                "partner_id": self.customer.id,
            }
        )

        self.env["stock.move"].create(
            {
                "name": self.product.name,
                "product_id": self.product.id,
                "product_uom_qty": quantity,
                "product_uom": self.product.uom_id.id,
                "picking_id": picking.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
            }
        )

        picking.action_confirm()
        picking.action_assign()

        move_line = picking.move_line_ids.filtered(lambda line: line.product_id == self.product)[:1]
        move_line.quantity = quantity
        move_line.lot_id = lot

        return picking

    def test_expired_lot_is_marked_as_expired(self):
        """Verifica que un lote con fecha vencida se marque reactivamente como is_expired = True."""
        lot = self._create_lot(
            fields.Datetime.subtract(fields.Datetime.now(), days=1),
            bypass_check=True,
        )
        self.assertTrue(
            lot.is_expired,
            "Un lote con fecha de vencimiento pasada debe marcarse como vencido.",
        )

    def test_expired_lot_cannot_be_dispensed(self):
        """Verifica que un albarán de salida hacia un cliente sea bloqueado si el lote está vencido."""
        lot = self._create_lot(
            fields.Datetime.subtract(fields.Datetime.now(), days=1),
            bypass_check=True,
        )
        self._add_stock(lot)
        picking = self._create_delivery(lot)

        with self.assertRaisesRegex(
            ValidationError,
            "No es posible dispensar el lote .* porque se encuentra vencido.",
        ):
            picking.button_validate()

    def test_valid_lot_can_be_dispensed(self):
        """Verifica que un lote con fecha futura vigente se dispense sin errores."""
        lot = self._create_lot(fields.Datetime.add(fields.Datetime.now(), days=30))
        self._add_stock(lot)
        picking = self._create_delivery(lot)
        picking.button_validate()

        self.assertEqual(
            picking.state,
            "done",
            "Un lote vigente debe poder dispensarse correctamente.",
        )

    def test_constraint_blocks_retroactive_expiration_date(self):
        """Verifica que el ORM impida ingresar lotes cuya fecha sea anterior a la creación/recepción."""
        past_date = fields.Datetime.subtract(fields.Datetime.now(), days=2)
        with self.assertRaisesRegex(
            ValidationError,
            "La fecha de vencimiento del lote .* no puede ser anterior a su fecha de creación/recepción.",
        ):
            self.env["stock.lot"].create(
                {
                    "name": "LOT-INVALID-PAST",
                    "product_id": self.product.id,
                    "company_id": self.env.company.id,
                    "expiration_date": past_date,
                }
            )

    def test_constraint_blocks_illogical_future_date(self):
        """Verifica que no se permitan fechas de vencimiento mayores a 10 años en el futuro."""
        absurd_future_date = fields.Datetime.now() + relativedelta(years=12)
        with self.assertRaisesRegex(
            ValidationError,
            "La fecha de vencimiento del lote .* no puede exceder un rango lógico de 10 años en el futuro.",
        ):
            self.env["stock.lot"].create(
                {
                    "name": "LOT-INVALID-FUTURE",
                    "product_id": self.product.id,
                    "company_id": self.env.company.id,
                    "expiration_date": absurd_future_date,
                }
            )

    def test_default_alert_and_removal_dates_computation(self):
        """Verifica que alert_date (60d) y removal_date (15d) se asignen por defecto automáticamente."""
        future_date = fields.Datetime.add(fields.Datetime.now(), days=90)
        lot = self._create_lot(future_date)

        expected_alert = fields.Datetime.subtract(future_date, days=60)
        expected_removal = fields.Datetime.subtract(future_date, days=15)

        self.assertTrue(lot.alert_date, "alert_date debe ser calculada automáticamente.")
        self.assertTrue(lot.removal_date, "removal_date debe ser calculada automáticamente.")
        self.assertEqual(lot.alert_date, expected_alert)
        self.assertEqual(lot.removal_date, expected_removal)

    def test_security_non_admin_cannot_modify_expiration_date(self):
        """Verifica que un cajero no pueda modificar la fecha de caducidad, pero un Administrador sí."""
        future_date = fields.Datetime.add(fields.Datetime.now(), days=60)
        lot = self._create_lot(future_date)

        # Intento como cajero (debe fallar)
        with self.assertRaisesRegex(
            ValidationError,
            "Solo un Administrador de Farmacia Caryvil puede modificar la fecha de vencimiento de un lote.",
        ):
            lot.with_user(self.cashier_user).write({"expiration_date": fields.Datetime.add(future_date, days=30)})

        # Modificación legítima como Administrador / Propietario (debe triunfar y auditar en chatter)
        new_date = fields.Datetime.add(future_date, days=45)
        lot.with_user(self.manager_user).write({"expiration_date": new_date})
        self.assertEqual(lot.expiration_date, new_date)

        # Verificar mensaje en chatter
        messages = lot.message_ids.mapped("body")
        has_audit_message = any("Fecha de vencimiento modificada" in msg for msg in messages)
        self.assertTrue(has_audit_message, "El cambio de fecha debe quedar auditado en el chatter.")

    def test_cron_updates_expired_lots(self):
        """Verifica que el cron diario sincronice el campo is_expired de lotes vencidos."""
        lot = self._create_lot(fields.Datetime.add(fields.Datetime.now(), days=1))
        self.assertFalse(lot.is_expired)

        # Simular que el lote venció actualizando su fecha de vencimiento en BD
        self.env.cr.execute(
            "UPDATE stock_lot SET expiration_date = %s, is_expired = FALSE WHERE id = %s",
            (fields.Datetime.subtract(fields.Datetime.now(), days=2), lot.id),
        )
        lot.invalidate_recordset()

        # Ejecutar acción del cron
        self.env["stock.lot"]._cron_update_expired_lots()
        lot.invalidate_recordset()

        self.assertTrue(
            lot.is_expired,
            "El cron debe marcar is_expired = True para lotes que hayan alcanzado su fecha de caducidad.",
        )

    def test_lot_traceability_link(self):
        """Verifica la trazabilidad del lote desde su existencia en inventario hasta el movimiento."""
        lot = self._create_lot(fields.Datetime.add(fields.Datetime.now(), days=120))
        self._add_stock(lot, quantity=15)

        quant = self.env["stock.quant"].search(
            [
                ("lot_id", "=", lot.id),
                ("location_id", "=", self.stock_location.id),
            ],
            limit=1,
        )
        self.assertTrue(quant, "El stock quant debe rastrear el lote con precisión.")
        self.assertEqual(quant.quantity, 15.0)
