# SPEC-3.3.1: Plantilla de Reporte para Factura Simple y Ticket

## 1. Objective
Diseñar, estructurar e implementar la plantilla de reporte QWeb en Odoo para la emisión e impresión de **Facturas Simples a Consumidor Final** y comprobantes tipo ticket para Farmacia Caryvil. Esta especificación define el formato visual para impresoras térmicas de punto de venta (80mm/58mm) y documentos PDF descargables, incluyendo el membrete corporativo, datos de la sucursal de Soyapango, identificación del cliente (DUI), desglose de medicamentos con sus cantidades y precios, cálculo de IVA (13%), total en números y letras, y mensajes legales.

## 2. Scope
### 2.1. Included
* Creación de la plantilla QWeb `custom_addons/caryvil_erp/reports/report_invoice_ticket.xml`.
* Definición de la acción de reporte `ir.actions.report` vinculada al modelo `account.move` y órdenes de venta.
* Formateo del encabezado institucional: Logotipo de Farmacia Caryvil, Razón Social, Dirección en Soyapango, Teléfono de atención y Número de Factura consecutivo.
* Sección de datos del cliente: Nombre, DUI con formato estándar o etiqueta "Consumidor Final" cuando no aplique.
* Tabla de detalle de productos: Cantidad dispensada, Nombre del medicamento y concentración, Precio unitario y Subtotal por línea.
* Bloque de liquidación financiera: Subtotal, Desglose de IVA (13%), Descuento aplicado (si aplica), Total a pagar en USD ($), Importe en letras (utilizando `num2words`), Método de pago, Monto recibido y Cambio entregado.
* Pie de página con mensaje de agradecimiento: "¡Gracias por su compra! Cuide su salud con Farmacia Caryvil" y leyendas fiscales básicas.

### 2.2. Not Included (Out of Scope)
* Generación del Documento Tributario Electrónico (DTE) firmado digitalmente hacia el Ministerio de Hacienda (excluido explícitamente en el alcance).
* Facturación con Crédito Fiscal para contribuyentes (fuera de alcance en esta fase).

## 3. Context and Restrictions
* **Context:** Es el comprobante físico o digital que se entrega al cliente tras concretar una compra en el mostrador de la farmacia, certificando la transacción y el pago.
* **Restrictions:**
  * Debe imprimirse de manera legible y compacta en rollos de papel térmico estándar de 80mm sin desbordamiento de columnas.
  * La conversión del monto total a letras en idioma español debe ser exacta y automática.
  * Debe generar el archivo PDF en menos de 1 segundo para no retrasar la fila de atención en caja.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-1.1.2` (Configuración del Servidor Odoo - librería `num2words`).
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
* **Definition of Ready (DoR):**
  * [x] Formato de factura simple y requerimientos de datos de Farmacia Caryvil revisados.
  * [x] Datos fiscales de la farmacia (Razón social, NIT, dirección en Soyapango) disponibles para la plantilla.

## 5. Design (Implementation Details)
* **Report Action (`reports/invoice_ticket_report_action.xml`):**
  ```xml
  <?xml version="1.0" encoding="utf-8"?>
  <odoo>
      <record id="action_report_caryvil_invoice_ticket" model="ir.actions.report">
          <field name="name">Factura Simple / Ticket Caryvil</field>
          <field name="model">account.move</field>
          <field name="report_type">qweb-pdf</field>
          <field name="report_name">caryvil_erp.report_invoice_ticket_template</field>
          <field name="report_file">caryvil_erp.report_invoice_ticket_template</field>
          <field name="binding_model_id" ref="account.model_account_move"/>
          <field name="binding_type">report</field>
          <field name="paperformat_id" ref="caryvil_erp.paperformat_ticket_80mm"/>
      </record>
  </odoo>
  ```
* **QWeb Template Structure (`reports/report_invoice_ticket.xml`):**
  * Encabezado con imagen corporativa y datos fiscales.
  * Línea divisoria punteada para formato ticket térmico.
  * Bucle `t-foreach="doc.invoice_line_ids" t-as="line"` para listar medicamentos vendidos.
  * Cálculo de montos en letras mediante método auxiliar Python `doc._get_amount_in_words()`.
  * Código QR opcional con resumen de transacción para verificación interna.

## 6. Acceptance Criteria
* **Scenario 1: Emisión de factura simple para cliente con DUI registrado**
  * **Given** Una factura de venta confirmada por $15.50 para el cliente "Juan Pérez" con DUI "01234567-8".
  * **When** El cajero presiona el botón "Imprimir Factura Simple".
  * **Then** El reporte QWeb debe generar el ticket mostrando el nombre del cliente, su DUI, el desglose de medicamentos, el total $15.50 y el texto "QUINCE DÓLARES CON 50/100 USD".
* **Scenario 2: Emisión de ticket para cliente no registrado (Consumidor Final)**
  * **Given** Una venta rápida efectuada en caja sin registro previo de cliente.
  * **When** Se imprime el comprobante.
  * **Then** El campo de cliente debe mostrar automáticamente "CLIENTE: CONSUMIDOR FINAL" y DUI: "N/A" sin provocar errores en el reporte.
* **Scenario 3: Desglose correcto del IVA (13%)**
  * **Given** Una transacción con medicamentos gravados.
  * **When** Se renderiza la sección de totales.
  * **Then** El comprobante debe mostrar el Subtotal neto, el IVA (13%) calculado con precisión de 2 decimales y el Total final coincidente.

## 7. Verification Plan
* **Automated Tests:**
  * Prueba automatizada en Python ejecutando la acción de reporte con una factura de prueba y validando que el binario PDF resultante contenga datos y código de salida `200`.
* **Manual Verification:**
  * Generar e imprimir un ticket de prueba en una impresora térmica virtual o física y validar alineación de texto y cortes de página.

## 8. Security and Privacy
* En cumplimiento con la protección de datos personales, el DUI se imprime formateado y no se exponen datos de tarjetas bancarias más allá de los últimos 4 dígitos cuando aplique.

## 9. Risks and Mitigation
* **Risk:** Desalineación de columnas o texto cortado al imprimir en impresoras térmicas de 58mm o 80mm.
  * **Mitigation:** Crear un formato de papel personalizado `paperformat_ticket_80mm` en Odoo con márgenes cero y ancho explícito de 80mm.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/reports/report_invoice_ticket.xml`.
* Archivo `custom_addons/caryvil_erp/reports/invoice_ticket_report_action.xml`.
* Archivo `custom_addons/caryvil_erp/data/paperformat_data.xml`.
* Inclusión de los tres archivos en la sección `data` de `__manifest__.py`.

## 11. Definition of Done (DoD)
* [ ] Plantilla QWeb creada con diseño térmico y adaptable a A4.
* [ ] Formato de papel de 80mm configurado en `paperformat_data.xml`.
* [ ] Conversión a letras en español probada para importes enteros y con centavos.
* [ ] Botón de impresión funcional desde la vista de facturas en Odoo.
* [ ] Aprobación visual del comprobante por el equipo de negocio.
