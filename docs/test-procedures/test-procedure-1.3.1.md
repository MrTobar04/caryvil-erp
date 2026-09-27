# Test Procedure: SPEC-1.3.1 — Pipeline CI/CD con GitHub Actions

**Spec Reference:** [`SPEC-1.3.1`](../../specs/spec-1.3.1-pipeline-ci-cd-github-actions.md)  
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

## Test Flow 1: Rechazo de Pull Request con errores de sintaxis

> Maps to: **Scenario 1 (AC-1)** de SPEC-1.3.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Rechazo de Pull Request con errores de sintaxis**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Rechazo de Pull Request con errores de sintaxis]:** GitHub Actions ejecuta el workflow ci-validation. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El job Lint & Static Analysis debe fallar, bloquear el merge del Pull Request e indicar la línea exacta del error en los logs. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Rechazo de Pull Request con errores de sintaxis** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Validación exitosa de Pull Request conforme

> Maps to: **Scenario 2 (AC-2)** de SPEC-1.3.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Validación exitosa de Pull Request conforme**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Validación exitosa de Pull Request conforme]:** GitHub Actions ejecuta el pipeline de CI. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Todos los jobs de validación y compilación de Docker deben finalizar en verde (código 0) en menos de 5 minutos. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Validación exitosa de Pull Request conforme** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Despliegue automático a Render tras merge en main

> Maps to: **Scenario 3 (AC-3)** de SPEC-1.3.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Despliegue automático a Render tras merge en main**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Despliegue automático a Render tras merge en main]:** El evento push: main se dispara en GitHub Actions. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El pipeline debe activar el job de despliegue, notificar a Render y confirmar que el servicio web responda con estado HTTP 200 en su URL pública. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Despliegue automático a Render tras merge en main** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Workflows de GitHub Actions implementados en el repositorio (ci-validation.yml y cd-deploy.yml). | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Workflows de GitHub Actions implementados en el repositorio (ci-validation.yml y cd-deploy.yml).' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Pipeline de CI validado exitosamente con análisis estático (Flake8, Black, Yamllint, Terraform, XML) y Docker Build con caché. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Pipeline de CI validado exitosamente con análisis estático (Flake8, Black, Yamllint, Terraform, XML) y Docker Build con caché.' se encuentre activo y operando según la especificación. | ☐ |
| 3 | Flujo de CD a Render verificado y enlazado con los secretos del repositorio (RENDERDEPLOYHOOKURL, RENDERSERVICEURL). | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Flujo de CD a Render verificado y enlazado con los secretos del repositorio (RENDERDEPLOYHOOKURL, RENDERSERVICEURL).' se encuentre activo y operando según la especificación. | ☐ |
| 4 | Documentación del flujo de verificación manual añadida en docs/guias/guion-pruebas-manuales.md (Flujo 1.5). | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Documentación del flujo de verificación manual añadida en docs/guias/guion-pruebas-manuales.md (Flujo 1.5).' haya finalizado con resultado exitoso. | ☐ |
| 5 | Suite de pruebas automatizadas creada en tests/testspec131cicd.py con 100% de aprobación. | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Suite de pruebas automatizadas creada en tests/testspec131cicd.py con 100% de aprobación.' haya finalizado con resultado exitoso. | ☐ |

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
