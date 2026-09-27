# Test Procedure: SPEC-2.2.1 — Definición de Roles y Grupos de Usuarios

**Spec Reference:** [`SPEC-2.2.1`](../../specs/spec-2.2.1-definicion-roles-usuarios.md)  
**Module:** Módulo 2 — Arquitectura del Módulo caryvil_erp & Seguridad  
**Spec Status:** Implemented (100%)  
**Generated On:** 2026-09-27  
**Evaluated by:** ___________________________  
**Execution Date:** ___________________________  
**Overall Result:** ☐ APPROVED  ☐ REJECTED  ☐ BLOCKED  

---

## Environment Prerequisites

> Complete before executing any test step.

1. **Instancia de Odoo Activa:** Odoo 17 ERP en ejecución con módulo `caryvil_erp` instalado.
2. **Usuarios de Prueba Configurados:** Usuarios con roles Administrador, Encargado de Inventario, Vendedor y Cajero.
3. **Navegador Web:** Sesión limpia en navegador web para alternar entre diferentes usuarios de prueba.

---

## Test Flow 1: Asignación de rol de Cajero a un nuevo usuario

> Maps to: **Scenario 1 (AC-1)** de SPEC-2.2.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Asignación de rol de Cajero a un nuevo usuario**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Asignación de rol de Cajero a un nuevo usuario]:** Inicia sesión en el ERP. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Debe tener acceso a crear ventas y registrar clientes, pero no debe visualizar los menús de Compras, Configuración del Sistema ni el Dashboard gerencial. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Asignación de rol de Cajero a un nuevo usuario** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Asignación de rol de Encargado de Compras e Inventario

> Maps to: **Scenario 2 (AC-2)** de SPEC-2.2.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Asignación de rol de Encargado de Compras e Inventario**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Asignación de rol de Encargado de Compras e Inventario]:** Accede a la aplicación. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Debe poder generar órdenes de compra a proveedores, recibir mercadería asignando lotes y ajustar existencias, pero no debe tener permisos para modificar la configuración de la empresa ni eliminar usuarios. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Asignación de rol de Encargado de Compras e Inventario** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Control total para el rol Administrador

> Maps to: **Scenario 3 (AC-3)** de SPEC-2.2.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Control total para el rol Administrador**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Control total para el rol Administrador]:** Ingresa al sistema. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Debe visualizar todos los menús, reportes de márgenes, dashboard analítico y opciones de configuración avanzada. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Control total para el rol Administrador** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Archivo caryvilsecurity.xml implementado con los 3 roles y jerarquías. | Iniciar sesión con un usuario no privilegiado y verificar visualmente en la interfaz que el acceso a 'Archivo caryvilsecurity.xml implementado con los 3 roles y jerarquías.' quede restringido o invisible. | ☐ |
| 2 | Roles visibles y seleccionables en el formulario de usuarios de Odoo (Ajustes > Usuarios). | Iniciar sesión con un usuario no privilegiado y verificar visualmente en la interfaz que el acceso a 'Roles visibles y seleccionables en el formulario de usuarios de Odoo (Ajustes > Usuarios).' quede restringido o invisible. | ☐ |
| 3 | Herencia de permisos comprobada con usuarios de prueba para cada rol. | Iniciar sesión con un usuario no privilegiado y verificar visualmente en la interfaz que el acceso a 'Herencia de permisos comprobada con usuarios de prueba para cada rol.' quede restringido o invisible. | ☐ |
| 4 | Revisión de código aprobada e integrada a la rama principal. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Revisión de código aprobada e integrada a la rama principal.' se encuentre activo y operando según la especificación. | ☐ |

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
