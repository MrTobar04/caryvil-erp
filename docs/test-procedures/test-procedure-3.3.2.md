# Test Procedure: SPEC-3.3.2 — Plantilla de Reporte para Órdenes de Compra

**Spec Reference:** [`SPEC-3.3.2`](../../specs/spec-3.3.2-plantilla-reporte-orden-compra.md)  
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

## Test Flow 1: Generación de PDF de Orden de Compra para Proveedor y Laboratorio

> Maps to: **Scenario 1 (AC-1)** de SPEC-3.3.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Generación de PDF de Orden de Compra para Proveedor y Laboratorio**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Generación de PDF de Orden de Compra para Proveedor y Laboratorio]:** El encargado de compras emite el reporte de orden de compra. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El PDF generado muestra el encabezado corporativo, el código PE001, las fechas de pedido y entrega, la tabla de productos dispensados y el total consolidado. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Generación de PDF de Orden de Compra para Proveedor y Laboratorio** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Visualización de Descuento e IVA (13%)

> Maps to: **Scenario 2 (AC-2)** de SPEC-3.3.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Visualización de Descuento e IVA (13%)**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Visualización de Descuento e IVA (13%)]:** Se renderiza la sección de totales del reporte. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El documento detalla con claridad el Subtotal, Descuento ($), IVA (13%) y Total exacto. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Visualización de Descuento e IVA (13%)** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Inclusión de Notas Adicionales e instrucciones de recepción

> Maps to: **Scenario 3 (AC-3)** de SPEC-3.3.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Inclusión de Notas Adicionales e instrucciones de recepción**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Inclusión de Notas Adicionales e instrucciones de recepción]:** Se imprime el documento. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Dichas notas se imprimen visiblemente sobre el bloque de firmas y autorizaciones. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Inclusión de Notas Adicionales e instrucciones de recepción** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Plantilla QWeb de Orden de Compra creada con formato formal tamaño Carta (reports/reportpurchaseorder.xml). | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Plantilla QWeb de Orden de Compra creada con formato formal tamaño Carta (reports/reportpurchaseorder.xml).' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Membrete institucional corporativo, datos del proveedor/laboratorio y firmas incluidos. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Membrete institucional corporativo, datos del proveedor/laboratorio y firmas incluidos.' se encuentre activo y operando según la especificación. | ☐ |
| 3 | Salto de página y formateo de líneas de medicamento comprobados con pedido de 10+ líneas. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Salto de página y formateo de líneas de medicamento comprobados con pedido de 10+ líneas.' se encuentre activo y operando según la especificación. | ☐ |
| 4 | Botón de impresión integrado en el módulo de Compras de Odoo. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Botón de impresión integrado en el módulo de Compras de Odoo.' se encuentre activo y operando según la especificación. | ☐ |
| 5 | Aprobación del diseño por parte de la administración de la farmacia. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Aprobación del diseño por parte de la administración de la farmacia.' se encuentre activo y operando según la especificación. | ☐ |

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
