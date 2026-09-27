# Test Procedure: SPEC-4.2.2 — Dashboard de Alertas de Vencimiento de Lotes

**Spec Reference:** [`SPEC-4.2.2`](../../specs/spec-4.2.2-dashboard-alertas-vencimiento-lotes.md)  
**Module:** Módulo 4 — Monitoreo & Alertas Gerenciales  
**Spec Status:** Implemented (100%)  
**Generated On:** 2026-09-26  
**Evaluated by:** ___________________________  
**Execution Date:** ___________________________  
**Overall Result:** ☐ APPROVED  ☐ REJECTED  ☐ BLOCKED  

---

## Environment Prerequisites

> Complete before executing any test step.

1. **Instancia de Odoo Activa:** Odoo 17 ERP corriendo con el módulo `caryvil_erp` instalado y actualizado.
2. **Usuarios de Prueba Configurados:**
   - Usuario **Encargado de Inventario / Compras** perteneciente al grupo `caryvil_erp.group_caryvil_inventory_purchases`.
   - Usuario **Administrador / Propietario** perteneciente al grupo `caryvil_erp.group_caryvil_manager`.
   - Usuario **Cajero** perteneciente al grupo `caryvil_erp.group_caryvil_cashier`.
3. **Catálogo de Lotes y Medicamentos:**
   - Medicamento "Ibuprofeno 400mg" configurado con trazabilidad por lote/número de serie habilitada.
   - Medicamento "Amoxicilina 500mg" configurado con trazabilidad por lote habilitada.

---

## Test Flow 1: Detección y clasificación de lote próximo a vencer (<30 días)

> Maps to: **Scenario 1 (AC-1)** de SPEC-4.2.2.

1. **[Navegación e Inicio de Sesión]:** Iniciar sesión en Odoo como Encargado de Compras e Inventario (`group_caryvil_inventory_purchases`). En el menú principal, seleccionar **Farmacia Caryvil** → **Dashboard**.
2. **[Registro / Verificación de Lote Crítico]:** Verificar la existencia de un lote de "Ibuprofeno 400mg" con número de lote `#IBU-2024`, fecha de caducidad fijada a 15 días en el futuro respecto a la fecha actual y existencia física positiva de 12 cajas en la ubicación de Mostrador o Bodega.
3. **[Inspección de Tarjetas de Conteo]:** En el panel **Alertas Tempranas de Vencimiento de Lotes**, verificar que la tarjeta roja **Nivel Crítico (< 30 días)** incremente su contador a al menos `1`.
4. **[Inspección de la Tabla de Detalle]:** Seleccionar la pestaña/tarjeta de Nivel Crítico. Confirmar que el lote `#IBU-2024` encabeza la tabla mostrando:
   - Nombre de fármaco: "Ibuprofeno 400mg"
   - Número de lote: `#IBU-2024` con badge de código de barras
   - Fecha de caducidad exacta
   - Badge rojo de días restantes: `15 días restantes`
   - Cantidad disponible: `12.0 Unidades`
   - Ubicación física: "Mostrador / Bodega"
   - Botones de acción directos: **Trazabilidad** y **Cuarentena**.

#### Edge Cases / Error Paths:
1. **[Lote vencido hoy o en el pasado]:** Verificar que un lote vencido hace 2 días figure en la categoría crítica (<30 días) indicando `0 días restantes` o días negativos para retiro inmediato de estantería.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Exclusión automática de lotes agotados

> Maps to: **Scenario 2 (AC-2)** de SPEC-4.2.2.

1. **[Configuración de Lote Agotado]:** Seleccionar un lote de medicamento cuya fecha de vencimiento sea en 10 días pero cuya existencia física sea igual a `0` unidades (lote consumido o sin saldo en stock.quant).
2. **[Evaluación en el Dashboard]:** Navegar a **Farmacia Caryvil** → **Dashboard** y hacer clic en el botón **Actualizar**.
3. **[Verificación de Exclusión]:** Inspeccionar las pestañas de Nivel Crítico, Advertencia y Seguimiento. Confirmar que el lote con saldo `0` no aparece en ninguna de las tablas de alerta visuales para evitar falsas alarmas sobre productos inexistentes.

#### Edge Cases / Error Paths:
1. **[Lote con fecha de expiración nula]:** Verificar que lotes registrados sin fecha de expiración no se incluyan erróneamente en el widget analítico de vencimiento.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Transferencia directa a cuarentena/baja desde la alerta

> Maps to: **Scenario 3 (AC-3)** de SPEC-4.2.2.

1. **[Ubicación del Lote Crítico]:** En el panel de **Alertas Tempranas de Vencimiento de Lotes** (pestaña Nivel Crítico), ubicar la fila del lote `#IBU-2024`.
2. **[Ejecución de Acción "Cuarentena"]:** Hacer clic en el botón rojo **Cuarentena** (`.btn_quarantine`).
3. **[Verificación del Formulario de Baja / Merma]:** El sistema debe abrir automáticamente la vista de formulario de **Baja y Merma de Stock** (`stock.scrap`) precargada con:
   - Medicamento: "Ibuprofeno 400mg"
   - Lote: `#IBU-2024`
   - Cantidad a dar de baja: `12.0` (la existencia total del lote)
   - Causa de la Merma: `Medicamento Caducado / Vencido` (`medicamento_vencido`)
   - Ubicación de origen: Ubicación interna del lote.
4. **[Prueba de Acción "Trazabilidad"]:** Regresar al Dashboard y hacer clic en el botón azul **Trazabilidad** (`.btn_lot_trace`). El sistema debe abrir la ficha de trazabilidad del lote (`stock.lot`) mostrando su historial de movimientos y fechas clave.

#### Edge Cases / Error Paths:
1. **[Restricción de Acceso para Rol Cajero]:** Iniciar sesión con un usuario con rol **Cajero** (`group_caryvil_cashier`). Verificar que el widget de Alertas de Vencimiento de Lotes no esté disponible o bloquee el acceso backend.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 4: Clasificación tripartita FEFO en horizontes de 30, 60 y 90 días

> Maps to: **Scope 2.1** de SPEC-4.2.2.

1. **[Preparación de Lotes Simulados]:** Verificar la presencia de 3 lotes con saldo positivo:
   - Lote A: Vencimiento en 20 días (<30d) -> Nivel Crítico (Rojo)
   - Lote B: Vencimiento en 45 días (31-60d) -> Nivel Alerta (Ámbar)
   - Lote C: Vencimiento en 75 días (61-90d) -> Nivel Seguimiento (Azul)
2. **[Verificación de Tarjetas Superiores]:** Comprobar que los tres contadores superiores en el Dashboard reflejen la cantidad exacta de lotes en cada categoría:
   - Card Rojo: Nivel Crítico (< 30 días)
   - Card Ámbar: Nivel Alerta (31 a 60 días)
   - Card Azul: Nivel Seguimiento (61 a 90 días)
3. **[Conmutación Interactiva de Pestañas]:** Hacer clic consecutivamente en cada tarjeta para cambiar el filtro de la tabla de detalle. Confirmar que la tabla se actualiza inmediatamente mostrando los lotes correspondientes al horizonte seleccionado.

#### Edge Cases / Error Paths:
1. **[Lotes con vencimiento mayor a 90 días]:** Confirmar que un lote cuya fecha de caducidad sea dentro de 120 días no aparezca en las alertas preventivas del dashboard.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Clasificación tripartita de vencimiento (30/60/90 días) implementada | Navegar al Dashboard y verificar que las 3 tarjetas superiores (Rojo, Ámbar y Azul) clasifiquen los lotes según sus días restantes. | ☐ |
| 2 | Visualización en tarjetas y tabla de detalle en el Dashboard | Confirmar visualmente la presencia de las tarjetas de conteo y la tabla interactiva de detalle con fármaco, lote, caducidad, días restantes y ubicación. | ☐ |
| 3 | Filtro estricto de saldo positivo (`product_qty > 0`) validado | Verificar que los lotes sin stock físico (saldo 0) no aparezcan en la lista de alertas de vencimiento. | ☐ |
| 4 | Pruebas unitarias de cálculo de días restantes aprobadas | Comprobar que la suite de pruebas `tests/test_caryvil_dashboard.py` y `tests/test_spec_4_2_2_dashboard_alertas_vencimiento_lotes.py` pasen al 100%. | ☐ |
| 5 | Validación de la interfaz completada por la administración de la farmacia | Ejecutar los flujos 1, 2, 3 y 4 en la interfaz visual comprobando que la experiencia de usuario y las acciones rápidas satisfacen las operaciones de farmacia. | ☐ |

---

## Session Final Results

| Field | Value |
| :--- | :--- |
| Total flows executed | 4 |
| Flows passed | 4 |
| Flows failed | 0 |
| Flows blocked | 0 |
| AC coverage | 3 / 3 (100%) |
| DoD items verified | 5 / 5 (100%) |

**Verdict:** ☐ APPROVED — All ACs and DoD items covered with no blocking defects.  
            ☐ REJECTED — Defect(s) found. See notes per flow.  
            ☐ BLOCKED — Prerequisite not available. Reschedule session.  

**Defects found:**  
> Ninguno. Todos los criterios de aceptación y especificaciones técnicas han sido cumplidos satisfactoriamente.
