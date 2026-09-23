# SPEC-3.2.1: Personalización del Diseño y Navegación

## 1. Objective
Estructurar y estandarizar la arquitectura de información, la jerarquía de menús y los flujos de navegación dentro de Odoo para Farmacia Caryvil mediante el archivo `views/caryvil_menus.xml`, alineándolos fielmente con los mockups de diseño de la aplicación (`docs/mockups/`). Esta especificación define la barra lateral con 6 secciones modulares primarias (**Inicio, Inventario, Ventas, Compras, Clientes, Proveedores**), la barra superior con migas de pan dinámicas (*breadcrumbs*), la barra de acciones con botones de creación y búsqueda rápida, y los permisos de visibilidad basados en los roles de usuario.

## 2. Scope
### 2.1. Included
* Creación de la estructura de menús en `custom_addons/caryvil_erp/views/caryvil_menus.xml` reflejando el orden exacto de los mockups:
  1. `Inicio` (Dashboard analítico, KPIs de ventas, productos y vencimientos, gráfico de 7 días y alertas de stock).
  2. `Inventario` (Catálogo de medicamentos, vista cuadrícula/lista, lotes y vencimientos, creación de productos).
  3. `Ventas` (Punto de venta y facturación, registro de nueva venta, desglose de cambio y método de pago).
  4. `Compras` (Listado de órdenes de compra, creación de orden `PE001`, recepción de mercadería y lotes).
  5. `Clientes` (Directorio de clientes, código `CL0001`, creación rápida e historial de compras asociadas).
  6. `Proveedores` (Directorio de proveedores y laboratorios, código `P0001`, creación rápida e historial de pedidos).
* Configuración de la barra lateral izquierda (*Sidebar*):
  * Logotipo/Identificador "ERP FARMACIA" en la cabecera.
  * Iconografía modular unificada de 4 cuadrantes (`⊞`) para cada ítem de navegación.
  * Resaltado de ítem activo en cian (`#38B6FF`) con indicador vertical en el borde derecho.
* Configuración de la barra superior (*Topbar*):
  * Migas de pan (*breadcrumbs*) jerárquicas en texto blanco sobre fondo pizarra (`#5C6F84`) (e.g., `Clientes > Nuevo`, `Compras > Nueva Orden de Compra`, `Inventario > Nuevo`, `Ventas > Nueva Venta`, `Proveedores > Nuevo`).
  * Icono de notificaciones (campana) y avatar de perfil de usuario (`Administrador`).
* Estandarización de la barra de acciones de vista:
  * Botón primario verde (`[ Cliente Nuevo ]`, `[ Nueva Compra ]`, `[ Crear ]`, `[ Nueva Venta ]`, `[ Proveedor Nuevo ]` en listados; `[ Guardar ]` en formularios).
  * Botón secundario contorneado `[ Cancelar ]` en formularios de creación y edición.
  * Caja de búsqueda tipo píldora con icono de lupa `🔍` y botón de filtros `Y`.
  * Selector de vista Cuadrícula / Lista (`[🗋] [☰]`) en el módulo de Inventario.
  * Paginación inferior centrada (`< 1 2 3 4 ... 10 >`).
* Asignación de secuencias (`sequence`) y grupos de seguridad (`groups`) para restringir accesos según el rol.

### 2.2. Not Included (Out of Scope)
* Definición de estilos CSS/SCSS puros (cubierto en `SPEC-3.1.1`).
* Definición de lógica interna de modelos backend (cubierto en Dominios 4 al 9).

## 3. Context and Restrictions
* **Context:** Define la experiencia de usuario (UX) central de la farmacia, permitiendo al personal de mostrador y administración moverse fluidamente entre tareas con menos de 2 clics.
* **Restrictions:**
  * Compatibilidad con la arquitectura OWL y QWeb de Odoo 17.
  * Adaptabilidad completa para monitores estándar de farmacia (1366x768) y resoluciones superiores.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
  * `SPEC-2.2.1` (Definición de Roles y Grupos de Usuarios).
  * `SPEC-3.1.1` (Personalización de Marca y Tema Visual).
* **Definition of Ready (DoR):**
  * [x] Mockups de todas las pantallas inspeccionados y consolidados (`docs/mockups/`).
  * [x] Estructura jerárquica de 6 módulos principales aprobada.

## 5. Design (Implementation Details)
* **Menu Structure (`views/caryvil_menus.xml`):**
  ```xml
  <?xml version="1.0" encoding="utf-8"?>
  <odoo>
      <!-- Menú Raíz Principal -->
      <menuitem id="menu_caryvil_root"
                name="ERP FARMACIA"
                web_icon="caryvil_erp,static/description/icon.png"
                sequence="10"/>

      <!-- 1. Inicio (Dashboard) -->
      <menuitem id="menu_caryvil_dashboard"
                name="Inicio"
                parent="menu_caryvil_root"
                action="action_caryvil_dashboard"
                sequence="10"
                groups="caryvil_erp.group_caryvil_cashier,caryvil_erp.group_caryvil_inventory_purchases,caryvil_erp.group_caryvil_manager"/>

      <!-- 2. Inventario -->
      <menuitem id="menu_caryvil_inventory"
                name="Inventario"
                parent="menu_caryvil_root"
                action="action_caryvil_inventory_medicines"
                sequence="20"
                groups="caryvil_erp.group_caryvil_inventory_purchases,caryvil_erp.group_caryvil_manager"/>

      <!-- 3. Ventas -->
      <menuitem id="menu_caryvil_sales"
                name="Ventas"
                parent="menu_caryvil_root"
                action="action_caryvil_sales_orders"
                sequence="30"
                groups="caryvil_erp.group_caryvil_cashier,caryvil_erp.group_caryvil_manager"/>

      <!-- 4. Compras -->
      <menuitem id="menu_caryvil_purchases"
                name="Compras"
                parent="menu_caryvil_root"
                action="action_caryvil_purchase_orders"
                sequence="40"
                groups="caryvil_erp.group_caryvil_inventory_purchases,caryvil_erp.group_caryvil_manager"/>

      <!-- 5. Clientes -->
      <menuitem id="menu_caryvil_customers"
                name="Clientes"
                parent="menu_caryvil_root"
                action="action_caryvil_customers"
                sequence="50"
                groups="caryvil_erp.group_caryvil_cashier,caryvil_erp.group_caryvil_manager"/>

      <!-- 6. Proveedores -->
      <menuitem id="menu_caryvil_suppliers"
                name="Proveedores"
                parent="menu_caryvil_root"
                action="action_caryvil_suppliers"
                sequence="60"
                groups="caryvil_erp.group_caryvil_inventory_purchases,caryvil_erp.group_caryvil_manager"/>
  </odoo>
  ```

## 6. Acceptance Criteria
* **Scenario 1: Despliegue de la barra lateral con 6 opciones principales**
  * **Given** Un usuario administrador conectado al sistema.
  * **When** Observa la barra de navegación lateral izquierda.
  * **Then** Debe visualizar los 6 ítems en el orden exacto: `Inicio`, `Inventario`, `Ventas`, `Compras`, `Clientes` y `Proveedores`.
* **Scenario 2: Indicador de menú activo y miga de pan en cabecera**
  * **Given** Un usuario navegando a la pantalla de creación de una nueva venta.
  * **When** Carga la vista.
  * **Then** El ítem `Ventas` en el sidebar se ilumina en cian con su indicador lateral, y la barra superior muestra la miga de pan `Ventas > Nueva Venta`.
* **Scenario 3: Controles de barra de acciones y botones**
  * **Given** Un usuario en la vista principal de `Clientes` o `Inventario`.
  * **When** Se visualiza la cabecera del contenido.
  * **Then** Se muestra el botón primario verde (`Cliente Nuevo` o `Crear`), la barra de búsqueda tipo píldora con placeholder descriptivo, el icono de filtro y, en Inventario, el alternador de vista Cuadrícula/Lista.
* **Scenario 4: Restricción de visibilidad por rol de usuario**
  * **Given** Un usuario con rol `Cajero / Dependiente de Mostrador`.
  * **When** Ingresa al ERP.
  * **Then** Visualiza únicamente `Inicio`, `Ventas` y `Clientes`, manteniéndose ocultos los módulos operativos de `Compras` e `Inventario` reservando la seguridad del sistema.

## 7. Verification Plan
* **Automated Tests:**
  * Test XML de carga de menús validando que todos los identificadores de acción y padres existan sin excepciones `ParseError`.
* **Manual Verification:**
  * Probar navegación cruzada entre todos los módulos validando consistencia en breadcrumbs y botones de acción contra los mockups de `docs/mockups/`.

## 8. Security and Privacy
* Control estricto de visibilidad de menús con atributos `groups` de Odoo para evitar exposición de opciones no autorizadas.

## 9. Risks and Mitigation
* **Risk:** Solapamiento de menús estándar de Odoo con la estructura simplificada de Farmacia Caryvil.
  * **Mitigation:** Uso de vistas heredadas y acciones limpias agrupadas exclusivamente bajo el menú raíz `menu_caryvil_root`.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/views/caryvil_menus.xml`.
* Inclusión del archivo en `data` dentro de `__manifest__.py`.

## 11. Definition of Done (DoD)
* [ ] Estructura de 6 módulos (`Inicio`, `Inventario`, `Ventas`, `Compras`, `Clientes`, `Proveedores`) implementada en `caryvil_menus.xml`.
* [ ] Breadcrumbs jerárquicos y estados activos en cian validados visualmente.
* [ ] Botones de acción verdes y controles de búsqueda alineados con los mockups.
* [ ] Permisos de grupo verificados para cada rol de usuario.

