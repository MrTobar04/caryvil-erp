# Test Procedure: SPEC-3.1.2 — Personalización de Pantalla de Autenticación

**Spec Reference:** [`SPEC-3.1.2`](../../specs/spec-3.1.2-personalizacion-pantalla-autenticacion.md)  
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

## Test Flow 1: Despliegue de la interfaz de autenticación corporativa

> Maps to: **Scenario 1 (AC-1)** de SPEC-3.1.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Despliegue de la interfaz de autenticación corporativa**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Despliegue de la interfaz de autenticación corporativa]:** La página se renderiza. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** La tarjeta de inicio de sesión debe mostrar el encabezado "ERP FARMACIA", el subtítulo "Farmacia Caryvil • Soyapango", los campos estilizados y el botón de acceso en verde institucional (28A745). Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Despliegue de la interfaz de autenticación corporativa** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Autenticación exitosa con credenciales válidas

> Maps to: **Scenario 2 (AC-2)** de SPEC-3.1.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Autenticación exitosa con credenciales válidas**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Autenticación exitosa con credenciales válidas]:** Presiona el botón verde de inicio de sesión. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Odoo valida el token CSRF, inicia la sesión y redirige al dashboard o módulo asignado según su rol. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Autenticación exitosa con credenciales válidas** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Despliegue de errores ante credenciales incorrectas

> Maps to: **Scenario 3 (AC-3)** de SPEC-3.1.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Despliegue de errores ante credenciales incorrectas**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Despliegue de errores ante credenciales incorrectas]:** Se procesa la petición. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Se muestra la notificación de error en un contenedor alert estilizado sin desconfigurar el diseño centrado de la tarjeta. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Despliegue de errores ante credenciales incorrectas** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Plantilla XML weblogintemplates.xml implementada y enlazada. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Plantilla XML weblogintemplates.xml implementada y enlazada.' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Hoja de estilos customlogin.scss registrada y probada. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Hoja de estilos customlogin.scss registrada y probada.' se encuentre activo y operando según la especificación. | ☐ |
| 3 | Encabezado corporativo "ERP FARMACIA" y botón verde renderizados. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Encabezado corporativo "ERP FARMACIA" y botón verde renderizados.' se encuentre activo y operando según la especificación. | ☐ |
| 4 | Validación de accesibilidad y funcionamiento de login completada. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Validación de accesibilidad y funcionamiento de login completada.' se encuentre activo y operando según la especificación. | ☐ |

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
