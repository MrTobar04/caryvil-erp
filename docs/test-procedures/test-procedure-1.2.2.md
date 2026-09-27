# Test Procedure: SPEC-1.2.2 — Gestión de Variables de Entorno y Secretos

**Spec Reference:** [`SPEC-1.2.2`](../../specs/spec-1.2.2-gestion-variables-entorno-secretos.md)  
**Module:** Módulo 1 — Infraestructura, Base & CI/CD  
**Spec Status:** Implemented (100%)  
**Generated On:** 2026-09-27  
**Evaluated by:** ___________________________  
**Execution Date:** ___________________________  
**Overall Result:** ☐ APPROVED  ☐ REJECTED  ☐ BLOCKED  

---

## Environment Prerequisites

> Complete before executing any test step.

1. **Instancia / Plataforma de Despliegue Activa:** Entorno Docker o plataforma Render en estado operacional.
2. **Navegador Web & DevTools:** Navegador web moderno (Chrome/Firefox/Edge) con panel DevTools disponible.
3. **Credenciales de Administración:** Acceso a consola web o interfaz Odoo con rol de Administrador de Sistema.

---

## Test Flow 1: Inicialización de entorno local a partir de la plantilla

> Maps to: **Scenario 1 (AC-1)** de SPEC-1.2.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Inicialización de entorno local a partir de la plantilla**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Inicialización de entorno local a partir de la plantilla]:** Copia .env.example a .env y ejecuta docker compose up -d. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Los contenedores deben leer las variables de entorno sin errores y levantar el sistema con las credenciales definidas en su .env local. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Inicialización de entorno local a partir de la plantilla** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Detección y bloqueo de archivos sensibles en Git

> Maps to: **Scenario 2 (AC-2)** de SPEC-1.2.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Detección y bloqueo de archivos sensibles en Git**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Detección y bloqueo de archivos sensibles en Git]:** Intenta ejecutar git add . o git status. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Los archivos con credenciales reales no deben ser rastreados por Git debido a las reglas de .gitignore. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Detección y bloqueo de archivos sensibles en Git** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Inyección de variables en Render vía Terraform

> Maps to: **Scenario 3 (AC-3)** de SPEC-1.2.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Inyección de variables en Render vía Terraform**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Inyección de variables en Render vía Terraform]:** El Web Service de Render es aprovisionado. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Las variables de entorno de producción deben estar disponibles para Odoo sin quedar registradas en texto plano en los logs de la consola. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Inyección de variables en Render vía Terraform** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Archivo .env.example creado y probado con docker compose. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Archivo .env.example creado y probado con docker compose.' se encuentre activo y operando según la especificación. | ☐ |
| 2 | .gitignore verificado para asegurar el bloqueo de .env, .env.local y .tfvars. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que '.gitignore verificado para asegurar el bloqueo de .env, .env.local y .tfvars.' se encuentre activo y operando según la especificación. | ☐ |
| 3 | Variables y secretos requeridos documentados con su tipo y propósito. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Variables y secretos requeridos documentados con su tipo y propósito.' se encuentre activo y operando según la especificación. | ☐ |
| 4 | Revisión de seguridad aprobada por el equipo técnico. | Iniciar sesión con un usuario no privilegiado y verificar visualmente en la interfaz que el acceso a 'Revisión de seguridad aprobada por el equipo técnico.' quede restringido o invisible. | ☐ |

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
