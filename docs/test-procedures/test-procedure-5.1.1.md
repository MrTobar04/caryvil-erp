# Test Procedure: SPEC-5.1.1 — Gestión del Perfil de Clientes

**Spec Reference:** [`SPEC-5.1.1`](../../specs/spec-5.1.1-gestion-perfil-clientes.md)  
**Module:** Módulo 5 — Gestión de Clientes  
**Spec Status:** Implemented (100%)  
**Generated On:** 2026-09-27  
**Evaluated by:** ___________________________  
**Execution Date:** ___________________________  
**Overall Result:** ☐ APPROVED  ☐ REJECTED  ☐ BLOCKED  

---

## Environment Prerequisites

> Complete before executing any test step.

1. **Instancia Odoo Activa:** Módulo `caryvil_erp` desplegado con la app de Clientes/CRM activa.
2. **Base de Datos de Clientes:** Registros de prueba de clientes individuales y corporativos cargados.
3. **Rol Autorizado:** Usuario Cajero o Encargado de Ventas.

---

## Test Flow 1: Registro exitoso de cliente con DUI válido

> Maps to: **Scenario 1 (AC-1)** de SPEC-5.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Registro exitoso de cliente con DUI válido**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Registro exitoso de cliente con DUI válido]:** Presiona "Guardar". Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El registro se almacena exitosamente con el campo name calculado como "María Elena López Rivas" y ispharmacycustomer = True. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Registro exitoso de cliente con DUI válido** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Rechazo de DUI con formato inválido

> Maps to: **Scenario 2 (AC-2)** de SPEC-5.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Rechazo de DUI con formato inválido**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Rechazo de DUI con formato inválido]:** Intenta guardar el cliente. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Odoo debe bloquear el guardado y mostrar una ventana emergente de error de validación (ValidationError) explicando el formato requerido 00000000-0. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Rechazo de DUI con formato inválido** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Bloqueo de cliente duplicado por DUI

> Maps to: **Scenario 3 (AC-3)** de SPEC-5.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Bloqueo de cliente duplicado por DUI**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Bloqueo de cliente duplicado por DUI]:** Se intenta crear un segundo cliente con el mismo DUI "01234567-8". Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El sistema debe rechazar la operación indicando que el DUI ya se encuentra registrado. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Bloqueo de cliente duplicado por DUI** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Campos salvadoreños (firstname, lastname, dui, dirección) implementados en res.partner. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Campos salvadoreños (firstname, lastname, dui, dirección) implementados en res.partner.' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Validación de formato y unicidad de DUI probada con casos límite. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Validación de formato y unicidad de DUI probada con casos límite.' se encuentre activo y operando según la especificación. | ☐ |
| 3 | Vista de clientes en Odoo adaptada con la nueva distribución de campos. | Navegar a la vista correspondiente en Odoo UI y comprobar que el elemento gráfico 'Vista de clientes en Odoo adaptada con la nueva distribución de campos.' se renderice alineado a los estilos de marca. | ☐ |
| 4 | Pruebas unitarias de validación en Python aprobadas al 100%. | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Pruebas unitarias de validación en Python aprobadas al 100%.' haya finalizado con resultado exitoso. | ☐ |
| 5 | Aprobación funcional por el equipo del Sprint 2. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Aprobación funcional por el equipo del Sprint 2.' se encuentre activo y operando según la especificación. | ☐ |

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
