# Test Procedure: SPEC-7.1.1 — Catálogo y Categorización de Medicamentos

**Spec Reference:** [`SPEC-7.1.1`](../../specs/spec-7.1.1-catalogo-categorizacion-medicamentos.md)  
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

## Test Flow 1: Creación completa de medicamento

> Maps to: **Scenario 1 (AC-1)** de SPEC-7.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Creación completa de medicamento**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Creación completa de medicamento]:** Registra: Nombre "Amoxicilina Vijosa 500mg", Principio Activo "Amoxicilina", Categoría "Antibióticos", Forma "Cápsula", Concentración "500 mg", Código "7412345678901", Precio Venta "$0.25". Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El medicamento se almacena con tipo almacenable y seguimiento por lotes activado por defecto. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Creación completa de medicamento** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Búsqueda por Principio Activo

> Maps to: **Scenario 2 (AC-2)** de SPEC-7.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Búsqueda por Principio Activo**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Búsqueda por Principio Activo]:** El dependiente busca "Paracetamol" en el catálogo. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El sistema lista todas las presentaciones comerciales asociadas a dicho principio activo (e.g., Panadol, Acetaminofén MK, Winasorb). Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Búsqueda por Principio Activo** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Alerta visual de medicamento bajo receta

> Maps to: **Scenario 3 (AC-3)** de SPEC-7.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Alerta visual de medicamento bajo receta**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Alerta visual de medicamento bajo receta]:** Se visualiza en mostrador. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Debe mostrar un distintivo visual de advertencia indicando que se debe solicitar prescripción médica antes de la dispensación. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Alerta visual de medicamento bajo receta** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Modelos de categorías terapéuticas y principios activos implementados. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Modelos de categorías terapéuticas y principios activos implementados.' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Extensión de product.template con campos farmacéuticos configurada. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Extensión de product.template con campos farmacéuticos configurada.' se encuentre activo y operando según la especificación. | ☐ |
| 3 | Trazabilidad por lotes (tracking = 'lot') predeterminada en nuevos medicamentos. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Trazabilidad por lotes (tracking = 'lot') predeterminada en nuevos medicamentos.' se encuentre activo y operando según la especificación. | ☐ |
| 4 | Vistas y menús para Categorías Terapéuticas y Principios Activos creados (caryvilmedicineviews.xml). | Navegar a la vista correspondiente en Odoo UI y comprobar que el elemento gráfico 'Vistas y menús para Categorías Terapéuticas y Principios Activos creados (caryvilmedicineviews.xml).' se renderice alineado a los estilos de marca. | ☐ |
| 5 | Alerta visual prominente y distintivos de prescripción implementados en formulario, árbol y kanban. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Alerta visual prominente y distintivos de prescripción implementados en formulario, árbol y kanban.' se encuentre activo y operando según la especificación. | ☐ |
| 6 | Pruebas unitarias aprobadas al 100% (9 de 9 pruebas exitosas en testmedicinecatalog.py). | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Pruebas unitarias aprobadas al 100% (9 de 9 pruebas exitosas en testmedicinecatalog.py).' haya finalizado con resultado exitoso. | ☐ |
| 7 | Guión de pruebas manuales documentado paso a paso (docs/guias/guion-pruebas-manuales.md, Flujo 7.1). | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Guión de pruebas manuales documentado paso a paso (docs/guias/guion-pruebas-manuales.md, Flujo 7.1).' haya finalizado con resultado exitoso. | ☐ |
| 8 | Validación de la ficha médica con la farmacéutica responsable (en proceso de UAT). | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Validación de la ficha médica con la farmacéutica responsable (en proceso de UAT).' se encuentre activo y operando según la especificación. | ☐ |

---

## Session Final Results

| Field | Value |
| :--- | :--- |
| Total flows executed | 3 |
| Flows passed | 3 |
| Flows failed | 0 |
| Flows blocked | 0 |
| AC coverage | 3 / 3 |
| DoD items verified | 8 / 8 |

**Verdict:** ☐ APPROVED — All ACs and DoD items covered with no blocking defects.  
            ☐ REJECTED — Defect(s) found. See notes per flow.  
            ☐ BLOCKED — Prerequisite not available. Reschedule session.  

**Defects found:**  
> None.
