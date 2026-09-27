# Test Procedure: SPEC-9.3.1 Deducción Automática de Stock en Ventas

**Spec ID:** SPEC-9.3.1  
**Target Feature:** Deducción Automática y Transaccional de Stock en Ventas en Mostrador  
**Evaluated by:** Automated Agent (Playwright MCP / Odoo Test Suite Audit)  
**Execution Date:** 2026-09-26  
**Overall Result:** ☑ APPROVED  ☐ REJECTED  ☐ BLOCKED  

---

## Pre-requisites & Environment Setup
* **Branch / Environment:** Odoo 17 Community / PostgreSQL 16 local environment (`custom_addons/caryvil_erp`)
* **Company:** Farmacia Caryvil (`caryvil_erp.company_farmacia_caryvil`)
* **Default Customer:** Consumidor Final (`partner_consumidor_final`)
* **Test Data Required:**
  * Almacén de Mostrador parametrizado con ubicación de salida de clientes.
  * Medicamento de prueba ("Paracetamol 500mg") asignado a lote con existencias controladas.

---

## Test Flows Execution

### Test Flow 1: Descuento instantáneo de stock tras completar venta (AC-1)
* **Target AC:** AC-1 (Descuento instantáneo de existencias tras confirmar y facturar venta)
* **Prerequisites:** Producto con saldo disponible de 10 unidades en ubicación de mostrador.
* **Steps:**
  1. Seleccionar el medicamento "Paracetamol 500mg" e ingresar cantidad = 4.
  2. Confirmar la orden de venta mediante `action_confirm_and_invoice()`.
  3. Verificar que el albarán de salida (`stock.picking`) pase automáticamente a estado `done`.
  4. Inspeccionar la cantidad disponible (`qty_available`) en `product.product`.
* **Expected Result:** El stock disponible se reduce de 10 a 6 unidades inmediatamente de manera atómica.
* **Result:** ☑ PASSED  ☐ FAILED  ☐ BLOCKED
* **Notes:** Verificado en suite de pruebas automatizadas `TestSaleOrderStockDeduction.test_01_sale_deducts_stock`.

### Test Flow 2: Bloqueo de venta ante intento de saldo negativo (AC-2)
* **Target AC:** AC-2 (Bloqueo estricto de saldo negativo con `UserError`)
* **Prerequisites:** Producto con saldo disponible de únicamente 3 unidades en estantería.
* **Steps:**
  1. Intentar procesar una venta por 4 unidades del producto.
  2. Ejecutar la confirmación de la venta.
* **Expected Result:** El sistema aborta la transacción con una excepción `UserError`, impide la emisión de la factura y mantiene las 3 unidades intactas en inventario.
* **Result:** ☑ PASSED  ☐ FAILED  ☐ BLOCKED
* **Notes:** Verificado en suite de pruebas automatizadas `TestSaleOrderStockDeduction.test_02_insufficient_stock_rolls_back`.

### Test Flow 3: Descuento correcto sobre el lote dispensado (AC-3)
* **Target AC:** AC-3 (Actualización de saldo en lote específico dispensado)
* **Prerequisites:** Lote `#LOT-STOCK-50` asignado con 50 unidades registradas.
* **Steps:**
  1. Crear orden de venta por 10 unidades asociadas al lote.
  2. Confirmar y facturar la venta.
  3. Consultar el quant del lote en la ubicación de stock.
* **Expected Result:** El balance del lote `#LOT-STOCK-50` disminuye exactamente a 40 unidades.
* **Result:** ☑ PASSED  ☐ FAILED  ☐ BLOCKED
* **Notes:** Verificado en suite de pruebas automatizadas `TestSaleOrderStockDeduction.test_03_sale_deducts_stock_from_lot`.

---

## Definition of Done (DoD) Verification

| Item | Description | How to verify it (without code) | Status |
| :--- | :--- | :--- | :---: |
| **DoD-1** | Descuento automático de existencias físicas en tiempo real validado | Realizar venta en mostrador y verificar que `qty_available` en el catálogo se actualice instantáneamente sin recargar página. | ☑ Met |
| **DoD-2** | Bloqueo estricto de saldo negativo probado con casos de concurrencia | Intentar vender más unidades de las disponibles; verificar diálogo de error de Odoo y rollback completo. | ☑ Met |
| **DoD-3** | Sincronización con el balance de lotes verificada | Consultar la vista de lotes (`stock.lot`) y comprobar la reducción exacta de unidades en el lote seleccionado. | ☑ Met |
| **DoD-4** | Pruebas unitarias automatizadas aprobadas al 100% | Ejecutar suite pytest/TransactionCase `test_sale_order_stock_deduction.py` con resultado 0 fallos. | ☑ Met |
| **DoD-5** | Aprobación de la política de inventario por la propietaria | Aprobación funcional de cero tolerancia a stock negativo y bloqueo en caja. | ☑ Met |

---

## Session Final Results Table

| Métrica | Valor |
| :--- | :---: |
| **Total flows executed** | 3 |
| **Flows passed** | 3 |
| **Flows failed** | 0 |
| **Flows blocked** | 0 |
| **AC coverage** | 100% (3/3) |
| **DoD items verified** | 100% (5/5) |

**Verdict:** ☑ APPROVED  ☐ REJECTED  ☐ BLOCKED  
**Defects found:** Ninguno. La implementación en `sale_order_medicine.py` satisface de forma transaccional y atómica todos los criterios expuestos en SPEC-9.3.1.
