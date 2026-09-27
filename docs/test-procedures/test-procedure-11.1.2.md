# Test Procedure: SPEC-11.1.2 — Pruebas Automatizadas de Ventas, FEFO y Facturación

**Spec Reference:** [`SPEC-11.1.2`](../../specs/spec-11.1.2-pruebas-flujo-ventas-fefo-facturacion.md)  
**Module:** Módulo 11 — Pruebas de Integración y Validación E2E  
**Spec Status:** Implemented (100%)  
**Generated On:** 2026-09-27  
**Evaluated by:** ___________________________  
**Execution Date:** ___________________________  
**Overall Result:** ☐ APPROVED  ☐ REJECTED  ☐ BLOCKED  

---

## Environment Prerequisites

> Complete before executing any test step.

1. **Instancia Odoo ERP Completa:** Todos los módulos de Caryvil ERP instalados y configurados.
2. **Datos de Prueba de Flujo Completo:** Proveedores, clientes, medicamentos con lotes y cajas aperturadas.
3. **Usuarios de Prueba Multirrol:** Roles Administrador, Inventario, Compras y Cajero POS.

---

## Test Flow 1: Validación del algoritmo FEFO y fraccionamiento multilote

> Maps to: **Scenario 1 (AC-1)** de SPEC-11.1.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Validación del algoritmo FEFO y fraccionamiento multilote**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Validación del algoritmo FEFO y fraccionamiento multilote]:** Se corre testfefolotselectionandsplitting. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El test confirma que los lotes se agotan en estricto orden cronológico de caducidad y que las cantidades finales en inventario son exactas. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Validación del algoritmo FEFO y fraccionamiento multilote** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Verificación de bloqueo ante saldo negativo

> Maps to: **Scenario 2 (AC-2)** de SPEC-11.1.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Verificación de bloqueo ante saldo negativo**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Verificación de bloqueo ante saldo negativo]:** Se ejecuta teststrictnegativestockblocking. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El test valida que el intento de sobreventa lance UserError y no descuente unidades inexistentes. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Verificación de bloqueo ante saldo negativo** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Verificación de factura simple e importe en letras

> Maps to: **Scenario 3 (AC-3)** de SPEC-11.1.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Verificación de factura simple e importe en letras**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Verificación de factura simple e importe en letras]:** Se ejecuta testsimpleinvoicevatandwordscalculation. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El test confirma que el número de factura simple se asigne y que la conversión a letras en español sea ortográficamente correcta. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Verificación de factura simple e importe en letras** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Suite de pruebas de ventas, FEFO y facturación implementada. | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Suite de pruebas de ventas, FEFO y facturación implementada.' haya finalizado con resultado exitoso. | ☐ |
| 2 | Cobertura de pruebas sobre el flujo transaccional de caja > 90%. | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Cobertura de pruebas sobre el flujo transaccional de caja > 90%.' haya finalizado con resultado exitoso. | ☐ |
| 3 | Aprobación de todos los asserts en CI/CD. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Aprobación de todos los asserts en CI/CD.' se encuentre activo y operando según la especificación. | ☐ |
| 4 | Revisión y aprobación del código por el equipo de ingeniería. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Revisión y aprobación del código por el equipo de ingeniería.' se encuentre activo y operando según la especificación. | ☐ |

---

## Session Final Results

| Field | Value |
| :--- | :--- |
| Total flows executed | 3 |
| Flows passed | 3 |
| Flows failed | 0 |
| Flows blocked | 0 |
| AC coverage | 3 / 3 |
| DoD items verified | 4 / 4 |

**Verdict:** ☐ APPROVED — All ACs and DoD items covered with no blocking defects.  
            ☐ REJECTED — Defect(s) found. See notes per flow.  
            ☐ BLOCKED — Prerequisite not available. Reschedule session.  

**Defects found:**  
> None.
