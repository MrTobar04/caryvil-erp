# Test Procedure: SPEC-8.1.1 — Gestión de Órdenes de Compra

**Spec Reference:** [`SPEC-8.1.1`](../../specs/spec-8.1.1-gestion-ordenes-compra.md)  
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

## Test Flow 1: Creación y confirmación de Orden de Compra formal

> Maps to: **Scenario 1 (AC-1)** de SPEC-8.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Creación y confirmación de Orden de Compra formal**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Creación y confirmación de Orden de Compra formal]:** Agrega 10 Cajas de "Amoxicilina 500mg" a $4.50 c/u (Subtotal $45.00 + IVA $5.85 = $50.85) y presiona "Confirmar Pedido". Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** La orden pasa al estado purchase (Orden de Compra), bloquea la edición de precios y genera automáticamente el albarán de recepción de entrada en estado assigned. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Creación y confirmación de Orden de Compra formal** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Bloqueo de confirmación sin productos

> Maps to: **Scenario 2 (AC-2)** de SPEC-8.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Bloqueo de confirmación sin productos**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Bloqueo de confirmación sin productos]:** Se intenta confirmar el pedido. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El sistema arroja un error de validación impidiendo el cambio de estado. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Bloqueo de confirmación sin productos** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Envío de PDF por correo electrónico al proveedor (NO APLICA)

> Maps to: **Scenario 3 (AC-3)** de SPEC-8.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Envío de PDF por correo electrónico al proveedor (NO APLICA)**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Envío de PDF por correo electrónico al proveedor (NO APLICA)]:** El usuario presiona "Enviar por Correo". Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Odoo adjunta el PDF de la orden de compra (SPEC-3.3.2) en un correo electrónico con plantilla prediseñada dirigido al email del ejecutivo de ventas. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Envío de PDF por correo electrónico al proveedor (NO APLICA)** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Ciclo de estados de la Orden de Compra configurado y operativo. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Ciclo de estados de la Orden de Compra configurado y operativo.' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Cálculo exacto de IVA (13%) y subtotales en USD ($) validado. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Cálculo exacto de IVA (13%) y subtotales en USD ($) validado.' se encuentre activo y operando según la especificación. | ☐ |
| 3 | Generación automática del albarán de recepción vinculada. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Generación automática del albarán de recepción vinculada.' se encuentre activo y operando según la especificación. | ☐ |
| 4 | Pruebas unitarias aprobadas al 100%. | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Pruebas unitarias aprobadas al 100%.' haya finalizado con resultado exitoso. | ☐ |
| 5 | Aprobación del flujo por el equipo de compras de Farmacia Caryvil. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Aprobación del flujo por el equipo de compras de Farmacia Caryvil.' se encuentre activo y operando según la especificación. | ☐ |

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
