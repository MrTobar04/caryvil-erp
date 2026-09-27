# Test Procedure: SPEC-4.1.1 — Dashboard de KPIs de Ventas

**Spec Reference:** [`SPEC-4.1.1`](../../specs/spec-4.1.1-dashboard-kpis-ventas.md)  
**Module:** Módulo 4 — Monitoreo & Alertas Gerenciales  
**Spec Status:** Implemented (100%)  
**Generated On:** 2026-09-27  
**Evaluated by:** ___________________________  
**Execution Date:** ___________________________  
**Overall Result:** ☐ APPROVED  ☐ REJECTED  ☐ BLOCKED  

---

## Environment Prerequisites

> Complete before executing any test step.

1. **Instancia Odoo Activa:** Módulo `caryvil_erp` instalado con datos de prueba de ventas e inventario.
2. **Catálogo y Lotes:** Productos configurados con stock crítico y lotes próximos a vencer.
3. **Rol Autorizado:** Usuario Gerente / Administrador o Encargado de Inventario.

---

## Test Flow 1: Visualización correcta de ventas del día

> Maps to: **Scenario 1 (AC-1)** de SPEC-4.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Visualización correcta de ventas del día**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Visualización correcta de ventas del día]:** La administradora abre la vista Dashboard. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** La tarjeta "Ventas del Día" debe mostrar exactamente $50.00, "Transacciones de Hoy" debe indicar 3 y "Ticket Promedio" debe mostrar $16.67. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Visualización correcta de ventas del día** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Actualización en tiempo real tras nueva venta

> Maps to: **Scenario 2 (AC-2)** de SPEC-4.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Actualización en tiempo real tras nueva venta**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Actualización en tiempo real tras nueva venta]:** Se completa y valida una nueva factura en mostrador por $20.00 y se refresca la vista. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Las métricas deben actualizarse inmediatamente reflejando $70.00 y 4 transacciones. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Actualización en tiempo real tras nueva venta** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Restricción de acceso para roles no autorizados

> Maps to: **Scenario 3 (AC-3)** de SPEC-4.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Restricción de acceso para roles no autorizados**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Restricción de acceso para roles no autorizados]:** Intenta acceder directamente a la acción del dashboard. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Odoo debe denegar el acceso mostrando un mensaje de restricción de permisos. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Restricción de acceso para roles no autorizados** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Modelo y métodos de agregación de KPIs implementados en Python. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Modelo y métodos de agregación de KPIs implementados en Python.' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Vista visual del dashboard integrada en la pantalla de inicio de Odoo. | Navegar a la vista correspondiente en Odoo UI y comprobar que el elemento gráfico 'Vista visual del dashboard integrada en la pantalla de inicio de Odoo.' se renderice alineado a los estilos de marca. | ☐ |
| 3 | Permisos de visualización restringidos al grupo Administrador. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Permisos de visualización restringidos al grupo Administrador.' se encuentre activo y operando según la especificación. | ☐ |
| 4 | Pruebas unitarias de cálculo de KPIs aprobadas al 100%. | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Pruebas unitarias de cálculo de KPIs aprobadas al 100%.' haya finalizado con resultado exitoso. | ☐ |
| 5 | Validación funcional con la propietaria de la farmacia. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Validación funcional con la propietaria de la farmacia.' se encuentre activo y operando según la especificación. | ☐ |

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
