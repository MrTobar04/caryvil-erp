# SPEC-3.3.1: Plantilla de Reporte para Factura Simple y Ticket

## 1. Objective
Diseñar, estructurar e implementar la plantilla de reporte QWeb en Odoo para la emisión e impresión de **Facturas Simples a Consumidor Final** y comprobantes tipo ticket para Farmacia Caryvil, alineada con los mockups del módulo de Ventas (`docs/mockups/Ventas.png`, `docs/mockups/Ventas_Crear.png`). Esta especificación define el formato visual para impresión térmica de mostrador (80mm) y documentos PDF descargables, incluyendo el membrete corporativo "ERP FARMACIA / Farmacia Caryvil", datos de la sucursal de Soyapango, identificación del cliente (DUI / Consumidor Final), desglose de medicamentos dispensados, desglose de IVA (13%), descuento, cálculo de cambio (`Monto Recibido`, `Cambio`, `Saldo Pendiente`), método de pago y monto en letras.

## 2. Scope
### 2.1. Included
* Creación de la plantilla QWeb `custom_addons/caryvil_erp/reports/report_invoice_ticket.xml`.
* Definición de la acción de reporte `ir.actions.report` vinculada al modelo `account.move` y órdenes de venta.
* Encabezado institucional: Logotipo corporativo, membrete "ERP FARMACIA • Farmacia Caryvil", Dirección en Soyapango, Teléfono de atención y Número correlativo de comprobante (e.g., `V0001`).
* Datos del cliente: Nombre del cliente, Documento Único de Identidad (DUI) o denominación "Consumidor Final" cuando no aplique.
* Tabla de dispensación de medicamentos:
  * Columnas: `Producto` (Nombre comercial y concentración), `Cantidad`, `Precio Unitario ($)`, `Descuento (%)`, y `SubTotal ($)`.
* Bloque de liquidación financiera (alineado con mockup `Ventas_Crear.png`):
  * `SubTotal`: Sumatoria de subtotales de líneas.
  * `Descuento`: Total de descuentos aplicados.
  * `IVA (13%)`: Desglose del impuesto al valor agregado.
  * `Total`: Monto neto total a pagar en USD ($).
  * `Importe en Letras`: Conversión automática en español (vía `num2words`).
  * `Método de Pago`: Efectivo / Transferencia / Tarjeta.
  * `Monto Recibido`: Importe entregado por el cliente en efectivo.
  * `Cambio`: Vuelto entregado al cliente.
  * `Saldo Pendiente`: Monto remanente (en caso de pagos parciales o transferencias diferidas).
* Pie de página con mensaje de fidelización y leyendas fiscales: "¡Gracias por su compra! Cuide su salud con Farmacia Caryvil • Soyapango".

### 2.2. Not Included (Out of Scope)
* Generación del Documento Tributario Electrónico (DTE) con firma digital hacia el Ministerio de Hacienda (excluido en esta fase).
* Facturación con Crédito Fiscal para contribuyentes empresariales (fuera de alcance en esta versión).

## 3. Context and Restrictions
* **Context:** Es el comprobante físico o digital que se entrega al cliente tras concretar una compra en el mostrador de la farmacia, certificando la transacción y el pago.
* **Restrictions:**
  * Debe imprimirse con perfecta legibilidad en impresoras térmicas de 80mm de mostrador.
  * El cálculo y desglose de `Monto Recibido`, `Cambio` y `Saldo Pendiente` debe cuadrar exactamente con el formulario de venta del frontend.
  * Tiempo de renderizado PDF inferior a 1 segundo para agilizar la cola de atención en mostrador.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-1.1.2` (Configuración del Servidor Odoo - librería `num2words`).
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
  * `SPEC-3.1.1` (Personalización de Marca y Tema Visual).
* **Definition of Ready (DoR):**
  * [x] Mockup de pantalla de venta (`Ventas_Crear.png`) y listado (`Ventas.png`) revisados.
  * [x] Datos fiscales y dirección de Farmacia Caryvil disponibles.

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
* **QWeb Template Highlights (`reports/report_invoice_ticket.xml`):**
  * Membrete centrado con logotipo y título "FARMACIA CARYVIL • ERP FARMACIA".
  * Código de transacción destacado (`V0001`).
  * Desglose tabular de medicamentos vendidos con tipografía monoespaciada/sans-serif de alta nitidez.
  * Desglose financiero completo: Subtotal, Descuento, Total, Monto Recibido, Cambio y Saldo Pendiente.
  * Total en letras en español mediante método Python auxiliar `_get_amount_in_words()`.

## 6. Acceptance Criteria
* **Scenario 1: Emisión de ticket de venta con desglose completo de pago**
  * **Given** Una venta completada por $2.10, pagada en efectivo con $3.00, generando $0.90 de cambio.
  * **When** Se pulsa el botón "Imprimir Ticket".
  * **Then** El ticket generado debe detallar los medicamentos (`Ibuprofeno 600mg`, `Virogrip AM GelCaps`), `SubTotal: $2.10`, `Total: $2.10`, `Monto Recibido: $3.00`, `Cambio: $0.90` y el texto en letras "DOS DÓLARES CON 10/100 USD".
* **Scenario 2: Emisión a Consumidor Final sin cliente registrado**
  * **Given** Una venta rápida efectuada en mostrador sin ingresar ficha de cliente.
  * **When** Se imprime el comprobante.
  * **Then** El comprobante muestra "Cliente: Consumidor Final" y DUI: "N/A" sin errores.
* **Scenario 3: Desglose de Descuentos e IVA (13%)**
  * **Given** Una transacción con descuento promocional aplicado.
  * **When** Se genera el reporte.
  * **Then** El ticket desglosa explícitamente el porcentaje de descuento, el monto descontado y el IVA retenido/calculado correctamente.

## 7. Verification Plan
* **Automated Tests:**
  * Prueba automatizada en Python ejecutando la acción de reporte sobre un registro mock de factura validando código HTTP 200 y generación del binario PDF.
* **Manual Verification:**
  * Generar un comprobante desde la vista de ventas e imprimirlo en visor térmico comprobando la alineación visual respecto al mockup `Ventas_Crear.png`.

## 8. Security and Privacy
* En cumplimiento con regulaciones de privacidad, el DUI se imprime formateado y no se exponen credenciales de pago ni números de tarjeta completos.

## 9. Risks and Mitigation
* **Risk:** Desalineación de columnas o corte de palabras en papel térmico de 80mm.
  * **Mitigation:** Uso de contenedor con ancho fijo de 80mm y tablas con ancho porcentual explícito.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/reports/report_invoice_ticket.xml`.
* Archivo `custom_addons/caryvil_erp/reports/invoice_ticket_report_action.xml`.
* Archivo `custom_addons/caryvil_erp/data/paperformat_data.xml`.
* Inclusión de los archivos en la lista `data` del archivo `__manifest__.py`.

## 11. Definition of Done (DoD)
* [ ] Plantilla QWeb creada con el formato térmico y adaptable.
* [ ] Parámetros de liquidación financiera (`Monto Recibido`, `Cambio`, `Saldo Pendiente`) integrados.
* [ ] Conversión de importe a letras en español validada.
* [ ] Verificación de fidelidad gráfica con los mockups de venta completada.

