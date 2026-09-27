# Test Procedure: SPEC-2.1.1 — Estructura del Módulo Personalizado caryvil_erp

**Spec Reference:** [`SPEC-2.1.1`](../../specs/spec-2.1.1-estructura-modulo-caryvil-erp.md)  
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

## Test Flow 1: Reconocimiento e instalación limpia del módulo

> Maps to: **Scenario 1 (AC-1)** de SPEC-2.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Reconocimiento e instalación limpia del módulo**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Reconocimiento e instalación limpia del módulo]:** El administrador actualiza la lista de aplicaciones e instala "Farmacia Caryvil ERP". Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Odoo debe instalar el módulo sin errores, cargando automáticamente todas sus dependencias (stock, purchase, salemanagement, contacts, account). Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Reconocimiento e instalación limpia del módulo** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Creación del menú raíz en la barra de navegación

> Maps to: **Scenario 2 (AC-2)** de SPEC-2.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Creación del menú raíz en la barra de navegación**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Creación del menú raíz en la barra de navegación]:** Un usuario autenticado accede a la interfaz principal de Odoo. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Debe visualizarse el icono y acceso a la aplicación "Farmacia Caryvil" con su estructura de menús base. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Creación del menú raíz en la barra de navegación** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Desinstalación sin residuos ni errores de integridad

> Maps to: **Scenario 3 (AC-3)** de SPEC-2.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Desinstalación sin residuos ni errores de integridad**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Desinstalación sin residuos ni errores de integridad]:** El administrador solicita desinstalar la aplicación. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Odoo debe desinstalar el módulo de forma limpia sin corromper los módulos nativos del sistema. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Desinstalación sin residuos ni errores de integridad** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Estructura de carpetas y archivos base creada bajo estándares Odoo. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Estructura de carpetas y archivos base creada bajo estándares Odoo.' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Manifiesto manifest.py configurado con todas las dependencias requeridas. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Manifiesto manifest.py configurado con todas las dependencias requeridas.' se encuentre activo y operando según la especificación. | ☐ |
| 3 | Instalación y desinstalación del módulo verificada en Odoo sin errores en logs. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Instalación y desinstalación del módulo verificada en Odoo sin errores en logs.' se encuentre activo y operando según la especificación. | ☐ |
| 4 | Menú raíz de Farmacia Caryvil visible en el backend. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Menú raíz de Farmacia Caryvil visible en el backend.' se encuentre activo y operando según la especificación. | ☐ |
| 5 | Revisión de código completada y fusionada en la rama principal. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Revisión de código completada y fusionada en la rama principal.' se encuentre activo y operando según la especificación. | ☐ |

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
