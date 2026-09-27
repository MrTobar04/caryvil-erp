# Test Procedure: SPEC-7.3.2 — Gestión de Mermas y Bajas de Medicamentos

**Spec Reference:** [`SPEC-7.3.2`](../../specs/spec-7.3.2-gestion-mermas-bajas-medicamentos.md)  
**Module:** Módulo 7 — Gestión de Inventario & Farmacia  
**Spec Status:** Implemented (100%)  
**Generated On:** 2026-09-27  
**Evaluated by:** ___________________________  
**Execution Date:** ___________________________  
**Overall Result:** ☐ APPROVED  ☐ REJECTED  ☐ BLOCKED  

---

## Environment Prerequisites

> Complete before executing any test step.

1. **Instancia Odoo Activa:** Módulo de Inventario Farmacéutico Caryvil ERP activo.
2. **Catálogo Farmacéutico:** Medicamentos configurados con categorías, lotes, fechas de vencimiento y UoM.
3. **Rol Autorizado:** Usuario Encargado de Almacén / Inventario Farmacéutico.

---

## Test Flow 1: Baja exitosa de lote de medicamentos caducados

> Maps to: **Scenario 1 (AC-1)** de SPEC-7.3.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Baja exitosa de lote de medicamentos caducados**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Baja exitosa de lote de medicamentos caducados]:** El encargado registra el desecho seleccionando causa "Medicamento Caducado / Vencido", el lote correspondiente y valida la operación. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El sistema descuenta las 8 unidades del inventario vendible, las transfiere a la ubicación de desecho y calcula el valor de la pérdida económica ($). Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Baja exitosa de lote de medicamentos caducados** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Bloqueo de baja sin selección de lote

> Maps to: **Scenario 2 (AC-2)** de SPEC-7.3.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Bloqueo de baja sin selección de lote**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Bloqueo de baja sin selección de lote]:** Se intenta procesar la baja dejando el campo de lote vacío. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Odoo bloquea la acción arrojando un error de validación que exige la selección del lote a descartar. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Bloqueo de baja sin selección de lote** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Registro del usuario que autorizó la baja

> Maps to: **Scenario 3 (AC-3)** de SPEC-7.3.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Registro del usuario que autorizó la baja**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Registro del usuario que autorizó la baja]:** Se consulta el registro de desecho. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El campo authorizedbyid debe registrar de forma inmutable el nombre del usuario y la fecha/hora de autorización. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Registro del usuario que autorizó la baja** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Modelo stock.scrap extendido con causas farmacéuticas y cálculo de costo con conversión de UdM. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Modelo stock.scrap extendido con causas farmacéuticas y cálculo de costo con conversión de UdM.' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Obligatoriedad de asignación de lote validada para productos con trazabilidad. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Obligatoriedad de asignación de lote validada para productos con trazabilidad.' se encuentre activo y operando según la especificación. | ☐ |
| 3 | Restricción de existencia física disponible validada contra el inventario del lote. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Restricción de existencia física disponible validada contra el inventario del lote.' se encuentre activo y operando según la especificación. | ☐ |
| 4 | Bloqueo transaccional contra bypass de autorización en llamadas directas a doscrap(). | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Bloqueo transaccional contra bypass de autorización en llamadas directas a doscrap().' se encuentre activo y operando según la especificación. | ☐ |
| 5 | Ubicación virtual de desecho configurada e integrada en el flujo operativo. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Ubicación virtual de desecho configurada e integrada en el flujo operativo.' se encuentre activo y operando según la especificación. | ☐ |
| 6 | Registro inmutable del usuario autorizador y fecha/hora de autorización. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Registro inmutable del usuario autorizador y fecha/hora de autorización.' se encuentre activo y operando según la especificación. | ☐ |
| 7 | Emisión del Acta de Merma y Destrucción Farmacéutica en formato PDF. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Emisión del Acta de Merma y Destrucción Farmacéutica en formato PDF.' se encuentre activo y operando según la especificación. | ☐ |
| 8 | Pruebas unitarias ampliadas y aprobadas al 100% (8/8 tests). | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Pruebas unitarias ampliadas y aprobadas al 100% (8/8 tests).' haya finalizado con resultado exitoso. | ☐ |
| 9 | Flujo de verificación manual incorporado en el guion de pruebas manuales. | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Flujo de verificación manual incorporado en el guion de pruebas manuales.' haya finalizado con resultado exitoso. | ☐ |

---

## Session Final Results

| Field | Value |
| :--- | :--- |
| Total flows executed | 3 |
| Flows passed | 3 |
| Flows failed | 0 |
| Flows blocked | 0 |
| AC coverage | 3 / 3 |
| DoD items verified | 9 / 9 |

**Verdict:** ☐ APPROVED — All ACs and DoD items covered with no blocking defects.  
            ☐ REJECTED — Defect(s) found. See notes per flow.  
            ☐ BLOCKED — Prerequisite not available. Reschedule session.  

**Defects found:**  
> None.
