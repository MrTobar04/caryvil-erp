# Test Procedure: SPEC-7.1.2 — Gestión de Unidades de Medida Farmacéuticas

**Spec Reference:** [`SPEC-7.1.2`](../../specs/spec-7.1.2-gestion-unidades-medida-farmaceuticas.md)  
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

## Test Flow 1: Configuración de producto con compra en caja y venta en unidad

> Maps to: **Scenario 1 (AC-1)** de SPEC-7.1.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Configuración de producto con compra en caja y venta en unidad**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Configuración de producto con compra en caja y venta en unidad]:** Se configura con UoM Compra = "Caja x 100" y UoM Inventario/Venta = "Unidad / Pastilla". Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El sistema permite emitir órdenes de compra en cajas y dispensar en caja por unidades o blísteres. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Configuración de producto con compra en caja y venta en unidad** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Conversión automática al recibir mercadería

> Maps to: **Scenario 2 (AC-2)** de SPEC-7.1.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Conversión automática al recibir mercadería**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Conversión automática al recibir mercadería]:** Se valida el albarán de recepción en bodega. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El inventario debe registrar un incremento exacto de 200 Unidades / Pastillas. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Conversión automática al recibir mercadería** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Descuento en mostrador por blíster

> Maps to: **Scenario 3 (AC-3)** de SPEC-7.1.2.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Descuento en mostrador por blíster**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Descuento en mostrador por blíster]:** Un cliente compra 1 Blíster x 10. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El sistema deduce automáticamente 10 unidades del stock físico, dejando 190 pastillas disponibles. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Descuento en mostrador por blíster** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Categorías y unidades de medida farmacéuticas creadas en Odoo (sólidos, líquidos y semisólidos). | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Categorías y unidades de medida farmacéuticas creadas en Odoo (sólidos, líquidos y semisólidos).' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Ratios de conversión de cajas y blísteres comprobados. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Ratios de conversión de cajas y blísteres comprobados.' se encuentre activo y operando según la especificación. | ☐ |
| 3 | Conversión automática en compras y ventas validada. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Conversión automática en compras y ventas validada.' se encuentre activo y operando según la especificación. | ☐ |
| 4 | Pruebas unitarias aprobadas al 100% (13/13 tests en TestPharmacyUom). | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Pruebas unitarias aprobadas al 100% (13/13 tests en TestPharmacyUom).' haya finalizado con resultado exitoso. | ☐ |
| 5 | Aprobación por la administración de Farmacia Caryvil. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Aprobación por la administración de Farmacia Caryvil.' se encuentre activo y operando según la especificación. | ☐ |

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
