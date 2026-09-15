# SPEC-5.2.2: Historial de Compras de Clientes

## 1. Objective
Centralizar, estructurar y desplegar la trazabilidad histórica de compras y comprobantes de facturación emitidos a nombre de cada cliente dentro de su ficha en Odoo (`res.partner`) para Farmacia Caryvil. Esta especificación permite al personal farmacéutico y a la administración consultar rápidamente el historial de transacciones previas, los medicamentos recurrentes adquiridos por el paciente (tratamientos crónicos o continuos), fechas de compra, lotes dispensados, montos totales invertidos y la reimpresión ágil de comprobantes pasados.

## 2. Scope
### 2.1. Included
* Creación de campos computados en el modelo `res.partner`:
  * `caryvil_invoice_count` (Integer): Número total de facturas y tickets emitidos al cliente.
  * `caryvil_total_spent` (Monetary): Monto monetario total acumulado en compras ($ USD).
* Implementación de un botón inteligente (*Smart Button*) en la cabecera del formulario de cliente que muestra el contador de compras y el total acumulado con acceso directo a la lista filtrada de facturas.
* Inclusión de una pestaña (*Tab*) dedicada en la vista de cliente: "Historial de Compras y Medicamentos":
  * Tabla con listado cronológico de comprobantes: Fecha/Hora, Número de Factura, Total ($), Estado de Pago y Líneas de medicamentos dispensados (con nombre, cantidad y precio).
* Botón de acción por registro: "Ver Factura" y "Reimprimir Ticket Simple".
* Restricción de acceso para roles Cajero (solo lectura de historial) y Administrador (acceso y auditoría completa).

### 2.2. Not Included (Out of Scope)
* Generación de recomendaciones automáticas basadas en IA o algoritmos predictivos (fuera del alcance del proyecto).
* Emisión o modificación de facturas desde la ficha del cliente (se gestiona en el flujo de ventas `SPEC-9.1.1`).

## 3. Context and Restrictions
* **Context:** Permite al farmacéutico responder con certeza preguntas frecuentes de los clientes como: "¿Cuál fue el medicamento para la presión que compré el mes pasado?" o "¿Cuánto gasté en mi última compra?".
* **Restrictions:**
  * La consulta del historial debe ejecutarse de forma diferida o computada para no ralentizar la apertura de la ficha del cliente.
  * Solo se contabilizan comprobantes en estado "Publicado" (`state = 'posted'`), excluyendo borradores o transacciones anuladas.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
  * `SPEC-5.1.1` (Gestión del Perfil de Clientes).
* **Definition of Ready (DoR):**
  * [x] Vinculación entre los modelos `res.partner` y `account.move` / `sale.order` validada.
  * [x] Diseño de pestañas y botones inteligentes en el formulario de cliente acordado.

## 5. Design (Implementation Details)
* **Model Extension (`models/res_partner_customer.py`):**
  ```python
  from odoo import models, fields, api

  class ResPartnerPurchaseHistory(models.Model):
      _inherit = 'res.partner'

      caryvil_invoice_count = fields.Integer(
          string='N° Compras',
          compute='_compute_caryvil_purchase_stats'
      )
      caryvil_total_spent = fields.Monetary(
          string='Total Comprado ($)',
          currency_field='currency_id',
          compute='_compute_caryvil_purchase_stats'
      )
      caryvil_invoice_ids = fields.One2many(
          'account.move',
          'partner_id',
          string='Facturas del Cliente',
          domain=[('move_type', '=', 'out_invoice'), ('state', '=', 'posted')]
      )

      @api.depends()
      def _compute_caryvil_purchase_stats(self):
          for partner in self:
              invoices = self.env['account.move'].search([
                  ('partner_id', '=', partner.id),
                  ('move_type', '=', 'out_invoice'),
                  ('state', '=', 'posted')
              ])
              partner.caryvil_invoice_count = len(invoices)
              partner.caryvil_total_spent = sum(invoices.mapped('amount_total'))

      def action_view_caryvil_invoices(self):
          self.ensure_one()
          action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
          action['domain'] = [('partner_id', '=', self.id), ('move_type', '=', 'out_invoice'), ('state', '=', 'posted')]
          action['context'] = {'default_partner_id': self.id}
          return action
  ```
* **View Structure (`views/res_partner_customer_views.xml`):**
  * *Smart button* con icono de bolsa de compras `fa-shopping-bag`.
  * Pestaña "Historial de Compras" con vista de lista embebida mostrando fechas, correlativo de factura y montos.

## 6. Acceptance Criteria
* **Scenario 1: Consulta de compras acumuladas de un cliente**
  * **Given** Un cliente "María Elena López Rivas" que ha realizado 3 compras de medicamentos en la farmacia por un valor acumulado de $45.00.
  * **When** El dependiente abre la ficha del cliente en Odoo.
  * **Then** El botón inteligente en la cabecera debe indicar `3 Compras` y un monto acumulado de `$45.00`.
* **Scenario 2: Apertura y revisión del detalle de transacciones previas**
  * **Given** El dependiente visualizando la ficha del cliente.
  * **When** Hace clic en la pestaña "Historial de Compras" o en el botón inteligente.
  * **Then** El sistema debe desplegar el listado de las 3 facturas emitidas, permitiendo abrir cualquiera de ellas para ver qué medicamentos específicos fueron dispensados.
* **Scenario 3: Reimpresión de ticket desde el historial**
  * **Given** Un cliente solicitando copia de su comprobante de compra emitido hace 2 semanas.
  * **When** El usuario localiza la factura en el historial y presiona "Imprimir Ticket".
  * **Then** El sistema genera inmediatamente el comprobante en formato térmico o PDF con los datos originales de la transacción.

## 7. Verification Plan
* **Automated Tests:**
  * Prueba unitaria en Python creando 2 facturas para un cliente de prueba, validando que `caryvil_invoice_count == 2` y `caryvil_total_spent` coincida exactamente con la sumatoria de las facturas.
* **Manual Verification:**
  * Registrar una venta asociada a un cliente y verificar que el contador y la pestaña de historial en su formulario se actualicen de inmediato.

## 8. Security and Privacy
* El historial de compras es visible únicamente para personal de mostrador y administración con el fin de asistencia farmacéutica.
* Se restringe la edición de facturas históricas desde esta vista.

## 9. Risks and Mitigation
* **Risk:** Lentitud al abrir la ficha de clientes con cientos de facturas registradas a lo largo de los años.
  * **Mitigation:** Utilizar paginación estándar en la sub-vista One2many y cálculo bajo demanda mediante `action_view_caryvil_invoices`.

## 10. Deliverables & Config as Code
* Métodos y campos computados en `models/res_partner_customer.py`.
* Extensión de vista con Smart Button y pestaña en `views/res_partner_customer_views.xml`.

## 11. Definition of Done (DoD)
* [ ] Campos `caryvil_invoice_count` y `caryvil_total_spent` implementados.
* [ ] Smart button y pestaña de historial visibles y funcionales en el formulario de cliente.
* [ ] Navegación y reimpresión de comprobantes pasados verificada.
* [ ] Pruebas unitarias de cálculo estadístico aprobadas al 100%.
* [ ] Validación con el personal de mostrador completada.
