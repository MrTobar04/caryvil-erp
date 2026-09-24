# SPEC-2.2.1: Definición de Roles y Grupos de Usuarios

## 1. Objective
Modelar, categorizar e implementar la jerarquía de grupos de seguridad y perfiles de usuario en Odoo para el personal de Farmacia Caryvil mediante el archivo de seguridad `security/caryvil_security.xml`. Esta especificación define los privilegios operacionales para cada nivel funcional de la farmacia (Cajero/Dependiente, Encargado de Compras e Inventario, y Administrador General / Propietaria), garantizando la separación de funciones y protegiendo las operaciones críticas del negocio.

## 2. Scope
### 2.1. Included
* Creación de la categoría de módulo `module_category_caryvil_erp` en Odoo para agrupar los permisos del sistema.
* Definición de los tres grupos de seguridad jerárquicos principales:
  1. `group_caryvil_cashier` (**Cajero / Dependiente de Mostrador**): Acceso al punto de venta y mostrador, consulta de existencias y precios de medicamentos, registro y búsqueda de clientes, y emisión de factura simple a consumidor final.
  2. `group_caryvil_inventory_purchases` (**Encargado de Compras e Inventario**): Creación de órdenes de compra a laboratorios, recepción física de mercadería con captura de lote y fecha de vencimiento, gestión de catálogo de medicamentos, registro de ajustes y mermas.
  3. `group_caryvil_manager` (**Administrador General / Propietaria**): Acceso total a todos los módulos operativos, visualización del Dashboard de analítica y métricas de ingresos, parametrización de reglas de reorden, anulación de transacciones y gestión de cuentas de usuario.
* Configuración de la herencia de privilegios (*implied groups*): el Administrador hereda los permisos de Encargado de Compras e Inventario, y este a su vez hereda los permisos de Cajero.

### 2.2. Not Included (Out of Scope)
* Configuración de permisos tabulares por modelo en `ir.model.access.csv` (cubierto en `SPEC-2.2.2`).
* Definición de reglas de registro por compañía o sucursal (`ir.rule`) (cubierto en `SPEC-2.2.2`).

## 3. Context and Restrictions
* **Context:** Establece la base de control de acceso basada en roles (RBAC) que gobierna la visualización de menús, botones de acción y formularios para cada empleado que inicie sesión en el ERP.
* **Restrictions:**
  * Un usuario con rol de Cajero no debe tener acceso a las pantallas de costo de adquisición de medicamentos de proveedores ni a la confirmación de órdenes de compra.
  * La anulación de facturas emitidas o bajas masivas de inventario debe estar estrictamente reservada para el rol de Administrador.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
* **Definition of Ready (DoR):**
  * [x] Organigrama y funciones del personal de Farmacia Caryvil analizados a partir de la entrevista técnica.
  * [x] Identificación de las operaciones permitidas y restringidas por puesto de trabajo.

## 5. Design (Implementation Details)
* **Architecture (`security/caryvil_security.xml`):**
  ```xml
  <?xml version="1.0" encoding="utf-8"?>
  <odoo>
      <data noupdate="0">
          <!-- Categoría de Seguridad Caryvil -->
          <record id="module_category_caryvil_erp" model="ir.module.category">
              <field name="name">Farmacia Caryvil</field>
              <field name="description">Gestión de niveles de acceso para Farmacia Caryvil</field>
              <field name="sequence">10</field>
          </record>

          <!-- Rol 1: Cajero / Dependiente de Mostrador -->
          <record id="group_caryvil_cashier" model="res.groups">
              <field name="name">Cajero / Dependiente de Mostrador</field>
              <field name="category_id" ref="module_category_caryvil_erp"/>
              <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
              <field name="comment">Acceso a ventas en mostrador, clientes y consulta de disponibilidad.</field>
          </record>

          <!-- Rol 2: Encargado de Compras e Inventario -->
          <record id="group_caryvil_inventory_purchases" model="res.groups">
              <field name="name">Encargado de Compras e Inventario</field>
              <field name="category_id" ref="module_category_caryvil_erp"/>
              <field name="implied_ids" eval="[(4, ref('group_caryvil_cashier')), (4, ref('stock.group_stock_user')), (4, ref('purchase.group_purchase_user'))]"/>
              <field name="comment">Acceso a catálogo de fármacos, lotes/vencimiento, compras y recepciones.</field>
          </record>

          <!-- Rol 3: Administrador General / Propietaria -->
          <record id="group_caryvil_manager" model="res.groups">
              <field name="name">Administrador / Propietario</field>
              <field name="category_id" ref="module_category_caryvil_erp"/>
              <field name="implied_ids" eval="[(4, ref('group_caryvil_inventory_purchases')), (4, ref('stock.group_stock_manager')), (4, ref('purchase.group_purchase_manager')), (4, ref('sales_team.group_sale_manager'))]"/>
              <field name="comment">Acceso total al sistema, configuraciones, costos y dashboard analítico.</field>
          </record>
      </data>
  </odoo>
  ```

## 6. Acceptance Criteria
* **Scenario 1: Asignación de rol de Cajero a un nuevo usuario**
  * **Given** Un usuario con el rol exclusivo `Cajero / Dependiente de Mostrador`.
  * **When** Inicia sesión en el ERP.
  * **Then** Debe tener acceso a crear ventas y registrar clientes, pero no debe visualizar los menús de Compras, Configuración del Sistema ni el Dashboard gerencial.
* **Scenario 2: Asignación de rol de Encargado de Compras e Inventario**
  * **Given** Un usuario con el rol `Encargado de Compras e Inventario`.
  * **When** Accede a la aplicación.
  * **Then** Debe poder generar órdenes de compra a proveedores, recibir mercadería asignando lotes y ajustar existencias, pero no debe tener permisos para modificar la configuración de la empresa ni eliminar usuarios.
* **Scenario 3: Control total para el rol Administrador**
  * **Given** Un usuario con el rol `Administrador / Propietario`.
  * **When** Ingresa al sistema.
  * **Then** Debe visualizar todos los menús, reportes de márgenes, dashboard analítico y opciones de configuración avanzada.

## 7. Verification Plan
* **Automated Tests:**
  * Prueba unitaria en Python creando tres usuarios de prueba (`test_cashier`, `test_stock_user`, `test_admin`) y verificando `user.has_group()` para cada grupo correspondiente.
* **Manual Verification:**
  * Iniciar sesión con cada usuario de prueba en el navegador y verificar visualmente la restricción y visibilidad de menús y botones de acción.

## 8. Security and Privacy
* Principio de mínimo privilegio: Los dependientes en mostrador no deben tener visibilidad sobre costos de compra ni márgenes de utilidad de los medicamentos.
* Los roles se almacenan en la tabla `res_groups_users_rel` y se evalúan en cada solicitud de vista o acción.

## 9. Risks and Mitigation
* **Risk:** Confusión de usuarios al no ver un menú por falta de un grupo heredado del núcleo de Odoo.
  * **Mitigation:** Incluir explícitamente en `implied_ids` los grupos nativos indispensables (`base.group_user`, `stock.group_stock_user`, `purchase.group_purchase_user`).

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/security/caryvil_security.xml`.
* Registro del archivo en la sección `data` del manifiesto `__manifest__.py`.

## 11. Definition of Done (DoD)
* [x] Archivo `caryvil_security.xml` implementado con los 3 roles y jerarquías.
* [x] Roles visibles y seleccionables en el formulario de usuarios de Odoo (`Ajustes > Usuarios`).
* [x] Herencia de permisos comprobada con usuarios de prueba para cada rol.
* [x] Revisión de código aprobada e integrada a la rama principal.
