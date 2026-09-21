# SPEC-8.1.2: Visibilidad de Abonos y Estado de Pago a Proveedores

## 1. Objective
Dar visibilidad, dentro del módulo de Compras, al estado de pago real de cada Orden de Compra confirmada a un laboratorio o droguería — incluyendo los abonos parciales que Farmacia Caryvil realiza después de vencido el plazo de crédito pactado, hasta saldar el total — sin obligar al Encargado de Compras a entrar al módulo de Contabilidad para consultarlo.

## 2. Scope
### 2.1. Included
* Extensión del modelo `purchase.order` en `custom_addons/caryvil_erp/models/purchase_order_medicine.py`:
  * `payment_status_label` (Selection): Estado de pago simplificado — `Sin Facturar`, `Pendiente de Pago`, `Abono Parcial`, `Pagado`. Calculado a partir de las Facturas de Proveedor (`account.move`, `move_type='in_invoice'`) ligadas a la orden (`invoice_ids`, campo nativo de `purchase.order`).
  * `amount_residual_total` (Monetary): Suma del saldo pendiente (`amount_residual`) de las facturas de proveedor asociadas. Se reduce automáticamente con cada abono registrado.
* Visualización en el formulario de la Orden de Compra (junto al estado de facturación nativo) y como columnas opcionales en la lista de Órdenes de Compra.
* Reutilización del flujo nativo de Odoo para registrar abonos: **Crear Factura de Proveedor** (botón nativo `action_create_invoice`) → **Registrar Pago** (parcial, tantas veces como sea necesario) directamente sobre la factura, sin necesidad de un asistente o modelo nuevo.

### 2.2. Not Included (Out of Scope)
* Un modelo/wizard custom de "abonos" independiente de las Facturas de Proveedor de Odoo — se decidió reutilizar el flujo contable nativo (Factura de Proveedor + Pagos) en vez de reconstruirlo, para no duplicar la lógica de conciliación contable que Odoo ya resuelve.
* Recordatorios automáticos de vencimiento de crédito (posible spec futura).
* Notas de crédito o descuentos por pronto pago.

## 3. Context and Restrictions
* **Context:** Actualmente Farmacia Caryvil paga sus compras a crédito (15/30/45/60 días) mediante abonos parciales sucesivos hasta completar el total adeudado al laboratorio, un proceso que hoy se lleva de forma manual/informal y no era visible en ninguna spec previa del módulo de Compras.
* **Restrictions:**
  * El saldo pendiente mostrado en Compras debe coincidir exactamente con el saldo de Contabilidad (`amount_residual`) — no se duplica el dato, solo se refleja.
  * No se puede marcar una orden como "Pagada" manualmente; el estado se deriva siempre de los pagos reales registrados contra la factura.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-8.1.1` (Gestión de Órdenes de Compra).
  * Módulo `account` instalado y el diario de compras/proveedores configurado (ya cubierto por la dependencia `account` en `__manifest__.py`).
* **Definition of Ready (DoR):**
  * [x] Orden de compra confirmada con datos de proveedor y montos correctos (SPEC-8.1.1).
  * [x] Contabilidad (`account`) instalada como dependencia del módulo.

## 5. Design (Implementation Details)
* **Model Extension (`models/purchase_order_medicine.py`):**
  ```python
  payment_status_label = fields.Selection([
      ('sin_facturar', 'Sin Facturar'),
      ('pendiente', 'Pendiente de Pago'),
      ('parcial', 'Abono Parcial'),
      ('pagado', 'Pagado'),
  ], string='Estado de Pago', compute='_compute_payment_status_caryvil', store=True)

  amount_residual_total = fields.Monetary(
      string='Saldo Pendiente',
      compute='_compute_payment_status_caryvil',
      store=True,
      currency_field='currency_id',
  )

  @api.depends('invoice_ids.amount_residual', 'invoice_ids.payment_state', 'invoice_ids.state')
  def _compute_payment_status_caryvil(self):
      for order in self:
          bills = order.invoice_ids.filtered(lambda move: move.state == 'posted')
          if not bills:
              order.amount_residual_total = 0.0
              order.payment_status_label = 'sin_facturar'
              continue
          order.amount_residual_total = sum(bills.mapped('amount_residual'))
          states = set(bills.mapped('payment_state'))
          if states <= {'paid', 'in_payment'}:
              order.payment_status_label = 'pagado'
          elif states & {'partial'}:
              order.payment_status_label = 'parcial'
          else:
              order.payment_status_label = 'pendiente'
  ```
* **Flujo de uso (100% nativo de Odoo, sin wizard custom):**
  1. Orden de Compra confirmada → botón nativo **"Crear Factura"** genera la Factura de Proveedor (`account.move`).
  2. En la factura, botón nativo **"Registrar Pago"** → se ingresa el monto del abono (puede ser parcial).
  3. Odoo recalcula `amount_residual` y `payment_state` de la factura automáticamente en cada abono.
  4. `payment_status_label` y `amount_residual_total` en la Orden de Compra se actualizan solos (campos `compute`, sin botones ni pasos manuales adicionales).

## 6. Acceptance Criteria
* **Scenario 1: Primer abono parcial**
  * **Given** Una Orden de Compra de $500.00 con Factura de Proveedor generada y sin pagos.
  * **When** Se registra un pago de $200.00 contra la factura.
  * **Then** La orden muestra `Estado de Pago = Abono Parcial` y `Saldo Pendiente = $300.00`.
* **Scenario 2: Pago completo tras varios abonos**
  * **Given** Una orden con $300.00 de saldo pendiente tras un abono previo.
  * **When** Se registra un segundo pago de $300.00.
  * **Then** La orden muestra `Estado de Pago = Pagado` y `Saldo Pendiente = $0.00`.
* **Scenario 3: Orden sin factura generada aún**
  * **Given** Una Orden de Compra recién confirmada, sin Factura de Proveedor creada.
  * **When** Se consulta su estado de pago.
  * **Then** Muestra `Estado de Pago = Sin Facturar`.

## 7. Verification Plan
* **Automated Tests:**
  * Prueba unitaria creando una orden, generando su factura, registrando un pago parcial y validando `payment_status_label == 'parcial'` y `amount_residual_total` exacto; luego completando el pago y validando `payment_status_label == 'pagado'`.
* **Manual Verification:**
  * Confirmar una orden en la interfaz, crear la factura, registrar dos abonos parciales y verificar que el estado y saldo se actualicen en tiempo real en la vista de Compras.

## 8. Security and Privacy
* La creación de facturas y registro de pagos permanece restringida a los roles con acceso a Contabilidad/Compras según los permisos ya definidos en `SPEC-2.2.1`.

## 9. Risks and Mitigation
* **Risk:** Confusión entre el estado de la Orden de Compra (`Pendiente/Recibido/Cancelado`, SPEC-8.1.1) y el Estado de Pago (`Sin Facturar/Pendiente/Abono Parcial/Pagado`, esta spec) por tener nombres similares.
  * **Mitigation:** Se muestran como dos columnas/campos claramente separados y con etiquetas distintas en la vista.

## 10. Deliverables & Config as Code
* Extensión de campos en `custom_addons/caryvil_erp/models/purchase_order_medicine.py`.
* Extensión de vista en `custom_addons/caryvil_erp/views/purchase_order_views.xml` (formulario y lista).

## 11. Definition of Done (DoD)
* [x] Campos `payment_status_label` y `amount_residual_total` implementados y calculados desde las Facturas de Proveedor nativas.
* [x] Visibles en formulario y lista de Órdenes de Compra.
* [x] Pruebas unitarias con flujo completo de abonos (factura → pago parcial → pago final) — `tests/test_purchase_order_medicine.py::test_abonos_parciales_actualizan_estado_de_pago`.
* [ ] Validación con el equipo de compras de que el flujo de "Crear Factura + Registrar Pago" nativo cubre su necesidad real, o si requieren un registro más simplificado (sin pasar por Contabilidad).
