# SPEC-7.2.1: Control de Stock, Lotes y Vencimientos

## 1. Objective
Habilitar, parametrizar y hacer mandatorio el control de inventario por números de lote (`stock.production.lot`) y fechas de caducidad para la totalidad de medicamentos almacenables en Odoo para Farmacia Caryvil. Esta especificación garantiza la trazabilidad biunívoca de cada unidad desde su recepción con el laboratorio hasta su dispensación al consumidor final, estableciendo alertas de vida útil, fechas de remoción preventiva de estantería y el bloqueo estricto de venta para lotes con fecha vencida.

## 2. Scope
### 2.1. Included
* Habilitación de las directivas de trazabilidad por lotes (`tracking = 'lot'`) y fechas de caducidad en el módulo `stock` de Odoo.
* Extensión del modelo `stock.production.lot` en `custom_addons/caryvil_erp/models/stock_lot_medicine.py`:
  * `expiration_date` (Datetime): Fecha exacta de caducidad certificada por el laboratorio.
  * `alert_date` (Datetime): Fecha para disparo de alerta preventiva (por defecto 60 días antes de vencer).
  * `removal_date` (Datetime): Fecha obligatoria de retiro de mostrador (por defecto 15 días antes de vencer).
  * `is_expired` (Boolean computado): Indicador reactivo de lote vencido (`expiration_date < today`).
* Bloqueo a nivel de ORM para impedir la selección y confirmación de venta de lotes marcados como vencidos (`is_expired = True`).
* Vista de árbol y formulario enriquecida para lotes en `views/stock_lot_medicine_views.xml` con semáforos de color según vigencia.

### 2.2. Not Included (Out of Scope)
* Configuración de la estrategia algorítmica FEFO en el despacho (cubierto en `SPEC-9.3.2`).
* Captura de lotes durante la recepción de compras (cubierto en `SPEC-8.2.1`).

## 3. Context and Restrictions
* **Context:** Es el requisito regulatorio sanitario más crítico para una farmacia, asegurando que nunca se entregue a un paciente un medicamento vencido o deteriorado.
* **Restrictions:**
  * No se puede ingresar inventario de medicamentos sin asignar un número de lote y una fecha de caducidad válida.
  * La fecha de vencimiento no puede ser anterior a la fecha actual del sistema al momento de la recepción.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
  * `SPEC-7.1.1` (Catálogo y Categorización de Medicamentos).
* **Definition of Ready (DoR):**
  * [x] Módulo `product_expiry` de Odoo identificado como dependencia.
  * [x] Políticas de vencimiento y tiempos de retiro de mostrador acordados con la dirección técnica.

## 5. Design (Implementation Details)
* **Data Model (`models/stock_lot_medicine.py`):**
  ```python
  from odoo import models, fields, api, _
  from odoo.exceptions import ValidationError

  class StockProductionLotMedicine(models.Model):
      _inherit = 'stock.production.lot'

      is_expired = fields.Boolean(
          string='Lote Vencido',
          compute='_compute_is_expired',
          store=True,
          index=True
      )

      @api.depends('expiration_date')
      def _compute_is_expired(self):
          today = fields.Datetime.now()
          for lot in self:
              lot.is_expired = bool(lot.expiration_date and lot.expiration_date < today)

      @api.constrains('expiration_date')
      def _check_expiration_date(self):
          for lot in self:
              if lot.expiration_date and lot.create_date and lot.expiration_date < lot.create_date:
                  raise ValidationError(_('La fecha de vencimiento del lote (%s) no puede ser anterior a su fecha de creación/recepción.') % lot.name)
  ```
* **UI Highlighting:**
  * Lotes con fondo rojo en listas si `is_expired = True`.
  * Filtro predeterminado: `[Lotes Vigentes]` (excluyendo vencidos).

## 6. Acceptance Criteria
* **Scenario 1: Asignación de lote y caducidad en el inventario**
  * **Given** Un lote registrado "LOT-AMX-2027" con fecha de caducidad "2027-12-31".
  * **When** Se consulta la existencia del medicamento.
  * **Then** El sistema muestra el stock desglosado indicando que las unidades corresponden al lote "LOT-AMX-2027" con estado vigente.
* **Scenario 2: Bloqueo de venta para lote caducado**
  * **Given** Un lote con fecha de caducidad vencida ayer (`is_expired = True`).
  * **When** Un cajero intenta seleccionar este lote en una venta de mostrador.
  * **Then** El sistema bloquea la operación y arroja un error: "No es posible dispensar el lote X porque se encuentra vencido".
* **Scenario 3: Trazabilidad completa de un lote**
  * **Given** El número de lote "LOT-AMX-2024-01".
  * **When** La administradora consulta su informe de trazabilidad.
  * **Then** Odoo muestra el historial completo: qué proveedor lo entregó, en qué fecha ingresó a bodega y en cuáles facturas fue vendido a los clientes.

## 7. Verification Plan
* **Automated Tests:**
  * Prueba unitaria en Python creando un lote con fecha pasada, verificando que `is_expired` sea `True` y que el intento de venta dispare `ValidationError`.
* **Manual Verification:**
  * Crear dos lotes con fechas distintas y verificar la correcta coloración en la vista de lista de `Inventario > Lotes`.

## 8. Security and Privacy
* La modificación de fechas de vencimiento de lotes ya existentes queda auditada en el chatter del registro y restringida al rol Administrador.

## 9. Risks and Mitigation
* **Risk:** Error humano en la digitación de la fecha de caducidad en el albarán de recepción.
  * **Mitigation:** Validación de rangos lógicos (bloquear años anteriores al actual o fechas posteriores a 10 años).

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/models/stock_lot_medicine.py`.
* Archivo `custom_addons/caryvil_erp/views/stock_lot_medicine_views.xml`.

## 11. Definition of Done (DoD)
* [ ] Modelo `stock.production.lot` extendido con cálculo de estado vencido.
* [ ] Bloqueo de venta para lotes caducados probado y validado.
* [ ] Trazabilidad de lotes desde compras hasta ventas verificada.
* [ ] Pruebas unitarias aprobadas al 100%.
* [ ] Aprobación de la dirección técnica farmacéutica.
