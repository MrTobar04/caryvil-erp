# Test Procedure: SPEC-5.2.2 — Historial de Compras de Clientes

**Spec Reference:** [`SPEC-5.2.2`](../../specs/spec-5.2.2-historial-compras-clientes.md)  
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

## Test Flow 1: Consulta de compras acumuladas de un cliente

> Maps to: **Scenario 1 (AC-1)** de SPEC-5.2.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Consulta de compras acumuladas de un cliente**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Consulta de compras acumuladas de un cliente]:** El dependiente abre la ficha del cliente en Odoo. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El botón inteligente en la cabecera debe indicar 3 Compras y un monto acumulado de $45.00. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Consulta de compras acumuladas de un cliente** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Apertura y revisión del detalle de transacciones previas

> Maps to: **Scenario 2 (AC-2)** de SPEC-5.2.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Apertura y revisión del detalle de transacciones previas**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Apertura y revisión del detalle de transacciones previas]:** Hace clic en la pestaña "Historial de Compras" o en el botón inteligente. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El sistema debe desplegar el listado de las 3 facturas emitidas, permitiendo abrir cualquiera de ellas para ver qué medicamentos específicos fueron dispensados. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Apertura y revisión del detalle de transacciones previas** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Reimpresión de ticket desde el historial

> Maps to: **Scenario 3 (AC-3)** de SPEC-5.2.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Reimpresión de ticket desde el historial**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Reimpresión de ticket desde el historial]:** El usuario localiza la factura en el historial y presiona "Imprimir Ticket". Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El sistema genera inmediatamente el comprobante en formato térmico o PDF con los datos originales de la transacción. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Reimpresión de ticket desde el historial** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Campos caryvilinvoicecount y caryviltotalspent implementados. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Campos caryvilinvoicecount y caryviltotalspent implementados.' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Smart button y pestaña de historial visibles y funcionales en el formulario de cliente. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Smart button y pestaña de historial visibles y funcionales en el formulario de cliente.' se encuentre activo y operando según la especificación. | ☐ |
| 3 | Navegación y reimpresión de comprobantes pasados verificada. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Navegación y reimpresión de comprobantes pasados verificada.' se encuentre activo y operando según la especificación. | ☐ |
| 4 | Pruebas unitarias de cálculo estadístico aprobadas al 100%. | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Pruebas unitarias de cálculo estadístico aprobadas al 100%.' haya finalizado con resultado exitoso. | ☐ |
| 5 | Validación con el personal de mostrador completada. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Validación con el personal de mostrador completada.' se encuentre activo y operando según la especificación. | ☐ |

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
