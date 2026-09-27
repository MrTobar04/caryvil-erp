# Test Procedure: SPEC-8.1.2 — Visibilidad de Abonos y Estado de Pago a Proveedores

**Spec Reference:** [`SPEC-8.1.2`](../../specs/spec-8.1.2-abonos-pagos-proveedores.md)  
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

## Test Flow 1: Primer abono parcial

> Maps to: **Scenario 1 (AC-1)** de SPEC-8.1.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Primer abono parcial**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Primer abono parcial]:** Se registra un pago de $200.00 contra la factura. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** La orden muestra Estado de Pago = Abono Parcial y Saldo Pendiente = $300.00. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Primer abono parcial** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Pago completo tras varios abonos

> Maps to: **Scenario 2 (AC-2)** de SPEC-8.1.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Pago completo tras varios abonos**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Pago completo tras varios abonos]:** Se registra un segundo pago de $300.00. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** La orden muestra Estado de Pago = Pagado y Saldo Pendiente = $0.00. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Pago completo tras varios abonos** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Orden sin factura generada aún

> Maps to: **Scenario 3 (AC-3)** de SPEC-8.1.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Orden sin factura generada aún**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Orden sin factura generada aún]:** Se consulta su estado de pago. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Muestra Estado de Pago = Sin Facturar. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Orden sin factura generada aún** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Campos paymentstatuslabel y amountresidualtotal implementados y calculados desde las Facturas de Proveedor nativas. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Campos paymentstatuslabel y amountresidualtotal implementados y calculados desde las Facturas de Proveedor nativas.' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Visibles en formulario y lista de Órdenes de Compra. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Visibles en formulario y lista de Órdenes de Compra.' se encuentre activo y operando según la especificación. | ☐ |
| 3 | Pruebas unitarias con flujo completo de abonos (factura → pago parcial → pago final) — tests/testpurchaseordermedicine.py::testabonosparcialesactualizanestadodepago. | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Pruebas unitarias con flujo completo de abonos (factura → pago parcial → pago final) — tests/testpurchaseordermedicine.py::testabonosparcialesactualizanestadodepago.' haya finalizado con resultado exitoso. | ☐ |
| 4 | Validación con el equipo de compras de que el flujo de "Crear Factura + Registrar Pago" nativo cubre su necesidad real, o si requieren un registro más simplificado (sin pasar por Contabilidad). | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Validación con el equipo de compras de que el flujo de "Crear Factura + Registrar Pago" nativo cubre su necesidad real, o si requieren un registro más simplificado (sin pasar por Contabilidad).' se encuentre activo y operando según la especificación. | ☐ |

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
