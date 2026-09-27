# Test Procedure: SPEC-2.2.2 — Reglas de Acceso y Seguridad de Modelos

**Spec Reference:** [`SPEC-2.2.2`](../../specs/spec-2.2.2-reglas-acceso-seguridad-modelos.md)  
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

## Test Flow 1: Intento de eliminación de medicamento por parte de un Cajero

> Maps to: **Scenario 1 (AC-1)** de SPEC-2.2.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Intento de eliminación de medicamento por parte de un Cajero**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Intento de eliminación de medicamento por parte de un Cajero]:** Intenta ejecutar la acción "Suprimir" en un registro del catálogo de medicamentos. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Odoo debe denegar la acción arrojando un error de permisos de acceso (AccessError) impidiendo la eliminación física del registro. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Intento de eliminación de medicamento por parte de un Cajero** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Creación y edición de clientes por parte del Cajero

> Maps to: **Scenario 2 (AC-2)** de SPEC-2.2.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Creación y edición de clientes por parte del Cajero**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Creación y edición de clientes por parte del Cajero]:** Registra un nuevo cliente con su DUI o edita el número telefónico de un cliente existente. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El sistema debe permitir la creación y guardado exitoso del cliente (permcreate = 1, permwrite = 1), pero impedir su eliminación (permunlink = 0). Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Creación y edición de clientes por parte del Cajero** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Intento de modificación de factura emitida

> Maps to: **Scenario 3 (AC-3)** de SPEC-2.2.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Intento de modificación de factura emitida**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Intento de modificación de factura emitida]:** Un usuario con rol de Cajero intenta modificar el precio o los ítems de dicha factura. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El sistema debe rechazar la modificación por la regla de registro activa, permitiendo únicamente la consulta y re-impresión del comprobante. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Intento de modificación de factura emitida** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Archivo ir.model.access.csv configurado sin advertencias en la carga del módulo. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Archivo ir.model.access.csv configurado sin advertencias en la carga del módulo.' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Reglas de registro caryvilsecurityrules.xml activas y probadas. | Iniciar sesión con un usuario no privilegiado y verificar visualmente en la interfaz que el acceso a 'Reglas de registro caryvilsecurityrules.xml activas y probadas.' quede restringido o invisible. | ☐ |
| 3 | Pruebas unitarias de denegación y autorización de acceso superadas al 100%. | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Pruebas unitarias de denegación y autorización de acceso superadas al 100%.' haya finalizado con resultado exitoso. | ☐ |
| 4 | Revisión de seguridad y permisos aprobada por el líder técnico. | Iniciar sesión con un usuario no privilegiado y verificar visualmente en la interfaz que el acceso a 'Revisión de seguridad y permisos aprobada por el líder técnico.' quede restringido o invisible. | ☐ |

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
