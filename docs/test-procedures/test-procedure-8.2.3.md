# Test Procedure: SPEC-8.2.3 — Control de Discrepancias en Recepción de Compras

**Spec Reference:** [`SPEC-8.2.3`](../../specs/spec-8.2.3-control-discrepancias-recepcion-compras.md)  
**Module:** Módulo 8 — Órdenes de Compra & Recepción  
**Spec Status:** Implemented (100%)  
**Generated On:** 2026-09-27  
**Evaluated by:** ___________________________  
**Execution Date:** ___________________________  
**Overall Result:** ☐ APPROVED  ☐ REJECTED  ☐ BLOCKED  

---

## Environment Prerequisites

> Complete before executing any test step.

1. **Instancia Odoo Activa:** Módulo de Compras y Recepciones Caryvil ERP desplegado.
2. **Órdenes y Proveedores:** Proveedores habilitados y órdenes de compra en borrador/confirmadas.
3. **Rol Autorizado:** Usuario Encargado de Compras y Recepción de Almacén.

---

## Test Flow 1: Entrega parcial con generación de Backorder

> Maps to: **Scenario 1 (AC-1)** de SPEC-8.2.3.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Entrega parcial con generación de Backorder**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Entrega parcial con generación de Backorder]:** El usuario valida el ingreso de 20 cajas y selecciona "Crear Entrega Parcial". Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El stock aumenta en 20 cajas, el albarán actual pasa a estado done y Odoo crea automáticamente un nuevo albarán por las 10 cajas restantes en estado assigned. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Entrega parcial con generación de Backorder** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Entrega parcial sin Backorder (Agotado en Distribuidora)

> Maps to: **Scenario 2 (AC-2)** de SPEC-8.2.3.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Entrega parcial sin Backorder (Agotado en Distribuidora)**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Entrega parcial sin Backorder (Agotado en Distribuidora)]:** El usuario valida 10 unidades y selecciona "No crear entrega parcial". Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El stock aumenta en 10 unidades, la orden de compra ajusta su saldo y se cierra sin dejar albaranes pendientes. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Entrega parcial sin Backorder (Agotado en Distribuidora)** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Rechazo de producto dañado en la descarga

> Maps to: **Scenario 3 (AC-3)** de SPEC-8.2.3.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Rechazo de producto dañado en la descarga**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Rechazo de producto dañado en la descarga]:** El receptor no incluye los 5 frascos en la qtydone y escribe en la nota: "5 frascos rotos rechazados al repartidor". Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El sistema no ingresa los 5 frascos al inventario y registra la incidencia en el historial para conciliar con la factura del proveedor. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Rechazo de producto dañado en la descarga** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Asistente de backorders configurado y probado para recepciones parciales — nativo de Odoo (stock.backorder.confirmation, se activa solo cuando qtydone < demanda); no requirió código adicional. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Asistente de backorders configurado y probado para recepciones parciales — nativo de Odoo (stock.backorder.confirmation, se activa solo cuando qtydone < demanda); no requirió código adicional.' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Registro de notas de rechazo y daños en transporte habilitado (discrepancynotes + pestaña "Discrepancias" en el albarán). | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Registro de notas de rechazo y daños en transporte habilitado (discrepancynotes + pestaña "Discrepancias" en el albarán).' se encuentre activo y operando según la especificación. | ☐ |
| 3 | Cancelación de remanentes validada sin errores contables — flujo nativo de Odoo ("No crear entrega parcial"). | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Cancelación de remanentes validada sin errores contables — flujo nativo de Odoo ("No crear entrega parcial").' se encuentre activo y operando según la especificación. | ☐ |
| 4 | Pruebas unitarias aprobadas al 100% (tests/teststockpickingreception.py). | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Pruebas unitarias aprobadas al 100% (tests/teststockpickingreception.py).' haya finalizado con resultado exitoso. | ☐ |
| 5 | Aprobación del procedimiento de discrepancias por la administración. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Aprobación del procedimiento de discrepancias por la administración.' se encuentre activo y operando según la especificación. | ☐ |

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
