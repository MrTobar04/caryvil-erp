# SPEC-3.3.2: Plantilla de Reporte para Órdenes de Compra

## 1. Objective
Diseñar, estructurar e implementar la plantilla de reporte QWeb en Odoo para la emisión formal en formato PDF de **Órdenes de Compra (PO)** dirigidas a laboratorios farmacéuticos y droguerías proveedoras de Farmacia Caryvil, alineada con los mockups del módulo de Compras (`docs/mockups/Compras.png`, `docs/mockups/Compras_Orden.png`, `docs/mockups/Compras_Orden_2.png`). Esta especificación estandariza el documento oficial de abastecimiento, incorporando el membrete corporativo "ERP FARMACIA / Farmacia Caryvil", datos fiscales del proveedor y laboratorio, detalle de medicamentos solicitados con sus respectivas presentaciones, precios unitarios pactados, subtotales, descuentos, cálculo de IVA (13%), notas adicionales, instrucciones de recepción y firmas autorizadas.

## 2. Scope
### 2.1. Included
* Creación de la plantilla QWeb `custom_addons/caryvil_erp/reports/report_purchase_order.xml`.
* Definición de la acción de reporte `ir.actions.report` vinculada al modelo `purchase.order`.
* Encabezado corporativo: Logotipo de Farmacia Caryvil, título "ERP FARMACIA", información de contacto en Soyapango, código de orden correlativo (e.g., `PE001` / `PE0001`), fecha de pedido y fecha de entrega estimada.
* Bloque de datos del proveedor y laboratorio: Razón Social del Proveedor, Laboratorio fabricante, NIT/NRC, Contacto, Teléfono y Correo electrónico.
* Tabla estructurada de requerimiento de productos (alineada con `Compras_Orden.png`):
  * Columnas: `Producto` (Nombre comercial y laboratorio), `Cantidad`, `Precio Unitario ($)`, `Descuento (%)` y `SubTotal ($)`.
* Sección de liquidación económica (alineada con `Compras_Orden.png` / `Compras_Orden_2.png`):
  * `SubTotal`: Sumatoria neta de líneas de compra.
  * `Descuento`: Monto consolidado de descuentos pactados.
  * `IVA (13%)`: Desglose fiscal aplicable a la compra.
  * `Total` / `Total Pagado`: Importe total en USD ($).
* Bloque de notas y control:
  * Campo de "Notas Adicionales" (instrucciones de entrega, requerimientos de lote y vigencia mínima).
  * Recuadros de firma: "Elaborado por (Encargado de Compras)" y "Autorizado por (Administración Caryvil)".

### 2.2. Not Included (Out of Scope)
* Generación de órdenes de compra automáticas sin revisión previa del encargado (cubierto en `SPEC-7.2.2`).
* Registro interactivo de recepción física y lotes en la interfaz web (cubierto en `SPEC-8.2.1`).

## 3. Context and Restrictions
* **Context:** Es el documento oficial que Farmacia Caryvil envía por correo electrónico o entrega a los agentes de venta de laboratorios para formalizar el pedido de reabastecimiento de medicamentos.
* **Restrictions:**
  * Estructurado en formato de hoja estándar Carta (US Letter) / A4 con márgenes uniformes.
  * Generación de archivo PDF profesional, nítido y de alta resolución.
  * Los subtotales, IVA y totales deben coincidir aritméticamente con los campos personalizados del formulario de compras.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
  * `SPEC-3.1.1` (Personalización de Marca y Tema Visual).
  * `SPEC-8.1.1` (Gestión de Órdenes de Compra).
* **Definition of Ready (DoR):**
  * [x] Mockups de Compras revisados (`Compras_Orden.png`, `Compras_Orden_2.png`).
  * [x] Estructura de campos y liquidación acordada.

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
  * Encabezado corporativo en azul marino institucional (`#002B49`) con tipografía limpia y clara.
  * Presentación de código de orden destacado (`PE001`).
  * Tabla de medicamentos con filas alternadas y columnas bien proporcionadas (`Producto`, `Cantidad`, `Precio Unitario`, `Descuento`, `SubTotal`).
  * Desglose inferior de `SubTotal`, `Descuento`, `IVA (13%)` y `Total`.
  * Sección destacada para "Notas Adicionales" y recuadros de firma formal.

## 6. Acceptance Criteria
* **Scenario 1: Generación de PDF de Orden de Compra para Proveedor y Laboratorio**
  * **Given** Una orden de compra confirmada para "Droguería Americana" y laboratorio "Laboratorios Vijosa".
  * **When** El encargado de compras emite el reporte de orden de compra.
  * **Then** El PDF generado muestra el encabezado corporativo, el código `PE001`, las fechas de pedido y entrega, la tabla de productos dispensados y el total consolidado.
* **Scenario 2: Visualización de Descuento e IVA (13%)**
  * **Given** Una orden de compra con precios pactados y descuentos.
  * **When** Se renderiza la sección de totales del reporte.
  * **Then** El documento detalla con claridad el Subtotal, Descuento ($), IVA (13%) y Total exacto.
* **Scenario 3: Inclusión de Notas Adicionales e instrucciones de recepción**
  * **Given** Una orden de compra con instrucciones en el campo "Notas Adicionales".
  * **When** Se imprime el documento.
  * **Then** Dichas notas se imprimen visiblemente sobre el bloque de firmas y autorizaciones.

## 7. Verification Plan
* **Automated Tests:**
  * Test unitario en Python ejecutando la acción de reporte sobre una orden mock de compra y validando retorno exitoso del binario PDF.
* **Manual Verification:**
  * Emitir una orden de compra con múltiples líneas de medicamentos y verificar la correlación visual con los mockups `Compras_Orden.png` y `Compras_Orden_2.png`.

## 8. Security and Privacy
* El reporte es accesible únicamente para usuarios con roles `Encargado de Compras e Inventario` o `Administrador`.

## 9. Risks and Mitigation
* **Risk:** Desbordamiento en nombres extensos de medicamentos o múltiples laboratorios.
  * **Mitigation:** Anchos de columna predefinidos y saltos de línea automáticos.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/reports/report_purchase_order.xml`.
* Archivo `custom_addons/caryvil_erp/reports/purchase_order_report_action.xml`.
* Inclusión de ambos archivos en `data` dentro de `__manifest__.py`.

## 11. Definition of Done (DoD)
* [x] Plantilla QWeb de Orden de Compra creada con formato formal tamaño Carta (`reports/report_purchase_order.xml`).
* [x] Membrete institucional corporativo, datos del proveedor/laboratorio y firmas incluidos.
* [ ] Salto de página y formateo de líneas de medicamento comprobados con pedido de 10+ líneas.
* [x] Botón de impresión integrado en el módulo de Compras de Odoo.
* [ ] Aprobación del diseño por parte de la administración de la farmacia.

