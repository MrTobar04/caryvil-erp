# SPEC-9.3.2: Estrategia de Salida FEFO por Lotes

## 1. Objective
Implementar, parametrizar y hacer mandatoria la estrategia de remoción algorítmica **FEFO (First Expired, First Out - Primero en Vencer, Primero en Salir)** para la asignación y despacho de lotes en las ventas de Farmacia Caryvil. Esta especificación asegura que al registrarse una venta en mostrador, el sistema identifique y reserve automáticamente las unidades del lote no vencido con la fecha de caducidad más próxima, previniendo el envejecimiento de inventario en estanterías, reduciendo a cero las mermas por vencimiento no detectado y garantizando la entrega de medicamentos en óptimas condiciones de vigencia.

## 2. Scope
### 2.1. Included
* Configuración de la estrategia de remoción FEFO (`stock.removal.strategy`) como política predeterminada para la categoría de productos farmacéuticos en `custom_addons/caryvil_erp/models/stock_removal_fefo.py`.
* Algoritmo de asignación automática de lotes en las líneas de operaciones de salida (`stock.move.line`):
  1. Filtra los lotes disponibles del medicamento con saldo físico positivo (`product_qty > 0`) en la ubicación de mostrador/bodega.
  2. Excluye automáticamente cualquier lote marcado como caducado (`is_expired = True`).
  3. Ordena los lotes vigentes de forma ascendente por fecha de caducidad (`order='expiration_date asc'`).
  4. Asigna y reserva la cantidad requerida del lote con fecha de caducidad más cercana.
* Fraccionamiento automático de líneas (*Split Line*): Si la cantidad solicitada supera las existencias del lote más próximo a vencer, el sistema toma el total disponible de ese lote y completa el remanente con el siguiente lote cronológicamente más próximo.
* Posibilidad de sobreescritura manual en mostrador con advertencia (*warning*) en caso de requerimiento médico o solicitud expresa del paciente.

### 2.2. Not Included (Out of Scope)
* Reubicación física de cajas en las estanterías (la rotación física debe acompañar a la directiva del sistema).
* Gestión de mermas por productos que lleguen a su fecha límite de retiro (cubierto en `SPEC-7.3.2`).

## 3. Context and Restrictions
* **Context:** Es la regla de oro de la logística farmacéutica moderna, evitando que medicamentos recibidos recientemente se vendan antes que aquellos recibidos con anterioridad y fecha más corta.
* **Restrictions:**
  * El algoritmo FEFO jamás debe sugerir ni permitir la reserva de un lote cuya fecha de caducidad sea anterior o igual al día actual.
  * La asignación debe ser totalmente automática y no requerir que el cajero busque manualmente en una lista de lotes.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-7.1.1` (Catálogo y Categorización de Medicamentos).
  * `SPEC-7.2.1` (Control de Stock, Lotes y Vencimientos).
  * `SPEC-9.1.1` (Procesamiento de Transacciones de Ventas).
  * `SPEC-9.3.1` (Deducción Automática de Stock en Ventas).
* **Definition of Ready (DoR):**
  * [x] Módulo `product_expiry` de Odoo activo.
  * [x] Medicamentos con trazabilidad por lotes configurada.

## 5. Design (Implementation Details)
* **FEFO Reservation Logic (`models/stock_removal_fefo.py`):**
  ```python
  from odoo import models, fields, api, _
  from odoo.exceptions import UserError

  class StockMoveFEFO(models.Model):
      _inherit = 'stock.move'

      def _update_reserved_quantity(self, need, available_quantity, location_id, lot_id=None, package_id=None, owner_id=None, strict=True):
          # Si el producto tiene seguimiento por lotes, priorizar ordenamiento FEFO
          if self.product_id.tracking == 'lot' and not lot_id:
              today = fields.Datetime.now()
              # Buscar lotes vigentes ordenados por fecha de vencimiento más próxima
              quants = self.env['stock.quant'].search([
                  ('product_id', '=', self.product_id.id),
                  ('location_id', '=', location_id.id),
                  ('quantity', '>', 0),
                  ('lot_id.expiration_date', '>=', today)
              ], order='lot_id.expiration_date asc')
              
              if not quants:
                  raise UserError(_('No hay lotes vigentes disponibles para el medicamento %s.') % self.product_id.name)
              
              # Asignar quants según FEFO
              for quant in quants:
                  if need <= 0:
                      break
                  lot_avail = quant.quantity - quant.reserved_quantity
                  if lot_avail > 0:
                      taken = min(need, lot_avail)
                      res = super(StockMoveFEFO, self)._update_reserved_quantity(taken, available_quantity, location_id, lot_id=quant.lot_id, strict=strict)
                      need -= taken
              return need
          
          return super(StockMoveFEFO, self)._update_reserved_quantity(need, available_quantity, location_id, lot_id=lot_id, strict=strict)
  ```

## 6. Acceptance Criteria
* **Scenario 1: Asignación automática del lote más próximo a caducar**
  * **Given** El medicamento "Amoxicilina 500mg" con dos lotes vigentes: Lote A (Vence: 2026-10-31, Saldo: 10) y Lote B (Vence: 2027-05-31, Saldo: 15).
  * **When** Un cajero registra una venta por 4 unidades.
  * **Then** El sistema asigna automáticamente las 4 unidades del **Lote A** por ser el más próximo a vencer.
* **Scenario 2: Fraccionamiento automático entre dos lotes por cantidad solicitada**
  * **Given** El mismo medicamento con Lote A (Vence: 2026-10-31, Saldo: 3) y Lote B (Vence: 2027-05-31, Saldo: 15).
  * **When** Un cliente solicita 5 unidades.
  * **Then** El sistema reserva automáticamente las 3 unidades del Lote A y toma las 2 unidades restantes del Lote B.
* **Scenario 3: Exclusión absoluta de lotes vencidos**
  * **Given** El Lote C con fecha de vencimiento expirada hace 5 días y Lote D con vencimiento el próximo año.
  * **When** Se realiza una venta.
  * **Then** El algoritmo FEFO ignora completamente el Lote C y selecciona únicamente unidades del Lote D.

## 7. Verification Plan
* **Automated Tests:**
  * Prueba unitaria en Python creando 2 lotes con distintas fechas de caducidad, simulando ventas unitarias y de cantidad mayor al primer lote, verificando que los lotes reservados coincidan exactamente con la regla FEFO.
* **Manual Verification:**
  * Procesar una venta en mostrador y verificar en el albarán de salida o en el ticket impreso el lote asignado automáticamente.

## 8. Security and Privacy
* La regla FEFO previene dispensaciones no conformes y queda registrada en la auditoría del movimiento de inventario.

## 9. Risks and Mitigation
* **Risk:** Falta de coincidencia física si el dependiente toma físicamente de la estantería una caja con lote distinto al asignado en el sistema.
  * **Mitigation:** El ticket de mostrador y la pantalla de caja muestran claramente el número de lote sugerido para que el dependiente tome la caja correcta.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/models/stock_removal_fefo.py`.
* Configuración de la estrategia FEFO en `data/pharmacy_removal_strategy_data.xml`.

## 11. Definition of Done (DoD)
* [ ] Estrategia de remoción FEFO implementada en el módulo de inventario.
* [ ] Asignación automática por fecha ascendente de vencimiento verificada.
* [ ] Fraccionamiento de líneas multilote probado con éxito.
* [ ] Pruebas unitarias automatizadas aprobadas al 100%.
* [ ] Aprobación de la política FEFO por la dirección técnica de Farmacia Caryvil.
