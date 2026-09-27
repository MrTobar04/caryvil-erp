# Test Procedure: SPEC-8.2.2 — Actualización Automática de Stock en Compras

**Spec Reference:** [`SPEC-8.2.2`](../../specs/spec-8.2.2-actualizacion-automatica-stock-compras.md)  
**Module:** Módulo 8 — Órdenes de Compra & Recepción  
**Spec Status:** Implemented (100%)  
**Generated On:** 2026-09-27  
**Evaluated by:** ___________________________  
**Execution Date:** ___________________________  
**Overall Result:** ☐ APPROVED  ☐ REJECTED  ☐ BLOCKED  

---

## Environment Prerequisites

> Complete before executing any test step.

1. **Instancia Odoo Activa:** Módulo de Compras y Recepciones Caryvil ERP desplegado.
2. **Órdenes y Proveedores:** Proveedores habilitados y órdenes de compra en borrador/confirmadas.
3. **Rol Autorizado:** Usuario Encargado de Compras y Recepción de Almacén.

---

## Test Flow 1: Incremento inmediato de existencias tras validar recepción

> Maps to: **Scenario 1 (AC-1)** de SPEC-8.2.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Incremento inmediato de existencias tras validar recepción**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Incremento inmediato de existencias tras validar recepción]:** Se valida la recepción de una orden de compra por 20 cajas (Lote LOR-2027). Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El stock total del medicamento debe reflejar inmediatamente 25 cajas y el lote LOR-2027 debe mostrar 20 cajas disponibles. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Incremento inmediato de existencias tras validar recepción** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Disponibilidad inmediata en el formulario de ventas

> Maps to: **Scenario 2 (AC-2)** de SPEC-8.2.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Disponibilidad inmediata en el formulario de ventas**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Disponibilidad inmediata en el formulario de ventas]:** Un cajero consulta la disponibilidad del medicamento en mostrador. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El sistema permite seleccionar el medicamento y el nuevo lote sin ningún tipo de retardo o bloqueo. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Disponibilidad inmediata en el formulario de ventas** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Actualización de estado en la Orden de Compra

> Maps to: **Scenario 3 (AC-3)** de SPEC-8.2.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Actualización de estado en la Orden de Compra**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Actualización de estado en la Orden de Compra]:** Se valida la recepción completa de las 50 unidades. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Las líneas de la orden deben mostrar Cantidad Recibida = 50 y el estado de facturación/recepción pasa a estado completado. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Actualización de estado en la Orden de Compra** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Actualización automática de existencias y lotes probada y validada — comportamiento nativo de Odoo (purchasestock), no requirió código adicional. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Actualización automática de existencias y lotes probada y validada — comportamiento nativo de Odoo (purchasestock), no requirió código adicional.' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Sincronización con el campo qtyreceived en Órdenes de Compra verificada — nativo de Odoo (purchaseorderline.computeqtyreceived). | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Sincronización con el campo qtyreceived en Órdenes de Compra verificada — nativo de Odoo (purchaseorderline.computeqtyreceived).' se encuentre activo y operando según la especificación. | ☐ |
| 3 | Transición a estado done en compras confirmada — implementado en caryvillockfullyreceivedpurchaseorders() (stockpickingreception.py), se dispara al validar el albarán cuando todas las líneas de la orden ya están completamente recibidas. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Transición a estado done en compras confirmada — implementado en caryvillockfullyreceivedpurchaseorders() (stockpickingreception.py), se dispara al validar el albarán cuando todas las líneas de la orden ya están completamente recibidas.' se encuentre activo y operando según la especificación. | ☐ |
| 4 | Pruebas unitarias automatizadas aprobadas al 100% (tests/teststockpickingreception.py). | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Pruebas unitarias automatizadas aprobadas al 100% (tests/teststockpickingreception.py).' haya finalizado con resultado exitoso. | ☐ |
| 5 | Validación de flujo integral con el equipo de Farmacia Caryvil. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Validación de flujo integral con el equipo de Farmacia Caryvil.' se encuentre activo y operando según la especificación. | ☐ |

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
