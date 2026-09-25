# SPEC-7.3.2: Gestión de Mermas y Bajas de Medicamentos

## 1. Objective
Diseñar, implementar y controlar el proceso formal de descarte, desincorporación y baja de medicamentos por merma en Odoo (`stock.scrap`) para Farmacia Caryvil. Esta especificación gestiona la transferencia de unidades dañadas, rotas, contaminadas o caducadas desde las ubicaciones operativas (mostrador y bodega) hacia una ubicación virtual de cuarentena y desecho farmacéutico, documentando obligatoriamente la causa de la baja, el lote afectado, el costo financiero de la pérdida y la autorización correspondiente.

## 2. Scope
### 2.1. Included
* Creación del modelo extendido `caryvil.stock.loss` / extensión de `stock.scrap` en `custom_addons/caryvil_erp/models/stock_scrap_medicine.py`:
  * `scrap_reason` (Selection): Causa formal de la merma (`medicamento_vencido`, `rotura_frasco_ampolla`, `empaque_deteriorado_humedad`, `retiro_sanitario_laboratorio`, `otro`).
  * `lot_id` (Many2one `stock.production.lot`): Lote específico al cual se le da de baja (obligatorio para fármacos con seguimiento).
  * `scrap_unit_cost` (Monetary): Costo de adquisición unitario del medicamento en USD ($).
  * `scrap_total_loss` (Monetary): Pérdida económica total calculada (`scrap_qty * scrap_unit_cost`).
  * `justification_notes` (Text): Explicación técnica de la merma.
  * `authorized_by_id` (Many2one `res.users`): Administrador que aprueba la baja.
* Configuración de la ubicación virtual interna de desecho: `Ubicación Virtual / Desecho y Cuarentena Caryvil`.
* Inhabilitación automática de las unidades dadas de baja para que no aparezcan disponibles en ventas ni en las alertas de stock activo.
* Generación del informe imprimible de Acta de Merma y Destrucción Farmacéutica.

### 2.2. Not Included (Out of Scope)
* Trámites ante el Ministerio de Salud o Dirección Nacional de Medicamentos (DNM) para destrucción de controlados (excluido del alcance del software).
* Ajustes ordinarios de inventario por conteo físico (cubierto en `SPEC-7.3.1`).

## 3. Context and Restrictions
* **Context:** Permite cuantificar con exactitud las pérdidas financieras por medicamentos no comercializables y asegurar que ningún producto en mal estado o vencido permanezca físicamente en el área de despacho de Farmacia Caryvil.
* **Restrictions:**
  * No se puede dar de baja una cantidad superior a la existencia física disponible en el lote seleccionado.
  * La aprobación definitiva de una merma está restringida al rol `Administrador / Propietaria`.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
  * `SPEC-2.2.1` (Definición de Roles y Grupos de Usuarios).
  * `SPEC-7.2.1` (Control de Stock, Lotes y Vencimientos).
* **Definition of Ready (DoR):**
  * [x] Causas de merma farmacéutica catalogadas.
  * [x] Ubicación de desecho/cuarentena definida en la parametrización de almacenes.

## 5. Design (Implementation Details)
* **Model Configuration (`models/stock_scrap_medicine.py`):**
  ```python
  from odoo import models, fields, api, _
  from odoo.exceptions import ValidationError

  class StockScrapMedicine(models.Model):
      _inherit = 'stock.scrap'

      scrap_reason = fields.Selection([
          ('medicamento_vencido', 'Medicamento Caducado / Vencido'),
          ('rotura_frasco_ampolla', 'Rotura de Frasco / Ampolla'),
          ('empaque_deteriorado_humedad', 'Deterioro de Empaque / Humedad'),
          ('retiro_sanitario_laboratorio', 'Retiro Sanitario por Laboratorio'),
          ('otro', 'Otra Causa')
      ], string='Causa de la Merma', required=True, default='medicamento_vencido')

      scrap_unit_cost = fields.Monetary(string='Costo Unitario ($)', currency_field='currency_id', compute='_compute_scrap_costs', store=True)
      scrap_total_loss = fields.Monetary(string='Pérdida Total ($)', currency_field='currency_id', compute='_compute_scrap_costs', store=True)
      currency_id = fields.Many2one('res.currency', string='Moneda', default=lambda self: self.env.company.currency_id)
      authorized_by_id = fields.Many2one('res.users', string='Autorizado por', readonly=True)

      @api.depends('product_id', 'scrap_qty')
      def _compute_scrap_costs(self):
          for scrap in self:
              cost = scrap.product_id.standard_price or 0.0
              scrap.scrap_unit_cost = cost
              scrap.scrap_total_loss = cost * scrap.scrap_qty

      def action_validate(self):
          for scrap in self:
              if scrap.product_id.tracking == 'lot' and not scrap.lot_id:
                  raise ValidationError(_('Debe especificar el número de lote para dar de baja el medicamento %s.') % scrap.product_id.name)
              scrap.authorized_by_id = self.env.user.id
          return super(StockScrapMedicine, self).action_validate()
  ```

## 6. Acceptance Criteria
* **Scenario 1: Baja exitosa de lote de medicamentos caducados**
  * **Given** 8 frascos de "Jarabe para la Tos 120ml" Lote #JAR-2023 vencidos.
  * **When** El encargado registra el desecho seleccionando causa "Medicamento Caducado / Vencido", el lote correspondiente y valida la operación.
  * **Then** El sistema descuenta las 8 unidades del inventario vendible, las transfiere a la ubicación de desecho y calcula el valor de la pérdida económica ($).
* **Scenario 2: Bloqueo de baja sin selección de lote**
  * **Given** Un medicamento con seguimiento por lotes activado.
  * **When** Se intenta procesar la baja dejando el campo de lote vacío.
  * **Then** Odoo bloquea la acción arrojando un error de validación que exige la selección del lote a descartar.
* **Scenario 3: Registro del usuario que autorizó la baja**
  * **Given** Una merma validada por la administradora.
  * **When** Se consulta el registro de desecho.
  * **Then** El campo `authorized_by_id` debe registrar de forma inmutable el nombre del usuario y la fecha/hora de autorización.

## 7. Verification Plan
* **Automated Tests:**
  * Prueba unitaria en Python creando una baja de stock para un medicamento rastreado por lote, verificando el descuento de existencias y el cálculo automático de `scrap_total_loss`.
* **Manual Verification:**
  * Acceder al menú `Inventario > Operaciones > Desecho`, registrar una merma y verificar que el stock en mostrador disminuya mientras la ubicación de merma refleje las unidades descartadas.

## 8. Security and Privacy
* La validación de mermas está protegida para usuarios con rol `Encargado de Compras e Inventario` y `Administrador`.

## 9. Risks and Mitigation
* **Risk:** Reintroducción accidental al mostrador de medicamentos destinados a merma.
  * **Mitigation:** Identificar físicamente el área de cuarentena en la farmacia y registrar inmediatamente en el ERP la transferencia virtual.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/models/stock_scrap_medicine.py`.
* Extensión de vista en `views/stock_scrap_views.xml`.

## 11. Definition of Done (DoD)
* [x] Modelo `stock.scrap` extendido con causas farmacéuticas y cálculo de costo.
* [x] Obligatoriedad de asignación de lote validada.
* [x] Ubicación virtual de desecho configurada.
* [x] Pruebas unitarias aprobadas al 100%.
* [x] Aprobación del procedimiento de bajas por la administración de Farmacia Caryvil.
