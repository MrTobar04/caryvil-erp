# SPEC-9.3.1: Deducción Automática de Stock en Ventas

## 1. Objective
Sincronizar transaccionalmente el procesamiento de ventas en mostrador con el módulo de Inventario en Odoo (`stock.move` y `stock.quant`), garantizando que al confirmarse cada venta y emitirse la factura simple, el sistema descuente de manera automática, instantánea y atómica las unidades físicas y lotes dispensados desde la ubicación de mostrador hacia la ubicación de clientes, previniendo discrepancias de stock y bloqueando estrictamente saldos negativos de inventario en Farmacia Caryvil.

## 2. Scope
### 2.1. Included
* Automatización del movimiento de salida de inventario (`stock.picking` de tipo `outgoing` / Albarán de Entrega al Cliente):
  * Ubicación Origen: `Ubicación Interna Farmacia / Mostrador` (`location_id`).
  * Ubicación Destino: `Ubicación de Clientes` (`location_dest_id`).
* Validación transaccional atómica: El descuento de stock ocurre en la misma transacción de base de datos que la emisión de la factura simple; si ocurre un fallo, toda la operación se revierte (*rollback*).
* Reducción inmediata de la cantidad a mano (`qty_available`) en `product.product`.
* Descuento exacto del balance de unidades (`product_qty`) en el lote correspondiente (`stock.production.lot`).
* **Bloqueo estricto de saldo negativo:** Validación a nivel de ORM que impide confirmar cualquier venta si el stock físico real disponible en la ubicación de despacho es menor a la cantidad solicitada.
* Actualización inmediata en los widgets del Dashboard de Inicio (`SPEC-4.1.1` y `SPEC-4.2.1`).

### 2.2. Not Included (Out of Scope)
* Lógica algorítmica de selección y priorización de lotes FEFO (cubierto en `SPEC-9.3.2`).
* Devoluciones de medicamentos por parte de clientes (gestionado mediante notas de crédito / recepciones de devolución estándar).

## 3. Context and Restrictions
* **Context:** Soluciona el principal dolor operativo expuesto por la propietaria en la entrevista inicial: las ventas realizadas en farmacia no actualizaban el stock en tiempo real, lo que causaba que el personal creyera que había producto disponible cuando ya se había vendido.
* **Restrictions:**
  * Cero tolerancia a stock negativo en productos farmacéuticos.
  * El tiempo de procesamiento del descuento de inventario debe ser menor a 300ms.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-7.1.1` (Catálogo y Categorización de Medicamentos).
  * `SPEC-7.2.1` (Control de Stock, Lotes y Vencimientos).
  * `SPEC-9.1.1` (Procesamiento de Transacciones de Ventas).
  * `SPEC-9.2.1` (Generación de Factura Simple).
* **Definition of Ready (DoR):**
  * [x] Ubicaciones físicas internas de Farmacia Caryvil configuradas.
  * [x] Tipo de operación de entrega de mostrador parametrizado con validación automática.

## 5. Design (Implementation Details)
* **Stock Deduction Logic (`models/sale_order_medicine.py`):**
  ```python
  from odoo import models, api, _
  from odoo.exceptions import UserError

  class SaleOrderStockDeduction(models.Model):
      _inherit = 'sale.order'

      def _action_confirm(self):
          # Validar existencias físicas reales antes de confirmar
          for order in self:
              for line in order.order_line:
                  product = line.product_id
                  if product.detailed_type == 'product':
                      # Verificar stock físico no reservado
                      if product.qty_available < line.product_uom_qty:
                          raise UserError(_(
                              'No hay existencias suficientes para el medicamento "%s".\n'
                              'Cantidad solicitada: %s %s\n'
                              'Cantidad disponible física: %s %s'
                          ) % (product.name, line.product_uom_qty, product.uom_id.name, product.qty_available, product.uom_id.name))
          
          res = super(SaleOrderStockDeduction, self)._action_confirm()

          # Auto-validar albaranes de salida vinculados inmediatamente
          for order in self:
              for picking in order.picking_ids.filtered(lambda p: p.state not in ('done', 'cancel')):
                  picking.action_assign()
                  for move in picking.move_lines:
                      move.quantity_done = move.product_uom_qty
                  picking.button_validate()

          return res
  ```

## 6. Acceptance Criteria
* **Scenario 1: Descuento instantáneo de stock tras completar venta**
  * **Given** El medicamento "Paracetamol 500mg" con existencia física de 100 tabletas.
  * **When** Un cajero vende y factura 20 tabletas a un cliente.
  * **Then** El stock total del medicamento debe reflejar inmediatamente `80 tabletas` sin requerir recargar manualmente la página.
* **Scenario 2: Bloqueo de venta ante intento de saldo negativo**
  * **Given** Un producto farmacéutico con únicamente 3 unidades disponibles en estantería.
  * **When** El dependiente intenta procesar una venta por 4 unidades.
  * **Then** El sistema aborta la transacción con un `UserError`, impide la emisión de la factura y mantiene las 3 unidades intactas en inventario.
* **Scenario 3: Descuento correcto sobre el lote dispensado**
  * **Given** El Lote #PAR-2025 con 50 pastillas registradas.
  * **When** Se despachan 10 pastillas de dicho lote en una venta.
  * **Then** El balance específico del Lote #PAR-2025 disminuye a `40 pastillas`.

## 7. Verification Plan
* **Automated Tests:**
  * Prueba unitaria en Python creando un producto con stock = 10, ejecutando una venta por 4 unidades y validando que `qty_available == 6` y que un intento subsiguiente de vender 7 unidades arroje `UserError`.
* **Manual Verification:**
  * Realizar una venta en el navegador, abrir en otra pestaña la vista de inventario del producto y corroborar la reducción inmediata del saldo físico.

## 8. Security and Privacy
* La auditoría de cada deducción de stock queda registrada de forma inmutable en `stock.move` con el número de factura simple vinculada.

## 9. Risks and Mitigation
* **Risk:** Ventas simultáneas en dos cajas de la última unidad física disponible de un medicamento.
  * **Mitigation:** Uso de bloqueos a nivel de fila (*row-locking*) en PostgreSQL durante el cálculo de disponibilidad previa a la confirmación.

## 10. Deliverables & Config as Code
* Lógica de deducción y bloqueo de saldo negativo en `custom_addons/caryvil_erp/models/sale_order_medicine.py`.

## 11. Definition of Done (DoD)
* [ ] Descuento automático de existencias físicas en tiempo real validado.
* [ ] Bloqueo estricto de saldo negativo probado con casos de concurrencia.
* [ ] Sincronización con el balance de lotes verificada.
* [ ] Pruebas unitarias automatizadas aprobadas al 100%.
* [ ] Aprobación de la política de inventario por la propietaria de Farmacia Caryvil.
