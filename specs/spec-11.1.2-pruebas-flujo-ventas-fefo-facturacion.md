# SPEC-11.1.2: Pruebas Automatizadas de Ventas, FEFO y Facturación

## 1. Objective
Diseñar, estructurar e implementar la suite de pruebas automatizadas de integración en Python/Odoo (`tests/test_sales_fefo_invoice_flow.py`) para certificar el ciclo de ventas de mostrador de Farmacia Caryvil. Esta especificación valida mediante tests unitarios y de integración la selección algorítmica de lotes bajo la política FEFO, el descuento transaccional e inmediato de inventario, la prevención de saldos negativos, el cálculo exacto del IVA (13%) y la emisión de facturas simples para consumidor final con su numeración correlativa.

## 2. Scope
### 2.1. Included
* Creación del archivo de pruebas `custom_addons/caryvil_erp/tests/test_sales_fefo_invoice_flow.py` heredando de `odoo.tests.common.TransactionCase`.
* Implementación de los siguientes casos de prueba automatizados:
  * **Test 1 (`test_sales_to_invoice_deduction_flow`):** Creación de venta en mostrador ➔ Cobro en efectivo ➔ Validación de emisión de factura simple `posted` con correlativo `FAC-YYYY-XXXXX` ➔ Verificación del descuento inmediato en `qty_available` y en el balance del lote dispensado.
  * **Test 2 (`test_fefo_lot_selection_and_splitting`):** Configuración de Lote A (vence en 30 días, 5 unidades) y Lote B (vence en 300 días, 10 unidades) ➔ Venta de 7 unidades ➔ Verificación de que el sistema asigne automáticamente 5 unidades del Lote A y 2 unidades del Lote B.
  * **Test 3 (`test_strict_negative_stock_blocking`):** Medicamento con 2 unidades en mostrador ➔ Intento de venta por 3 unidades ➔ Captura y verificación de que se dispare `UserError` impidiendo la transacción.
  * **Test 4 (`test_simple_invoice_vat_and_words_calculation`):** Venta de $22.60 ➔ Comprobación del desglose del IVA 13% ($2.60) y de la cadena de texto en letras generada por `num2words`.
* Ejecución desatendida en el flujo de CI/CD de GitHub Actions (`SPEC-1.3.1`).

### 2.2. Not Included (Out of Scope)
* Pruebas del ciclo de compras e ingresos a bodega (cubierto en `SPEC-11.1.1`).
* Pruebas de validación de formato de DUI (cubierto en `SPEC-11.1.3`).

## 3. Context and Restrictions
* **Context:** Asegura que los procesos de mayor frecuencia en la farmacia (ventas y facturación) operen con cero fallos, protegiendo la exactitud del inventario físico y la coherencia de los comprobantes fiscales entregados a los clientes.
* **Restrictions:**
  * Todas las pruebas deben ejecutarse en aislamiento transaccional con reversión automática al finalizar.
  * El tiempo de ejecución de la suite de ventas no debe superar los 45 segundos.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-7.1.1` (Catálogo y Categorización de Medicamentos).
  * `SPEC-7.2.1` (Control de Stock, Lotes y Vencimientos).
  * `SPEC-9.1.1` (Procesamiento de Transacciones de Ventas).
  * `SPEC-9.2.1` (Generación de Factura Simple).
  * `SPEC-9.3.1` (Deducción Automática de Stock en Ventas).
  * `SPEC-9.3.2` (Estrategia de Salida FEFO por Lotes).
* **Definition of Ready (DoR):**
  * [x] Modelos de venta, deducción de stock y facturación implementados.
  * [x] Algoritmo FEFO configurado en el entorno de desarrollo.

## 5. Design (Implementation Details)
* **Test Architecture (`tests/test_sales_fefo_invoice_flow.py`):**
  ```python
  # -*- coding: utf-8 -*-
  from odoo.tests.common import TransactionCase
  from odoo.exceptions import UserError
  from datetime import datetime, timedelta

  class TestSalesFEFOInvoiceFlow(TransactionCase):

      def setUp(self):
          super(TestSalesFEFOInvoiceFlow, self).setUp()
          self.customer = self.env['res.partner'].create({
              'first_name': 'Cliente',
              'last_name': 'Prueba',
              'dui': '01234567-8',
              'is_pharmacy_customer': True
          })
          self.medicine = self.env['product.product'].create({
              'name': 'Ibuprofeno FEFO Test 400mg',
              'detailed_type': 'product',
              'tracking': 'lot',
              'list_price': 5.00,
          })

      def test_fefo_lot_selection_and_splitting(self):
          # 1. Crear dos lotes con fechas distintas
          lot_near = self.env['stock.production.lot'].create({
              'name': 'LOT-NEAR-EXP',
              'product_id': self.medicine.id,
              'expiration_date': datetime.now() + timedelta(days=30),
              'company_id': self.env.company.id,
          })
          lot_far = self.env['stock.production.lot'].create({
              'name': 'LOT-FAR-EXP',
              'product_id': self.medicine.id,
              'expiration_date': datetime.now() + timedelta(days=365),
              'company_id': self.env.company.id,
          })

          # 2. Asignar existencias iniciales (5 en lote cercano, 10 en lote lejano)
          stock_location = self.env.ref('stock.stock_location_stock')
          self.env['stock.quant']._update_available_quantity(self.medicine, stock_location, 5.0, lot_id=lot_near)
          self.env['stock.quant']._update_available_quantity(self.medicine, stock_location, 10.0, lot_id=lot_far)

          # 3. Vender 7 unidades (Debe tomar 5 de lot_near y 2 de lot_far)
          so = self.env['sale.order'].create({
              'partner_id': self.customer.id,
              'payment_method': 'efectivo',
              'amount_tendered': 50.0,
              'order_line': [(0, 0, {
                  'product_id': self.medicine.id,
                  'product_uom_qty': 7.0,
                  'price_unit': 5.00,
              })]
          })
          so.action_confirm_and_invoice()

          # 4. Validar saldos resultantes
          self.assertEqual(lot_near.product_qty, 0.0)
          self.assertEqual(lot_far.product_qty, 8.0)
          self.assertEqual(self.medicine.qty_available, 8.0)
  ```

## 6. Acceptance Criteria
* **Scenario 1: Validación del algoritmo FEFO y fraccionamiento multilote**
  * **Given** La suite de pruebas ejecutándose en entorno de testing.
  * **When** Se corre `test_fefo_lot_selection_and_splitting`.
  * **Then** El test confirma que los lotes se agotan en estricto orden cronológico de caducidad y que las cantidades finales en inventario son exactas.
* **Scenario 2: Verificación de bloqueo ante saldo negativo**
  * **When** Se ejecuta `test_strict_negative_stock_blocking`.
  * **Then** El test valida que el intento de sobreventa lance `UserError` y no descuente unidades inexistentes.
* **Scenario 3: Verificación de factura simple e importe en letras**
  * **When** Se ejecuta `test_simple_invoice_vat_and_words_calculation`.
  * **Then** El test confirma que el número de factura simple se asigne y que la conversión a letras en español sea ortográficamente correcta.

## 7. Verification Plan
* **Automated Tests:**
  * Comando: `docker compose exec web odoo -u caryvil_erp --test-enable --stop-after-init -d test_db --test-tags=caryvil_erp.TestSalesFEFOInvoiceFlow`.
* **Manual Verification:**
  * Revisar que los 4 tests finalicen en verde en los registros de GitHub Actions.

## 8. Security and Privacy
* Los datos de prueba se generan dinámicamente y se destruyen al finalizar la ejecución sin dejar huellas en la base de datos.

## 9. Risks and Mitigation
* **Risk:** Variaciones en el redondeo de decimales de IVA que provoquen fallos en los asserts de igualdad estricta (`assertEqual`).
  * **Mitigation:** Uso de `assertAlmostEqual(val1, val2, places=2)` para comparaciones de precisión monetaria.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/tests/test_sales_fefo_invoice_flow.py`.
* Registro del archivo en `custom_addons/caryvil_erp/tests/__init__.py`.

## 11. Definition of Done (DoD)
* [ ] Suite de pruebas de ventas, FEFO y facturación implementada.
* [ ] Cobertura de pruebas sobre el flujo transaccional de caja > 90%.
* [ ] Aprobación de todos los asserts en CI/CD.
* [ ] Revisión y aprobación del código por el equipo de ingeniería.
