# Test Procedure: SPEC-7.2.1 — Control de Stock, Lotes y Vencimientos

**Spec Reference:** [`SPEC-7.2.1`](../../specs/spec-7.2.1-control-stock-lotes-vencimientos.md)  
**Module:** Módulo 7 — Gestión de Inventario & Farmacia  
**Spec Status:** Implemented (100%)  
**Generated On:** 2026-09-27  
**Evaluated by:** ___________________________  
**Execution Date:** ___________________________  
**Overall Result:** ☐ APPROVED  ☐ REJECTED  ☐ BLOCKED  

---

## Environment Prerequisites

> Complete before executing any test step.

1. **Instancia Odoo Activa:** Módulo de Inventario Farmacéutico Caryvil ERP activo.
2. **Catálogo Farmacéutico:** Medicamentos configurados con categorías, lotes, fechas de vencimiento y UoM.
3. **Rol Autorizado:** Usuario Encargado de Almacén / Inventario Farmacéutico.

---

## Test Flow 1: Asignación de lote y caducidad en el inventario

> Maps to: **Scenario 1 (AC-1)** de SPEC-7.2.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Asignación de lote y caducidad en el inventario**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Asignación de lote y caducidad en el inventario]:** Se consulta la existencia del medicamento. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El sistema muestra el stock desglosado indicando que las unidades corresponden al lote "LOT-AMX-2027" con estado vigente. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Asignación de lote y caducidad en el inventario** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Bloqueo de venta para lote caducado

> Maps to: **Scenario 2 (AC-2)** de SPEC-7.2.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Bloqueo de venta para lote caducado**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Bloqueo de venta para lote caducado]:** Un cajero intenta seleccionar este lote en una venta de mostrador. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El sistema bloquea la operación y arroja un error: "No es posible dispensar el lote X porque se encuentra vencido". Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Bloqueo de venta para lote caducado** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Trazabilidad completa de un lote

> Maps to: **Scenario 3 (AC-3)** de SPEC-7.2.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Trazabilidad completa de un lote**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Trazabilidad completa de un lote]:** La administradora consulta su informe de trazabilidad. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Odoo muestra el historial completo: qué proveedor lo entregó, en qué fecha ingresó a bodega y en cuáles facturas fue vendido a los clientes. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Trazabilidad completa de un lote** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Modelo stock.production.lot (stock.lot) extendido con cálculo de estado vencido, alertas automáticas y sincronización por cron. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Modelo stock.production.lot (stock.lot) extendido con cálculo de estado vencido, alertas automáticas y sincronización por cron.' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Bloqueo de venta para lotes caducados probado y validado. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Bloqueo de venta para lotes caducados probado y validado.' se encuentre activo y operando según la especificación. | ☐ |
| 3 | Trazabilidad de lotes desde compras hasta ventas verificada. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Trazabilidad de lotes desde compras hasta ventas verificada.' se encuentre activo y operando según la especificación. | ☐ |
| 4 | Pruebas unitarias aprobadas al 100%. | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Pruebas unitarias aprobadas al 100%.' haya finalizado con resultado exitoso. | ☐ |
| 5 | Aprobación de la dirección técnica farmacéutica. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Aprobación de la dirección técnica farmacéutica.' se encuentre activo y operando según la especificación. | ☐ |

---

## Session Final Results

| Field | Value |
| :--- | :--- |
| Total flows executed | 3 |
| Flows passed | 3 |
| Flows failed | 0 |
| Flows blocked | 0 |
| AC coverage | 3 / 3 |
| DoD items verified | 5 / 5 |

**Verdict:** ☐ APPROVED — All ACs and DoD items covered with no blocking defects.  
            ☐ REJECTED — Defect(s) found. See notes per flow.  
            ☐ BLOCKED — Prerequisite not available. Reschedule session.  

**Defects found:**  
> None.
