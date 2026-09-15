# SPEC-8.2.1: Recepción de Mercadería y Registro de Lotes

## 1. Objective
Modelar, controlar y hacer obligatoria la captura de números de lote y fechas de caducidad durante la recepción física de mercadería en Odoo (`stock.picking` de tipo `incoming` / Albarán de Entrada) para Farmacia Caryvil. Esta especificación asegura que al momento de ingresar medicamentos enviados por los laboratorios o droguerías, el personal verifique el pedido contra el documento físico de entrega y digite mandatoriamente el lote impreso por el fabricante y su fecha de vencimiento real antes de permitir la validación del albarán.

## 2. Scope
### 2.1. Included
* Personalización de la vista de operaciones detalladas del albarán de entrada (`stock.picking` y `stock.move.line`) en `custom_addons/caryvil_erp/models/stock_picking_reception.py`.
* Inclusión de campos obligatorios por línea de recepción de medicamentos rastreados:
  * `lot_name` (Char): Número o código de lote provisto por el laboratorio farmacéutico.
  * `expiration_date` (Date/Datetime): Fecha de caducidad impresa en las cajas/frascos del lote recibido.
  * `qty_done` (Float): Cantidad física real verificada y recibida.
* Validación estricta a nivel de código (`button_validate`): Bloqueo automático si el usuario intenta validar la entrada sin asignar número de lote o si la fecha de vencimiento es nula o anterior a la fecha actual.
* Soporte para recepción de un mismo medicamento fraccionado en múltiples lotes distintos (e.g., de 20 cajas recibidas: 10 cajas corresponden al Lote A con vencimiento 2026 y 10 cajas al Lote B con vencimiento 2027).

### 2.2. Not Included (Out of Scope)
* Incremento transaccional automático del stock físico en inventario (cubierto en `SPEC-8.2.2`).
* Gestión de discrepancias por faltantes o daños en el transporte (cubierto en `SPEC-8.2.3`).

## 3. Context and Restrictions
* **Context:** Es el punto crítico de control de calidad donde la información física del empaque del medicamento se traslada al sistema digital de Farmacia Caryvil.
* **Restrictions:**
  * Ningún producto farmacéutico con seguimiento por lotes puede ingresar a las ubicaciones internas sin lote y fecha de vencimiento.
  * La fecha de vencimiento debe ser posterior a la fecha actual del sistema.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-7.1.1` (Catálogo y Categorización de Medicamentos).
  * `SPEC-7.2.1` (Control de Stock, Lotes y Vencimientos).
  * `SPEC-8.1.1` (Gestión de Órdenes de Compra).
* **Definition of Ready (DoR):**
  * [x] Orden de compra confirmada con estado de albarán en `assigned` (Listo para recibir).
  * [x] Formulario de operaciones detalladas de albarán de entrada configurado.

## 5. Design (Implementation Details)
* **Validation Logic (`models/stock_picking_reception.py`):**
  ```python
  from odoo import models, fields, api, _
  from odoo.exceptions import ValidationError

  class StockPickingReception(models.Model):
      _inherit = 'stock.picking'

      def button_validate(self):
          today = fields.Datetime.now()
          for picking in self:
              if picking.picking_type_code == 'incoming':
                  for line in picking.move_line_ids:
                      product = line.product_id
                      if product.tracking == 'lot' and line.qty_done > 0:
                          # Validar que exista lote asignado o escrito
                          if not line.lot_id and not line.lot_name:
                              raise ValidationError(_('Debe asignar el Número de Lote para el medicamento %s en la recepción.') % product.name)
                          
                          # Validar fecha de vencimiento en el lote nuevo
                          if line.lot_name and not line.expiration_date:
                              raise ValidationError(_('Debe especificar la Fecha de Vencimiento para el lote %s del producto %s.') % (line.lot_name, product.name))
                          
                          if line.expiration_date and line.expiration_date < today:
                              raise ValidationError(_('La fecha de vencimiento (%s) del lote %s ya está caducada. No se puede recibir mercadería vencida.') % (line.expiration_date, line.lot_name))

          return super(StockPickingReception, self).button_validate()

  class StockMoveLineReception(models.Model):
      _inherit = 'stock.move.line'

      expiration_date = fields.Datetime(string='Fecha de Vencimiento')
  ```

## 6. Acceptance Criteria
* **Scenario 1: Recepción exitosa con captura de lote y fecha válida**
  * **Given** Un albarán de entrada por 15 cajas de "Ibuprofeno 400mg".
  * **When** El encargado físico digita Lote: "LOT-IBU-2027-01", Vencimiento: "2027-08-31", Cantidad: 15 y presiona "Validar".
  * **Then** El albarán se valida con éxito, creando el nuevo registro de lote en `stock.production.lot` con su fecha de caducidad vinculada.
* **Scenario 2: Bloqueo de recepción por omisión de lote**
  * **Given** Un medicamento con seguimiento por lotes activado.
  * **When** El usuario intenta presionar "Validar" sin haber escrito el número de lote.
  * **Then** Odoo arroja un `ValidationError` deteniendo la validación y solicitando la captura del lote.
* **Scenario 3: Recepción de pedido dividido en dos lotes distintos**
  * **Given** Un pedido de 20 unidades donde el proveedor envió 10 unidades de lote A (exp: 2026) y 10 unidades de lote B (exp: 2027).
  * **When** El usuario desglosa la recepción en dos líneas de operaciones detalladas.
  * **Then** El sistema crea ambos lotes en el inventario con sus respectivas cantidades y fechas de forma independiente.

## 7. Verification Plan
* **Automated Tests:**
  * Test unitario en Python simulando la validación de un `stock.picking` entrante sin lote (verificando captura de excepción) y con lote válido (verificando transición a estado `done`).
* **Manual Verification:**
  * Recibir una orden de compra en la interfaz de Odoo, registrar el lote y verificar que el lote aparezca en la lista de lotes activos.

## 8. Security and Privacy
* Operación restringida al `Encargado de Compras e Inventario` y `Administrador`.

## 9. Risks and Mitigation
* **Risk:** Digitación errónea de caracteres en el número de lote.
  * **Mitigation:** Permitir al usuario escanear directamente el código de barras Datamatrix/QR del empaque del medicamento si el fabricante lo incluye.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/models/stock_picking_reception.py`.
* Extensión de vista `views/stock_picking_views.xml`.

## 11. Definition of Done (DoD)
* [ ] Captura de lote y fecha de vencimiento integrada en el albarán de entrada.
* [ ] Bloqueo estricto ante ausencia de lote o fechas caducadas probado.
* [ ] Creación automática de registros en `stock.production.lot` validada.
* [ ] Pruebas unitarias aprobadas al 100%.
* [ ] Validación con el encargado de bodega de Farmacia Caryvil.
