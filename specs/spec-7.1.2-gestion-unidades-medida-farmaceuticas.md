# SPEC-7.1.2: Gestión de Unidades de Medida Farmacéuticas

## 1. Objective
Parametrizar y estructurar las categorías y unidades de medida (UoM) específicas del sector farmacéutico en Odoo (`uom.category` y `uom.uom`) para Farmacia Caryvil. Esta especificación permite comprar medicamentos a laboratorios por cajas o bultos de gran volumen (Unidad de Medida de Compra - `uom_po_id`) y gestionar el almacenamiento y la dispensación al menudeo en mostrador por blísteres o pastillas sueltas (Unidad de Medida de Venta/Inventario - `uom_id`), garantizando la conversión automática y precisa de cantidades en el inventario.

## 2. Scope
### 2.1. Included
* Creación de la categoría de unidad de medida `uom_category_pharmacy` ("Unidades Farmacéuticas") en `custom_addons/caryvil_erp/data/pharmacy_uom_data.xml`.
* Definición de las unidades de medida base y derivadas con sus respectivos ratios de conversión:
  * **Unidad Base:** `Unidad / Pastilla / Cápsula suelta` (Unidad de referencia del inventario).
  * **Blíster:** `Blíster x 10` (Ratio: 10 unidades base), `Blíster x 4` (Ratio: 4 unidades base).
  * **Cajas:** `Caja x 20` (Ratio: 20 unidades), `Caja x 50` (Ratio: 50 unidades), `Caja x 100` (Ratio: 100 unidades).
  * **Presentaciones Líquidas/Semisólidas:** `Frasco 60ml`, `Frasco 120ml`, `Tubo / Pomada`, `Ampolla / Vial`.
* Habilitación de la directiva nativa de Odoo para selección dual: Unidad de Medida estándar (`uom_id`) y Unidad de Medida de Compra (`uom_po_id`) en la ficha de medicamentos.
* Conversión matemática automática en la recepción de mercadería (e.g., recibir 5 cajas x 100 incrementa automáticamente en 500 unidades el stock disponible).

### 2.2. Not Included (Out of Scope)
* Configuración de listas de precios mayoristas por caja (cubierto en `SPEC-6.2.1` y `SPEC-9.1.1`).

## 3. Context and Restrictions
* **Context:** Resuelve la discrepancia operativa común en farmacias donde los laboratorios distribuyen en empaques maestros pero el paciente en mostrador adquiere blísteres o tabletas individuales.
* **Restrictions:**
  * Las unidades de una misma categoría deben mantener relaciones numéricas exactas para evitar fracciones erróneas en inventario.
  * No se debe permitir la venta de fracciones menores a la unidad base (1 pastilla).

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
  * `SPEC-7.1.1` (Catálogo y Categorización de Medicamentos).
* **Definition of Ready (DoR):**
  * [x] Presentaciones comerciales más habituales en Farmacia Caryvil analizadas.
  * [x] Módulo estándar `uom` de Odoo identificado como dependencia.

## 5. Design (Implementation Details)
* **Data Definition (`data/pharmacy_uom_data.xml`):**
  ```xml
  <?xml version="1.0" encoding="utf-8"?>
  <odoo>
      <data noupdate="1">
          <!-- Categoría Farmacéutica -->
          <record id="uom_category_pharmacy_units" model="uom.category">
              <field name="name">Presentaciones Farmacéuticas</field>
          </record>

          <!-- Unidad de Referencia Base -->
          <record id="uom_unit_pill" model="uom.uom">
              <field name="name">Unidad / Pastilla</field>
              <field name="category_id" ref="uom_category_pharmacy_units"/>
              <field name="uom_type">reference</field>
              <field name="factor_inv" eval="1.0"/>
              <field name="rounding" eval="1.0"/>
          </record>

          <!-- Blíster x 10 -->
          <record id="uom_blister_10" model="uom.uom">
              <field name="name">Blíster x 10 unidades</field>
              <field name="category_id" ref="uom_category_pharmacy_units"/>
              <field name="uom_type">bigger</field>
              <field name="factor_inv" eval="10.0"/>
              <field name="rounding" eval="0.01"/>
          </record>

          <!-- Caja x 100 -->
          <record id="uom_box_100" model="uom.uom">
              <field name="name">Caja x 100 unidades</field>
              <field name="category_id" ref="uom_category_pharmacy_units"/>
              <field name="uom_type">bigger</field>
              <field name="factor_inv" eval="100.0"/>
              <field name="rounding" eval="0.01"/>
          </record>
      </data>
  </odoo>
  ```

## 6. Acceptance Criteria
* **Scenario 1: Configuración de producto con compra en caja y venta en unidad**
  * **Given** El medicamento "Acetaminofén 500mg".
  * **When** Se configura con UoM Compra = "Caja x 100" y UoM Inventario/Venta = "Unidad / Pastilla".
  * **Then** El sistema permite emitir órdenes de compra en cajas y dispensar en caja por unidades o blísteres.
* **Scenario 2: Conversión automática al recibir mercadería**
  * **Given** Una orden de compra por `2 Cajas x 100` de Acetaminofén.
  * **When** Se valida el albarán de recepción en bodega.
  * **Then** El inventario debe registrar un incremento exacto de `200 Unidades / Pastillas`.
* **Scenario 3: Descuento en mostrador por blíster**
  * **Given** Un stock de 200 pastillas en mostrador.
  * **When** Un cliente compra `1 Blíster x 10`.
  * **Then** El sistema deduce automáticamente 10 unidades del stock físico, dejando 190 pastillas disponibles.

## 7. Verification Plan
* **Automated Tests:**
  * Test unitario en Python verificando la conversión de cantidades entre `uom_box_100` y `uom_unit_pill` mediante el método `uom._compute_quantity()`.
* **Manual Verification:**
  * Crear un producto con UoMs farmacéuticas, simular una compra de 1 caja y validar que el stock muestre 100 unidades.

## 8. Security and Privacy
* La creación o modificación de factores de conversión está restringida exclusivamente a usuarios con rol `Administrador` para evitar descalces contables.

## 9. Risks and Mitigation
* **Risk:** Confusión del cajero al registrar ventas en cajas en lugar de tabletas sueltas.
  * **Mitigation:** Mostrar siempre la unidad de medida explícita en la línea de venta de mostrador (e.g., "1 Blíster" vs "1 Pastilla").

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/data/pharmacy_uom_data.xml`.
* Inclusión del archivo en la sección `data` de `__manifest__.py`.

## 11. Definition of Done (DoD)
* [x] Categorías y unidades de medida farmacéuticas creadas en Odoo (sólidos, líquidos y semisólidos).
* [x] Ratios de conversión de cajas y blísteres comprobados.
* [x] Conversión automática en compras y ventas validada.
* [x] Pruebas unitarias aprobadas al 100% (13/13 tests en TestPharmacyUom).
* [ ] Aprobación por la administración de Farmacia Caryvil.
