# Test Procedure: SPEC-7.3.1 — Movimientos y Ajustes de Inventario

**Spec Reference:** [`SPEC-7.3.1`](../../specs/spec-7.3.1-movimientos-ajustes-inventario.md)  
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

## Test Flow 1: Conteo físico coincidente

> Maps to: **Scenario 1 (AC-1)** de SPEC-7.3.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Conteo físico coincidente**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Conteo físico coincidente]:** El encargado realiza el conteo en estantería y registra 50 tabletas. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** La diferencia es 0 y el sistema marca el producto como verificado sin generar movimientos de ajuste. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Conteo físico coincidente** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Conciliación de sobrante con justificación

> Maps to: **Scenario 2 (AC-2)** de SPEC-7.3.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Conciliación de sobrante con justificación**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Conciliación de sobrante con justificación]:** El usuario registra la cantidad contada de 12, selecciona motivo "Conteo Cíclico Periódico" y el administrador valida. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El stock del producto se actualiza a 12 unidades y se registra la bitácora del movimiento. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Conciliación de sobrante con justificación** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Bloqueo de ajuste sin motivo seleccionado

> Maps to: **Scenario 3 (AC-3)** de SPEC-7.3.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Bloqueo de ajuste sin motivo seleccionado**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Bloqueo de ajuste sin motivo seleccionado]:** Se intenta presionar "Aplicar Ajuste" con el campo de motivo vacío. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Odoo bloquea la acción mediante un ValidationError exigiendo la selección de la causa. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Bloqueo de ajuste sin motivo seleccionado** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Modelo stock.quant extendido con campos de justificación de ajuste. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Modelo stock.quant extendido con campos de justificación de ajuste.' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Validación de motivo obligatorio implementada y probada. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Validación de motivo obligatorio implementada y probada.' se encuentre activo y operando según la especificación. | ☐ |
| 3 | Permisos de aprobación restringidos al rol Administrador. | Iniciar sesión con un usuario no privilegiado y verificar visualmente en la interfaz que el acceso a 'Permisos de aprobación restringidos al rol Administrador.' quede restringido o invisible. | ☐ |
| 4 | Pruebas unitarias aprobadas al 100%. | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Pruebas unitarias aprobadas al 100%.' haya finalizado con resultado exitoso. | ☐ |
| 5 | Procedimiento de conteo validado con la propietaria de la farmacia. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Procedimiento de conteo validado con la propietaria de la farmacia.' se encuentre activo y operando según la especificación. | ☐ |

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
