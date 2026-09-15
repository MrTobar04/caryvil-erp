# SPEC-7.1.1: Catálogo y Categorización de Medicamentos

## 1. Objective
Estructurar, modelar y personalizar la ficha técnica y categorización del catálogo de productos farmacéuticos en Odoo (`product.template` y `product.product`) para Farmacia Caryvil. Esta especificación adapta los atributos médicos indispensables: nombre comercial, principio activo, concentración/dosis, forma farmacéutica (tabletas, cápsulas, jarabes, inyectables, ungüentos), código de barras (EAN-13), categoría terapéutica (analgésicos, antibióticos, antihistamínicos, etc.), condición de venta (venta libre vs bajo receta) y precio de venta al público en USD ($).

## 2. Scope
### 2.1. Included
* Creación del modelo `caryvil.therapeutic.category` en `custom_addons/caryvil_erp/models/caryvil_medicine.py` para organizar las familias farmacológicas.
* Creación del modelo `caryvil.active.ingredient` para normalizar principios activos (e.g., Paracetamol, Amoxicilina, Loratadina).
* Extensión de `product.template` con campos médicos y comerciales:
  * `active_ingredient_id` (Many2one a `caryvil.active.ingredient`).
  * `therapeutic_category_id` (Many2one a `caryvil.therapeutic.category`).
  * `dosage_form` (Selection: `tableta`, `capsula`, `jarabe`, `suspension`, `inyectable`, `crema_unguento`, `gotas_oftalmicas`, `otro`).
  * `concentration` (Char: e.g., "500 mg", "125 mg / 5 ml", "1%").
  * `prescription_required` (Boolean: Indicador de medicamento bajo receta médica).
  * `barcode` (Char: Código de barras EAN-13 para lectura con escáner en caja).
  * `list_price` (Monetary: Precio de venta al público con IVA 13% incluido).
* Adaptación de la vista formulario de productos (`views/product_template_views.xml`) con pestaña "Información Farmacéutica".

### 2.2. Not Included (Out of Scope)
* Configuración de unidades de medida y factores de conversión (cubierto en `SPEC-7.1.2`).
* Gestión de números de lote y fechas de vencimiento (cubierto en `SPEC-7.2.1`).

## 3. Context and Restrictions
* **Context:** Es el núcleo del catálogo de Farmacia Caryvil, utilizado en ventas, compras, inventario y consultas en mostrador.
* **Restrictions:**
  * El código de barras debe ser único por producto (`_sql_constraints`).
  * Los medicamentos deben crearse por defecto con tipo almacenable (`detailed_type = 'product'`) y con trazabilidad por lotes habilitada.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
  * `SPEC-2.2.1` (Definición de Roles y Grupos de Usuarios).
* **Definition of Ready (DoR):**
  * [x] Listado de categorías terapéuticas y formas farmacéuticas estándar definido.
  * [x] Catálogo representativo de medicamentos de Farmacia Caryvil recopilado.

## 5. Design (Implementation Details)
* **Data Model (`models/caryvil_medicine.py`):**
  ```python
  from odoo import models, fields, api

  class CaryvilTherapeuticCategory(models.Model):
      _name = 'caryvil.therapeutic.category'
      _description = 'Categoría Terapéutica Farmacéutica'

      name = fields.Char(string='Categoría', required=True, index=True)
      code = fields.Char(string='Código ATC / Clave', size=10)
      description = fields.Text(string='Descripción / Uso Terapéutico')

  class CaryvilActiveIngredient(models.Model):
      _name = 'caryvil.active.ingredient'
      _description = 'Principio Activo'

      name = fields.Char(string='Nombre del Principio Activo', required=True, index=True)
      description = fields.Text(string='Acción Farmacológica')

  class ProductTemplateMedicine(models.Model):
      _inherit = 'product.template'

      detailed_type = fields.Selection(default='product')
      tracking = fields.Selection(default='lot')
      active_ingredient_id = fields.Many2one('caryvil.active.ingredient', string='Principio Activo', index=True)
      therapeutic_category_id = fields.Many2one('caryvil.therapeutic.category', string='Categoría Terapéutica', index=True)
      dosage_form = fields.Selection([
          ('tableta', 'Tableta / Comprimido'),
          ('capsula', 'Cápsula'),
          ('jarabe', 'Jarabe'),
          ('suspension', 'Suspensión Oral'),
          ('inyectable', 'Inyectable / Ampolla'),
          ('crema_unguento', 'Crema / Ungüento / Pomada'),
          ('gotas_oftalmicas', 'Gotas Oftálmicas / Óticas'),
          ('otro', 'Otro')
      ], string='Forma Farmacéutica', default='tableta')
      concentration = fields.Char(string='Concentración', help='Ej: 500 mg, 10 mg/ml')
      prescription_required = fields.Boolean(string='Requiere Receta Médica', default=False)
  ```

## 6. Acceptance Criteria
* **Scenario 1: Creación completa de medicamento**
  * **Given** El encargado de compras e inventario creando un nuevo producto.
  * **When** Registra: Nombre "Amoxicilina Vijosa 500mg", Principio Activo "Amoxicilina", Categoría "Antibióticos", Forma "Cápsula", Concentración "500 mg", Código "7412345678901", Precio Venta "$0.25".
  * **Then** El medicamento se almacena con tipo almacenable y seguimiento por lotes activado por defecto.
* **Scenario 2: Búsqueda por Principio Activo**
  * **Given** Un cliente solicitando cualquier medicamento que contenga "Paracetamol".
  * **When** El dependiente busca "Paracetamol" en el catálogo.
  * **Then** El sistema lista todas las presentaciones comerciales asociadas a dicho principio activo (e.g., Panadol, Acetaminofén MK, Winasorb).
* **Scenario 3: Alerta visual de medicamento bajo receta**
  * **Given** Un medicamento marcado con `prescription_required = True`.
  * **When** Se visualiza en mostrador.
  * **Then** Debe mostrar un distintivo visual de advertencia indicando que se debe solicitar prescripción médica antes de la dispensación.

## 7. Verification Plan
* **Automated Tests:**
  * Prueba unitaria en Python creando categorías, principios activos y medicamentos, verificando relaciones relacionales y unicidad de códigos de barra.
* **Manual Verification:**
  * Navegar a `Inventario > Medicamentos > Crear` y validar los selectores y la pestaña de datos médicos.

## 8. Security and Privacy
* Los cajeros tienen permisos de lectura para consulta y venta; la creación y edición está reservada para inventario y administración.

## 9. Risks and Mitigation
* **Risk:** Falta de estandarización en la digitación de concentraciones (e.g., "500mg" vs "500 mg").
  * **Mitigation:** Uso de campos estandarizados y textos de ayuda (*placeholders*) descriptivos en la interfaz.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/models/caryvil_medicine.py`.
* Archivo `custom_addons/caryvil_erp/views/caryvil_medicine_views.xml`.
* Archivo `custom_addons/caryvil_erp/views/product_template_views.xml`.

## 11. Definition of Done (DoD)
* [ ] Modelos de categorías terapéuticas y principios activos implementados.
* [ ] Extensión de `product.template` con campos farmacéuticos configurada.
* [ ] Trazabilidad por lotes (`tracking = 'lot'`) predeterminada en nuevos medicamentos.
* [ ] Pruebas unitarias aprobadas al 100%.
* [ ] Validación de la ficha médica con la farmacéutica responsable.
