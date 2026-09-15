# SPEC-3.2.1: Personalización del Diseño y Navegación

## 1. Objective
Estructurar y optimizar la navegación, jerarquía de menús y accesibilidad de la interfaz de usuario en Odoo para Farmacia Caryvil mediante el archivo `views/caryvil_menus.xml`. Esta especificación organiza los accesos a los módulos operativos siguiendo el flujo de trabajo real de una farmacia de mostrador (Inicio/Dashboard, Ventas, Inventario, Compras, Clientes y Configuración), reduciendo la cantidad de clics necesarios para completar operaciones frecuentes y ofreciendo atajos de teclado y botones ergonómicos.

## 2. Scope
### 2.1. Included
* Creación de la estructura jerárquica de menús en `custom_addons/caryvil_erp/views/caryvil_menus.xml`:
  * `menu_caryvil_root`: Menú principal "Farmacia Caryvil".
  * `menu_caryvil_dashboard`: Acceso directo al panel analítico (Dashboard de Inicio).
  * `menu_caryvil_sales`: Menú de Ventas (Punto de Venta / Mostrador, Facturas Simples, Sesiones de Caja).
  * `menu_caryvil_inventory`: Menú de Inventario (Medicamentos, Lotes y Vencimientos, Ajustes de Stock, Mermas).
  * `menu_caryvil_purchases`: Menú de Compras (Órdenes de Compra, Recepciones de Mercadería, Proveedores/Laboratorios).
  * `menu_caryvil_customers`: Menú de Clientes (Directorio de Clientes, Historial de Compras).
  * `menu_caryvil_config`: Menú de Configuración (Categorías Terapéuticas, Principios Activos, Unidades de Medida).
* Asignación de secuencias (`sequence`) numéricas para garantizar el orden de izquierda a derecha o de arriba hacia abajo.
* Asignación de grupos de seguridad (`groups`) a cada menú para que los usuarios visualicen únicamente las secciones autorizadas para su rol.

### 2.2. Not Included (Out of Scope)
* Estilos de color y tema general (cubierto en `SPEC-3.1.1`).
* Definición de vistas de árbol o formularios específicas de cada entidad (cubierto en los Dominios 4 a 9).

## 3. Context and Restrictions
* **Context:** Define la arquitectura de información y el mapa del sitio dentro de Odoo, determinando cómo el personal interactúa diariamente con el software de forma ágil y sin fricción.
* **Restrictions:**
  * El dependiente de farmacia no debe tener que realizar más de 2 clics desde la pantalla principal para iniciar una venta o buscar un medicamento.
  * Los menús deben adaptarse a resoluciones compactas (pantallas táctiles de punto de venta y laptops de 14 pulgadas).

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
  * `SPEC-2.2.1` (Definición de Roles y Grupos de Usuarios).
  * `SPEC-3.1.1` (Personalización de Marca y Tema Visual).
* **Definition of Ready (DoR):**
  * [x] Mapa de navegación acordado con base en los mockups de Figma.
  * [x] Grupos de seguridad identificados para asignación a cada nivel de menú.

## 5. Design (Implementation Details)
* **Menu Architecture (`views/caryvil_menus.xml`):**
  ```xml
  <?xml version="1.0" encoding="utf-8"?>
  <odoo>
      <!-- Menú Raíz Principal -->
      <menuitem id="menu_caryvil_root"
                name="Farmacia Caryvil"
                web_icon="caryvil_erp,static/description/icon.png"
                sequence="10"/>

      <!-- 1. Dashboard de Inicio -->
      <menuitem id="menu_caryvil_dashboard"
                name="Dashboard"
                parent="menu_caryvil_root"
                action="action_caryvil_dashboard"
                sequence="10"
                groups="caryvil_erp.group_caryvil_manager"/>

      <!-- 2. Ventas y Facturación -->
      <menuitem id="menu_caryvil_sales_root"
                name="Ventas"
                parent="menu_caryvil_root"
                sequence="20"
                groups="caryvil_erp.group_caryvil_cashier"/>

      <!-- 3. Inventario y Medicamentos -->
      <menuitem id="menu_caryvil_inventory_root"
                name="Inventario"
                parent="menu_caryvil_root"
                sequence="30"
                groups="caryvil_erp.group_caryvil_inventory_purchases"/>

      <!-- 4. Compras y Abastecimiento -->
      <menuitem id="menu_caryvil_purchases_root"
                name="Compras"
                parent="menu_caryvil_root"
                sequence="40"
                groups="caryvil_erp.group_caryvil_inventory_purchases"/>

      <!-- 5. Directorio de Clientes -->
      <menuitem id="menu_caryvil_customers_root"
                name="Clientes"
                parent="menu_caryvil_root"
                sequence="50"
                groups="caryvil_erp.group_caryvil_cashier"/>

      <!-- 6. Configuración Farmacéutica -->
      <menuitem id="menu_caryvil_config_root"
                name="Configuración"
                parent="menu_caryvil_root"
                sequence="60"
                groups="caryvil_erp.group_caryvil_manager"/>
  </odoo>
  ```

## 6. Acceptance Criteria
* **Scenario 1: Navegación del personal de mostrador (Cajero)**
  * **Given** Un usuario con rol `Cajero / Dependiente de Mostrador` conectado al sistema.
  * **When** Observa la barra de menús principal.
  * **Then** Debe visualizar exclusivamente los menús "Ventas" y "Clientes", ocultando "Dashboard", "Compras", "Inventario" y "Configuración".
* **Scenario 2: Navegación del Encargado de Compras e Inventario**
  * **Given** Un usuario con rol `Encargado de Compras e Inventario`.
  * **When** Accede a la aplicación.
  * **Then** Debe visualizar los menús "Ventas", "Inventario", "Compras" y "Clientes", con acceso directo a recepciones y lotes.
* **Scenario 3: Acceso unificado para la Propietaria/Administradora**
  * **Given** El usuario administrador conectado.
  * **When** Ingresa al sistema.
  * **Then** El primer elemento destacado debe ser el menú "Dashboard" seguido de la totalidad de las opciones operativas y de configuración.

## 7. Verification Plan
* **Automated Tests:**
  * Prueba XML en Odoo comprobando que todos los identificadores de `parent` y `action` existan y no generen errores `ParseError` durante la carga.
* **Manual Verification:**
  * Iniciar sesión con diferentes roles y validar que la barra de navegación muestre el orden correcto (`Dashboard -> Ventas -> Inventario -> Compras -> Clientes -> Configuración`).

## 8. Security and Privacy
* La directiva `groups="..."` en cada etiqueta `menuitem` asegura que usuarios no autorizados ni siquiera conozcan la existencia de menús sensibles en el DOM.

## 9. Risks and Mitigation
* **Risk:** Confusión del usuario si los menús nativos de Odoo (`Ventas`, `Inventario` estándar) aparecen duplicados junto a los de Caryvil.
  * **Mitigation:** Reutilizar o reordenar los menús existentes vinculando las acciones correspondientes bajo el menú raíz `menu_caryvil_root`.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/views/caryvil_menus.xml`.
* Inclusión del archivo en la sección `data` del manifiesto `__manifest__.py`.

## 11. Definition of Done (DoD)
* [ ] Estructura completa de menús implementada en `caryvil_menus.xml`.
* [ ] Orden de secuencias verificado de acuerdo al flujo de trabajo de la farmacia.
* [ ] Filtros de visibilidad por grupo de seguridad validados en pruebas manuales.
* [ ] Revisión de arquitectura de información aprobada.
