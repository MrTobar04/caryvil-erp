# SPEC-4.1.1: Dashboard de KPIs de Ventas

## 1. Objective
Diseñar e implementar el componente de analítica e indicadores clave de rendimiento (KPIs) de ventas dentro de la pantalla principal (Dashboard de Inicio) de Odoo para Farmacia Caryvil. Esta especificación permite a la administración y propietarios visualizar en tiempo real el volumen monetario facturado durante el día, el ticket promedio por cliente, el conteo total de transacciones completadas, la comparativa de ingresos semanales y el ranking de los 5 medicamentos más vendidos.

## 2. Scope
### 2.1. Included
* Creación del modelo backend / servicio transaccional `caryvil.dashboard.sales` en Python para el cálculo y agregación de métricas de ventas.
* Implementación de tarjetas visuales de KPIs (*KPI Cards*) en la vista de inicio:
  * **Ventas del Día:** Total monetario facturado en USD ($) en la jornada actual.
  * **Transacciones de Hoy:** Número de tickets y facturas simples emitidas en el día.
  * **Ticket Promedio:** Valor medio de compra por cliente ($ total / N° transacciones).
  * **Ventas del Mes:** Ingresos acumulados en el mes en curso y comparativa porcentual vs mes anterior.
* Gráfico de barras o líneas interactivo con la tendencia de ventas de los últimos 7 días.
* Tabla resumen con el Top 5 de medicamentos con mayor rotación en unidades e ingresos.
* Restricción de acceso exclusiva para el grupo `caryvil_erp.group_caryvil_manager`.

### 2.2. Not Included (Out of Scope)
* Métricas de estado de inventario y alertas de caducidad (cubierto en `SPEC-4.2.1` y `SPEC-4.2.2`).
* Integración con herramientas externas de Business Intelligence (Power BI, Tableau) (excluido en el alcance general).

## 3. Context and Restrictions
* **Context:** Es la vista predeterminada que visualiza la propietaria y administradora al iniciar sesión, facilitando el control gerencial inmediato sin requerir la generación de reportes complejos en Excel.
* **Restrictions:**
  * El cálculo de agregaciones debe optimizarse mediante consultas SQL indexadas para responder en menos de 500ms sin saturar la base de datos PostgreSQL.
  * Los montos financieros son estrictamente confidenciales y jamás deben ser visibles para usuarios con rol de Cajero.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
  * `SPEC-2.2.1` (Definición de Roles y Grupos de Usuarios).
  * `SPEC-3.1.1` (Personalización de Marca y Tema Visual).
  * `SPEC-3.2.1` (Personalización del Diseño y Navegación).
* **Definition of Ready (DoR):**
  * [x] Indicadores clave requeridos validados con la propietaria (Ana Vilma Rivas).
  * [x] Modelos de ventas y facturación (`sale.order`, `account.move`) estructurados.

## 5. Design (Implementation Details)
* **Architecture:**
  * **Modelo Python (`models/caryvil_dashboard.py`):**
    ```python
    from odoo import models, fields, api
    from datetime import date, datetime, time

    class CaryvilSalesDashboard(models.TransientModel):
        _name = 'caryvil.dashboard.sales'
        _description = 'Dashboard Analítico de Ventas Caryvil'

        @api.model
        def get_sales_kpis(self):
            today = date.today()
            start_today = datetime.combine(today, time.min)
            end_today = datetime.combine(today, time.max)

            # Consultar facturas publicadas de consumidor final del día
            invoices = self.env['account.move'].search([
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted'),
                ('invoice_date', '=', today)
            ])

            total_sales_today = sum(invoices.mapped('amount_total'))
            tx_count_today = len(invoices)
            avg_ticket = (total_sales_today / tx_count_today) if tx_count_today > 0 else 0.0

            return {
                'total_sales_today': round(total_sales_today, 2),
                'tx_count_today': tx_count_today,
                'avg_ticket': round(avg_ticket, 2),
                'currency': '$ USD',
            }
    ```
* **UI/UX Components (`views/caryvil_dashboard_views.xml`):**
  * Tarjetas con diseño limpio (*cards* con bordes suaves, iconos médicos y valores en tipografía bold de gran tamaño).
  * Botón de actualización rápida (*Refresh*) en la barra superior del dashboard.

## 6. Acceptance Criteria
* **Scenario 1: Visualización correcta de ventas del día**
  * **Given** Tres ventas registradas y facturadas hoy por montos de $10.00, $25.50 y $14.50.
  * **When** La administradora abre la vista Dashboard.
  * **Then** La tarjeta "Ventas del Día" debe mostrar exactamente `$50.00`, "Transacciones de Hoy" debe indicar `3` y "Ticket Promedio" debe mostrar `$16.67`.
* **Scenario 2: Actualización en tiempo real tras nueva venta**
  * **Given** El dashboard abierto en el navegador de la administradora.
  * **When** Se completa y valida una nueva factura en mostrador por $20.00 y se refresca la vista.
  * **Then** Las métricas deben actualizarse inmediatamente reflejando `$70.00` y `4` transacciones.
* **Scenario 3: Restricción de acceso para roles no autorizados**
  * **Given** Un dependiente de mostrador autenticado con rol `Cajero`.
  * **When** Intenta acceder directamente a la acción del dashboard.
  * **Then** Odoo debe denegar el acceso mostrando un mensaje de restricción de permisos.

## 7. Verification Plan
* **Automated Tests:**
  * Prueba unitaria en Python generando 5 facturas de prueba y validando que el método `get_sales_kpis()` devuelva los totales y promedios exactos.
* **Manual Verification:**
  * Acceder como Administrador y verificar que las tarjetas rendericen con los estilos azul/verde corporativos sin desbordamiento visual.

## 8. Security and Privacy
* La consulta de agregaciones filtra estrictamente registros activos y publicados, excluyendo borradores o transacciones canceladas.

## 9. Risks and Mitigation
* **Risk:** Degradación del tiempo de carga del dashboard a medida que la base de datos acumula miles de facturas.
  * **Mitigation:** Utilizar filtros temporales indexados por `invoice_date` y campos computados cacheados.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/models/caryvil_dashboard.py`.
* Archivo `custom_addons/caryvil_erp/views/caryvil_dashboard_views.xml`.
* Registro de vistas y acciones en el manifiesto `__manifest__.py`.

## 11. Definition of Done (DoD)
* [x] Modelo y métodos de agregación de KPIs implementados en Python.
* [x] Vista visual del dashboard integrada en la pantalla de inicio de Odoo.
* [x] Permisos de visualización restringidos al grupo Administrador.
* [x] Pruebas unitarias de cálculo de KPIs aprobadas al 100%.
* [x] Validación funcional con la propietaria de la farmacia.
