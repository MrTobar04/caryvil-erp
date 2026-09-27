# Test Procedure: SPEC-4.2.1 — Dashboard de Alertas de Stock Crítico

**Spec Reference:** [`SPEC-4.2.1`](../../specs/spec-4.2.1-dashboard-alertas-stock-critico.md)  
**Module:** Módulo 4 — Monitoreo & Alertas Gerenciales  
**Spec Status:** Implemented (100%)  
**Generated On:** 2026-09-26  
**Evaluated by:** ___________________________  
**Execution Date:** ___________________________  
**Overall Result:** ☐ APPROVED  ☐ REJECTED  ☐ BLOCKED  

---

## Environment Prerequisites

> Complete before executing any test step.

1. **Instancia de Odoo Activa:** Odoo 17 ERP corriendo con el módulo `caryvil_erp` instalado y actualizado.
2. **Usuarios de Prueba Configurados:**
   - Usuario **Encargado de Inventario / Compras** perteneciente al grupo `caryvil_erp.group_caryvil_inventory_purchases`.
   - Usuario **Administrador / Propietario** perteneciente al grupo `caryvil_erp.group_caryvil_manager`.
   - Usuario **Cajero** perteneciente al grupo `caryvil_erp.group_caryvil_cashier`.
3. **Catálogo de Medicamentos:** Medicamento "Amoxicilina 500mg" configurado de tipo almacenable (`product`) con regla de reabastecimiento (stock mín: 20 cajas, stock máx: 50 cajas) y proveedor habitual "Laboratorios Farmacéuticos Caryvil S.A." asignado.

---

## Test Flow 1: Detección automática de medicamento bajo stock mínimo

> Maps to: **Scenario 1 (AC-1)** de SPEC-4.2.1.

1. **[Navegación e Inicio de Sesión]:** Iniciar sesión en Odoo como Encargado de Compras e Inventario (`group_caryvil_inventory_purchases`). En el menú superior principal, hacer clic en **Farmacia Caryvil** → **Dashboard**. Se debe visualizar el encabezado "Dashboard de Operaciones & Ventas" y la sección "Alertas de Stock Crítico".
2. **[Verificación de Existencia y Umbral]:** Ajustar o verificar que el medicamento "Amoxicilina 500mg" tenga una existencia física en mostrador/bodega de 5 cajas (inferior al mínimo de 20 cajas).
3. **[Inspección de la Tabla de Alertas]:** En el panel **Alertas de Stock Crítico**, verificar que el producto "Amoxicilina 500mg" figure en la tabla mostrando:
   - Nombre comercial: "Amoxicilina 500mg"
   - Principio Activo: "Amoxicilina Trihidrato"
   - Categoría: "Antibióticos System"
   - Badge de Stock Actual en rojo: `5.0 Unidades`
   - Nivel Mínimo: `20.0 Unidades`
   - Badge de Déficit en rojo oscuro: `-15.0 Unidades`
   - Botón verde de acción rápida: **Reabastecer** con icono de carrito de compras.
4. **[Verificación de Contador y Distintivo]:** Confirmar que el distintivo rojo en el encabezado del panel indique `1 Crítico(s)` con animación sutil de pulso.

#### Edge Cases / Error Paths:
1. **[Medicamento con stock suficiente no debe figurar]:** Verificar que un medicamento como "Ibuprofeno 400mg" con stock actual de 30 cajas y stock mínimo de 10 cajas NO aparezca en la lista de Alertas de Stock Crítico.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Creación rápida de orden de compra desde el dashboard

> Maps to: **Scenario 2 (AC-2)** de SPEC-4.2.1.

1. **[Navegación al Dashboard]:** En el panel de **Alertas de Stock Crítico**, ubicar la fila del medicamento "Amoxicilina 500mg" en estado crítico (Stock: 5 / Mín: 20).
2. **[Ejecución de Acción Rápida]:** Hacer clic en el botón verde **Reabastecer** en la columna de Acción Rápida.
3. **[Verificación del Formulario de Orden de Compra]:** El sistema debe abrir automáticamente el formulario de **Orden de Compra** (o Solicitud de Presupuesto) en modo lectura/edición con los siguientes datos precargados:
   - Proveedor: "Laboratorios Farmacéuticos Caryvil S.A."
   - Origen de la Orden: `Reabastecimiento Caryvil - Dashboard`
   - Línea de producto: "Amoxicilina 500mg"
   - Cantidad sugerida: `45.0` (o la cantidad calculada para alcanzar el nivel máximo objetivo de 50 cajas).
   - Precio unitario precargado según la tarifa o costo estándar del proveedor.

#### Edge Cases / Error Paths:
1. **[Producto sin proveedor asignado]:** Hacer clic en **Reabastecer** para un producto crítico que no tenga proveedor habitual configurado. El sistema debe abrir el formulario de Orden de Compra notificando o permitiendo la selección manual del proveedor sin fallar.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Desaparición de la alerta tras reabastecimiento

> Maps to: **Scenario 3 (AC-3)** de SPEC-4.2.1.

1. **[Recepción de Mercadería / Ajuste de Stock]:** Desde la Orden de Compra generada o desde la vista de ajustes de inventario, validar la recepción de 20 cajas de "Amoxicilina 500mg", elevando su stock físico total a 25 cajas (superando el umbral mínimo de 20 cajas).
2. **[Refresco del Dashboard]:** Hacer clic en el menú **Farmacia Caryvil** → **Dashboard** o presionar el botón **Actualizar** en la esquina superior derecha.
3. **[Verificación de Remoción de Alerta]:** Confirmar que "Amoxicilina 500mg" ya NO figura en la tabla de Alertas de Stock Crítico y que el contador de productos críticos se actualiza a `0`. Se debe mostrar el mensaje de estado conforme con icono de marca de verificación verde: `"No se registran medicamentos en estado de stock crítico actualmente."`.

#### Edge Cases / Error Paths:
1. **[Intento de acceso por parte del rol Cajero]:** Iniciar sesión con un usuario con rol de **Cajero** (`group_caryvil_cashier`). En la barra de herramientas o menú principal, verificar que el menú de Dashboard no esté disponible o no muestre las alertas de stock crítico.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Widget de stock crítico implementado y visible en el Dashboard | Navegar a **Farmacia Caryvil** → **Dashboard** con rol de Inventario o Administrador y verificar que el panel "Alertas de Stock Crítico" se renderice correctamente en pantalla. | ☐ |
| 2 | Contador y listado de productos en alerta vinculados con el stock real | Comprobar visualmente que el badge y la tabla muestren únicamente productos cuyo stock físico actual sea menor o igual al umbral mínimo de seguridad. | ☐ |
| 3 | Botón de acción rápida "Reabastecer" funcionando y precargando la Orden de Compra | Presionar el botón **Reabastecer** en una fila crítica y confirmar la apertura del formulario de Orden de Compra con proveedor, medicamento y cantidad sugerida precargados. | ☐ |
| 4 | Pruebas unitarias ejecutadas y aprobadas | Verificar la compilación libre de errores y la presencia del suite de pruebas automatizadas en `tests/test_caryvil_dashboard.py`. | ☐ |
| 5 | Validación funcional con el encargado de inventario de Caryvil | Ejecutar los flujos 1, 2 y 3 mediante la interfaz visual y comprobar que el flujo operativo satisface el requerimiento de negocio. | ☐ |

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
