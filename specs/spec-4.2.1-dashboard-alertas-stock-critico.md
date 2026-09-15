# SPEC-4.2.1: Dashboard de Alertas de Stock Crítico

## 1. Objective
Diseñar e implementar el componente visual de monitoreo y alerta de **Stock Crítico** dentro del Dashboard de inicio de Odoo para Farmacia Caryvil. Esta especificación permite identificar de forma instantánea y proactiva aquellos medicamentos cuyas existencias físicas actuales se encuentren en o por debajo del umbral mínimo de seguridad establecido, proporcionando accesos directos para la generación inmediata de órdenes de reabastecimiento a proveedores y previniendo el desabastecimiento de fármacos esenciales.

## 2. Scope
### 2.1. Included
* Creación del método de consulta y agregación en el modelo del dashboard para identificar productos con existencias en nivel de alerta: `qty_available <= min_stock_alert_level`.
* Implementación del widget visual en el Dashboard de inicio:
  * **Tarjeta de Resumen:** Conteo total de productos en situación crítica con distintivo visual en color rojo (`#DC3545`).
  * **Tabla de Detalle:** Listado de los medicamentos afectados mostrando: Nombre comercial, Principio activo, Categoría terapéutica, Existencia actual en mostrador/bodega, Nivel mínimo requerido y Déficit.
* Botón de acción rápida por fila: "Reabastecer", el cual abre un asistente (*wizard*) o genera un borrador de Orden de Compra precargado con el proveedor habitual y la cantidad sugerida de reposición.
* Acceso disponible para los grupos `group_caryvil_inventory_purchases` y `group_caryvil_manager`.

### 2.2. Not Included (Out of Scope)
* Configuración de reglas automatizadas de reorden desatendidas (cubierto en `SPEC-7.2.2`).
* Alertas de caducidad por fechas de lote (cubierto en `SPEC-4.2.2`).

## 3. Context and Restrictions
* **Context:** Resuelve directamente el problema identificado en la entrevista inicial con la propietaria, donde la falta de visibilidad provocaba que el personal se percatara de la falta de un medicamento solo cuando un cliente lo solicitaba en mostrador.
* **Restrictions:**
  * Debe evaluar exclusivamente productos de tipo almacenable (`detailed_type = 'product'`) y con estado activo (`active = True`).
  * El tiempo de renderizado del widget no debe exceder 400ms.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
  * `SPEC-2.2.1` (Definición de Roles y Grupos de Usuarios).
  * `SPEC-4.1.1` (Dashboard de KPIs de Ventas).
* **Definition of Ready (DoR):**
  * [x] Definición del campo de nivel mínimo de stock en la ficha del medicamento.
  * [x] Diseño visual del widget de alertas en Figma revisado.

## 5. Design (Implementation Details)
* **Backend Logic (`models/caryvil_dashboard.py`):**
  ```python
  @api.model
  def get_critical_stock_data(self):
      # Buscar productos almacenables con stock menor o igual a su stock mínimo
      critical_products = self.env['product.product'].search([
          ('detailed_type', '=', 'product'),
          ('active', '=', True),
          ('orderpoint_min_qty', '>', 0)
      ]).filtered(lambda p: p.qty_available <= p.orderpoint_min_qty)

      results = []
      for prod in critical_products[:10]: # Top 10 más críticos
          results.append({
              'product_id': prod.id,
              'name': prod.name,
              'active_ingredient': getattr(prod, 'active_ingredient_id', False) and prod.active_ingredient_id.name or 'N/A',
              'qty_available': prod.qty_available,
              'min_qty': prod.orderpoint_min_qty,
              'deficit': prod.orderpoint_min_qty - prod.qty_available,
              'uom': prod.uom_id.name,
              'supplier_name': prod.seller_ids and prod.seller_ids[0].partner_id.name or 'Sin Asignar'
          })

      return {
          'critical_count': len(critical_products),
          'critical_list': results
      }
  ```
* **UI/UX Presentation:**
  * Badge rojo brillante con animación sutil de pulso si el conteo crítico es superior a 0.
  * Botón verde "Crear PO" con icono de carrito de compras en cada fila de la tabla.

## 6. Acceptance Criteria
* **Scenario 1: Detección automática de medicamento bajo stock mínimo**
  * **Given** El medicamento "Amoxicilina 500mg" con stock mínimo configurado en 20 cajas y stock actual de 5 cajas.
  * **When** El encargado de inventario o la administradora cargan el Dashboard.
  * **Then** "Amoxicilina 500mg" debe figurar en la tabla de Alertas de Stock Crítico con badge rojo indicando stock: 5 / mín: 20 (Déficit: 15).
* **Scenario 2: Creación rápida de orden de compra desde el dashboard**
  * **Given** Un medicamento en estado crítico en la tabla de alertas.
  * **When** El usuario presiona el botón "Reabastecer" de esa fila.
  * **Then** El sistema debe abrir el formulario de Orden de Compra con el proveedor, medicamento y cantidad de reposición (15 cajas) precargados.
* **Scenario 3: Desaparición de la alerta tras reabastecimiento**
  * **Given** Un medicamento que figuraba en la lista crítica.
  * **When** Se recibe y valida un pedido que eleva su stock por encima del nivel mínimo.
  * **Then** El medicamento debe desaparecer automáticamente de la lista de alertas del dashboard.

## 7. Verification Plan
* **Automated Tests:**
  * Prueba unitaria en Python configurando un producto de prueba con stock inferior al umbral y verificando su inclusión en el payload retornado por `get_critical_stock_data()`.
* **Manual Verification:**
  * Forzar un ajuste de stock para dejar un fármaco en cero unidades y comprobar que aparezca de inmediato en el widget de inicio.

## 8. Security and Privacy
* Visibilidad restringida a usuarios con permisos de gestión de inventario y administración.

## 9. Risks and Mitigation
* **Risk:** Saturación visual si decenas de productos se encuentran sin stock al inicio del sistema.
  * **Mitigation:** Implementar paginación y límite de visualización en el Top 10 más prioritarios con enlace "Ver todos los productos críticos".

## 10. Deliverables & Config as Code
* Extensión del modelo `caryvil.dashboard.sales` con métodos de análisis de inventario.
* Componente XML en `views/caryvil_dashboard_views.xml`.

## 11. Definition of Done (DoD)
* [ ] Widget de stock crítico implementado y visible en el Dashboard.
* [ ] Contador y listado de productos en alerta vinculados con el stock real.
* [ ] Botón de acción rápida "Reabastecer" funcionando y precargando la Orden de Compra.
* [ ] Pruebas unitarias ejecutadas y aprobadas.
* [ ] Validación funcional con el encargado de inventario de Caryvil.
