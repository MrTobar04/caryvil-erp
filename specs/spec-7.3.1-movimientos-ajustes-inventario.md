# SPEC-7.3.1: Movimientos y Ajustes de Inventario

## 1. Objective
Implementar, auditar y controlar los procesos de conteo físico periódico, conciliación de inventario y ajustes de existencias en Odoo (`stock.quant`) para Farmacia Caryvil. Esta especificación permite realizar recuentos físicos por estantería o categoría terapéutica, registrar las cantidades reales contadas contra las cantidades teóricas del sistema, documentar obligatoriamente la justificación de cualquier discrepancia (sobrantes o faltantes) y aplicar el ajuste al balance de existencias y lotes con total trazabilidad y control de usuario.

## 2. Scope
### 2.1. Included
* Personalización de la vista de ajustes de inventario (`stock.quant`) en `custom_addons/caryvil_erp/models/stock_inventory_adjustment.py`:
  * `adjustment_reason` (Selection): Motivo obligatorio del ajuste (`ajuste_inicial`, `conteo_ciclico_periodico`, `error_conteo_previo`, `diferencia_despacho`, `otro`).
  * `adjustment_notes` (Text): Explicación detallada del ajuste.
  * `counted_by_user_id` (Many2one `res.users`): Usuario que realizó el conteo físico en estantería.
  * `validated_by_user_id` (Many2one `res.users`): Administrador que autoriza el ajuste.
* Mecanismo de aplicación de ajustes con actualización de lotes específicos (`stock.production.lot`).
* Generación automática de movimientos contables y de stock hacia la ubicación virtual de ajuste de inventario (`virtual_location/inventory`).
* Restricción de permisos: El personal de inventario puede registrar conteos físicos, pero la aprobación y aplicación del ajuste requiere el rol `Administrador / Propietaria`.

### 2.2. Not Included (Out of Scope)
* Bajas formales por deterioro, rotura o medicamentos vencidos (cubierto en `SPEC-7.3.2`).
* Actualización de stock por compras o ventas (cubierto en `SPEC-8.2.2` y `SPEC-9.3.1`).

## 3. Context and Restrictions
* **Context:** Garantiza que los registros digitales de Odoo coincidan fielmente con los medicamentos reales existentes en las vitrinas y bodegas de Farmacia Caryvil, eliminando las discrepancias históricas que ocurrían con Excel.
* **Restrictions:**
  * No se puede validar un ajuste de inventario sin seleccionar un motivo explícito (`adjustment_reason`).
  * Si el ajuste modifica un medicamento rastreado por lotes, es obligatorio especificar a qué lote exacto corresponde la variación.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
  * `SPEC-2.2.1` (Definición de Roles y Grupos de Usuarios).
  * `SPEC-7.2.1` (Control de Stock, Lotes y Vencimientos).
* **Definition of Ready (DoR):**
  * [x] Ubicaciones físicas de Farmacia Caryvil definidas (Mostrador/Vitrinas y Bodega Interna).
  * [x] Protocolo de conteo físico periódico aprobado por la administración.

## 5. Design (Implementation Details)
* **Model Configuration (`models/stock_inventory_adjustment.py`):**
  ```python
  from odoo import models, fields, api, _
  from odoo.exceptions import ValidationError

  class StockQuantAdjustment(models.Model):
      _inherit = 'stock.quant'

      adjustment_reason = fields.Selection([
          ('ajuste_inicial', 'Carga de Inventario Inicial'),
          ('conteo_ciclico_periodico', 'Conteo Cíclico Periódico'),
          ('error_conteo_previo', 'Corrección de Conteo Previo'),
          ('diferencia_despacho', 'Diferencia en Despacho'),
          ('otro', 'Otro Motivo')
      ], string='Motivo del Ajuste', default='conteo_ciclico_periodico')
      adjustment_notes = fields.Text(string='Observaciones / Justificación')

      def action_apply_inventory(self):
          for quant in self:
              if quant.inventory_quantity_set and quant.inventory_diff_quantity != 0:
                  if not quant.adjustment_reason:
                      raise ValidationError(_('Debe especificar el Motivo del Ajuste para el producto %s.') % quant.product_id.name)
          return super(StockQuantAdjustment, self).action_apply_inventory()
  ```

## 6. Acceptance Criteria
* **Scenario 1: Conteo físico coincidente**
  * **Given** Un medicamento con stock teórico de 50 tabletas.
  * **When** El encargado realiza el conteo en estantería y registra `50 tabletas`.
  * **Then** La diferencia es `0` y el sistema marca el producto como verificado sin generar movimientos de ajuste.
* **Scenario 2: Conciliación de sobrante con justificación**
  * **Given** Un producto con stock teórico de 10 unidades, pero el conteo físico arroja 12 unidades.
  * **When** El usuario registra la cantidad contada de 12, selecciona motivo "Conteo Cíclico Periódico" y el administrador valida.
  * **Then** El stock del producto se actualiza a 12 unidades y se registra la bitácora del movimiento.
* **Scenario 3: Bloqueo de ajuste sin motivo seleccionado**
  * **Given** Un conteo que presenta diferencia de stock.
  * **When** Se intenta presionar "Aplicar Ajuste" con el campo de motivo vacío.
  * **Then** Odoo bloquea la acción mediante un `ValidationError` exigiendo la selección de la causa.

## 7. Verification Plan
* **Automated Tests:**
  * Test unitario en Python simulando un conteo con diferencia, validando el bloqueo ante ausencia de motivo y la correcta actualización de `quantity` tras la validación.
* **Manual Verification:**
  * Realizar un ajuste de prueba desde el menú `Inventario > Ajustes de Inventario` y verificar la auditoría en los movimientos de stock.

## 8. Security and Privacy
* El botón "Aplicar Ajuste" está disponible únicamente para usuarios con permisos del grupo `group_caryvil_manager`.

## 9. Risks and Mitigation
* **Risk:** Ajustes no autorizados para ocultar pérdidas o hurtos.
  * **Mitigation:** Registro inmutable del usuario autenticado, fecha/hora y motivo en el historial de trazabilidad de cada ajuste.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/models/stock_inventory_adjustment.py`.
* Extensión de vista en `views/stock_quant_views.xml`.

## 11. Definition of Done (DoD)
* [x] Modelo `stock.quant` extendido con campos de justificación de ajuste.
* [x] Validación de motivo obligatorio implementada y probada.
* [x] Permisos de aprobación restringidos al rol Administrador.
* [x] Pruebas unitarias aprobadas al 100%.
* [x] Procedimiento de conteo validado con la propietaria de la farmacia.
