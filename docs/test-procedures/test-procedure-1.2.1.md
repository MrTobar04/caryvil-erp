# Test Procedure: SPEC-1.2.1 — Aprovisionamiento en Render con Terraform

**Spec Reference:** [`SPEC-1.2.1`](../../specs/spec-1.2.1-aprovisionamiento-render-terraform.md)  
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

## Test Flow 1: Validación y plan de infraestructura exitoso

> Maps to: **Scenario 1 (AC-1)** de SPEC-1.2.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Validación y plan de infraestructura exitoso**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Validación y plan de infraestructura exitoso]:** El ingeniero ejecuta terraform plan. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Terraform debe generar un plan limpio mostrando la adición de 2 recursos (renderpostgres y renderwebservice) sin errores de sintaxis. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Validación y plan de infraestructura exitoso** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Aprovisionamiento y despliegue en la nube

> Maps to: **Scenario 2 (AC-2)** de SPEC-1.2.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Aprovisionamiento y despliegue en la nube**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Aprovisionamiento y despliegue en la nube]:** Se ejecuta terraform apply -auto-approve. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Render debe instanciar la base de datos PostgreSQL y el Web Service de Odoo, devolviendo una URL pública accesible vía HTTPS en menos de 10 minutos. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Aprovisionamiento y despliegue en la nube** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Destrucción limpia de recursos temporales

> Maps to: **Scenario 3 (AC-3)** de SPEC-1.2.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Destrucción limpia de recursos temporales**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Destrucción limpia de recursos temporales]:** Se ejecuta terraform destroy -auto-approve. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Todos los recursos asociados en Render deben ser eliminados sin dejar costos residuales ni instancias huérfanas. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Destrucción limpia de recursos temporales** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Manifiestos de Terraform formateados y validados (terraform validate). | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Manifiestos de Terraform formateados y validados (terraform validate).' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Despliegue de prueba exitoso realizado en Render mediante terraform apply. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Despliegue de prueba exitoso realizado en Render mediante terraform apply.' se encuentre activo y operando según la especificación. | ☐ |
| 3 | URL pública accesible y conectada a la base de datos PostgreSQL. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'URL pública accesible y conectada a la base de datos PostgreSQL.' se encuentre activo y operando según la especificación. | ☐ |
| 4 | Archivos de estado excluidos del repositorio Git. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Archivos de estado excluidos del repositorio Git.' se encuentre activo y operando según la especificación. | ☐ |
| 5 | Pull Request revisado y aprobado por el equipo de arquitectura. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Pull Request revisado y aprobado por el equipo de arquitectura.' se encuentre activo y operando según la especificación. | ☐ |

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
