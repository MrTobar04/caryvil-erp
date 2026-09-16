# SPEC-3.3.2: Plantilla de Reporte para Órdenes de Compra

## 1. Objective
Diseñar, estructurar e implementar la plantilla de reporte QWeb en Odoo para la emisión formal en formato PDF de **Órdenes de Compra (PO)** dirigidas a laboratorios farmacéuticos y droguerías proveedoras de Farmacia Caryvil. Esta especificación estandariza el documento oficial de abastecimiento, incorporando el membrete corporativo, datos fiscales del proveedor, detalle de medicamentos solicitados con sus respectivas presentaciones y unidades de medida (caja, blíster, frasco), precios unitarios pactados, subtotales, desglose de impuestos, condiciones de pago y firmas autorizadas.

## 2. Scope
### 2.1. Included
* Creación de la plantilla QWeb `custom_addons/caryvil_erp/reports/report_purchase_order.xml`.
* Definición de la acción de reporte `ir.actions.report` vinculada al modelo `purchase.order`.
* Encabezado corporativo: Logotipo de Farmacia Caryvil, Información de contacto en Soyapango, Número correlativo de la orden (e.g., `OC-2026-0012`) y Fecha de emisión.
* Bloque de datos del laboratorio/proveedor: Razón Social, NIT/NRC, Nombre del contacto/vendedor, Teléfono, Correo electrónico y Dirección fiscal.
* Tabla estructurada de requerimiento: Código interno/proveedor, Descripción del medicamento (principio activo y concentración), Presentación/UoM (Caja, Frasco, Blíster), Cantidad solicitada, Precio unitario de costo ($) y Subtotal.
* Sección de liquidación económica: Subtotal neto, IVA (13%), Total de la orden en USD ($) y Términos comerciales (e.g., "Crédito 30 días", "Contado contra entrega").
* Bloque de validación y control: Fecha estimada de entrega solicitada, Notas e instrucciones de recepción (e.g., "Requerido lote con vigencia mayor a 18 meses"), y Firmas de "Elaborado por" y "Autorizado por".

### 2.2. Not Included (Out of Scope)
* Generación de órdenes de compra automáticas sin revisión previa del encargado (cubierto en `SPEC-7.2.2`).
* Registro de recepción física de mercadería (cubierto en `SPEC-8.2.1`).

## 3. Context and Restrictions
* **Context:** Es el documento oficial que Farmacia Caryvil envía por correo electrónico o entrega a los agentes de venta de laboratorios para formalizar el pedido de reabastecimiento de medicamentos.
* **Restrictions:**
  * Debe estructurarse en formato de hoja estándar Carta / A4 con márgenes uniformes.
  * Debe generar un documento PDF profesional y nítido para su envío digital o archivo físico.
  * Los precios y subtotales deben reflejar exactamente los términos de costo pactados en la negociación con el proveedor.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
  * `SPEC-3.1.1` (Personalización de Marca y Tema Visual).
* **Definition of Ready (DoR):**
  * [x] Estructura del formato de orden de compra aprobada por la administración de la farmacia.
  * [x] Catálogo de laboratorios y distribuidores definido para pruebas de impresión.

## 5. Design (Implementation Details)
* **Report Action (`reports/purchase_order_report_action.xml`):**
  ```xml
  <?xml version="1.0" encoding="utf-8"?>
  <odoo>
      <record id="action_report_caryvil_purchase_order" model="ir.actions.report">
          <field name="name">Orden de Compra Caryvil</field>
          <field name="model">purchase.order</field>
          <field name="report_type">qweb-pdf</field>
          <field name="report_name">caryvil_erp.report_purchase_order_template</field>
          <field name="report_file">caryvil_erp.report_purchase_order_template</field>
          <field name="binding_model_id" ref="purchase.model_purchase_order"/>
          <field name="binding_type">report</field>
          <field name="paperformat_id" ref="base.paperformat_us_letter"/>
      </record>
  </odoo>
  ```
* **QWeb Layout Highlights:**
  * Tabla con bordes limpios y encabezado en color azul institucional (`#004085`) con texto blanco.
  * Filas alternadas para facilitar la lectura de pedidos extensos de medicamentos.
  * Sección inferior con recuadros para firma del encargado de compras y sello de autorización de Farmacia Caryvil.

## 6. Acceptance Criteria
* **Scenario 1: Generación de Orden de Compra para Laboratorio**
  * **Given** Una orden de compra en estado "Confirmado" dirigida a "Laboratorios Vijosa S.A. de C.V.".
  * **When** El encargado de compras presiona "Imprimir Orden de Compra".
  * **Then** Se genera un PDF en tamaño Carta conteniendo los datos fiscales del laboratorio, la tabla de medicamentos con sus presentaciones y el total monetario desglosado.
* **Scenario 2: Especificación de condiciones de caducidad en el reporte**
  * **Given** Una orden de compra con la nota "Medicamentos con vencimiento mínimo de 2 años".
  * **When** Se visualiza el documento PDF generado.
  * **Then** Dicha instrucción debe aparecer claramente visible en la sección de "Instrucciones de Recepción" para constancia del distribuidor.
* **Scenario 3: Cálculo exacto de impuestos en la orden**
  * **Given** Un pedido de medicamentos gravados con IVA.
  * **When** Se imprime el documento.
  * **Then** El cálculo del Subtotal, IVA 13% y Total debe ser aritméticamente consistente y coincidir con el registro en Odoo.

## 7. Verification Plan
* **Automated Tests:**
  * Prueba unitaria en Python ejecutando la acción `action_report_caryvil_purchase_order` sobre una orden de compra mock y validando la generación exitosa del PDF.
* **Manual Verification:**
  * Emitir una orden de compra de prueba con más de 10 líneas de medicamentos y verificar que el salto de página mantenga los encabezados de tabla de forma legible.

## 8. Security and Privacy
* El documento solo es accesible y emitible por usuarios con rol `Encargado de Compras e Inventario` o `Administrador`.
* No se exponen datos bancarios confidenciales en el cuerpo de la orden.

## 9. Risks and Mitigation
* **Risk:** Solapamiento de texto en tablas con nombres largos de medicamentos o principios activos complejos.
  * **Mitigation:** Asignar anchos porcentuales fijos a las columnas de la tabla QWeb y habilitar salto de línea automático (`word-break: break-word`).

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/reports/report_purchase_order.xml`.
* Archivo `custom_addons/caryvil_erp/reports/purchase_order_report_action.xml`.
* Registro de ambos archivos en la lista `data` de `__manifest__.py`.

## 11. Definition of Done (DoD)
* [x] Plantilla QWeb de Orden de Compra creada con formato formal tamaño Carta (`reports/report_purchase_order.xml`).
* [x] Membrete institucional (vía `web.external_layout`, usa el logo/datos de la empresa configurados en `res.company`), datos del proveedor y firmas incluidos.
* [ ] Salto de página y formateo de líneas de medicamento comprobados — pendiente probar manualmente con un pedido de 10+ líneas.
* [x] Botón de impresión integrado en el módulo de Compras de Odoo (automático vía `binding_model_id`/`binding_type=report`, aparece en el menú "Imprimir" del formulario).
* [ ] Aprobación del diseño por parte de la propietaria y el equipo de compras.
* **Nota de implementación:** el resumen de IVA/Total del PDF usa los campos custom de SPEC-8.1.1 (`amount_subtotal_gross`, `amount_discount_total`, `amount_tax`, `amount_iva_percibido`, `amount_total_final`) en vez del widget nativo `document_tax_totals`, para mantener consistencia con la pantalla de Compras.
