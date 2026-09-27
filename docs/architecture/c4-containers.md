# Diagrama C4 - Nivel 2: Contenedores (Container Diagram)

Este documento detalla la arquitectura de contenedores de software de **Farmacia Caryvil ERP**, ilustrando las aplicaciones ejecutables, almacenes de datos y protocolos de comunicación entre los límites del sistema.

## Diagrama de Contenedores C4

```mermaid
C4Container
  title Diagrama de Contenedores - Farmacia Caryvil ERP

  Person(user, "Usuario del ERP", "Farmacéutico, Cajero o Gestor.")

  Container_Boundary(caryvilSystem, "Sistema Farmacia Caryvil ERP") {
    Container(webBrowser, "Cliente Web Browser", "HTML5, SCSS, JS (OWL)", "SPA interactiva con vistas de venta, dashboards y catálogos.")
    Container(odooServer, "Servidor Odoo 17", "Python 3.10, Werkzeug, ORM", "Servidor de aplicación, enrutamiento RPC y motor ORM.")
    Container(caryvilAddon, "Módulo caryvil_erp", "Python, XML, QWeb, OWL", "Lógica de negocio: FEFO, UoM farmacéuticas y validación DUI/NIT.")
    ContainerDb(postgresDb, "Base de Datos", "PostgreSQL 16", "Persistencia relacional de catálogos, lotes, ventas y contabilidad.")
  }

  System_Ext(impresoraTicket, "Impresora POS 80mm", "Hardware Térmico", "Impresión física de tickets.")

  Rel_D(user, webBrowser, "Opera interfaz", "HTTPS")
  Rel_D(webBrowser, odooServer, "Envía peticiones", "JSON-RPC / 8069")
  Rel_R(odooServer, caryvilAddon, "Carga módulo", "Python Hook")
  Rel_D(odooServer, postgresDb, "Gestiona sesiones y tablas", "SQL / 5432")
  Rel_D(caryvilAddon, postgresDb, "Persiste modelos de negocio", "SQL / 5432")
  Rel_R(caryvilAddon, impresoraTicket, "Emite ticket de venta", "QWeb / RAW")
```

## Descripción de Contenedores

### 1. Cliente Web Browser (Frontend OWL)
- **Tecnología:** JavaScript (OWL Framework de Odoo 17), HTML5, SCSS.
- **Responsabilidad:** Presentación interactiva para el usuario. Incorpora widgets personalizados como `caryvil_sales_dashboard.js` (KPIs en tiempo real), `masked_char_field.js` (máscaras para DUI/NIT) y `purchase_live_totals.js`.

### 2. Servidor de Aplicaciones Odoo (Runtime Python)
- **Tecnología:** Python 3.10+, Werkzeug WSGI, Motor ORM de Odoo 17.0.
- **Responsabilidad:** Procesamiento de solicitudes HTTP/RPC, control transaccional ACID, gestión de permisos a nivel de modelo/registro y compilación de plantillas QWeb.

### 3. Módulo de Negocio `caryvil_erp` (Custom Addon)
- **Tecnología:** Python, XML (Views/Data), QWeb (Reports), JS/XML (OWL Assets).
- **Responsabilidad:** Lógica farmacéutica especializada:
  - **Estrategia FEFO (`pharmacy_removal_strategy_data.xml`):** Despacho prioritario del lote con fecha de caducidad más cercana.
  - **Unidades de Medida Farmacéuticas (`pharmacy_uom_data.xml`):** Jerarquía de Caja, Blíster y Unidad/Pastilla.
  - **Validación de Identidad Salvadoreña:** Verificación sintáctica y módulo 10 para DUI (`00000000-0`) y formato de NIT.
  - **Tickets Térmicos:** Formato estrecho de 80mm optimizado para impresión rápida.

### 4. Base de Datos PostgreSQL 16 (Persistence Storage)
- **Tecnología:** PostgreSQL 16.x.
- **Responsabilidad:** Almacenamiento relacional de tablas principales (`res_partner`, `product_template`, `stock_lot`, `stock_quant`, `sale_order`, `purchase_order`, `account_move`).
