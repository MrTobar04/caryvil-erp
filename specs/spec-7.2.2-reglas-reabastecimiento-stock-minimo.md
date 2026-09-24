# SPEC-7.2.2: Reglas de Reabastecimiento y Stock Mínimo

## 1. Objective
Parametrizar y automatizar las reglas de inventario de seguridad y puntos de reorden (`stock.warehouse.orderpoint`) para los medicamentos de Farmacia Caryvil. Esta especificación define los niveles mínimos y máximos de existencias para cada fármaco según su rotación histórica, calculando automáticamente las cantidades sugeridas de reposición y generando borradores de solicitud de abastecimiento para evitar quiebres de stock en mostrador.

## 2. Scope
### 2.1. Included
* Parametrización del modelo `stock.warehouse.orderpoint` en `custom_addons/caryvil_erp/models/stock_reordering_rules.py`:
  * `product_min_qty` (Float): Nivel mínimo de seguridad de existencias (Punto de Reorden).
  * `product_max_qty` (Float): Nivel máximo objetivo de existencias.
  * `qty_multiple` (Float): Lote mínimo de compra o múltiplo de empaque del proveedor (e.g., múltiplos de 5 cajas).
  * `trigger` (Selection): Disparo manual para revisión o automático para generación de borrador de presupuesto en Compras.
* Cálculo del reabastecimiento: `Cantidad Sugerida = product_max_qty - (qty_available + qty_incoming - qty_outgoing)`.
* Pestaña "Niveles de Stock y Reorden" en la vista de producto con configuración simplificada.
* Integración con el widget de alertas de stock crítico del Dashboard (`SPEC-4.2.1`).

### 2.2. Not Included (Out of Scope)
* Generación de órdenes de compra definitivas sin validación humana del encargado (se generan en estado borrador `draft`).

## 3. Context and Restrictions
* **Context:** Asegura la continuidad operativa de la farmacia para medicamentos de alta demanda (como analgésicos, antihipertensivos y antibióticos de primera línea).
* **Restrictions:**
  * Las reglas de reorden deben respetar la unidad de medida de compra (`uom_po_id`) del medicamento.
  * Solo los usuarios con rol `Encargado de Compras e Inventario` o `Administrador` pueden modificar los umbrales mínimos y máximos.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-7.1.1` (Catálogo y Categorización de Medicamentos).
  * `SPEC-7.1.2` (Gestión de Unidades de Medida Farmacéuticas).
  * `SPEC-6.2.1` (Catálogo de Precios y Códigos de Proveedor).
* **Definition of Ready (DoR):**
  * [x] Listado de medicamentos clave con sus niveles de consumo mensual estimado.
  * [x] Proveedores habituales configurados para cada producto.

## 5. Design (Implementation Details)
* **Reordering Model Extension (`models/stock_reordering_rules.py`):**
  ```python
  from odoo import models, fields, api

  class StockWarehouseOrderpointMedicine(models.Model):
      _inherit = 'stock.warehouse.orderpoint'

      suggested_replenishment_qty = fields.Float(
          string='Cantidad Sugerida a Comprar',
          compute='_compute_suggested_qty'
      )

      @api.depends('product_id', 'product_min_qty', 'product_max_qty')
      def _compute_suggested_qty(self):
          for rule in self:
              virtual_stock = rule.product_id.virtual_available
              if virtual_stock < rule.product_min_qty:
                  needed = rule.product_max_qty - virtual_stock
                  # Ajustar al múltiplo de compra si aplica
                  if rule.qty_multiple > 1:
                      remainder = needed % rule.qty_multiple
                      if remainder > 0:
                          needed += (rule.qty_multiple - remainder)
                  rule.suggested_replenishment_qty = max(needed, 0.0)
              else:
                  rule.suggested_replenishment_qty = 0.0
  ```

## 6. Acceptance Criteria
* **Scenario 1: Cálculo de cantidad sugerida ante descenso de existencias**
  * **Given** El medicamento "Loratadina 10mg" con Mínimo = 10 cajas, Máximo = 30 cajas, Múltiplo = 5 cajas y Stock Actual = 6 cajas.
  * **When** Se evalúa la regla de reabastecimiento.
  * **Then** El sistema calcula un déficit de 24 cajas y sugiere una compra redondeada al múltiplo de `25 cajas`.
* **Scenario 2: Generación de borrador de compra agrupado**
  * **Given** Tres medicamentos del proveedor "Laboratorios Vijosa" con stock por debajo del mínimo.
  * **When** El encargado de compras ejecuta la acción "Calcular Reorden de Compras".
  * **Then** Odoo genera una única Solicitud de Presupuesto (RFQ) borrador para Vijosa con las 3 líneas de medicamentos y sus cantidades sugeridas.
* **Scenario 3: No generar sugerencia si el stock es suficiente**
  * **Given** Un producto con Mínimo = 15 y Stock Actual = 22.
  * **When** Se consulta la regla de reorden.
  * **Then** La cantidad sugerida debe ser `0` y no debe disparar órdenes de compra.

## 7. Verification Plan
* **Automated Tests:**
  * Prueba unitaria en Python verificando la fórmula de cálculo de `suggested_replenishment_qty` con y sin múltiplos de compra.
* **Manual Verification:**
  * Simular una venta que baje el stock de un producto por debajo del mínimo y verificar que aparezca en el planificador de compras.

## 8. Security and Privacy
* La parametrización de niveles de stock está protegida contra modificaciones accidentales por parte de cajeros.

## 9. Risks and Mitigation
* **Risk:** Compras excesivas de productos de baja rotación por configurar máximos irreales.
  * **Mitigation:** Revisión periódica de reglas de reorden sugeridas en el Dashboard de Inicio.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/models/stock_reordering_rules.py`.
* Extensión de vistas en `views/product_template_views.xml`.

## 11. Definition of Done (DoD)
* [x] Reglas de reorden y cálculo de sugeridos implementadas.
* [x] Agrupación por proveedor en borradores de compra validada.
* [x] Pruebas unitarias aprobadas al 100%.
* [x] Aprobación de los parámetros de stock mínimo por la propietaria de Caryvil.
