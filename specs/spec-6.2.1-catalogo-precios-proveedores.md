# SPEC-6.2.1: Catálogo de Precios y Códigos de Proveedor

## 1. Objective
Estructurar y parametrizar la gestión de listas de precios de compra, códigos de referencia del fabricante y condiciones mínimas de pedido por proveedor mediante el modelo `product.supplierinfo` en Odoo para Farmacia Caryvil. Esta especificación permite registrar múltiples proveedores para un mismo medicamento, comparar costos unitarios entre diferentes laboratorios farmacéuticos (e.g., Laboratorios Vijosa vs Laboratorios López), fijar cantidades mínimas de adquisición y autocompletar automáticamente el precio pactado al generar órdenes de compra.

## 2. Scope
### 2.1. Included
* Extensión y personalización del modelo `product.supplierinfo` en `custom_addons/caryvil_erp/models/product_supplierinfo.py`:
  * `product_name` (Char): Nombre o denominación comercial del medicamento según el catálogo del laboratorio.
  * `product_code` (Char): Código de barras o código interno del artículo asignado por el proveedor.
  * `price` (Monetary): Precio de costo unitario neto acordado en USD ($).
  * `min_qty` (Float): Cantidad mínima requerida por el laboratorio para aplicar el precio (e.g., compra mínima de 5 cajas).
  * `delay` (Integer): Plazo de entrega garantizado en días para este producto específico.
  * `date_start` y `date_end` (Date): Periodo de vigencia de la lista de precios o convenio comercial.

  > **(ACTUAL)** se agregó al modelo 2 campos nuevos: `product_presentation` (Char) y `discount_percentage` (Float, con recálculo automático del precio).

* Inclusión de la pestaña **"Proveedores y Costos"** dentro de la vista formulario de medicamentos (`product.template`).

  > **(ACTUAL)** No se creó una pestaña nueva llamada "Proveedores y Costos". Se reutilizó la pestaña **"Purchase"** (Compras) que Odoo ya trae de fábrica en la ficha de cada producto, agregándole ahí las 2 columnas nuevas (`product_presentation`, `discount_percentage`). El nombre de la pestaña no coincide con lo aquí escrito — pendiente decidir si se renombra o se deja así.

* Mecanismo de autocompletado del precio de compra unitario en las líneas de Órdenes de Compra (`purchase.order.line`) basado en el proveedor seleccionado y la cantidad solicitada.

  > **(ACTUAL)** No implementado ni verificado todavía. Es funcionalidad nativa de Odoo (`purchase.order` ya autocompleta desde `product.supplierinfo`), pero no se puede probar porque las Órdenes de Compra no existen aún (`SPEC-8.1.1`, bloqueada por `SPEC-7.1.1`/`7.1.2`). Queda pendiente de verificación cuando esas specs avancen.

### 2.2. Not Included (Out of Scope)
* Creación de listas de precios de venta para clientes finales (se gestiona en `SPEC-7.1.1` y `SPEC-9.1.1`).
* Liquidación de facturas de proveedor (cubierto en el módulo de compras nativo de Odoo).

## 3. Context and Restrictions
* **Context:** Permite a la propietaria evaluar rápidamente cuál laboratorio ofrece el mejor costo de adquisición para un principio activo (e.g., Acetaminofén o Amoxicilina) antes de emitir una orden de compra formal.
* **Restrictions:**
  * Un medicamento puede tener múltiples proveedores registrados, pero debe existir un proveedor principal o preferente por defecto (`sequence = 1`).
  * Los precios de compra no deben ser visibles para usuarios con rol exclusivo de `Cajero`.

  > **(ACTUAL)** Implementado: el campo nativo `price` y los 2 campos nuevos (`product_presentation`, `discount_percentage`) están restringidos al grupo `caryvil_erp.group_caryvil_compras_inventario`. No se probó manualmente con un usuario Cajero real.

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
      _inherit = 'product.supplierinfo'

      product_presentation = fields.Char(string='Presentación Proveedor', help='Ej: Caja con 100 tabletas')
      discount_percentage = fields.Float(string='% Descuento Comercial', default=0.0)

      @api.onchange('discount_percentage')
      def _onchange_discount(self):
          if self.discount_percentage > 0 and self.price > 0:
              self.price = self.price * (1 - (self.discount_percentage / 100.0))
  ```
* **UI/UX Integration:**
  * Pestaña "Proveedores" en la ficha del medicamento con tabla editable: Nombre del Laboratorio, Código Proveedor, Cantidad Mínima, Plazo de Entrega y Precio Unitario de Costo ($).

  > **(ACTUAL)** De esas columnas, "Nombre del Laboratorio" y "Precio" se ven por defecto. "Código Proveedor" (`product_code`), "Cantidad Mínima" (`min_qty`) y las fechas de vigencia quedan **ocultas por defecto** (`optional="hide"` en la vista base de Odoo)

## 6. Acceptance Criteria
* **Scenario 1: Registro de múltiples proveedores para un mismo medicamento**
  * **Given** El medicamento "Amoxicilina 500mg (Caja x 50)".
  * **When** El encargado de compras agrega dos proveedores: "Laboratorios Vijosa" a $4.50 (entrega 2 días) y "Droguería Santa Lucía" a $4.80 (entrega 1 día).
  * **Then** Ambos registros deben quedar guardados en la pestaña "Proveedores", permitiendo consultar el comparativo de costos.
* **Scenario 2: Autocompletado de precio en Orden de Compra**
  * **Given** Una Orden de Compra iniciada para "Laboratorios Vijosa".
  * **When** El usuario selecciona en las líneas el medicamento "Amoxicilina 500mg".
  * **Then** El sistema debe rellenar automáticamente el campo de costo unitario con `$4.50` sin requerir que el usuario lo digite manualmente.
* **Scenario 3: Aplicación de precio por escala de volumen**
  * **Given** Un proveedor configurado con precio de $5.00 para cantidades < 10 cajas y $4.20 para cantidades >= 10 cajas.
  * **When** Se crea una orden por 12 cajas.
  * **Then** El sistema debe aplicar automáticamente el precio con descuento por volumen de `$4.20`.

> **(ACTUAL)** Escenarios 2 y 3 **no verificados** — dependen de que existan Órdenes de Compra (`SPEC-8.1.1`). Solo se probó (con pruebas automatizadas) el Escenario 1: crear un `product.supplierinfo` con datos y que un mismo medicamento admita varios proveedores.

## 7. Verification Plan
* **Automated Tests:**
  * Test unitario en Python creando un `product.supplierinfo` para un producto de prueba y verificando que al instanciar una línea de orden de compra con ese proveedor el precio retornado coincida con el configurado.
* **Manual Verification:**
  * Crear una orden de compra, alternar entre dos proveedores distintos y comprobar que el precio de línea cambie de acuerdo a la lista de cada laboratorio.

> **(ACTUAL)** Se escribieron 3 pruebas en `tests/test_product_supplierinfo.py` (todas pasando): crear un proveedor con presentación y precio, múltiples proveedores para un mismo medicamento, y que el % de descuento recalcule el precio. La prueba de "instanciar una línea de orden de compra" **no se hizo** — no existe `purchase.order.line` en el sistema todavía. La verificación manual tampoco se hizo (no hay Órdenes de Compra que crear).

## 8. Security and Privacy
* La pestaña de proveedores y costos está protegida para ser visible únicamente por `Encargado de Compras e Inventario` y `Administrador`.

> **(ACTUAL)** No se restringió la pestaña completa (sigue rigiéndose por el grupo nativo `purchase.group_purchase_user` de Odoo, fuera del alcance de esta spec). Lo que sí se restringió puntualmente a `group_caryvil_compras_inventario` son los campos de precio: `price` (nativo), `product_presentation` y `discount_percentage`.

## 9. Risks and Mitigation
* **Risk:** Variaciones frecuentes de precios por parte de los laboratorios que dejen obsoletos los costos registrados.
  * **Mitigation:** Actualizar automáticamente el registro de `product.supplierinfo` si al confirmar una recepción de compra el usuario modifica el precio unitario acordado.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/models/product_supplierinfo.py`.
* Extensión de vista `views/product_template_views.xml` con la pestaña de proveedores.
* Inclusión del modelo en `models/__init__.py`.

> **(ACTUAL)** El archivo de vista real se llama `views/product_supplierinfo_views.xml` (no `product_template_views.xml`), porque termina inhereditando la vista de lista `product.supplierinfo`, no un formulario de `product.template` nuevo. También se agregó `tests/test_product_supplierinfo.py`

## 11. Definition of Done (DoD)
* [ ] Modelo `product.supplierinfo` extendido con campos farmacéuticos.
* [ ] Pestaña de proveedores integrada en la vista de medicamentos.
* [ ] Autocompletado de precios en órdenes de compra validado.
* [ ] Pruebas unitarias ejecutadas y aprobadas.
* [ ] Aprobación funcional por el equipo de compras de Caryvil.

> **(ACTUAL)** Estado real de cada punto:
> * [x] Modelo extendido (`product_presentation`, `discount_percentage`).
> * [x] Columnas integradas en la tabla de proveedores existente (no una pestaña nueva).
> * [ ] Autocompletado de precios — bloqueado hasta `SPEC-8.1.1`.
> * [x] Pruebas unitarias — 3 pruebas propias + 9 de `SPEC-6.1.1`, las 12 pasando.
> * [ ] Aprobación del negocio — pendiente, es del equipo de Caryvil, no técnica.
