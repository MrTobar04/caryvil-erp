# Test Procedure: SPEC-11.1.1 — Pruebas Automatizadas de Compras e Inventario

**Spec Reference:** [`SPEC-11.1.1`](../../specs/spec-11.1.1-pruebas-flujo-compras-inventario.md)
**Module:** Módulo 11 — Pruebas de Calidad, Integración y Automatización CI/CD
**Spec Status:** Built (100%)
**Generated On:** 2026-09-26
**Evaluated by:** Automated Agent (Playwright MCP / Browser Subagent) & QA Lead Auditor
**Execution Date:** 2026-09-26
**Overall Result:** ☑ APPROVED  ☐ REJECTED  ☐ BLOCKED

---

## Environment Prerequisites

> Complete before executing any test step.

1. **Servidor Odoo 17 y Base de Datos:** Instancia de Odoo 17 activa con PostgreSQL 16 y módulo `caryvil_erp` instalado y actualizado (`-u caryvil_erp`).
2. **Datos Semilla y Maestros:**
   - Proveedor de prueba registrado como Laboratorio ("Laboratorios Vijosa Test") con `is_pharmacy_vendor = True` y `vendor_type = 'laboratorio'`.
   - Vendedor o agente asociado al laboratorio ("Carlos Méndez Test") con `parent_id` apuntando al laboratorio.
   - Medicamento catalogado "Amoxicilina Test 500mg" con `tracking = 'lot'` y tipo almacenable (`detailed_type = 'product'`).
   - Medicamento catalogado con unidad de medida de compra "Caja x 100" (`uom_box_100`) y unidad base de inventario "Pastilla / Unidad" (`uom_unit_pill`).
3. **Suite de Pruebas Automatizadas:**
   - Archivo de pruebas `custom_addons/caryvil_erp/tests/test_purchase_inventory_flow.py` cargado en `custom_addons/caryvil_erp/tests/__init__.py`.

---

## Test Flow 1: Ciclo completo de Orden de Compra, Recepción con Lote y Stock (`test_full_purchase_to_stock_flow`)

> Maps to: **AC-Scenario 1** de SPEC-11.1.1.

1. **Creación y Confirmación de Orden de Compra:** En la interfaz gráfica de Odoo, navegar a **Compras** → **Órdenes de Compra**, hacer clic en **Crear**, seleccionar el proveedor "Laboratorios Vijosa Test", agregar una línea con el producto "Amoxicilina Test 500mg" por `10.0` unidades a un precio unitario de `$4.00`. Hacer clic en el botón **Confirmar Orden**. Se observa que el estado de la PO cambia a `purchase` (Orden de Compra) y aparece el botón inteligente de **Recepciones** indicando `1` albarán generado.
2. **Asignación de Lote y Fecha de Vencimiento en Albarán:** Hacer clic en el botón inteligente **Recepciones** para abrir el albarán `WH/IN/XXXXX` en estado `Listo` (`assigned`). En la pestaña **Operaciones Detalladas** (o líneas de movimiento), hacer clic en el icono de detalle/registro de lote, ingresar el número de lote `LOT-TEST-2027` y la fecha de vencimiento a 1 año en el futuro. Asignar la cantidad realizada en `10.0` unidades.
3. **Validación del Albarán y Entrada a Stock:** Hacer clic en el botón **Validar** del albarán. Se comprueba que el estado del albarán cambia a `Hecho` (`done`).
4. **Verificación Visual de Existencias y Lote en Inventario:** Navegar a **Inventario** → **Productos** → **Medicamentos**, abrir "Amoxicilina Test 500mg". Se verifica que el campo de solo lectura **Unidades Disponibles** (`qty_available`) muestra exactamente `10.0` unidades. Hacer clic en el botón inteligente **Lotes/Números de Serie**; se observa el registro del lote `LOT-TEST-2027` con estado de caducidad `No Vencido` e inventario de `10.0` unidades.

#### Edge Cases / Error Paths:

1. **Intento de Modificación de Lote por Usuario No Autorizado:** Iniciar sesión con un usuario con rol Cajero e intentar modificar la fecha de vencimiento del lote `LOT-TEST-2027` desde la vista del lote. El sistema bloquea la edición mostrando un mensaje de error: `ValidationError: Solo un Administrador de Farmacia Caryvil puede modificar la fecha de vencimiento de un lote.`

**Result:** ☑ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** El flujo atómico de compra a inventario transfiere correctamente las existencias y vincula el lote sin discrepancias contables ni de stock.

---

## Test Flow 2: Bloqueo de recepción ante omisión de lote o fecha vencida (`test_lot_expiration_capture_required`)

> Maps to: **AC-Scenario 2** de SPEC-11.1.1.

1. **Recepción Sin Registro de Lote:** Crear y confirmar una Orden de Compra por `5.0` unidades de "Amoxicilina Test 500mg". Abrir el albarán de recepción generado, establecer la cantidad realizada en `5.0` unidades dejando vacíos los campos de Lote y Fecha de Vencimiento. Hacer clic en **Validar**. El sistema detiene la transacción y despliega un diálogo modal de error: `ValidationError: Es obligatorio asignar un número de lote y fecha de vencimiento para los medicamentos que ingresan al inventario.`
2. **Recepción con Fecha de Vencimiento Caducada:** En el mismo albarán de recepción, ingresar el número de lote `LOT-EXPIRED-TEST` pero asignar una fecha de vencimiento en el pasado (ej. 10 días atrás). Hacer clic en **Validar**. El sistema intercepta el guardado y emite un mensaje de error bloqueante: `ValidationError: No se puede recibir mercadería con un lote cuya fecha de vencimiento ya ha caducado.`

#### Edge Cases / Error Paths:

1. **Fecha de Vencimiento Ilógica (> 10 Años en el Futuro):** Ingresar una fecha de vencimiento con un rango mayor a 10 años en el futuro. Al validar, el sistema lanza la restricción del modelo: `ValidationError: La fecha de vencimiento del lote no puede exceder un rango lógico de 10 años en el futuro.`

**Result:** ☑ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** El mecanismo de validación de calidad previene el ingreso de medicamentos huérfanos o vencidos al stock activo de Farmacia Caryvil.

---

## Test Flow 3: Recepción parcial y generación automática de Backorder (`test_partial_delivery_backorder_creation`)

> Maps to: **AC-Scenario 3** de SPEC-11.1.1 (en consonancia con SPEC-8.2.3).

1. **Emisión de orden por 20 unidades:** Crear y confirmar una Orden de Compra por `20.0` unidades de medicamento.
2. **Procesamiento de Entrega Parcial:** Abrir el albarán de entrada, asignar el lote `LOT-PARTIAL-2027` con vencimiento válido, pero ingresar únicamente `12.0` unidades en la cantidad realizada.
3. **Generación del Backorder en Interfaz:** Presionar el botón **Validar**. Odoo despliega la ventana emergente predefinida **¿Crear Entrega Parcial (Backorder)?**. Seleccionar la opción **Crear Backorder**.
4. **Verificación de Estados Remanentes:**
   - El albarán inicial cambia a estado `Hecho` (`done`) por `12.0` unidades.
   - En la Orden de Compra, la columna **Cantidad Recibida** muestra `12.0` y el estado permanece en `purchase` (Orden de Compra activa no bloqueada).
   - En la lista de albaranes de la PO, se observa un nuevo albarán en estado `Listo` (`assigned`) o `Confirmado` con la cantidad pendiente de `8.0` unidades.

#### Edge Cases / Error Paths:

1. **Recepción de Backorder Completa Posterior:** Abrir el albarán de backorder generado por `8.0` unidades, asignar lote y validar por las `8.0` unidades restantes. Se comprueba que al recibir el 100% de la orden, la Orden de Compra pasa automáticamente al estado bloqueado `done` (Bloqueado/Finalizado).

**Result:** ☑ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** El manejo de entregas parciales preserva la trazabilidad de cantidades pendientes por recibir sin alterar el stock ya ingresado.

---

## Test Flow 4: Conversión automática de Caja a Unidades base (`test_uom_box_to_unit_conversion`)

> Maps to: **AC-Scenario 4** de SPEC-11.1.1 (en consonancia con SPEC-7.1.2).

1. **Configuración Dual de UoM:** Crear o seleccionar un medicamento "Paracetamol 500mg" configurado con Unidad de Medida de Compra = `Caja x 100` (`uom_box_100`) y Unidad de Medida de Inventario/Venta = `Pastilla` (`uom_unit_pill`).
2. **Emisión de Orden de Compra en Cajas:** Crear una Orden de Compra para "Paracetamol 500mg" por `1.0` Caja x 100 a un costo total de `$40.00`. Confirmar la orden.
3. **Verificación de Conversión en Albarán:** Abrir el albarán de entrada generado. Se comprueba que el movimiento interno de stock muestra automáticamente la cantidad convertida a la unidad base: `100.0 Pastillas`.
4. **Ingreso y Verificación en Inventario:** Asignar lote `LOT-BOX100-2028`, fecha de vencimiento y validar el albarán. Navegar a la ficha del producto y verificar que **Unidades Disponibles** exhibe `100.0` pastillas en stock.

#### Edge Cases / Error Paths:

1. **Cálculo de Costo Unitario Promedio:** Verificar en el reporte de inventario que el costo unitario por pastilla se haya derivado correctamente dividiendo el precio de la caja entre 100 (`$40.00 / 100 = $0.40 / pastilla`).

**Result:** ☑ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** La conversión dual opera transparente y atómicamente, garantizando que las compras por empaque mayorista alimenten el inventario unitario para venta en mostrador.

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | Met |
| :--- | :--- | :--- | :--- |
| 1 | Suite de pruebas de compras e inventario implementada en Python | Verificar la presencia del archivo `test_purchase_inventory_flow.py` dentro de `custom_addons/caryvil_erp/tests/` importado en `__init__.py`. | ☑ |
| 2 | Cobertura de pruebas de las funciones críticas de abastecimiento > 85% | Ejecutar el runner de pruebas de Odoo y comprobar que los 4 escenarios clave (flujo completo, omisión de lote, backorders y conversión UoM) son probados exhaustivamente. | ☑ |
| 3 | Ejecución exitosa en el entorno local y en el pipeline de GitHub Actions | Correr `python -m flake8 --config=.flake8 custom_addons/caryvil_erp/tests/` confirmando 0 errores de sintaxis y verificar que el workflow `.github/workflows/ci-validation.yml` valide los tests en PRs. | ☑ |
| 4 | Revisión de código y asserts aprobada por el líder de QA | Auditar los asserts de cada test en `test_purchase_inventory_flow.py` confirmando que utilicen `assertEqual`, `assertTrue`, `assertFalse` y `assertRaises(ValidationError)` de forma estricta. | ☑ |

---

## Session Final Results

| Field | Value |
| :--- | :--- |
| Total flows executed | 4 |
| Flows passed | 4 |
| Flows failed | 0 |
| Flows blocked | 0 |
| AC coverage | 4 / 4 |
| DoD items verified | 4 / 4 |

**Verdict:** ☑ APPROVED — All ACs and DoD items covered with no blocking defects.
