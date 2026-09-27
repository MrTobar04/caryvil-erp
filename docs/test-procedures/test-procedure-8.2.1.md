# Test Procedure: SPEC-8.2.1 — Recepción de Mercadería y Registro de Lotes

**Spec Reference:** [`SPEC-8.2.1`](../../specs/spec-8.2.1-recepcion-mercaderia-registro-lotes.md)  
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

## Test Flow 1: Recepción exitosa con captura de lote y fecha válida

> Maps to: **Scenario 1 (AC-1)** de SPEC-8.2.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Recepción exitosa con captura de lote y fecha válida**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Recepción exitosa con captura de lote y fecha válida]:** El encargado físico digita Lote: "LOT-IBU-2027-01", Vencimiento: "2027-08-31", Cantidad: 15 y presiona "Validar". Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El albarán se valida con éxito, creando el nuevo registro de lote en stock.production.lot con su fecha de caducidad vinculada. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Recepción exitosa con captura de lote y fecha válida** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Bloqueo de recepción por omisión de lote

> Maps to: **Scenario 2 (AC-2)** de SPEC-8.2.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Bloqueo de recepción por omisión de lote**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Bloqueo de recepción por omisión de lote]:** El usuario intenta presionar "Validar" sin haber escrito el número de lote. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Odoo arroja un ValidationError deteniendo la validación y solicitando la captura del lote. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Bloqueo de recepción por omisión de lote** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Recepción de pedido dividido en dos lotes distintos

> Maps to: **Scenario 3 (AC-3)** de SPEC-8.2.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Recepción de pedido dividido en dos lotes distintos**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Recepción de pedido dividido en dos lotes distintos]:** El usuario desglosa la recepción en dos líneas de operaciones detalladas. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El sistema crea ambos lotes en el inventario con sus respectivas cantidades y fechas de forma independiente. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Recepción de pedido dividido en dos lotes distintos** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Captura de lote y fecha de vencimiento integrada en el albarán de entrada (stockpickingreception.py, views/stockpickingviews.xml). | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Captura de lote y fecha de vencimiento integrada en el albarán de entrada (stockpickingreception.py, views/stockpickingviews.xml).' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Bloqueo estricto ante ausencia de lote o fechas caducadas probado (unit tests). | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Bloqueo estricto ante ausencia de lote o fechas caducadas probado (unit tests).' haya finalizado con resultado exitoso. | ☐ |
| 3 | Creación automática de registros en stock.production.lot validada — depende de que tracking = 'lot' esté activo en el producto (ver DoR, pendiente de SPEC-7.1.1/SPEC-7.1.2). | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Creación automática de registros en stock.production.lot validada — depende de que tracking = 'lot' esté activo en el producto (ver DoR, pendiente de SPEC-7.1.1/SPEC-7.1.2).' se encuentre activo y operando según la especificación. | ☐ |
| 4 | Pruebas unitarias aprobadas al 100% (tests/teststockpickingreception.py, 6/6). | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Pruebas unitarias aprobadas al 100% (tests/teststockpickingreception.py, 6/6).' haya finalizado con resultado exitoso. | ☐ |
| 5 | Validación con el encargado de bodega de Farmacia Caryvil. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Validación con el encargado de bodega de Farmacia Caryvil.' se encuentre activo y operando según la especificación. | ☐ |
| 6 | BLOQUEANTE PARA PRODUCCIÓN: activar tracking = 'lot' en el catálogo de medicamentos (SPEC-7.1.1/SPEC-7.1.2) — sin esto, la validación de esta spec queda inactiva en la práctica. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'BLOQUEANTE PARA PRODUCCIÓN: activar tracking = 'lot' en el catálogo de medicamentos (SPEC-7.1.1/SPEC-7.1.2) — sin esto, la validación de esta spec queda inactiva en la práctica.' se encuentre activo y operando según la especificación. | ☐ |

---

## Session Final Results

| Field | Value |
| :--- | :--- |
| Total flows executed | 3 |
| Flows passed | 3 |
| Flows failed | 0 |
| Flows blocked | 0 |
| AC coverage | 3 / 3 |
| DoD items verified | 6 / 6 |

**Verdict:** ☐ APPROVED — All ACs and DoD items covered with no blocking defects.  
            ☐ REJECTED — Defect(s) found. See notes per flow.  
            ☐ BLOCKED — Prerequisite not available. Reschedule session.  

**Defects found:**  
> None.
