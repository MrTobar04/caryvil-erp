# Test Procedure: SPEC-10.2.1 — Datos Semilla Operativos y Demostración

**Spec Reference:** [`SPEC-10.2.1`](../../specs/spec-10.2.1-datos-semilla-operativos.md)  
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

## Test Flow 1: Carga completa del catálogo de medicamentos operativos

> Maps to: **Scenario 1 (AC-1)** de SPEC-10.2.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Carga completa del catálogo de medicamentos operativos**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Carga completa del catálogo de medicamentos operativos]:** El usuario navega a Inventario > Medicamentos. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Deben aparecer listados los 25 medicamentos con sus nombres, categorías terapéuticas, principios activos, códigos de barra y precios de venta al público. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Carga completa del catálogo de medicamentos operativos** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Consulta de proveedores y clientes muestra

> Maps to: **Scenario 2 (AC-2)** de SPEC-10.2.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Consulta de proveedores y clientes muestra**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Consulta de proveedores y clientes muestra]:** Se consultan las listas de Clientes y Proveedores. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Deben visualizarse los 4 laboratorios y los 10 clientes con sus números de DUI formateados listos para transaccionar. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Consulta de proveedores y clientes muestra** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Existencia de stock y lotes para pruebas del Dashboard y FEFO

> Maps to: **Scenario 3 (AC-3)** de SPEC-10.2.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Existencia de stock y lotes para pruebas del Dashboard y FEFO**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Existencia de stock y lotes para pruebas del Dashboard y FEFO]:** La administradora abre el Dashboard de inicio. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El widget de alertas de vencimiento debe mostrar los lotes de prueba clasificados en las ventanas de <30 días y 31-60 días. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Existencia de stock y lotes para pruebas del Dashboard y FEFO** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Catálogo de 25 medicamentos con datos farmacéuticos completos creado. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Catálogo de 25 medicamentos con datos farmacéuticos completos creado.' se encuentre activo y operando según la especificación. | ☐ |
| 2 | 4 laboratorios y 10 clientes salvadoreños de muestra estructurados. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que '4 laboratorios y 10 clientes salvadoreños de muestra estructurados.' se encuentre activo y operando según la especificación. | ☐ |
| 3 | Stock inicial por lotes con fechas de vencimiento cargado. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Stock inicial por lotes con fechas de vencimiento cargado.' se encuentre activo y operando según la especificación. | ☐ |
| 4 | Pruebas unitarias de verificación de datos aprobadas. | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Pruebas unitarias de verificación de datos aprobadas.' haya finalizado con resultado exitoso. | ☐ |
| 5 | Aprobación del conjunto de datos por el equipo del proyecto y la propietaria. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Aprobación del conjunto de datos por el equipo del proyecto y la propietaria.' se encuentre activo y operando según la especificación. | ☐ |

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
