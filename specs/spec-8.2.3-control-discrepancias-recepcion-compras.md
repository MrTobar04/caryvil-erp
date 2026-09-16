# SPEC-8.2.3: Control de Discrepancias en Recepción de Compras

## 1. Objective
Gestionar, controlar y documentar las discrepancias entre las cantidades físicas entregadas por laboratorios farmacéuticos y las cantidades solicitadas en las Órdenes de Compra originales en Odoo (`stock.picking` y `stock.backorder.confirmation`) para Farmacia Caryvil. Esta especificación regula el tratamiento de entregas parciales (*backorders*), excesos no autorizados, rechazo de productos dañados en transporte y cancelación de remanentes, manteniendo la coherencia entre las facturas de proveedores y el inventario real.

## 2. Scope
### 2.1. Included
* Configuración del asistente de confirmación de entregas pendientes (`stock.backorder.confirmation`):
  * **Opción 1: Crear Entrega Parcial (*Backorder*):** Genera automáticamente un nuevo albarán de entrada pendiente con las unidades no recibidas para esperar su entrega posterior por el laboratorio.
  * **Opción 2: No Crear Entrega Parcial:** Cancela el remanente de la orden de compra si el laboratorio notifica que el producto está descontinuado o agotado.
* Control de entregas en exceso: Si el proveedor entrega una cantidad superior a la ordenada originalmente, el sistema solicita autorización explícita del Administrador o rechaza la recepción del excedente.
* Registro de incidencias y rechazos por daños en transporte (frascos quebrados, sellos rotos, empaques húmedos) directamente en el albarán de entrada mediante notas de discrepancia en el chatter.
* Notificación automática por correo interno o mensaje de chatter al `Encargado de Compras` ante cualquier discrepancia detectada durante la descarga.

### 2.2. Not Included (Out of Scope)
* Trámites de reclamo legal o notas de crédito con el laboratorio (se gestionan administrativamente fuera del sistema).

## 3. Context and Restrictions
* **Context:** Protege a Farmacia Caryvil de pagar por mercadería no recibida o asumir costos de medicamentos que llegaron en mal estado desde la droguería distribuidora.
* **Restrictions:**
  * No se puede validar una entrega con discrepancia sin que el encargado de recepción elija explícitamente entre crear un *backorder* o cancelar el remanente.
  * Los medicamentos rechazados no deben ingresar bajo ninguna circunstancia a las existencias vendibles.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-8.1.1` (Gestión de Órdenes de Compra).
  * `SPEC-8.2.1` (Recepción de Mercadería y Registro de Lotes).
  * `SPEC-8.2.2` (Actualización Automática de Stock en Compras).
* **Definition of Ready (DoR):**
  * [x] Protocolo de recepción de mercadería y tolerancia a entregas parciales acordado con la administración.
  * [x] Asistente de *backorders* habilitado en la configuración de almacenes de Odoo.

## 5. Design (Implementation Details)
* **Discrepancy Flow:**
  ```
  [Recepción Física: Cantidad Recibida < Cantidad Ordenada]
                             │
                             ▼
              [¿El proveedor enviará el resto?]
                     /                \
                   SÍ                  NO
                   /                    \
                  ▼                      ▼
      [Crear Entrega Parcial]    [No Crear Entrega Parcial]
      - Nuevo albarán creado     - Remanente cancelado
      - Espera segundo envío     - PO ajustada a lo recibido
  ```
* **Model Extension (`models/stock_picking_reception.py`):**
  ```python
  from odoo import models, fields, api, _

  class StockPickingDiscrepancy(models.Model):
      _inherit = 'stock.picking'

      has_discrepancy = fields.Boolean(
          string='Presenta Discrepancia',
          compute='_compute_has_discrepancy',
          store=True
      )
      discrepancy_notes = fields.Text(string='Detalle de Discrepancia / Daños')

      @api.depends('move_lines.quantity_done', 'move_lines.product_uom_qty')
      def _compute_has_discrepancy(self):
          for picking in self:
              discrepancy = False
              if picking.picking_type_code == 'incoming':
                  for move in picking.move_lines:
                      if move.quantity_done < move.product_uom_qty and picking.state == 'done':
                          discrepancy = True
                          break
              picking.has_discrepancy = discrepancy
  ```

## 6. Acceptance Criteria
* **Scenario 1: Entrega parcial con generación de Backorder**
  * **Given** Una orden de compra por 30 cajas de "Loratadina 10mg" donde el laboratorio entrega solo 20 cajas hoy.
  * **When** El usuario valida el ingreso de 20 cajas y selecciona "Crear Entrega Parcial".
  * **Then** El stock aumenta en 20 cajas, el albarán actual pasa a estado `done` y Odoo crea automáticamente un nuevo albarán por las 10 cajas restantes en estado `assigned`.
* **Scenario 2: Entrega parcial sin Backorder (Agotado en Distribuidora)**
  * **Given** Un pedido de 15 frascos donde el proveedor entrega 10 y notifica que no tiene más existencias.
  * **When** El usuario valida 10 unidades y selecciona "No crear entrega parcial".
  * **Then** El stock aumenta en 10 unidades, la orden de compra ajusta su saldo y se cierra sin dejar albaranes pendientes.
* **Scenario 3: Rechazo de producto dañado en la descarga**
  * **Given** 5 frascos de jarabe que llegaron quebrados en la caja de transporte.
  * **When** El receptor no incluye los 5 frascos en la `qty_done` y escribe en la nota: "5 frascos rotos rechazados al repartidor".
  * **Then** El sistema no ingresa los 5 frascos al inventario y registra la incidencia en el historial para conciliar con la factura del proveedor.

## 7. Verification Plan
* **Automated Tests:**
  * Prueba unitaria en Python simulando una recepción parcial (`qty_done < product_uom_qty`), ejecutando `stock.backorder.confirmation` y validando la creación exitosa del albarán secundario con las cantidades remanentes exactas.
* **Manual Verification:**
  * Validar una entrega parcial en la interfaz web y verificar que aparezcan ambos albaranes vinculados a la misma orden de compra.

## 8. Security and Privacy
* El cierre forzado de órdenes de compra con discrepancia requiere privilegios del `Encargado de Compras e Inventario` o `Administrador`.

## 9. Risks and Mitigation
* **Risk:** Albaranes pendientes (*backorders*) olvidados indefinidamente en el sistema.
  * **Mitigation:** Filtro predeterminado en el menú de Compras: `[Entregas Pendientes / Retrasadas]` para dar seguimiento semanal con laboratorios.

## 10. Deliverables & Config as Code
* Campos y métodos de control de discrepancias en `models/stock_picking_reception.py`.
* Vistas de alertas en `views/stock_picking_views.xml`.

## 11. Definition of Done (DoD)
* [x] Asistente de *backorders* configurado y probado para recepciones parciales — **nativo de Odoo** (`stock.backorder.confirmation`, se activa solo cuando `qty_done < demanda`); no requirió código adicional.
* [x] Registro de notas de rechazo y daños en transporte habilitado (`discrepancy_notes` + pestaña "Discrepancias" en el albarán).
* [x] Cancelación de remanentes validada sin errores contables — flujo nativo de Odoo ("No crear entrega parcial").
* [x] Pruebas unitarias aprobadas al 100% (`tests/test_stock_picking_reception.py`).
* [ ] Aprobación del procedimiento de discrepancias por la administración.
