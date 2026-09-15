# SPEC-9.1.1: Procesamiento de Transacciones de Ventas

## 1. Objective
Optimizar, agilizar y registrar las transacciones de venta en mostrador dentro de Odoo (`sale.order` / interfaz de mostrador) para Farmacia Caryvil. Esta especificación permite la búsqueda y selección ultrarrápida de medicamentos mediante escaneo de código de barras (EAN-13) o búsqueda por nombre/principio activo, la asignación inmediata del cliente (o cliente genérico "Consumidor Final"), el cálculo automático de subtotales y cambios en efectivo/tarjeta, y la validación de disponibilidad física de stock antes de concretar la operación.

## 2. Scope
### 2.1. Included
* Personalización del formulario de venta rápida de mostrador en `custom_addons/caryvil_erp/models/sale_order_medicine.py`:
  * Soporte para escaneo de código de barras: Al escanear un código EAN-13, el medicamento se agrega automáticamente a las líneas de venta con cantidad `1` (o incrementa la cantidad si ya estaba en la lista).
  * Selector rápido de clientes integrado con la búsqueda por DUI y teléfono (`SPEC-5.2.1`).
  * Asignación por defecto del cliente genérico "Consumidor Final" si no se especifica un cliente registrado.
* Bloque de cálculo de cobro en mostrador:
  * `payment_method` (Selection: `efectivo`, `tarjeta_debito_credito`, `transferencia_qr`).
  * `amount_tendered` (Monetary: Monto en efectivo entregado por el cliente).
  * `amount_change` (Monetary: Cambio o vuelto exacto a devolver al cliente, calculado reactivamente: `amount_tendered - amount_total`).
* Validación estricta de existencias: Bloqueo de la transacción si la cantidad solicitada supera las existencias físicas disponibles en mostrador.
* Botón de acción principal: "Cobrar y Facturar", que valida la venta, descuenta inventario y emite la factura simple en un único flujo continuo.

### 2.2. Not Included (Out of Scope)
* Generación del comprobante contable de factura simple (cubierto en `SPEC-9.2.1`).
* Algoritmo de asignación FEFO de lotes (cubierto en `SPEC-9.3.2`).

## 3. Context and Restrictions
* **Context:** Es la interfaz de mayor uso en la farmacia, donde los dependientes y cajeros pasan la mayor parte de su jornada atendiendo a los clientes que llegan a la sucursal de Soyapango.
* **Restrictions:**
  * La adición de un medicamento por código de barras debe procesarse en menos de 100ms.
  * No se permite procesar ventas con montos entregados inferiores al total de la transacción cuando el método de pago sea efectivo.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-5.1.1` (Gestión del Perfil de Clientes).
  * `SPEC-5.2.1` (Búsqueda Rápida de Clientes en Caja).
  * `SPEC-7.1.1` (Catálogo y Categorización de Medicamentos).
  * `SPEC-7.1.2` (Gestión de Unidades de Medida Farmacéuticas).
* **Definition of Ready (DoR):**
  * [x] Catálogo de medicamentos con precios de venta al público y códigos de barra cargados.
  * [x] Formulario de venta simplificado diseñado para mostrador.

## 5. Design (Implementation Details)
* **Model Configuration (`models/sale_order_medicine.py`):**
  ```python
  from odoo import models, fields, api, _
  from odoo.exceptions import UserError

  class SaleOrderMedicine(models.Model):
      _inherit = 'sale.order'

      payment_method = fields.Selection([
          ('efectivo', 'Efectivo'),
          ('tarjeta_debito_credito', 'Tarjeta de Débito / Crédito'),
          ('transferencia_qr', 'Transferencia / Pago QR')
      ], string='Forma de Pago', default='efectivo', required=True)

      amount_tendered = fields.Monetary(string='Efectivo Recibido ($)', currency_field='currency_id')
      amount_change = fields.Monetary(string='Cambio / Vuelto ($)', currency_field='currency_id', compute='_compute_amount_change')

      @api.depends('amount_tendered', 'amount_total')
      def _compute_amount_change(self):
          for order in self:
              if order.payment_method == 'efectivo' and order.amount_tendered:
                  order.amount_change = max(order.amount_tendered - order.amount_total, 0.0)
              else:
                  order.amount_change = 0.0

      def action_confirm_and_invoice(self):
          for order in self:
              if order.payment_method == 'efectivo' and order.amount_tendered < order.amount_total:
                  raise UserError(_('El monto en efectivo recibido ($%s) es menor al total a pagar ($%s).') % (order.amount_tendered, order.amount_total))
              
              # Validar existencias físicas
              for line in order.order_line:
                  if line.product_id.detailed_type == 'product' and line.product_uom_qty > line.product_id.qty_available:
                      raise UserError(_('Stock insuficiente para %s. Solicitado: %s, Disponible en mostrador: %s.') % (line.product_id.name, line.product_uom_qty, line.product_id.qty_available))

              order.action_confirm()
              invoices = order._create_invoices()
              invoices.action_post()
              return order.action_view_invoice_ticket(invoices)
  ```

## 6. Acceptance Criteria
* **Scenario 1: Venta rápida con escaneo de código de barras y pago en efectivo**
  * **Given** El dependiente en el formulario de mostrador.
  * **When** Escanea el código "7412345678901" (Amoxicilina $4.50), digita Efectivo Recibido: $10.00 y presiona "Cobrar y Facturar".
  * **Then** El sistema calcula automáticamente el cambio de `$5.50`, confirma la venta, valida la factura simple y abre la pantalla de impresión del ticket.
* **Scenario 2: Bloqueo de venta ante stock insuficiente**
  * **Given** El medicamento "Jarabe 120ml" con existencia física de 2 unidades.
  * **When** El cajero intenta ingresar una cantidad de 5 unidades y cobrar.
  * **Then** Odoo arroja un `UserError` bloqueando la venta e informando que solo existen 2 unidades disponibles en mostrador.
* **Scenario 3: Asignación de cliente registrado por DUI**
  * **Given** Un cliente frecuente solicitando que su compra quede registrada a su nombre.
  * **When** El cajero busca su DUI "04589632-1" en el selector.
  * **Then** El cliente queda asignado inmediatamente a la orden con sus datos de contacto vinculados.

## 7. Verification Plan
* **Automated Tests:**
  * Test unitario en Python creando una orden de venta con pago en efectivo, validando el cálculo exacto de `amount_change` y el bloqueo ante dinero insuficiente o stock en cero.
* **Manual Verification:**
  * Realizar 3 ventas consecutivas de prueba en mostrador verificando que el tiempo total por transacción sea inferior a 15 segundos.

## 8. Security and Privacy
* El Cajero solo puede registrar ventas de su propia sesión de mostrador. La anulación de ventas confirmadas requiere autorización de Administrador.

## 9. Risks and Mitigation
* **Risk:** Lentitud en la atención si el cajero debe cambiar entre múltiples pantallas para cobrar e imprimir.
  * **Mitigation:** Método unificado `action_confirm_and_invoice` que ejecuta la confirmación, facturación e impresión en un solo clic.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/models/sale_order_medicine.py`.
* Extensión de vista `views/sale_order_views.xml`.

## 11. Definition of Done (DoD)
* [ ] Formulario de venta rápida en mostrador implementado.
* [ ] Escaneo de código de barras y cálculo automático de cambio validados.
* [ ] Bloqueo de venta ante stock insuficiente verificado.
* [ ] Pruebas unitarias aprobadas al 100%.
* [ ] Validación de experiencia de usuario en mostrador aprobada.
