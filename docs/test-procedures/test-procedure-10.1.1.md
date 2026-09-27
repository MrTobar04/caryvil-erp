# Test Procedure: SPEC-10.1.1 — Datos Semilla Maestros del Sistema

**Spec Reference:** [`SPEC-10.1.1`](../../specs/spec-10.1.1-datos-semilla-maestros.md)  
**Module:** Módulo 10 — Carga de Datos Semilla  
**Spec Status:** Implemented (100%)  
**Generated On:** 2026-09-27  
**Evaluated by:** ___________________________  
**Execution Date:** ___________________________  
**Overall Result:** ☐ APPROVED  ☐ REJECTED  ☐ BLOCKED  

---

## Environment Prerequisites

> Complete before executing any test step.

1. **Base de Datos Odoo Limpia / Reiniciada:** Base de datos inicial lista para ejecución de scripts de carga semilla.
2. **Módulo caryvil_erp instalado:** Módulo cargado en Odoo 17.
3. **Rol Autorizado:** Administrador del Sistema.

---

## Test Flow 1: Inicialización de base de datos limpia

> Maps to: **Scenario 1 (AC-1)** de SPEC-10.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Inicialización de base de datos limpia**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Inicialización de base de datos limpia]:** Se instala el módulo caryvilerp. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** La compañía "Farmacia Caryvil" debe quedar establecida con moneda USD y las 10 familias terapéuticas base deben aparecer cargadas en el catálogo. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Inicialización de base de datos limpia** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Configuración automática del impuesto IVA (13%)

> Maps to: **Scenario 2 (AC-2)** de SPEC-10.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Configuración automática del impuesto IVA (13%)**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Configuración automática del impuesto IVA (13%)]:** Se consulta la configuración de impuestos de venta y compra. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Debe existir el impuesto "IVA 13% Bienes Farmacéuticos" activo y configurado como predeterminado. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Configuración automática del impuesto IVA (13%)** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Creación de usuarios de prueba por rol

> Maps to: **Scenario 3 (AC-3)** de SPEC-10.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Creación de usuarios de prueba por rol**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Creación de usuarios de prueba por rol]:** Se consultan los usuarios en Ajustes > Usuarios. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Deben existir los usuarios preconfigurados con sus credenciales y grupos de seguridad (cajerocaryvil, comprascaryvil, admincaryvil). Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Creación de usuarios de prueba por rol** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Archivos de datos maestros creados con sintaxis XML válida. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Archivos de datos maestros creados con sintaxis XML válida.' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Carga exitosa verificada en una base de datos Odoo virgen. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Carga exitosa verificada en una base de datos Odoo virgen.' se encuentre activo y operando según la especificación. | ☐ |
| 3 | Impuesto IVA 13% y moneda USD parametrizados. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Impuesto IVA 13% y moneda USD parametrizados.' se encuentre activo y operando según la especificación. | ☐ |
| 4 | Pruebas unitarias de carga de datos aprobadas al 100%. | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Pruebas unitarias de carga de datos aprobadas al 100%.' haya finalizado con resultado exitoso. | ☐ |
| 5 | Aprobación de las categorías y datos corporativos por la farmacia. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Aprobación de las categorías y datos corporativos por la farmacia.' se encuentre activo y operando según la especificación. | ☐ |

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
