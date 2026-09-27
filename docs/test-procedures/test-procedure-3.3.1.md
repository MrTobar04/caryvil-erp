# Test Procedure: SPEC-3.3.1 — Plantilla de Reporte para Factura Simple y Ticket

**Spec Reference:** [`SPEC-3.3.1`](../../specs/spec-3.3.1-plantilla-reporte-factura-ticket.md)  
**Module:** Módulo 3 — Branding UI/UX & Plantillas de Reportes  
**Spec Status:** Implemented (100%)  
**Generated On:** 2026-09-27  
**Evaluated by:** ___________________________  
**Execution Date:** ___________________________  
**Overall Result:** ☐ APPROVED  ☐ REJECTED  ☐ BLOCKED  

---

## Environment Prerequisites

> Complete before executing any test step.

1. **Instancia Odoo Activa:** Odoo 17 con tema visual y branding de Farmacia Caryvil aplicado.
2. **Plantillas e Impresora/PDF:** Generador de reportes PDF habilitado y visor PDF integrado en navegador.
3. **Usuarios de Prueba:** Usuario Administrador y Usuario Cajero/Vendedor.

---

## Test Flow 1: Emisión de ticket de venta con desglose completo de pago

> Maps to: **Scenario 1 (AC-1)** de SPEC-3.3.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Emisión de ticket de venta con desglose completo de pago**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Emisión de ticket de venta con desglose completo de pago]:** Se pulsa el botón "Imprimir Ticket". Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El ticket generado debe detallar los medicamentos (Ibuprofeno 600mg, Virogrip AM GelCaps), SubTotal: $2.10, Total: $2.10, Monto Recibido: $3.00, Cambio: $0.90 y el texto en letras "DOS DÓLARES CON 10/100 USD". Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Emisión de ticket de venta con desglose completo de pago** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Emisión a Consumidor Final sin cliente registrado

> Maps to: **Scenario 2 (AC-2)** de SPEC-3.3.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Emisión a Consumidor Final sin cliente registrado**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Emisión a Consumidor Final sin cliente registrado]:** Se imprime el comprobante. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El comprobante muestra "Cliente: Consumidor Final" y DUI: "N/A" sin errores. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Emisión a Consumidor Final sin cliente registrado** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Desglose de Descuentos e IVA (13%)

> Maps to: **Scenario 3 (AC-3)** de SPEC-3.3.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Desglose de Descuentos e IVA (13%)**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Desglose de Descuentos e IVA (13%)]:** Se genera el reporte. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El ticket desglosa explícitamente el porcentaje de descuento, el monto descontado y el IVA retenido/calculado correctamente. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Desglose de Descuentos e IVA (13%)** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Plantilla QWeb creada con el formato térmico y adaptable. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Plantilla QWeb creada con el formato térmico y adaptable.' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Parámetros de liquidación financiera (Monto Recibido, Cambio, Saldo Pendiente) integrados. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Parámetros de liquidación financiera (Monto Recibido, Cambio, Saldo Pendiente) integrados.' se encuentre activo y operando según la especificación. | ☐ |
| 3 | Conversión de importe a letras en español validada. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Conversión de importe a letras en español validada.' se encuentre activo y operando según la especificación. | ☐ |
| 4 | Verificación de fidelidad gráfica con los mockups de venta completada. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Verificación de fidelidad gráfica con los mockups de venta completada.' se encuentre activo y operando según la especificación. | ☐ |

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
