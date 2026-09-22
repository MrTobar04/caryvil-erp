# SPEC-2.2.2: Reglas de Acceso y Seguridad de Modelos

## 1. Objetivo
Definir y configurar de forma granular los permisos de lectura, escritura, creación y eliminación (CRUD) a nivel de modelo de datos mediante el archivo `security/ir.model.access.csv`, así como las reglas de seguridad a nivel de registro (`ir.rule`) en `security/caryvil_security_rules.xml`. Esta especificación salvaguarda la integridad de las bases de datos de Farmacia Caryvil, asegurando que cada rol de usuario interactúe estrictamente con los objetos de negocio que le corresponden y previniendo la alteración o eliminación no autorizada de registros históricos (como facturas emitidas, albaranes validados o compras confirmadas).

## 2. Scope
### 2.1. Included
* Creación y parametrización del archivo `security/ir.model.access.csv` con los permisos CRUD (`perm_read`, `perm_write`, `perm_create`, `perm_unlink`) para los modelos personalizados y extensiones de Farmacia Caryvil:
  * Modelos propios: `caryvil.therapeutic.category`, `caryvil.active.ingredient`, `caryvil.stock.loss`.
  * Modelos base extendidos: `res.partner` (Clientes y Proveedores), `product.template` / `product.product` (Medicamentos), `stock.production.lot` (Lotes y Vencimientos), `purchase.order`, `sale.order`, `account.move` (Facturación simple).
* Creación de reglas de registro (`ir.rule`) en `security/caryvil_security_rules.xml`:
  * Regla de solo lectura para facturas validadas/publicadas para el rol Cajero (impedir edición de facturas emitidas).
  * Regla de bloqueo de eliminación de órdenes de venta confirmadas y albaranes validados para usuarios sin rol Administrador.
  * Regla de autorización obligatoria de mermas y bajas de inventario para personal no administrador.

### 2.2. Not Included (Out of Scope)
* Definición de la jerarquía de grupos de seguridad (cubierto en `SPEC-2.2.1`).
* Implementación de los campos de los modelos en Python (cubierto en los Dominios 5, 6, 7, 8 y 9).

## 3. Context and Restrictions
* **Context:** Constituye la barrera de seguridad transaccional del ERP, evaluada por el motor ORM de Odoo antes de permitir cualquier operación en la base de datos PostgreSQL.
* **Restrictions:**
  * Ningún usuario que no sea Administrador puede tener permisos de eliminación (`perm_unlink = 1`) sobre el catálogo de medicamentos, historial de compras o clientes registrados.
  * Los cajeros no deben tener permiso de escritura (`perm_write = 1`) en listas de precios de compra a proveedores ni en el costo de medicamentos.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
  * `SPEC-2.2.1` (Definición de Roles y Grupos de Usuarios).
* **Definition of Ready (DoR):**
  * [x] Listado completo de modelos de datos custom y nativos identificados.
  * [x] Matriz de permisos CRUD por rol acordada con la administración de Farmacia Caryvil.

## 5. Design (Implementation Details)
* **Access Control List (`security/ir.model.access.csv`):**
  ```csv
  id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
  access_caryvil_therapeutic_category_cashier,caryvil.therapeutic.category.cashier,model_caryvil_therapeutic_category,caryvil_erp.group_caryvil_cashier,1,0,0,0
  access_caryvil_therapeutic_category_stock,caryvil.therapeutic.category.stock,model_caryvil_therapeutic_category,caryvil_erp.group_caryvil_inventory_purchases,1,1,1,0
  access_caryvil_therapeutic_category_manager,caryvil.therapeutic.category.manager,model_caryvil_therapeutic_category,caryvil_erp.group_caryvil_manager,1,1,1,1
  access_caryvil_active_ingredient_cashier,caryvil.active.ingredient.cashier,model_caryvil_active_ingredient,caryvil_erp.group_caryvil_cashier,1,0,0,0
  access_caryvil_active_ingredient_stock,caryvil.active.ingredient.stock,model_caryvil_active_ingredient,caryvil_erp.group_caryvil_inventory_purchases,1,1,1,0
  access_caryvil_active_ingredient_manager,caryvil.active.ingredient.manager,model_caryvil_active_ingredient,caryvil_erp.group_caryvil_manager,1,1,1,1
  access_caryvil_stock_loss_stock,caryvil.stock.loss.stock,model_caryvil_stock_loss,caryvil_erp.group_caryvil_inventory_purchases,1,1,1,0
  access_caryvil_stock_loss_manager,caryvil.stock.loss.manager,model_caryvil_stock_loss,caryvil_erp.group_caryvil_manager,1,1,1,1
  access_caryvil_partner_cashier,res.partner.cashier,base.model_res_partner,caryvil_erp.group_caryvil_cashier,1,1,1,0
  access_caryvil_partner_manager,res.partner.manager,base.model_res_partner,caryvil_erp.group_caryvil_manager,1,1,1,1
  ```
* **Record Rules (`security/caryvil_security_rules.xml`):**
  ```xml
  <?xml version="1.0" encoding="utf-8"?>
  <odoo>
      <data noupdate="1">
          <!-- Regla: Cajero solo puede ver ventas de su propia sesión/sucursal o activas -->
          <record id="rule_caryvil_sale_order_cashier" model="ir.rule">
              <field name="name">Ventas accesibles por Cajero</field>
              <field name="model_id" ref="sale.model_sale_order"/>
              <field name="groups" eval="[(4, ref('caryvil_erp.group_caryvil_cashier'))]"/>
              <field name="domain_force">['|', ('user_id', '=', user.id), ('user_id', '=', False)]</field>
              <field name="perm_read" eval="True"/>
              <field name="perm_write" eval="True"/>
              <field name="perm_create" eval="True"/>
              <field name="perm_unlink" eval="False"/>
          </record>

          <!-- Regla: Impedir anulación o eliminación de facturas publicadas para no administradores -->
          <record id="rule_caryvil_posted_invoices_readonly" model="ir.rule">
              <field name="name">Facturas Publicadas Solo Lectura para Cajeros</field>
              <field name="model_id" ref="account.model_account_move"/>
              <field name="groups" eval="[(4, ref('caryvil_erp.group_caryvil_cashier'))]"/>
              <field name="domain_force">[('state', '=', 'posted')]</field>
              <field name="perm_read" eval="True"/>
              <field name="perm_write" eval="False"/>
              <field name="perm_create" eval="True"/>
              <field name="perm_unlink" eval="False"/>
          </record>
      </data>
  </odoo>
  ```

## 6. Acceptance Criteria
* **Scenario 1: Intento de eliminación de medicamento por parte de un Cajero**
  * **Given** Un usuario autenticado con el rol `Cajero / Dependiente de Mostrador`.
  * **When** Intenta ejecutar la acción "Suprimir" en un registro del catálogo de medicamentos.
  * **Then** Odoo debe denegar la acción arrojando un error de permisos de acceso (*AccessError*) impidiendo la eliminación física del registro.
* **Scenario 2: Creación y edición de clientes por parte del Cajero**
  * **Given** Un usuario con rol de Cajero atendiendo a un cliente en mostrador.
  * **When** Registra un nuevo cliente con su DUI o edita el número telefónico de un cliente existente.
  * **Then** El sistema debe permitir la creación y guardado exitoso del cliente (`perm_create = 1`, `perm_write = 1`), pero impedir su eliminación (`perm_unlink = 0`).
* **Scenario 3: Intento de modificación de factura emitida**
  * **Given** Una factura simple en estado "Publicado" (`posted`).
  * **When** Un usuario con rol de Cajero intenta modificar el precio o los ítems de dicha factura.
  * **Then** El sistema debe rechazar la modificación por la regla de registro activa, permitiendo únicamente la consulta y re-impresión del comprobante.

## 7. Verification Plan
* **Automated Tests:**
  * Pruebas unitarias en Python ejecutando operaciones CRUD con `with_user(cashier)` y `with_user(manager)`, verificando que `AccessError` sea capturado en operaciones no permitidas y que operaciones válidas se completen.
* **Manual Verification:**
  * Intentar eliminar un producto desde la vista formulario utilizando la cuenta de un cajero y confirmar el bloqueo por interfaz.

## 8. Security and Privacy
* Cumplimiento estricto del principio de inmutabilidad de registros contables y fiscales tras su emisión.
* Auditoría de intentos de acceso denegados registrada en los logs de seguridad de Odoo.

## 9. Risks and Mitigation
* **Risk:** Bloqueo accidental de flujos legítimos de venta si las reglas de registro son demasiado restrictivas.
  * **Mitigation:** Incluir pruebas integrales con usuarios no administradores en el pipeline de CI/CD para validar que las ventas se completen sin interrupciones.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/security/ir.model.access.csv`.
* Archivo `custom_addons/caryvil_erp/security/caryvil_security_rules.xml`.
* Registro de ambos archivos en el manifiesto `__manifest__.py`.

## 11. Definition of Done (DoD)
* [x] Archivo `ir.model.access.csv` configurado sin advertencias en la carga del módulo.
* [x] Reglas de registro `caryvil_security_rules.xml` activas y probadas.
* [x] Pruebas unitarias de denegación y autorización de acceso superadas al 100%.
* [x] Revisión de seguridad y permisos aprobada por el líder técnico.
