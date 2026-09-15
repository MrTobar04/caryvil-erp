# SPEC-11.1.1: Pruebas Automatizadas de Compras e Inventario

## 1. Objective
Diseñar, implementar y automatizar la suite de pruebas de integración en Python/Odoo (`tests/test_purchase_inventory_flow.py`) para validar de extremo a extremo el ciclo de compras y reabastecimiento de medicamentos para Farmacia Caryvil. Esta especificación verifica mediante tests automatizados que la emisión de una orden de compra a un laboratorio, la recepción física de mercadería con captura de lote y fecha de vencimiento, y el incremento inmediato de existencias en el inventario operen de forma atómica y sin inconsistencias contables o de stock.

## 2. Scope
### 2.1. Included
* Creación del archivo de pruebas `custom_addons/caryvil_erp/tests/test_purchase_inventory_flow.py` heredando de `odoo.tests.common.TransactionCase`.
* Implementación de casos de prueba automatizados para los siguientes flujos:
  * **Test 1 (`test_full_purchase_to_stock_flow`):** Creación de PO ➔ Confirmación ➔ Recepción en albarán con asignación de lote y caducidad ➔ Verificación de aumento en `qty_available` del medicamento y balance del lote.
  * **Test 2 (`test_lot_expiration_capture_required`):** Intento de validar un albarán de entrada sin lote o con fecha vencida ➔ Captura y comprobación del lanzamiento de `ValidationError`.
  * **Test 3 (`test_partial_delivery_backorder_creation`):** Recepción parcial de unidades ➔ Creación de *backorder* ➔ Verificación de estado del remanente y cantidades en la PO.
  * **Test 4 (`test_uom_box_to_unit_conversion`):** Compra en presentación Caja x 100 ➔ Verificación de que el inventario aumente en 100 unidades base.
* Integración de la suite en el pipeline de CI/CD de GitHub Actions (`SPEC-1.3.1`).

### 2.2. Not Included (Out of Scope)
* Pruebas del flujo de ventas y facturación de mostrador (cubierto en `SPEC-11.1.2`).
* Pruebas de validación de sintaxis de DUI o datos locales (cubierto en `SPEC-11.1.3`).

## 3. Context and Restrictions
* **Context:** Asegura la calidad continua del software y previene regresiones en el código ante futuras modificaciones o actualizaciones del módulo `caryvil_erp`.
* **Restrictions:**
  * Las pruebas deben ejecutarse en un entorno transaccional aislado (`TransactionCase`) que revierta los datos al finalizar cada test (*rollback* automático).
  * El tiempo de ejecución de la suite de compras e inventario no debe superar los 45 segundos.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-7.1.1` (Catálogo y Categorización de Medicamentos).
  * `SPEC-7.1.2` (Gestión de Unidades de Medida Farmacéuticas).
  * `SPEC-7.2.1` (Control de Stock, Lotes y Vencimientos).
  * `SPEC-8.1.1` (Gestión de Órdenes de Compra).
  * `SPEC-8.2.1` (Recepción de Mercadería y Registro de Lotes).
  * `SPEC-8.2.2` (Actualización Automática de Stock en Compras).
* **Definition of Ready (DoR):**
  * [x] Modelos de compras, lotes y recepciones implementados en el código base.
  * [x] Entorno de testing de Odoo (`odoo --test-enable`) configurado.

## 5. Design (Implementation Details)
* **Test Architecture (`tests/test_purchase_inventory_flow.py`):**
  ```python
  # -*- coding: utf-8 -*-
  from odoo.tests.common import TransactionCase
  from odoo.exceptions import ValidationError
  from datetime import datetime, timedelta

  class TestPurchaseInventoryFlow(TransactionCase):

      def setUp(self):
          super(TestPurchaseInventoryFlow, self).setUp()
          self.vendor = self.env['res.partner'].create({
              'name': 'Laboratorios Vijosa Test',
              'is_pharmacy_vendor': True,
              'vendor_type': 'laboratorio'
          })
          self.medicine = self.env['product.product'].create({
              'name': 'Amoxicilina Test 500mg',
              'detailed_type': 'product',
              'tracking': 'lot',
              'standard_price': 4.00,
              'list_price': 6.00,
          })

      def test_full_purchase_to_stock_flow(self):
          # 1. Crear Orden de Compra por 10 unidades
          po = self.env['purchase.order'].create({
              'partner_id': self.vendor.id,
              'order_line': [(0, 0, {
                  'product_id': self.medicine.id,
                  'name': self.medicine.name,
                  'product_qty': 10.0,
                  'price_unit': 4.00,
                  'date_planned': datetime.now(),
              })]
          })
          po.button_confirm()
          self.assertEqual(po.state, 'purchase')

          # 2. Procesar Albarán de Recepción
          picking = po.picking_ids[0]
          picking.action_assign()
          
          exp_date = datetime.now() + timedelta(days=365)
          for move in picking.move_lines:
              move.move_line_ids.unlink() # Limpiar para asignar lote
              self.env['stock.move.line'].create({
                  'move_id': move.id,
                  'picking_id': picking.id,
                  'product_id': self.medicine.id,
                  'product_uom_id': self.medicine.uom_id.id,
                  'location_id': picking.location_id.id,
                  'location_dest_id': picking.location_dest_id.id,
                  'qty_done': 10.0,
                  'lot_name': 'LOT-TEST-2027',
                  'expiration_date': exp_date,
              })

          picking.button_validate()
          self.assertEqual(picking.state, 'done')

          # 3. Validar Incremento de Existencias
          self.medicine.refresh()
          self.assertEqual(self.medicine.qty_available, 10.0)

          # 4. Validar Registro de Lote
          lot = self.env['stock.production.lot'].search([('name', '=', 'LOT-TEST-2027')], limit=1)
          self.assertTrue(lot.exists())
          self.assertEqual(lot.product_qty, 10.0)
          self.assertFalse(lot.is_expired)
  ```

## 6. Acceptance Criteria
* **Scenario 1: Ejecución exitosa del test del ciclo completo**
  * **Given** La suite de tests ejecutada en consola mediante `odoo --test-enable -u caryvil_erp`.
  * **When** Se corre `test_full_purchase_to_stock_flow`.
  * **Then** El test debe finalizar con estado `OK` (código de salida 0) confirmando que la orden de compra, el albarán, el lote y el stock se procesaron correctamente.
* **Scenario 2: Verificación de bloqueo ante lote inválido**
  * **When** Se ejecuta `test_lot_expiration_capture_required`.
  * **Then** El test confirma que el sistema lanza `ValidationError` al omitir el lote y no permite ingresar stock huérfano.
* **Scenario 3: Integración en GitHub Actions**
  * **Given** Un Pull Request con cambios en el módulo de compras o inventario.
  * **When** Se ejecuta el pipeline de CI.
  * **Then** La suite de pruebas de compras e inventario debe ejecutarse automáticamente y reportar estado verde antes de permitir el merge.

## 7. Verification Plan
* **Automated Tests:**
  * Ejecución en contenedor local: `docker compose exec web odoo -u caryvil_erp --test-enable --stop-after-init -d test_db --test-tags=caryvil_erp`.
* **Manual Verification:**
  * Revisar los logs de salida comprobando que todos los asserts pasen sin advertencias (*warnings* de deprecación).

## 8. Security and Privacy
* Las pruebas utilizan datos sintéticos efímeros y no interactúan con bases de datos de producción ni exponen credenciales.

## 9. Risks and Mitigation
* **Risk:** Pruebas frágiles que fallen por diferencias en la zona horaria del servidor.
  * **Mitigation:** Uso de `fields.Datetime.now()` y comparaciones relativas con `timedelta`.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/tests/__init__.py`.
* Archivo `custom_addons/caryvil_erp/tests/test_purchase_inventory_flow.py`.

## 11. Definition of Done (DoD)
* [ ] Suite de pruebas de compras e inventario implementada en Python.
* [ ] Cobertura de pruebas de las funciones críticas de abastecimiento > 85%.
* [ ] Ejecución exitosa en el entorno local y en el pipeline de GitHub Actions.
* [ ] Revisión de código y asserts aprobada por el líder de QA.
