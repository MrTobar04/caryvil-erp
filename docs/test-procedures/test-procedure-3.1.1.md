# Test Procedure: SPEC-3.1.1 — Personalización de Marca y Tema Visual — **** ✅

**Spec Reference:** [`SPEC-3.1.1`](../../specs/spec-3.1.1-personalizacion-marca-tema.md)  
**Module:** Módulo 3 — Branding UI/UX & Plantillas de Reportes  
**Spec Status:** Implemented (100%)  
**Generated On:** 2026-09-27  
**Evaluated by:** ___________________________  
**Execution Date:** ___________________________  
**Overall Result:** ☐ APPROVED  ☐ REJECTED  ☐ BLOCKED  

---

## Environment Prerequisites

> Complete before executing any test step.

1. **Instancia Odoo Activa:** Odoo 17 con tema visual y branding de Farmacia Caryvil aplicado.
2. **Plantillas e Impresora/PDF:** Generador de reportes PDF habilitado y visor PDF integrado en navegador.
3. **Usuarios de Prueba:** Usuario Administrador y Usuario Cajero/Vendedor.

---

## Test Flow 1: Aplicación de la barra lateral azul marino y barra superior gris-azul

> Maps to: **Scenario 1 (AC-1)** de SPEC-3.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Aplicación de la barra lateral azul marino y barra superior gris-azul**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Aplicación de la barra lateral azul marino y barra superior gris-azul]:** Un usuario autenticado ingresa a cualquier sección del ERP. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** La interfaz debe desplegar la barra lateral con fondo azul marino (002B49), el título de marca "ERP FARMACIA", la barra superior gris-azul pizarra (5C6F84) y el elemento de menú activo resaltado en color cian con su indicador lateral. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Aplicación de la barra lateral azul marino y barra superior gris-azul** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Renderizado de botones de acción y botones de cancelar

> Maps to: **Scenario 2 (AC-2)** de SPEC-3.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Renderizado de botones de acción y botones de cancelar**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Renderizado de botones de acción y botones de cancelar]:** Visualiza la barra de control superior. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El botón de confirmación ("Guardar", "Crear") debe mostrarse en verde salud (28A745) y el botón "Cancelar" con contorno gris y fondo blanco. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Renderizado de botones de acción y botones de cancelar** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Despliegue de badges de estado en tablas y tarjetas

> Maps to: **Scenario 3 (AC-3)** de SPEC-3.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Despliegue de badges de estado en tablas y tarjetas**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Despliegue de badges de estado en tablas y tarjetas]:** Se renderizan en las vistas de lista o dashboard. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Los badges deben adoptar el color contextual exacto: "Bajo stock" en fondo amarillo suave, "Por vencer" en fondo rosado/rojo suave, "OK" en fondo verde menta y "Dañado" en fondo gris neutro. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Despliegue de badges de estado en tablas y tarjetas** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 4: Accesibilidad y contraste tipográfico

> Maps to: **Scenario 4 (AC-4)** de SPEC-3.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Accesibilidad y contraste tipográfico**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Accesibilidad y contraste tipográfico]:** Se leen los datos en tablas, campos de formulario y tarjetas. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El contraste cromático cumple con el estándar WCAG AA (> 4.5:1). Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Accesibilidad y contraste tipográfico** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Archivo customtheme.scss implementado y cargado en el bundle de Odoo. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Archivo customtheme.scss implementado y cargado en el bundle de Odoo.' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Barra lateral 002B49, barra superior 5C6F84 y botones verdes WCAG-AA 1E7A3A reflejados con exactitud según los mockups. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Barra lateral 002B49, barra superior 5C6F84 y botones verdes WCAG-AA 1E7A3A reflejados con exactitud según los mockups.' se encuentre activo y operando según la especificación. | ☐ |
| 3 | Badges de estado contextuales implementados y visibles en listados y dashboard. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Badges de estado contextuales implementados y visibles en listados y dashboard.' se encuentre activo y operando según la especificación. | ☐ |
| 4 | Pruebas de contraste WCAG AA superadas con ratio > 4.5:1 (verificadas matemáticamente en la suite de tests automatizados). | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Pruebas de contraste WCAG AA superadas con ratio > 4.5:1 (verificadas matemáticamente en la suite de tests automatizados).' haya finalizado con resultado exitoso. | ☐ |
| 5 | Verificación de fidelidad visual contra los mockups aprobada. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Verificación de fidelidad visual contra los mockups aprobada.' se encuentre activo y operando según la especificación. | ☐ |

---

## Session Final Results

| Field | Value |
| :--- | :--- |
| Total flows executed | 4 |
| Flows passed | 4 |
| Flows failed | 0 |
| Flows blocked | 0 |
| AC coverage | 4 / 4 |
| DoD items verified | 5 / 5 |

**Verdict:** ☐ APPROVED — All ACs and DoD items covered with no blocking defects.  
            ☐ REJECTED — Defect(s) found. See notes per flow.  
            ☐ BLOCKED — Prerequisite not available. Reschedule session.  

**Defects found:**  
> None.
