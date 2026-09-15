# SPEC-4.2.2: Dashboard de Alertas de Vencimiento de Lotes

## 1. Objective
Diseñar e implementar el componente analítico y visual de **Alertas Tempranas de Vencimiento de Lotes** dentro del Dashboard de inicio de Odoo para Farmacia Caryvil. Esta especificación clasifica y alerta de forma preventiva sobre lotes de medicamentos en existencia física con fechas de caducidad próximas a vencer en tres horizontes temporales estratégicos (menos de 30 días, 31 a 60 días y 61 a 90 días), facilitando la toma de decisiones oportunas para evitar la dispensación accidental de productos expirados y reducir pérdidas por mermas en farmacia.

## 2. Scope
### 2.1. Included
* Creación del método backend en Python para clasificar lotes activos con saldo positivo (`product_qty > 0`) según su fecha de expiración (`expiration_date`):
  * 🔴 **Nivel Crítico (< 30 días):** Alerta urgente en color rojo para retiro preventivo de estanterías o gestión de devolución a laboratorios.
  * 🟡 **Nivel Alerta (31 a 60 días):** Alerta preventiva en color ámbar para priorizar rotación mediante política FEFO.
  * 🔵 **Nivel Seguimiento (61 a 90 días):** Indicador informativo en color azul para monitoreo de demanda.
* Implementación del panel visual en el Dashboard con tarjetas de conteo por nivel de urgencia y tabla interactiva de detalle.
* Visualización en tabla: Nombre del fármaco, Número de lote, Fecha de caducidad exacta, Días restantes de vigencia, Cantidad disponible y Ubicación (Mostrador o Bodega).
* Botones de acción directa: "Ver Trazabilidad de Lote" y "Transferir a Cuarentena/Baja".
* Restricción de acceso para los grupos `group_caryvil_inventory_purchases` y `group_caryvil_manager`.

### 2.2. Not Included (Out of Scope)
* Configuración de la estrategia de salida algorítmica FEFO en ventas (cubierto en `SPEC-9.3.2`).
* Ejecución del registro contable de bajas por merma (cubierto en `SPEC-7.3.2`).

## 3. Context and Restrictions
* **Context:** Es un pilar crítico para la seguridad del paciente y el cumplimiento de normativas sanitarias farmacéuticas en El Salvador, garantizando que ningún medicamento vencido permanezca disponible para venta en mostrador.
* **Restrictions:**
  * Debe excluir automáticamente lotes con saldo cero (`product_qty <= 0`) o lotes ya dados de baja en ubicaciones de merma/pérdida.
  * La consulta debe considerar la zona horaria local de El Salvador (`America/El_Salvador` - UTC-6).

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
  * `SPEC-2.2.1` (Definición de Roles y Grupos de Usuarios).
  * `SPEC-4.1.1` (Dashboard de KPIs de Ventas).
* **Definition of Ready (DoR):**
  * [x] Módulo nativo `stock` configurado con trazabilidad por lotes (`stock.production.lot`) y fechas de caducidad habilitadas.
  * [x] Definición de los tres rangos temporales de alerta (30, 60 y 90 días) acordada con la administración.

## 5. Design (Implementation Details)
* **Backend Logic (`models/caryvil_dashboard.py`):**
  ```python
  @api.model
  def get_expiring_lots_data(self):
      today = fields.Date.today()
      date_30 = today + fields.Date.timedelta(days=30)
      date_60 = today + fields.Date.timedelta(days=60)
      date_90 = today + fields.Date.timedelta(days=90)

      # Lotes con stock positivo en ubicaciones internas
      lots = self.env['stock.production.lot'].search([
          ('product_qty', '>', 0),
          ('expiration_date', '!=', False),
          ('expiration_date', '<=', fields.Datetime.to_datetime(date_90))
      ], order='expiration_date asc')

      critical_30 = []
      warning_60 = []
      notice_90 = []

      for lot in lots:
          exp_date = fields.Date.to_date(lot.expiration_date)
          days_left = (exp_date - today).days
          lot_info = {
              'lot_id': lot.id,
              'lot_name': lot.name,
              'product_name': lot.product_id.display_name,
              'expiration_date': str(exp_date),
              'days_left': days_left,
              'qty': lot.product_qty,
              'uom': lot.product_uom_id.name,
          }
          if exp_date <= date_30:
              critical_30.append(lot_info)
          elif exp_date <= date_60:
              warning_60.append(lot_info)
          else:
              notice_90.append(lot_info)

      return {
          'count_critical_30': len(critical_30),
          'count_warning_60': len(warning_60),
          'count_notice_90': len(notice_90),
          'critical_lots': critical_30[:8],
          'warning_lots': warning_60[:8],
      }
  ```
* **UI Layout in Dashboard:**
  * Tarjetas superiores con contadores coloreados: Rojo (<30d), Ámbar (31-60d) y Azul (61-90d).
  * Pestañas para alternar entre lotes críticos y lotes en advertencia.

## 6. Acceptance Criteria
* **Scenario 1: Detección y clasificación de lote próximo a vencer (<30 días)**
  * **Given** Un lote de "Ibuprofeno 400mg" Lote #IBU-2024 con fecha de vencimiento dentro de 15 días y existencia de 12 cajas.
  * **When** Se consulta el Dashboard principal.
  * **Then** La tarjeta roja (<30 días) debe incrementar su contador y el lote debe aparecer encabezando la lista crítica con badge de "15 días restantes".
* **Scenario 2: Exclusión automática de lotes agotados**
  * **Given** Un lote con fecha de caducidad en 10 días pero con existencia física de `0` unidades.
  * **When** Se evalúan las alertas de vencimiento en el dashboard.
  * **Then** El lote no debe aparecer en el widget para evitar alarmas sobre productos no existentes.
* **Scenario 3: Transferencia directa a cuarentena desde la alerta**
  * **Given** Un lote visualizado en el panel crítico (<30 días).
  * **When** El encargado de inventario hace clic en "Transferir a Cuarentena".
  * **Then** El sistema debe abrir un movimiento interno de stock con el lote y cantidad precargados hacia la ubicación de merma/cuarentena.

## 7. Verification Plan
* **Automated Tests:**
  * Crear en test unitario 3 lotes con fechas simuladas a 10, 45 y 75 días futuros con stock y verificar la correcta categorización en los arrays `critical_30`, `warning_60` y `notice_90`.
* **Manual Verification:**
  * Registrar un lote con fecha vencida o de caducidad cercana y verificar la alerta visual inmediata en la pantalla de inicio.

## 8. Security and Privacy
* La gestión de lotes y visualización de caducidades está protegida para usuarios con perfiles de gestión y administración.

## 9. Risks and Mitigation
* **Risk:** Lotes registrados sin fecha de caducidad que omitan las alertas del sistema.
  * **Mitigation:** Hacer obligatorio el campo `expiration_date` al recibir mercadería en el módulo de compras (`SPEC-8.2.1`).

## 10. Deliverables & Config as Code
* Métodos de análisis de lotes en `models/caryvil_dashboard.py`.
* Vistas XML de alertas de vencimiento en `views/caryvil_dashboard_views.xml`.

## 11. Definition of Done (DoD)
* [ ] Clasificación tripartita de vencimiento (30/60/90 días) implementada.
* [ ] Visualización en tarjetas y tabla de detalle en el Dashboard.
* [ ] Filtro estricto de saldo positivo (`product_qty > 0`) validado.
* [ ] Pruebas unitarias de cálculo de días restantes aprobadas.
* [ ] Validación de la interfaz completada por la administración de la farmacia.
