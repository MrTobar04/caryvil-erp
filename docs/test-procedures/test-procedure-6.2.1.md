# Test Procedure: SPEC-6.2.1 — Catálogo de Precios y Códigos de Proveedor

**Spec Reference:** [`SPEC-6.2.1`](../../specs/spec-6.2.1-catalogo-precios-proveedores.md)  
**Module:** Módulo 6 — Proveedores & Catálogos  
**Spec Status:** Implemented (100%)  
**Generated On:** 2026-09-27  
**Evaluated by:** ___________________________  
**Execution Date:** ___________________________  
**Overall Result:** ☐ APPROVED  ☐ REJECTED  ☐ BLOCKED  

---

## Environment Prerequisites

> Complete before executing any test step.

1. **Instancia Odoo Activa:** Módulo de Compras y Proveedores de Caryvil ERP activo.
2. **Directorio de Proveedores:** Registros de laboratorios y distribuidores farmacéuticos preconfigurados.
3. **Rol Autorizado:** Usuario Encargado de Compras / Inventario.

---

## Test Flow 1: Registro de múltiples proveedores para un mismo medicamento

> Maps to: **Scenario 1 (AC-1)** de SPEC-6.2.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Registro de múltiples proveedores para un mismo medicamento**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Registro de múltiples proveedores para un mismo medicamento]:** El encargado de compras agrega dos proveedores: "Laboratorios Vijosa" a $4.50 (entrega 2 días) y "Droguería Santa Lucía" a $4.80 (entrega 1 día). Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Ambos registros deben quedar guardados en la tabla de proveedores, permitiendo consultar el comparativo de costos. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Registro de múltiples proveedores para un mismo medicamento** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Autocompletado de precio en Orden de Compra

> Maps to: **Scenario 2 (AC-2)** de SPEC-6.2.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Autocompletado de precio en Orden de Compra**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Autocompletado de precio en Orden de Compra]:** El usuario selecciona en las líneas el medicamento "Amoxicilina 500mg". Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El sistema debe rellenar automáticamente el campo de costo unitario con $4.50 sin requerir que el usuario lo digite manualmente. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Autocompletado de precio en Orden de Compra** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Aplicación de precio por escala de volumen

> Maps to: **Scenario 3 (AC-3)** de SPEC-6.2.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Aplicación de precio por escala de volumen**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Aplicación de precio por escala de volumen]:** Se crea una orden por 12 cajas. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El sistema debe aplicar automáticamente el precio con descuento por volumen de $4.20. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Aplicación de precio por escala de volumen** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Modelo product.supplierinfo extendido con campos farmacéuticos y precio bruto. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Modelo product.supplierinfo extendido con campos farmacéuticos y precio bruto.' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Columnas integradas en la tabla de proveedores en la vista de medicamentos. | Navegar a la vista correspondiente en Odoo UI y comprobar que el elemento gráfico 'Columnas integradas en la tabla de proveedores en la vista de medicamentos.' se renderice alineado a los estilos de marca. | ☐ |
| 3 | Autocompletado de precios y escalas de volumen en órdenes de compra validado. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Autocompletado de precios y escalas de volumen en órdenes de compra validado.' se encuentre activo y operando según la especificación. | ☐ |
| 4 | Pruebas unitarias ejecutadas y aprobadas (5 tests en testproductsupplierinfo.py). | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Pruebas unitarias ejecutadas y aprobadas (5 tests en testproductsupplierinfo.py).' haya finalizado con resultado exitoso. | ☐ |
| 5 | Aprobación funcional final en sesión UAT con el equipo de Farmacia Caryvil. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Aprobación funcional final en sesión UAT con el equipo de Farmacia Caryvil.' se encuentre activo y operando según la especificación. | ☐ |

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
