# SPEC-8.2.2: Actualización Automática de Stock en Compras

## 1. Objective
Automatizar la actualización transaccional e instantánea de las existencias físicas y el saldo por lotes en el módulo de Inventario tras la validación satisfactoria de la recepción de mercadería (`stock.picking` en estado `done`) para Farmacia Caryvil. Esta especificación garantiza que al confirmar el ingreso de medicamentos procedentes de proveedores, las cantidades se sumen automáticamente a la ubicación física de almacenamiento (bodega/mostrador), queden inmediatamente disponibles para la venta al público y actualicen el estado de la Orden de Compra asociada sin requerir procesos manuales adicionales.

## 2. Scope
### 2.1. Included
* Ejecución transaccional atómica de movimientos de stock (`stock.move` y `stock.move.line`):
  * Origen: `Ubicación de Proveedores` (`location_id`).
  * Destino: `Ubicación Interna de Farmacia Caryvil` (`location_dest_id` - e.g., `WH/Existencias`).
* Incremento inmediato de la cantidad física a mano (`qty_available`) y cantidad disponible libre de reservas (`free_qty`) en `product.product`.
* Incremento exacto del balance de unidades (`product_qty`) en el registro del lote correspondiente (`stock.production.lot`).
* Actualización reactiva del campo "Cantidad Recibida" (`qty_received`) en las líneas de la Orden de Compra original (`purchase.order.line`).
* Transición automática del estado de la Orden de Compra a `done` (Bloqueada / Completada) cuando la totalidad de los ítems ordenados hayan sido recibidos.
* Reevaluación automática de los niveles del Dashboard de Inicio para eliminar al producto de la lista de Alertas de Stock Crítico (`SPEC-4.2.1`).

### 2.2. Not Included (Out of Scope)
* Generación o registro de la factura de proveedor (se procesa mediante el flujo contable estándar de Odoo).
* Manejo de remanentes o entregas parciales no recibidas (cubierto en `SPEC-8.2.3`).

## 3. Context and Restrictions
* **Context:** Resuelve la desconexión histórica documentada en la entrevista diagnóstica, donde la llegada física de medicamentos tardaba horas o días en reflejarse en los registros manuales de Excel, impidiendo vender productos recién ingresados.
* **Restrictions:**
  * La actualización debe ser completamente atómica: Si ocurre un error durante el movimiento, la transacción debe revertirse (*rollback*) para evitar inconsistencias en la base de datos PostgreSQL.
  * Los medicamentos ingresados deben estar disponibles para venta en mostrador en menos de 1 segundo tras presionar "Validar".

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-7.2.1` (Control de Stock, Lotes y Vencimientos).
  * `SPEC-8.1.1` (Gestión de Órdenes de Compra).
  * `SPEC-8.2.1` (Recepción de Mercadería y Registro de Lotes).
* **Definition of Ready (DoR):**
  * [x] Albarán de recepción con lotes y cantidades capturados.
  * [x] Ubicaciones de almacén configuradas en Odoo.

## 5. Design (Implementation Details)
* **Integration Lifecycle:**
  ```
  [Proveedor Entrega Mercadería]
                │
                ▼
  [Recepción Validada en Odoo (stock.picking -> done)]
                │
         ┌──────┴─────────────────────────────────────────┐
         ▼                                                ▼
  [Actualización de Stock]                       [Actualización de Compra]
  - Incremento en stock.quant                    - qty_received += qty_done
  - Balance del Lote (stock.production.lot)      - PO pasa a estado 'done'
  - Disponibilidad inmediata en Ventas/Caja      - Actualización de Dashboard
  ```
* **Hook en `stock.picking`:**
  * Al ejecutarse `button_validate()`, Odoo procesa los `stock.move` y ejecuta los hooks de post-validación que actualizan el `qty_received` en la orden de compra enlazada (`purchase_id`).

## 6. Acceptance Criteria
* **Scenario 1: Incremento inmediato de existencias tras validar recepción**
  * **Given** El medicamento "Loratadina 10mg" con stock actual de 5 cajas.
  * **When** Se valida la recepción de una orden de compra por 20 cajas (Lote #LOR-2027).
  * **Then** El stock total del medicamento debe reflejar inmediatamente `25 cajas` y el lote #LOR-2027 debe mostrar `20 cajas` disponibles.
* **Scenario 2: Disponibilidad inmediata en el formulario de ventas**
  * **Given** Un albarán de recepción validado hace 5 segundos.
  * **When** Un cajero consulta la disponibilidad del medicamento en mostrador.
  * **Then** El sistema permite seleccionar el medicamento y el nuevo lote sin ningún tipo de retardo o bloqueo.
* **Scenario 3: Actualización de estado en la Orden de Compra**
  * **Given** Una Orden de Compra por 50 unidades de analgésicos.
  * **When** Se valida la recepción completa de las 50 unidades.
  * **Then** Las líneas de la orden deben mostrar `Cantidad Recibida = 50` y el estado de facturación/recepción pasa a estado completado.

## 7. Verification Plan
* **Automated Tests:**
  * Test unitario en Python ejecutando el flujo completo: Crear PO ➔ Confirmar PO ➔ Procesar albarán de entrada con lote ➔ Validar que `product.qty_available` aumente en la cantidad exacta recibida y que el lote contenga el balance asignado.
* **Manual Verification:**
  * Simular la recepción en Odoo y verificar que la vista de inventario en mostrador muestre el nuevo saldo al instante.

## 8. Security and Privacy
* Los movimientos de inventario generan una bitácora auditada inmutable en `stock.move` con el ID del usuario que validó la operación.

## 9. Risks and Mitigation
* **Risk:** Bloqueos de base de datos (*deadlocks*) por transacciones concurrentes de venta y recepción sobre el mismo producto.
  * **Mitigation:** Uso del gestor de bloqueo por fila (*row-level locking*) nativo del ORM de Odoo (`SELECT FOR UPDATE` en `stock.quant`).

## 10. Deliverables & Config as Code
* Lógica de actualización e integración en `custom_addons/caryvil_erp/models/stock_picking_reception.py`.
* Métodos de sincronización con órdenes de compra.

## 11. Definition of Done (DoD)
* [x] Actualización automática de existencias y lotes probada y validada — **comportamiento nativo de Odoo** (`purchase_stock`), no requirió código adicional.
* [x] Sincronización con el campo `qty_received` en Órdenes de Compra verificada — nativo de Odoo (`purchase_order_line._compute_qty_received`).
* [x] Transición a estado `done` en compras confirmada — implementado en `_caryvil_lock_fully_received_purchase_orders()` (`stock_picking_reception.py`), se dispara al validar el albarán cuando todas las líneas de la orden ya están completamente recibidas.
* [x] Pruebas unitarias automatizadas aprobadas al 100% (`tests/test_stock_picking_reception.py`).
* [ ] Validación de flujo integral con el equipo de Farmacia Caryvil.
* **NOTA:** "Reevaluación del Dashboard de Inicio / Alertas de Stock Crítico (`SPEC-4.2.1`)" del alcance original **no aplica todavía** — ese dashboard no está construido en el proyecto. Se retoma cuando `SPEC-4.2.1` exista.
