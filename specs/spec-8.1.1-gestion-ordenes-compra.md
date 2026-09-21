# SPEC-8.1.1: Gestión de Órdenes de Compra

## 1. Objective
Modelar, configurar e implementar el flujo de gestión del ciclo de vida de **Órdenes de Compra (PO)** en Odoo (`purchase.order` y `purchase.order.line`) para Farmacia Caryvil. Esta especificación permite la creación ágil de solicitudes de cotización a laboratorios y droguerías, el cálculo automático de costos e impuestos salvadoreños (IVA 13%), la fijación de condiciones de entrega y plazos de pago, y la confirmación formal del pedido para iniciar el proceso de abastecimiento de medicamentos.

## 2. Scope
### 2.1. Included
* Extensión del modelo `purchase.order` y `purchase.order.line` en `custom_addons/caryvil_erp/models/purchase_order_medicine.py`:
  * Ciclo de estados formal: `draft` (Solicitud de Presupuesto / RFQ) ➔ `sent` (Enviado al Laboratorio) ➔ `purchase` (Orden de Compra Confirmada) ➔ `done` (Completada tras recepción) ➔ `cancel` (Cancelada).
  * `commercial_terms_id` (Many2one o Selection): Condiciones de pago pactadas (Contado, Crédito 15/30/45/60 días).
  * `expected_delivery_date` (Date): Fecha límite esperada de entrega de los medicamentos en farmacia.
  * `notes_reception` (Text): Requerimientos especiales de calidad (e.g., "Vigencia mínima de 18 meses para lotes").
  * `laboratory_id` (Many2one `res.partner`, related a `partner_id.commercial_partner_id`, store=True): Empresa/Laboratorio a la que pertenece el vendedor (`partner_id`) seleccionado en la orden. Se deriva automáticamente de la jerarquía Empresa/Vendedor definida en `SPEC-6.1.1` (`parent_id`), no es un campo independiente editable.
  * Descuento por línea (`Descuento %`): se usa el campo nativo `discount` de `purchase.order.line` (Odoo 17 Community lo incluye de fábrica, con `price_unit_discounted` calculado) — no requiere campo custom.
* Autocompletado de impuestos locales: Aplicación del IVA (13%) salvadoreño sobre las líneas de compra gravadas.
* Cálculo aritmético automático: Subtotal neto, IVA total desglosado y Total de la orden en USD ($).
* Envío de la orden de compra en formato PDF por correo electrónico directamente desde Odoo al contacto comercial del laboratorio. (NO APLICA)
* Restricción de permisos: El `Encargado de Compras e Inventario` puede elaborar y confirmar órdenes; el `Administrador / Propietaria` tiene acceso irrestricto de aprobación y anulación.

### 2.2. Not Included (Out of Scope)
* Verificación física y registro de lotes recibidos (cubierto en `SPEC-8.2.1`).
* Actualización de existencias en el inventario (cubierto en `SPEC-8.2.2`).
* Gestión de discrepancias y entregas parciales (cubierto en `SPEC-8.2.3`).

## 3. Context and Restrictions
* **Context:** Estandariza el proceso de adquisición de medicamentos de Farmacia Caryvil, reemplazando las llamadas informales o notas manuales por un registro digital auditable y con trazabilidad de costos.
* **Restrictions:**
  * No se puede confirmar una orden de compra si no tiene al menos una línea de medicamento con cantidad mayor a cero.
  * El proveedor seleccionado debe estar catalogado como proveedor farmacéutico (`is_pharmacy_vendor = True` o `supplier_rank > 0`).

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
  * `SPEC-2.2.1` (Definición de Roles y Grupos de Usuarios).
  * `SPEC-6.1.1` (Directorio y Gestión de Proveedores).
  * `SPEC-6.2.1` (Catálogo de Precios y Códigos de Proveedor).
  * `SPEC-7.1.1` (Catálogo y Categorización de Medicamentos).
  * `SPEC-7.1.2` (Gestión de Unidades de Medida Farmacéuticas).
* **Definition of Ready (DoR):**
  * [x] Catálogo de medicamentos y proveedores registrado en Odoo.
  * [x] Impuesto de IVA (13%) configurado en el sistema contable base.

## 5. Design (Implementation Details)
* **Model Configuration (`models/purchase_order_medicine.py`):**
  ```python
  from odoo import models, fields, api, _
  from odoo.exceptions import ValidationError

  class PurchaseOrderMedicine(models.Model):
      _inherit = 'purchase.order'

      reception_instructions = fields.Char(
          string='Instrucciones de Recepción',
          default='Requerir lotes con fecha de caducidad mayor a 18 meses.'
      )

      def button_confirm(self):
          for order in self:
              if not order.order_line:
                  raise ValidationError(_('No puede confirmar una orden de compra sin líneas de medicamentos.'))
              for line in order.order_line:
                  if line.product_qty <= 0:
                      raise ValidationError(_('La cantidad del medicamento %s debe ser mayor a 0.') % line.product_id.name)
          return super(PurchaseOrderMedicine, self).button_confirm()
  ```
* **View Structure (`views/purchase_order_views.xml`):**
  * Formulario de compra con selector filtrado de laboratorios, tabla de líneas con medicamentos, presentación (cajas/unidades), precios pactados y bloque lateral con IVA y Total.

## 6. Acceptance Criteria
* **Scenario 1: Creación y confirmación de Orden de Compra formal**
  * **Given** El encargado de compras creando una orden para "Laboratorios Vijosa".
  * **When** Agrega 10 Cajas de "Amoxicilina 500mg" a $4.50 c/u (Subtotal $45.00 + IVA $5.85 = $50.85) y presiona "Confirmar Pedido".
  * **Then** La orden pasa al estado `purchase` (Orden de Compra), bloquea la edición de precios y genera automáticamente el albarán de recepción de entrada en estado `assigned`.
* **Scenario 2: Bloqueo de confirmación sin productos**
  * **Given** Un borrador de compra sin líneas registradas.
  * **When** Se intenta confirmar el pedido.
  * **Then** El sistema arroja un error de validación impidiendo el cambio de estado.
* **Scenario 3: Envío de PDF por correo electrónico al proveedor** (NO APLICA)
  * **Given** Una orden de compra confirmada.
  * **When** El usuario presiona "Enviar por Correo".
  * **Then** Odoo adjunta el PDF de la orden de compra (`SPEC-3.3.2`) en un correo electrónico con plantilla prediseñada dirigido al email del ejecutivo de ventas.

## 7. Verification Plan
* **Automated Tests:**
  * Prueba unitaria en Python creando una orden de compra con IVA (13%), validando que `amount_untaxed == 45.0`, `amount_tax == 5.85`, `amount_total == 50.85` y que `button_confirm()` genere el albarán en `stock.picking`.
* **Manual Verification:**
  * Crear una orden en la interfaz web de Odoo, confirmarla y verificar que aparezca el botón inteligente de "Recepción" en la parte superior derecha.

## 8. Security and Privacy
* Permisos de creación y modificación restringidos a los roles `Encargado de Compras e Inventario` y `Administrador`. Los cajeros no tienen acceso al módulo de compras.

## 9. Risks and Mitigation
* **Risk:** Emisión de órdenes duplicadas al mismo laboratorio por falta de coordinación.
  * **Mitigation:** Alertas visuales en Odoo si existe otra orden en estado borrador o confirmada para el mismo proveedor en los últimos 3 días.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/models/purchase_order_medicine.py`.
* Extensión de vista `views/purchase_order_views.xml`.
* Registro del modelo en `models/__init__.py`.

## 11. Definition of Done (DoD)
* [ ] Ciclo de estados de la Orden de Compra configurado y operativo.
* [ ] Cálculo exacto de IVA (13%) y subtotales en USD ($) validado.
* [ ] Generación automática del albarán de recepción vinculada.
* [ ] Pruebas unitarias aprobadas al 100%.
* [ ] Aprobación del flujo por el equipo de compras de Farmacia Caryvil.
