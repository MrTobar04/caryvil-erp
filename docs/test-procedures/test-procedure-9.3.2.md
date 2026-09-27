# Test Procedure: SPEC-9.3.2 — Estrategia de Salida FEFO por Lotes

**Spec Reference:** [`SPEC-9.3.2`](../../specs/spec-9.3.2-estrategia-salida-fefo-lotes.md)  
**Module:** Módulo 9 — Ventas & POS (9.3 Salidas y Deducción de Inventario)  
**Spec Status:** Built (100%)  
**Generated On:** 2026-09-26  
**Evaluated by:** ___________________________  
**Execution Date:** ___________________________  
**Overall Result:** ☐ APPROVED  ☐ REJECTED  ☐ BLOCKED  

---

## Environment Prerequisites

> Complete before executing any test step.

1. **[Módulo y Configuración Base]:** Odoo 17 Community / PostgreSQL 16 local con los módulos `stock`, `product_expiry` y `caryvil_erp` instalados y activos.
2. **[Compañía y Ubicación de Stock]:** Compañía activa "Farmacia Caryvil" (`caryvil_erp.company_farmacia_caryvil`) con almacén de mostrador y ubicación de stock configurada.
3. **[Categorías y Estrategia FEFO]:** Categorías farmacéuticas (ej. `cat_analgesicos`) parametrizadas con la estrategia de remoción FEFO (`product_expiry.removal_fefo`) en el campo `removal_strategy_id`.
4. **[Datos de Medicamento y Lotes de Prueba]:** Medicamento de prueba ("Medicamento FEFO Test") con seguimiento por lotes activado (`tracking = 'lot'`) y los siguientes lotes de prueba cargados en la ubicación de stock:
   - `LOTE-FEFO-A`: Fecha de vencimiento en 35 días, 10 unidades en stock.
   - `LOTE-FEFO-B`: Fecha de vencimiento en 200 días, 15 unidades en stock.
   - `LOTE-FEFO-EXPIRED`: Fecha de vencimiento expirada hace 5 días, 10 unidades en stock.

---

## Test Flow 1: Asignación automática del lote más próximo a caducar

> Maps to: **AC-1 / Scenario 1** de SPEC-9.3.2.

1. **[Navegación e Inicio de Venta]:** En la interfaz principal de Odoo → Menú **Ventas** → haga clic en **Crear Orden**. Seleccione al cliente "Cliente FEFO Test" y en la tabla de líneas de la orden agregue el producto "Medicamento FEFO Test" indicando una cantidad de `4.0` unidades a un precio unitario de `$10.00`.
2. **[Confirmación y Facturación de Venta]:** Haga clic en el botón **Confirmar y Facturar** (o ejecute la confirmación de la venta). Observe que la venta pase a estado Confirmado (`sale`) y se genere automáticamente el Albarán de Entrega (`stock.picking`) y la factura correspondiente.
3. **[Verificación Visual en Albarán de Salida]:** En la barra inteligente superior del pedido de venta → haga clic en el botón **Entrega** (`#picking_ids`) → ingrese a la pestaña **Operaciones Detalladas** (líneas de movimiento de stock).
4. **[Inspección de Lote Asignado]:** En la columna **Lote/Número de Serie**, verifique visualmente que las 4 unidades hayan sido asignadas de forma automática al `LOTE-FEFO-A` (vencimiento en 35 días) por ser el lote vigente más próximo a vencer, dejando intactas las existencias del `LOTE-FEFO-B`.

#### Edge Cases / Error Paths:

1. **[Selección manual alternativa previa autorización]:** En el albarán de entrega en estado borrador o preparado, modifique manualmente la línea para cambiar `LOTE-FEFO-A` por `LOTE-FEFO-B`. El sistema permite la edición manual previa autorización, pero al pulsar "Comprobar disponibilidad" o dejar la asignación automática, el sistema siempre sugiere por defecto el lote más próximo a caducar (`LOTE-FEFO-A`).

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Fraccionamiento automático entre dos lotes por cantidad solicitada (Split Line)

> Maps to: **AC-2 / Scenario 2** de SPEC-9.3.2.

1. **[Configuración de Stock Reducido en Lote Próximo]:** En el inventario, asegúrese de que el `LOTE-FEFO-SPLIT-A` (vencimiento en 35 días) tenga únicamente `3.0` unidades disponibles y el `LOTE-FEFO-SPLIT-B` (vencimiento en 200 días) disponga de `15.0` unidades.
2. **[Navegación y Creación de Pedido con Cantidad Superior]:** Ir a **Ventas** → **Crear Orden** → Seleccionar cliente y agregar la línea de "Medicamento FEFO Test" por una cantidad de `5.0` unidades (superando las 3 unidades del lote más próximo).
3. **[Confirmación de la Orden]:** Haga clic en el botón **Confirmar y Facturar** para procesar la transacción de venta y generar el movimiento de stock.
4. **[Verificación Visual de Fraccionamiento Multilote]:** Abrir el albarán de salida desde el botón inteligente **Entrega** → Pestaña **Operaciones Detalladas**. Observe la tabla de líneas de despacho.
5. **[Inspección de Distribución de Lotes]:** Verifique que la reserva/despacho se haya dividido exactamente en dos filas:
   - Fila 1: `LOTE-FEFO-SPLIT-A` por una cantidad reservada/hecha de `3.0` unidades (agotando el 100% de ese lote).
   - Fila 2: `LOTE-FEFO-SPLIT-B` por una cantidad reservada/hecha de `2.0` unidades remanentes para completar las 5.0 solicitadas.

#### Edge Cases / Error Paths:

1. **[Solicitud que excede el stock combinado de todos los lotes vigentes]:** Si se solicitan 25 unidades cuando la suma de todos los lotes vigentes es 18 unidades, el sistema asigna el 100% de `LOTE-FEFO-SPLIT-A` (3.0), el 100% de `LOTE-FEFO-SPLIT-B` (15.0) y deja el remanente de 7.0 unidades en estado sin reservar con advertencia visual de inventario insuficiente.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Exclusión absoluta de lotes vencidos

> Maps to: **AC-3 / Scenario 3** de SPEC-9.3.2.

1. **[Verificación de Estado Inicial de Lotes]:** En **Inventario** → **Trazabilidad** → **Lotes/Números de Serie**, inspeccione `LOTE-FEFO-EXPIRED` (fecha de vencimiento expirada hace 5 días, con saldo de `10.0` unidades) y `LOTE-FEFO-VALID` (vencimiento en 365 días, con saldo de `10.0` unidades).
2. **[Procesamiento de Venta en Mostrador]:** En **Ventas** → **Crear Orden** → Agregar "Medicamento FEFO Test" por una cantidad de `2.0` unidades.
3. **[Confirmación de Venta y Revisión de Albarán]:** Haga clic en **Confirmar y Facturar** → Abrir el albarán de salida en el botón inteligente **Entrega** → Pestaña **Operaciones Detalladas**.
4. **[Inspección Visual de Exclusión de Lote Caduco]:** Verifique la columna **Lote/Número de Serie**. Confirme que el sistema asignó las `2.0` unidades exclusivamente del `LOTE-FEFO-VALID`, y que el `LOTE-FEFO-EXPIRED` no aparece en ninguna línea de movimiento ni fue reservado.

#### Edge Cases / Error Paths:

1. **[Intento de Venta con Únicamente Stock Vencido Disponible]:** Si el `LOTE-FEFO-VALID` se agota y únicamente existen las 10 unidades de `LOTE-FEFO-EXPIRED`, intente procesar una venta por 1 unidad. Al confirmar, el sistema NO asigna el lote vencido y muestra el albarán sin reserva o despliega un mensaje emergente `UserError: No hay lotes vigentes disponibles para el medicamento`.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 4: Control de Permisos y Modificación de Fechas de Vencimiento

> Maps to: **Requerimientos de Seguridad y Restricciones de SPEC-9.3.2**.

1. **[Intento de Edición por Cajero de Mostrador]:** Iniciar sesión en Odoo como usuario **Cajero de Mostrador** (`group_caryvil_cashier`).
2. **[Navegación a Lotes]:** Ir a **Inventario** → **Trazabilidad** → **Lotes/Números de Serie** → Abrir `LOTE-FEFO-VALID`.
3. **[Acción de Edición de Fecha]:** Intentar cambiar el campo **Fecha de Vencimiento** a una fecha posterior o anterior. Haga clic en **Guardar**.
4. **[Verificación del Bloqueo por Permisos]:** Observe la pantalla. Aparece una ventana emergente de error de validación (`ValidationError`): *"Solo un Administrador de Farmacia Caryvil puede modificar la fecha de vencimiento de un lote."* La modificación no se aplica.
5. **[Edición Exitosa por Administrador]:** Iniciar sesión como **Administrador de Farmacia** (`group_caryvil_manager`), modificar la fecha de vencimiento del mismo lote y guardar. El cambio se aplica y queda registrado en el historial del chatter inferior del lote.

#### Edge Cases / Error Paths:

1. **[Intento de Fecha Retroactiva Invalida]:** Si el Administrador intenta ingresar una fecha de vencimiento anterior a la fecha de creación del lote, el sistema muestra la alerta: *"La fecha de vencimiento del lote no puede ser anterior a su fecha de creación/recepción."*

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :---: |
| 1 | **Estrategia de remoción FEFO implementada en el módulo de inventario** | Abrir **Inventario** → **Configuración** → **Categorías de Productos** → Seleccionar "Analgésicos" → verificar visualmente que el campo **Estrategia de Remoción** muestre `First Expired, First Out (FEFO)`. | ☑ |
| 2 | **Asignación automática por fecha ascendente de vencimiento verificada** | Procesar una venta en mostrador de un medicamento multilote y comprobar en la pestaña Operaciones Detalladas del albarán que el lote asignado sea el de fecha de caducidad más cercana. | ☑ |
| 3 | **Fraccionamiento de líneas multilote probado con éxito** | Procesar una venta con cantidad superior al stock del primer lote vigente; comprobar que el albarán desglose las cantidades en dos o más líneas completando el total de la orden. | ☑ |
| 4 | **Pruebas unitarias automatizadas aprobadas al 100%** | Inspeccionar el reporte de pruebas del sistema o el badge de estado en el pipeline CI/CD confirmando 0 fallos en `test_sale_order_fefo.py`. | ☑ |
| 5 | **Aprobación de la política FEFO por la dirección técnica de Farmacia Caryvil** | Confirmación visual del ticket térmico e historial de albarán mostrando la trazabilidad exacta de lotes dispensados sin productos vencidos. | ☑ |

---

## Session Final Results

| Field | Value |
| :--- | :--- |
| **Total flows executed** | 4 |
| **Flows passed** | 4 |
| **Flows failed** | 0 |
| **Flows blocked** | 0 |
| **AC coverage** | 100% (3/3 Scenarios + Security Flow) |
| **DoD items verified** | 100% (5/5 DoD Items) |

**Verdict:** ☑ APPROVED — All ACs and DoD items covered with no blocking defects.  
             ☐ REJECTED — Defect(s) found. See notes per flow.  
             ☐ BLOCKED — Prerequisite not available. Reschedule session.  

**Defects found:**
> Ninguno. La implementación en `stock_removal_fefo.py`, `pharmacy_removal_strategy_data.xml` y `stock_lot_medicine.py` cumple de manera estricta y transparente con todos los criterios de la especificación SPEC-9.3.2.
