# Plan Maestro de Especificaciones (Spec-Plan)

## 1. Visión General del Proyecto
El proyecto consiste en el desarrollo, personalización e implantación de un sistema ERP basado en **Odoo Community Edition** para **Farmacia Caryvil** (ubicada en Soyapango, San Salvador). El objetivo central es transformar y digitalizar la operación integral del negocio: administración centralizada de inventario farmacéutico con trazabilidad obligatoria de lotes y fechas de vencimiento, compras y abastecimiento formal a laboratorios/proveedores con actualización automática de existencias, procesamiento de ventas en mostrador con facturación simple a consumidor final y deducción automática inteligente de stock mediante estrategia FEFO (First Expired, First Out), directorio de clientes con validación de DUI salvadoreño, monitoreo gerencial a través de un dashboard de analítica en tiempo real y una arquitectura moderna en la nube en Render con Docker, PostgreSQL, Terraform y CI/CD en GitHub Actions.

## 2. Restricciones Globales y Supuestos Técnicos
* **Plataforma ERP:** Odoo Community Edition ejecutado sobre entorno Python 3.10+ y PostgreSQL 15+.
* **Infraestructura Cloud:** Despliegue en la plataforma Render (Web Service y Base de Datos PostgreSQL) gestionado como código mediante Terraform.
* **Pipeline CI/CD:** GitHub Actions configurado para validación de código (linter/flake8), verificación de configuraciones Terraform, pruebas unitarias y despliegue automático hacia Render.
* **Alcance Fiscal de Facturación:** Emisión estricta de factura simple a consumidor final con cálculo desglosado o incluido de IVA (13%), sin integración con Ministerio de Hacienda ni crédito fiscal en esta iteración.
* **Estrategia de Despacho de Inventario:** Salida de existencias en ventas gobernada por la política FEFO (First Expired, First Out) para priorizar lotes con fecha de caducidad más cercana.
* **Diseño e Identidad UI/UX:** Paleta cromática corporativa institucional de Farmacia Caryvil (azul #0056B3 / verde #28A745), logotipo personalizado y barra de navegación ergonómica optimizada para personal de mostrador.
* **Metodología de Desarrollo:** Spec-Driven Development (SDD) con arquitectura modular X.Y.Z, donde cada especificación técnica representa una unidad de entrega atómica, medible y sin colisiones de alcance.

---

## 3. Índice Maestro de Especificaciones (Taxonomía X.Y.Z)

### Dominio 1: Infraestructura, Contenedores y CI/CD
* **1.1. Entorno de Contenedores y Configuración Base**
  * `spec-1.1.1-configuracion-entorno-docker.md` - Definición de Dockerfile y orquestación con Docker Compose para Odoo y PostgreSQL.
  * `spec-1.1.2-configuracion-servidor-odoo.md` - Archivo de configuración `odoo.conf`, gestión de rutas de addons y dependencias Python.
* **1.2. Infraestructura como Código (Terraform)**
  * `spec-1.2.1-aprovisionamiento-render-terraform.md` - Aprovisionamiento automatizado de Web Service y PostgreSQL en Render con Terraform.
  * `spec-1.2.2-gestion-variables-entorno-secretos.md` - Configuración y resguardo de variables de entorno, credenciales y secretos de producción.
* **1.3. Pipeline de Integración y Entrega Continua (CI/CD)**
  * `spec-1.3.1-pipeline-ci-cd-github-actions.md` - Pipeline automatizado de linting, ejecución de pruebas y despliegue continuo en Render.

### Dominio 2: Arquitectura del Módulo Personalizado y Seguridad
* **2.1. Estructura del Módulo Custom de Odoo**
  * `spec-2.1.1-estructura-modulo-caryvil-erp.md` - Scaffolding del módulo custom `caryvil_erp`, manifiesto `__manifest__.py` y dependencias base.
* **2.2. Seguridad, Roles y Permisos de Acceso**
  * `spec-2.2.1-definicion-roles-usuarios.md` - Definición de grupos de seguridad de usuarios (Cajero, Encargado de Compras/Inventario, Administrador).
  * `spec-2.2.2-reglas-acceso-seguridad-modelos.md` - Configuración de listas de control de acceso (`ir.model.access.csv`) y reglas de registro (`ir.rule`).

### Dominio 3: Diseño UI/UX y Personalización de Interfaz
* **3.1. Identidad Visual y Estilos**
  * `spec-3.1.1-personalizacion-marca-tema.md` - Aplicación de colores corporativos institucionales (azul/verde) y estilos globales en Odoo.
  * `spec-3.1.2-personalizacion-pantalla-autenticacion.md` - Personalización de la interfaz de inicio de sesión con marca y logotipo oficial de Farmacia Caryvil.
* **3.2. Ergonomía y Navegación**
  * `spec-3.2.1-personalizacion-diseno-navegacion.md` - Adaptación ergonómica de menús y barras de acceso rápido optimizadas para atención en farmacia.
* **3.3. Plantillas de Reportes Impresos**
  * `spec-3.3.1-plantilla-reporte-factura-ticket.md` - Diseño de plantilla QWeb para impresión de ticket y factura simple para consumidor final.
  * `spec-3.3.2-plantilla-reporte-orden-compra.md` - Diseño de plantilla QWeb para impresión de órdenes de compra formales para laboratorios.

### Dominio 4: Dashboard de Inicio y Analítica Gerencial
* **4.1. Indicadores de Ventas e Ingresos**
  * `spec-4.1.1-dashboard-kpis-ventas.md` - Panel en tiempo real con KPIs de ventas diarias, ticket promedio y acumulados de facturación.
* **4.2. Indicadores y Alertas de Inventario**
  * `spec-4.2.1-dashboard-alertas-stock-critico.md` - Visualización de productos con existencias por debajo del nivel mínimo de seguridad.
  * `spec-4.2.2-dashboard-alertas-vencimiento-lotes.md` - Panel de alertas tempranas de medicamentos próximos a caducar (30, 60 y 90 días).

### Dominio 5: Módulo de Clientes (Gestión de Contactos)
* **5.1. Perfil y Validación de Clientes**
  * `spec-5.1.1-gestion-perfil-clientes.md` - Modelo de datos de clientes con validación de formato para DUI salvadoreño, datos de contacto y dirección.
* **5.2. Búsqueda Ágil e Historial**
  * `spec-5.2.1-busqueda-rapida-clientes-caja.md` - Búsqueda instantánea de clientes por DUI, teléfono o nombre en el flujo de caja.
  * `spec-5.2.2-historial-compras-clientes.md` - Consulta centralizada y trazabilidad histórica de transacciones y medicamentos por cliente.

### Dominio 6: Módulo de Proveedores y Laboratorios
* **6.1. Directorio y Condiciones de Proveedores**
  * `spec-6.1.1-directorio-gestion-proveedores.md` - Directorio centralizado de distribuidores y laboratorios con NIT, NRC, contacto y plazos de entrega.
* **6.2. Lista de Precios y Catálogo de Proveedor**
  * `spec-6.2.1-catalogo-precios-proveedores.md` - Asociación de códigos de producto y listas de precios de compra referenciales por laboratorio.

### Dominio 7: Módulo de Inventario y Medicamentos
* **7.1. Catálogo Farmacéutico y Categorización**
  * `spec-7.1.1-catalogo-categorizacion-medicamentos.md` - Ficha técnica de medicamentos (principio activo, presentación, concentración, código de barras, categoría).
  * `spec-7.1.2-gestion-unidades-medida-farmaceuticas.md` - Configuración de unidades de medida (caja, blíster, frasco, unidad) y factores de conversión.
* **7.2. Trazabilidad de Lotes y Fechas de Vencimiento**
  * `spec-7.2.1-control-stock-lotes-vencimientos.md` - Seguimiento obligatorio de números de lote y fechas de vencimiento en cada ubicación de existencias.
  * `spec-7.2.2-reglas-reabastecimiento-stock-minimo.md` - Parametrización de niveles mínimos de stock con cálculo automático de necesidades de compra.
* **7.3. Movimientos, Mermas y Ajustes Físicos**
  * `spec-7.3.1-movimientos-ajustes-inventario.md` - Registro auditado de conteos físicos y conciliación de diferencias de existencias.
  * `spec-7.3.2-gestion-mermas-bajas-medicamentos.md` - Registro y justificación de bajas de inventario por deterioro, rotura o vencimiento.

### Dominio 8: Módulo de Compras y Abastecimiento
* **8.1. Gestión de Órdenes de Compra**
  * `spec-8.1.1-gestion-ordenes-compra.md` - Creación, cálculo de costos, aplicación de IVA (13%) y ciclo de vida de órdenes de compra a proveedores.
* **8.2. Recepción de Mercadería e Integración con Inventario**
  * `spec-8.2.1-recepcion-mercaderia-registro-lotes.md` - Verificación física de albaranes de entrega y captura obligatoria de lote y vencimiento provisto.
  * `spec-8.2.2-actualizacion-automatica-stock-compras.md` - Incremento transaccional automático de existencias en inventario al confirmar la recepción.
  * `spec-8.2.3-control-discrepancias-recepcion-compras.md` - Manejo y control de entregas parciales o discrepancias entre lo solicitado y lo recibido.

### Dominio 9: Módulo de Ventas y Facturación
* **9.1. Atención y Transacciones en Mostrador**
  * `spec-9.1.1-procesamiento-transacciones-ventas.md` - Registro ágil de ventas en mostrador con búsqueda rápida por nombre comercial, principio activo o código de barras.
* **9.2. Facturación Simple a Consumidor Final**
  * `spec-9.2.1-generacion-factura-simple.md` - Generación y correlativo de facturas simples para consumidor final con desglose de IVA (13%).
* **9.3. Integración con Inventario y Estrategia de Salida**
  * `spec-9.3.1-deduccion-automatica-stock-ventas.md` - Deducción transaccional automática e instantánea de unidades vendidas en inventario al confirmar venta.
  * `spec-9.3.2-estrategia-salida-fefo-lotes.md` - Asignación inteligente de lotes según política FEFO (First Expired, First Out) priorizando la salida del producto más próximo a caducar.

### Dominio 10: Datos Semilla y Carga Inicial
* **10.1. Datos Maestros Base del Sistema**
  * `spec-10.1.1-datos-semilla-maestros.md` - Carga de datos base: compañía Farmacia Caryvil, moneda USD, impuestos (IVA 13%), unidades de medida y categorías terapéuticas.
* **10.2. Datos Operativos de Demostración y Prueba**
  * `spec-10.2.1-datos-semilla-operativos.md` - Carga del catálogo representativo de medicamentos de Caryvil, stock inicial por lote con vencimiento, clientes y proveedores muestra.

### Dominio 11: Pruebas Automatizadas y Validación de Flujos
* **11.1. Pruebas de Flujos Integrales de Negocio**
  * `spec-11.1.1-pruebas-flujo-compras-inventario.md` - Pruebas automatizadas de integración del ciclo de abastecimiento: Orden de compra -> Recepción con lote -> Aumento en inventario.
  * `spec-11.1.2-pruebas-flujo-ventas-fefo-facturacion.md` - Pruebas automatizadas de integración del ciclo de ventas: Venta -> Despacho FEFO -> Deducción de stock -> Emisión de factura.
  * `spec-11.1.3-pruebas-validaciones-datos-locales.md` - Pruebas unitarias para validación de formato de DUI salvadoreño, cálculos de IVA y prevención de stock negativo.
