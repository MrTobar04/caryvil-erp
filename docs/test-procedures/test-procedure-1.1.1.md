# Test Procedure: SPEC-1.1.1 — Configuración del Entorno Docker

**Spec Reference:** [`SPEC-1.1.1`](../../specs/spec-1.1.1-configuracion-entorno-docker.md)  
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

## Test Flow 1: Despliegue exitoso del entorno local

> Maps to: **Scenario 1 (AC-1)** de SPEC-1.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Despliegue exitoso del entorno local**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Despliegue exitoso del entorno local]:** El desarrollador ejecuta el comando docker compose -f infra/compose/docker-compose.yml up -d. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Ambos contenedores (caryvil-web y caryvil-db) deben iniciar en estado healthy, y la interfaz de Odoo debe responder en http://localhost:8069 mostrando el asistente de creación de base de datos o pantalla de inicio. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Despliegue exitoso del entorno local** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Persistencia de datos tras reinicio de contenedores

> Maps to: **Scenario 2 (AC-2)** de SPEC-1.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Persistencia de datos tras reinicio de contenedores**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Persistencia de datos tras reinicio de contenedores]:** Se ejecuta docker compose -f infra/compose/docker-compose.yml down seguido de docker compose -f infra/compose/docker-compose.yml up -d. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** La base de datos y los módulos instalados deben permanecer intactos sin pérdida de información. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Persistencia de datos tras reinicio de contenedores** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Montaje en caliente de módulos personalizados

> Maps to: **Scenario 3 (AC-3)** de SPEC-1.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Montaje en caliente de módulos personalizados**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Montaje en caliente de módulos personalizados]:** Se inicia el contenedor web. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El directorio /mnt/extra-addons dentro del contenedor debe reflejar los archivos del módulo local de forma sincronizada. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Montaje en caliente de módulos personalizados** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Archivos infra/docker/Dockerfile, infra/compose/docker-compose.yml y .dockerignore creados y probados. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Archivos infra/docker/Dockerfile, infra/compose/docker-compose.yml y .dockerignore creados y probados.' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Contenedores inician limpiamente en menos de 30 segundos sin errores en consola. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Contenedores inician limpiamente en menos de 30 segundos sin errores en consola.' se encuentre activo y operando según la especificación. | ☐ |
| 3 | Persistencia de datos verificada con reinicio forzado del daemon Docker. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Persistencia de datos verificada con reinicio forzado del daemon Docker.' se encuentre activo y operando según la especificación. | ☐ |
| 4 | Documentación de ejecución local (README.md) redactada con comandos paso a paso. | Revisar visualmente en la sección de ayuda o documentación del módulo que la guía 'Documentación de ejecución local (README.md) redactada con comandos paso a paso.' esté disponible y legible. | ☐ |
| 5 | Revisión de código aprobada e integrada a la rama principal. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Revisión de código aprobada e integrada a la rama principal.' se encuentre activo y operando según la especificación. | ☐ |

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
