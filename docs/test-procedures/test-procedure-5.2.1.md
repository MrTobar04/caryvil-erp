# Test Procedure: SPEC-5.2.1 — Búsqueda Rápida de Clientes en Caja

**Spec Reference:** [`SPEC-5.2.1`](../../specs/spec-5.2.1-busqueda-rapida-clientes-caja.md)  
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

## Test Flow 1: Búsqueda por número de DUI en el campo de cliente

> Maps to: **Scenario 1 (AC-1)** de SPEC-5.2.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Búsqueda por número de DUI en el campo de cliente**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Búsqueda por número de DUI en el campo de cliente]:** Digita en el campo de cliente "04589632". Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** La lista desplegable debe mostrar de inmediato [04589632-1] María Elena López Rivas - Tel: 7845-1234 para selección con la tecla Enter. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Búsqueda por número de DUI en el campo de cliente** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Búsqueda por número de teléfono

> Maps to: **Scenario 2 (AC-2)** de SPEC-5.2.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Búsqueda por número de teléfono**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Búsqueda por número de teléfono]:** El cajero ingresa dicho número en el buscador. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El sistema debe localizar y autocompletar la ficha de dicho cliente. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Búsqueda por número de teléfono** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Alta rápida de cliente nuevo desde el desplegable

> Maps to: **Scenario 3 (AC-3)** de SPEC-5.2.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Alta rápida de cliente nuevo desde el desplegable**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Alta rápida de cliente nuevo desde el desplegable]:** El cajero escribe su nombre o DUI y presiona "Crear y Editar...". Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Se despliega una ventana modal simplificada con solo los campos indispensables (Nombre, DUI, Teléfono) y, al guardar, el cliente queda automáticamente asignado a la venta en curso. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Alta rápida de cliente nuevo desde el desplegable** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Búsqueda multicampo (DUI, teléfono, nombre) implementada y testeada. | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Búsqueda multicampo (DUI, teléfono, nombre) implementada y testeada.' haya finalizado con resultado exitoso. | ☐ |
| 2 | Formato displayname con DUI visible en todos los selectores de cliente. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Formato displayname con DUI visible en todos los selectores de cliente.' se encuentre activo y operando según la especificación. | ☐ |
| 3 | Tiempo de respuesta de búsqueda < 200ms comprobado. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Tiempo de respuesta de búsqueda < 200ms comprobado.' se encuentre activo y operando según la especificación. | ☐ |
| 4 | Pruebas unitarias en Python aprobadas. | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Pruebas unitarias en Python aprobadas.' haya finalizado con resultado exitoso. | ☐ |
| 5 | Validación de experiencia de usuario en mostrador aprobada. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Validación de experiencia de usuario en mostrador aprobada.' se encuentre activo y operando según la especificación. | ☐ |

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
