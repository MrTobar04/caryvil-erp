# Diagrama C4 - Nivel 3: Componentes del Addon caryvil_erp (Component Diagram)

Este documento describe la estructura interna de componentes del módulo `caryvil_erp`, ilustrando cómo se relacionan los modelos ORM, controladores HTTP, vistas OWL y motores de reportes dentro del contenedor del servidor Odoo.

## Diagrama de Componentes C4

```mermaid
C4Component
  title Diagrama de Componentes - Módulo caryvil_erp

  UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")

  Container(webClient, "Cliente Web Browser", "JS / OWL Framework", "Interfaz de usuario de Odoo.")

  Container_Boundary(caryvilAddon, "Módulo caryvil_erp") {
    Component(dashboardWidget, "Dashboard OWL", "OWL / JS", "KPIs de ventas diarias y stock crítico.")
    Component(qwebEngine, "Motor Reportes QWeb", "XML / Python", "Generación de ticket térmico 80mm.")
    Component(securityRules, "Seguridad RBAC", "XML / CSV", "Grupos y reglas de acceso a registros.")

    Component(partnerModel, "Clientes (res.partner)", "Python ORM", "Validación DUI/NIT salvadoreño.")
    Component(saleModel, "Ventas (sale.order)", "Python ORM", "Venta mostrador, cálculo IVA y cobro.")
    Component(purchaseModel, "Compras (purchase.order)", "Python ORM", "Abastecimiento y costes.")

    Component(medicineModel, "Medicamentos (product.product)", "Python ORM", "Principio activo y UoM farmacéuticas.")
    Component(lotModel, "Lotes FEFO (stock.lot)", "Python ORM", "Vencimiento y asignación FEFO.")
    Component(scrapModel, "Mermas (stock.scrap)", "Python ORM", "Bajas de lotes caducados.")
  }

  ContainerDb(postgresDb, "Base de Datos", "PostgreSQL 16", "Persistencia relacional.")

  Rel_D(webClient, dashboardWidget, "Consulta KPIs", "JSON-RPC")
  Rel_D(webClient, saleModel, "Envía orden venta", "JSON-RPC")
  Rel_D(webClient, purchaseModel, "Registra compra", "JSON-RPC")

  Rel_R(saleModel, qwebEngine, "Renderiza ticket", "QWeb")
  Rel_L(saleModel, partnerModel, "Asocia cliente", "ORM")
  Rel_D(saleModel, medicineModel, "Valida producto", "ORM")
  Rel_D(saleModel, lotModel, "Reserva por FEFO", "ORM")

  Rel_D(purchaseModel, lotModel, "Registra lote", "ORM")
  Rel_L(scrapModel, lotModel, "Descarga lote", "ORM")

  Rel_D(partnerModel, postgresDb, "Persiste contactos", "SQL")
  Rel_D(saleModel, postgresDb, "Persiste transacciones", "SQL")
  Rel_D(lotModel, postgresDb, "Persiste inventario", "SQL")
```

## Descripción de Componentes Internos

### 1. Componentes de Presentación y Reportes
- **Dashboard OWL (`caryvil_sales_dashboard.js`):** Componente reactivo en OWL para la visualización de indicadores operativos (ventas del día, categorías con mayor rotación y alertas de lotes por caducar en 30/60 días).
- **Motor Reportes QWeb (`report_invoice_ticket.xml`):** Plantilla optimizada para rollos térmicos estándar de 80mm con desglose legal del IVA (13%) y encabezado fiscal.
- **Seguridad RBAC (`caryvil_security.xml`, `ir.model.access.csv`):** Matriz de permisos segmentada por roles (Cajero, Farmacéutico, Gestor de Inventario, Administrador).

### 2. Capa de Modelos Transaccionales
- **Clientes y Proveedores (`res.partner`):** Validador con algoritmo de comprobación para DUI (`00000000-0`) y NIT, además de segmentación de clientes comerciales y Consumidor Final.
- **Ventas de Mostrador (`sale.order`):** Flujo ágil para venta en caja, confirmación inmediata, cálculo de impuestos salvadoreños y generación de salida de almacén.
- **Compras y Abastecimiento (`purchase.order`):** Órdenes de reabastecimiento con proveedores, captura de costos unitarios netos y recepción de mercancía.

### 3. Capa de Inventario y Trazabilidad Farmacéutica
- **Medicamentos (`product.product`):** Catálogo especializado con atributos de principio activo, concentración, registro sanitario y jerarquía de unidades fraccionadas (Caja, Blíster, Unidad).
- **Lotes y FEFO (`stock.lot`):** Núcleo de trazabilidad sanitaria. Aplica la estrategia *First Expired, First Out* garantizando el despacho prioritario de productos próximos a vencer.
- **Mermas (`stock.scrap`):** Registro de bajas controladas por caducidad o deterioro físico con destino a ubicaciones de desecho farmacéutico.
