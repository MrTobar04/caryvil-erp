# SPEC-6.2.1: Catálogo de Precios y Códigos de Proveedor

## 1. Objective
Estructurar y parametrizar la gestión de listas de precios de compra, códigos de referencia del fabricante y condiciones mínimas de pedido por proveedor mediante el modelo `product.supplierinfo` en Odoo para Farmacia Caryvil. Esta especificación permite registrar múltiples proveedores para un mismo medicamento, comparar costos unitarios entre diferentes laboratorios farmacéuticos (e.g., Laboratorios Vijosa vs Droguería Santa Lucía), fijar cantidades mínimas de adquisición y autocompletar automáticamente el precio pactado al generar órdenes de compra.

## 2. Scope
### 2.1. Included
* Extensión y personalización del modelo `product.supplierinfo` en `custom_addons/caryvil_erp/models/product_supplierinfo.py`:
  * `product_name` (Char): Nombre o denominación comercial del medicamento según el catálogo del laboratorio.
  * `product_code` (Char): Código de barras o código interno del artículo asignado por el proveedor.
  * `gross_price` (Monetary): Precio de catálogo o lista oficial del laboratorio (antes de descuentos comerciales). Formalizado en [ADR-0014](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/docs/adr/ADR-0014-desacoplamiento-precio-bruto-y-gestion-descuentos-proveedores.md).
  * `discount_percentage` (Float): Porcentaje de descuento comercial con cálculo reactivo no destructivo ni acumulativo.
  * `price` (Monetary): Precio de costo unitario neto acordado en USD ($).
  * `product_presentation` (Char): Presentación farmacéutica según empaque del laboratorio (e.g., Caja x 50 tabletas).
  * `min_qty` (Float): Cantidad mínima requerida por el laboratorio para aplicar el precio o escala de volumen (e.g., compra mínima de 10 cajas).
  * `delay` (Integer): Plazo de entrega garantizado en días para este producto específico.
  * `date_start` y `date_end` (Date): Periodo de vigencia de la lista de precios o convenio comercial.
* Inclusión y personalización de la tabla de proveedores dentro de la pestaña **"Compras"** (`Purchase`) de la vista formulario de medicamentos (`product.template`) mediante extensión XML en `views/product_supplierinfo_views.xml`.
* Autocompletado del precio de compra unitario en las líneas de Órdenes de Compra (`purchase.order.line`) basado en el proveedor seleccionado y la escala por cantidad (`min_qty`), validado mediante integración nativa con `purchase.order`.

### 2.2. Not Included (Out of Scope)
* Creación de listas de precios de venta para clientes finales (se gestiona en `SPEC-7.1.1` y `SPEC-9.1.1`).
* Liquidación y pagos de facturas de proveedor (gestionado en `SPEC-8.1.2`).

## 3. Context and Restrictions
* **Context:** Permite al encargado de compras y a la propietaria evaluar rápidamente cuál laboratorio ofrece el mejor costo y tiempo de entrega antes de emitir una orden de compra formal.
* **Restrictions:**
  * Un medicamento puede tener múltiples proveedores registrados, permitiendo comparar alternativas comerciales.
  * Los precios de compra (`gross_price`, `discount_percentage`, `price`, `product_presentation`) están estrictamente restringidos al grupo `caryvil_erp.group_caryvil_compras_inventario`, manteniéndose confidenciales para usuarios con rol `Cajero / Mostrador`.
  * Consulta de decisiones arquitectónicas y mitigación de degradación en descuentos: ver [ADR-0014](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/docs/adr/ADR-0014-desacoplamiento-precio-bruto-y-gestion-descuentos-proveedores.md).

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
  * `SPEC-2.2.1` (Definición de Roles y Grupos de Usuarios).
  * `SPEC-6.1.1` (Directorio y Gestión de Proveedores).
* **Definition of Ready (DoR):**
  * [x] Catálogo de proveedores registrado en el sistema.
  * [x] Listas de precios de compra referenciales recopiladas.

## 5. Design (Implementation Details)
* **Model Configuration (`models/product_supplierinfo.py`):**
  ```python
  from odoo import models, fields, api

  class ProductSupplierinfoCaryvil(models.Model):
      _inherit = "product.supplierinfo"

      product_presentation = fields.Char(string="Presentación Proveedor", help="Ej: Caja con 100 tabletas")
      gross_price = fields.Monetary(string="Precio Lista / Bruto", currency_field="currency_id")
      discount_percentage = fields.Float(string="% Descuento Comercial", default=0.0)

      @api.onchange("gross_price", "discount_percentage")
      def _onchange_pricing_caryvil(self):
          for record in self:
              if record.gross_price > 0:
                  discount = max(0.0, min(record.discount_percentage, 100.0))
                  record.price = record.gross_price * (1.0 - (discount / 100.0))
              elif record.price > 0 and not record.gross_price:
                  record.gross_price = record.price

      @api.onchange("price")
      def _onchange_price_sync_gross(self):
          for record in self:
              if record.price > 0 and record.discount_percentage == 0.0 and not record.gross_price:
                  record.gross_price = record.price
  ```
* **UI/UX Integration (`views/product_supplierinfo_views.xml`):**
  * Extensión sobre `product.product_supplierinfo_tree_view` insertando `product_presentation`, visibilidad de `min_qty`, `gross_price`, `discount_percentage` y `price` con protección de grupos de seguridad.

## 6. Acceptance Criteria
* **Scenario 1: Registro de múltiples proveedores para un mismo medicamento**
  * **Given** El medicamento "Amoxicilina 500mg (Caja x 50)".
  * **When** El encargado de compras agrega dos proveedores: "Laboratorios Vijosa" a $4.50 (entrega 2 días) y "Droguería Santa Lucía" a $4.80 (entrega 1 día).
  * **Then** Ambos registros deben quedar guardados en la tabla de proveedores, permitiendo consultar el comparativo de costos.
  * *Estado:* **[x] Cumplido y verificado** (`test_crear_supplierinfo_con_presentacion` y `test_multiples_proveedores_mismo_medicamento`).
* **Scenario 2: Autocompletado de precio en Orden de Compra**
  * **Given** Una Orden de Compra iniciada para "Laboratorios Vijosa".
  * **When** El usuario selecciona en las líneas el medicamento "Amoxicilina 500mg".
  * **Then** El sistema debe rellenar automáticamente el campo de costo unitario con `$4.50` sin requerir que el usuario lo digite manualmente.
  * *Estado:* **[x] Cumplido y verificado** (`test_autocompletado_precio_orden_compra`).
* **Scenario 3: Aplicación de precio por escala de volumen**
  * **Given** Un proveedor configurado con precio de $5.00 para cantidades < 10 cajas y $4.20 para cantidades >= 10 cajas.
  * **When** Se crea una orden por 12 cajas.
  * **Then** El sistema debe aplicar automáticamente el precio con descuento por volumen de `$4.20`.
  * *Estado:* **[x] Cumplido y verificado** (`test_precio_escala_volumen_min_qty`).

## 7. Verification Plan
* **Automated Tests:**
  * Suite automatizada en `tests/test_product_supplierinfo.py` cubriendo creación con presentación, múltiples proveedores por producto, cálculo determinista de descuentos, autocompletado en líneas de compra y resolución de escalas de volumen `min_qty`.
* **Manual Verification Runbook:**
  * Procedimiento paso a paso detallado en [Runbook SPEC-6.2.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/docs/runbooks/runbook-spec-6.2.1-catalogo-precios-proveedores.md) e integrado en [Guión de Pruebas Manuales - Flujo 6.2](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/docs/guias/guion-pruebas-manuales.md#flujo-62-catálogo-de-precios-y-condiciones-de-proveedores-spec-621).

## 8. Security and Privacy
* Los campos de costo y descuento comercial (`gross_price`, `discount_percentage`, `price`, `product_presentation`) están protegidos a nivel de vista con `groups="caryvil_erp.group_caryvil_compras_inventario"`.
* Los usuarios con rol `group_caryvil_cajero` no tienen visibilidad de los costos de adquisición al consultar la información de productos.

## 9. Risks and Mitigation
* **Risk:** Degradación acumulativa de descuentos comerciales en modificaciones sucesivas.
  * **Mitigation:** Implementación del campo `gross_price` y sincronización no destructiva descrita en [ADR-0014](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/docs/adr/ADR-0014-desacoplamiento-precio-bruto-y-gestion-descuentos-proveedores.md).

## 10. Deliverables & Config as Code
* [x] Archivo de modelo: `custom_addons/caryvil_erp/models/product_supplierinfo.py`.
* [x] Archivo de vistas: `custom_addons/caryvil_erp/views/product_supplierinfo_views.xml`.
* [x] Suite de pruebas automatizadas: `custom_addons/caryvil_erp/tests/test_product_supplierinfo.py`.
* [x] Registro de Decisión de Arquitectura: [ADR-0014](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/docs/adr/ADR-0014-desacoplamiento-precio-bruto-y-gestion-descuentos-proveedores.md).
* [x] Runbook de verificación: [docs/runbooks/runbook-spec-6.2.1-catalogo-precios-proveedores.md](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/docs/runbooks/runbook-spec-6.2.1-catalogo-precios-proveedores.md).

## 11. Definition of Done (DoD)
* [x] Modelo `product.supplierinfo` extendido con campos farmacéuticos y precio bruto.
* [x] Columnas integradas en la tabla de proveedores en la vista de medicamentos.
* [x] Autocompletado de precios y escalas de volumen en órdenes de compra validado.
* [x] Pruebas unitarias ejecutadas y aprobadas (5 tests en `test_product_supplierinfo.py`).
* [ ] Aprobación funcional final en sesión UAT con el equipo de Farmacia Caryvil.
