# SPEC-9.2.1: Generación de Factura Simple

## 1. Objective
Generar, numerar y validar de forma automática e inmediata la **Factura Simple a Consumidor Final** en Odoo (`account.move` con `move_type = 'out_invoice'`) al concretarse cada transacción en mostrador para Farmacia Caryvil. Esta especificación automatiza la asignación de la secuencia correlativa interna (e.g., `FAC-2026-00001`), el desglose del impuesto IVA (13%), el registro contable del cobro y la preparación inmediata del comprobante para su impresión térmica o digital sin requerir pasos contables complejos por parte del dependiente.

## 2. Scope
### 2.1. Included
* Configuración de la secuencia numérica correlativa exclusiva para facturación simple en `custom_addons/caryvil_erp/data/invoice_sequence_data.xml` (`FAC-YYYY-XXXXX`).
* Extensión del modelo `account.move` en `custom_addons/caryvil_erp/models/account_move_invoice.py`:
  * `simple_invoice_number` (Char): Número correlativo consecutivo asignado al validar la factura.
  * `payment_method_display` (Char): Método de pago utilizado en caja (Efectivo, Tarjeta, Transferencia).
  * `amount_in_words` (Char): Importe total en letras en idioma español computado automáticamente mediante `num2words`.
* Generación de asientos contables automáticos: Débito a Caja/Banco (`1101`) y Crédito a Ingresos por Ventas de Medicamentos (`4101`) con pasivo de IVA Débito Fiscal (13% - `2107`).
* Conciliación automática del pago al momento de confirmar la transacción de venta en mostrador.
* Disparo automático de la acción de impresión del ticket térmico (`SPEC-3.3.1`).

### 2.2. Not Included (Out of Scope)
* Generación de Crédito Fiscal o Factura de Exportación (restringido únicamente a facturación simple a consumidor final).
* Integración directa con el Ministerio de Hacienda (excluido expresamente del alcance en esta etapa).

## 3. Context and Restrictions
* **Context:** Formaliza el registro contable de cada venta realizada en Farmacia Caryvil, garantizando que los reportes financieros del Dashboard coincidan con los ingresos reales percibidos en caja.
* **Restrictions:**
  * Toda factura simple debe generarse en estado `posted` (Publicado) para garantizar la inmutabilidad de los registros fiscales.
  * La numeración debe ser estrictamente consecutiva sin saltos numéricos injustificados.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
  * `SPEC-3.3.1` (Plantilla de Reporte para Factura Simple y Ticket).
  * `SPEC-9.1.1` (Procesamiento de Transacciones de Ventas).
* **Definition of Ready (DoR):**
  * [x] Catálogo de cuentas contables simplificado configurado en Odoo.
  * [x] Formato de numeración correlativa acordado con la administración.

## 5. Design (Implementation Details)
* **Model Configuration (`models/account_move_invoice.py`):**
  ```python
  from odoo import models, fields, api
  from num2words import num2words

  class AccountMoveInvoice(models.Model):
      _inherit = 'account.move'

      simple_invoice_number = fields.Char(string='N° Factura Simple', readonly=True, index=True, copy=False)
      amount_in_words = fields.Char(string='Monto en Letras', compute='_compute_amount_in_words')

      @api.depends('amount_total')
      def _compute_amount_in_words(self):
          for move in self:
              if move.amount_total and move.currency_id:
                  entero = int(move.amount_total)
                  decimales = int(round((move.amount_total - entero) * 100))
                  texto = num2words(entero, lang='es').upper()
                  move.amount_in_words = f"{texto} DÓLARES CON {decimales:02d}/100 USD"
              else:
                  move.amount_in_words = "CERO DÓLARES CON 00/100 USD"

      def action_post(self):
          for move in self:
              if move.move_type == 'out_invoice' and not move.simple_invoice_number:
                  move.simple_invoice_number = self.env['ir.sequence'].next_by_code('caryvil.simple.invoice.sequence') or '/'
          return super(AccountMoveInvoice, self).action_post()
  ```
* **Sequence Definition (`data/invoice_sequence_data.xml`):**
  * Código: `caryvil.simple.invoice.sequence`, Prefijo: `FAC-%(year)s-`, Relleno: `5 dígitos` (e.g., `FAC-2026-00001`).

## 6. Acceptance Criteria
* **Scenario 1: Emisión y numeración correlativa automática**
  * **Given** Una venta confirmada en mostrador por un total de $12.50.
  * **When** Se ejecuta la acción de cobro y facturación.
  * **Then** Odoo genera la factura en estado `posted`, le asigna el siguiente correlativo (e.g. `FAC-2026-00105`) y calcula el monto en letras: "DOCE DÓLARES CON 50/100 USD".
* **Scenario 2: Desglose aritmético de IVA (13%)**
  * **Given** Una factura simple por $11.30 (precio con IVA incluido).
  * **When** Se visualiza la liquidación contable.
  * **Then** La factura registra Subtotal neto: `$10.00`, IVA (13%): `$1.30` y Total: `$11.30`.
* **Scenario 3: Bloqueo de modificación de factura emitida**
  * **Given** Una factura simple en estado `posted`.
  * **When** Un cajero intenta modificar las líneas de producto o precios.
  * **Then** El sistema bloquea los campos en modo de solo lectura impidiendo cualquier alteración posterior (`SPEC-2.2.2`).

## 7. Verification Plan
* **Automated Tests:**
  * Prueba unitaria en Python generando una factura de venta, validando que `simple_invoice_number` no sea nulo, que la secuencia incremente en 1 y que `amount_in_words` coincida con la conversión esperada.
* **Manual Verification:**
  * Realizar 2 ventas consecutivas y comprobar que los números de factura sean correlativos consecutivos (`FAC-2026-00001` y `FAC-2026-00002`).

## 8. Security and Privacy
* Los cajeros solo tienen permisos para crear y validar facturas de su propia sesión de mostrador; la anulación contable requiere autorización de Administrador.

## 9. Risks and Mitigation
* **Risk:** Bloqueos en la generación de secuencias ante ventas concurrentes en múltiples cajas.
  * **Mitigation:** Uso del generador nativo de secuencias de Odoo (`ir.sequence`) con transacciones seguras en PostgreSQL.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/models/account_move_invoice.py`.
* Archivo `custom_addons/caryvil_erp/data/invoice_sequence_data.xml`.
* Extensión de vista en `views/account_move_views.xml`.

## 11. Definition of Done (DoD)
* [ ] Secuencia correlativa `FAC-YYYY-XXXXX` configurada y probada.
* [ ] Conversión automática de montos a letras en español implementada.
* [ ] Validación y pase a estado `posted` en menos de 500ms comprobado.
* [ ] Pruebas unitarias aprobadas al 100%.
* [ ] Aprobación de los formatos contables por la propietaria de la farmacia.
