# SPEC-6.1.1: Directorio y Gestión de Proveedores

## 1. Objective
Implementar y estructurar el catálogo centralizado de proveedores, laboratorios farmacéuticos y droguerías distribuidoras dentro de Odoo (`res.partner`) para Farmacia Caryvil. Esta especificación permite registrar y administrar la información de contacto corporativo, identificación fiscal salvadoreña (NIT y NRC), tipo de proveedor (Laboratorio, Distribuidora o Droguería), plazos promedio de entrega, condiciones comerciales de crédito/contado y datos del agente de ventas asignado, sirviendo como base indispensable para el módulo de compras y abastecimiento.

## 2. Scope
### 2.1. Included
* Extensión del modelo `res.partner` en `custom_addons/caryvil_erp/models/res_partner_vendor.py` añadiendo:
  * `is_pharmacy_vendor` (Boolean): Bandera distintiva para proveedores y laboratorios farmacéuticos.
  * `vendor_type` (Selection): Clasificación del proveedor (`laboratorio`, `distribuidora`, `drogueria`, `otro`).
  * `nit` (Char): Número de Identificación Tributaria salvadoreño (formato `0000-000000-000-0` o nuevo formato homologado DUI).
  * `nrc` (Char): Número de Registro de Contribuyente (IVA).
  * `delivery_lead_time` (Integer): Tiempo promedio de despacho/entrega en días hábiles.
  * `commercial_terms` (Selection): Condiciones de pago acordadas (`contado`, `credito_15`, `credito_30`, `credito_60`).
  * `commercial_contact_name` (Char): Nombre completo del agente o ejecutivo de ventas asignado a la farmacia.
  * `commercial_contact_phone` (Char): Teléfono directo o celular del ejecutivo.
  * `commercial_contact_email` (Char): Correo electrónico para envío de órdenes de compra.
* Creación de la vista de formulario, lista y búsqueda específica para proveedores en `views/res_partner_vendor_views.xml`.
* Creación del menú de acceso "Proveedores y Laboratorios" bajo el menú de Compras en Odoo.

### 2.2. Not Included (Out of Scope)
* Gestión de catálogos de precios y códigos de artículo del proveedor (cubierto en `SPEC-6.2.1`).
* Emisión y validación de órdenes de compra formales (cubierto en `SPEC-8.1.1`).

## 3. Context and Restrictions
* **Context:** Permite a la propietaria y al encargado de compras mantener una base de datos unificada de distribuidores (e.g., Laboratorios Vijosa, Droguería Santa Lucía, Laboratorios López) para cotizar y emitir pedidos de forma ágil y formal.
* **Restrictions:**
  * Un proveedor no debe confundirse con un cliente en las listas de selección del punto de venta.
  * El NIT/NRC debe ser validado para evitar registros incompletos en compras formales.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
  * `SPEC-2.2.1` (Definición de Roles y Grupos de Usuarios).
* **Definition of Ready (DoR):**
  * [x] Listado de laboratorios y distribuidores habituales de Farmacia Caryvil recopilado.
  * [x] Tipología de proveedores y términos de pago acordados con la administración.

## 5. Design (Implementation Details)
* **Data Model (`models/res_partner_vendor.py`):**
  ```python
  from odoo import models, fields, api

  class ResPartnerVendor(models.Model):
      _inherit = 'res.partner'

      is_pharmacy_vendor = fields.Boolean(string='Es Proveedor Farmacéutico', default=False)
      vendor_type = fields.Selection([
          ('laboratorio', 'Laboratorio Farmacéutico'),
          ('distribuidora', 'Distribuidora / Droguería'),
          ('otro', 'Otro Proveedor')
      ], string='Tipo de Proveedor', default='laboratorio')

      nit = fields.Char(string='NIT', size=17, help='Formato: 0000-000000-000-0')
      nrc = fields.Char(string='NRC', size=10, help='Número de Registro de Contribuyente')
      delivery_lead_time = fields.Integer(string='Tiempo de Entrega (Días)', default=2)
      commercial_terms = fields.Selection([
          ('contado', 'Contado contra entrega'),
          ('credito_15', 'Crédito a 15 días'),
          ('credito_30', 'Crédito a 30 días'),
          ('credito_60', 'Crédito a 60 días')
      ], string='Condiciones de Pago', default='contado')

      commercial_contact_name = fields.Char(string='Ejecutivo de Ventas')
      commercial_contact_phone = fields.Char(string='Teléfono Ejecutivo')
      commercial_contact_email = fields.Char(string='Email Pedidos')
  ```
* **View Structure (`views/res_partner_vendor_views.xml`):**
  * Vista de lista con filtros rápidos: `[Laboratorios]`, `[Distribuidoras]`, `[Con Crédito Activo]`.
  * Formulario con tarjeta de datos corporativos, pestaña de "Condiciones Comerciales" y "Contacto de Ventas".

## 6. Acceptance Criteria
* **Scenario 1: Creación de ficha de Laboratorio Farmacéutico**
  * **Given** El encargado de compras ingresando al menú `Compras > Proveedores > Crear`.
  * **When** Registra: Nombre "Laboratorios Vijosa S.A. de C.V.", Tipo "Laboratorio", NRC "12345-6", Tiempo de entrega "2 días", Términos "Crédito a 30 días", Ejecutivo "Carlos Méndez" y Teléfono "7788-9900".
  * **Then** El registro se almacena con `is_pharmacy_vendor = True` y `supplier_rank = 1`, quedando disponible de inmediato para emitirle órdenes de compra.
* **Scenario 2: Filtrado exclusivo de proveedores en Compras**
  * **Given** La vista de selección de proveedores en una Orden de Compra.
  * **When** El usuario despliega la lista de opciones.
  * **Then** Solo deben aparecer contactos marcados con `is_pharmacy_vendor = True` o `supplier_rank > 0`, excluyendo a los clientes finales.
* **Scenario 3: Visualización de datos de contacto del agente para pedidos urgentes**
  * **Given** La necesidad de consultar el teléfono del agente de ventas de una droguería.
  * **When** El usuario abre la ficha del proveedor en Odoo.
  * **Then** La tarjeta de contacto del ejecutivo debe mostrar claramente su nombre, teléfono directo y correo para envío del pedido.

## 7. Verification Plan
* **Automated Tests:**
  * Prueba unitaria en Python creando un proveedor con `vendor_type = 'laboratorio'`, verificando que los campos fiscales y comerciales se almacenen correctamente y que el dominio de búsqueda filtre clientes.
* **Manual Verification:**
  * Navegar a `Compras > Proveedores`, registrar un proveedor muestra y validar la navegación entre pestañas del formulario.

## 8. Security and Privacy
* Los datos de condiciones comerciales y plazos de pago son accesibles únicamente para los roles `Encargado de Compras e Inventario` y `Administrador`.

## 9. Risks and Mitigation
* **Risk:** Registros duplicados del mismo laboratorio bajo nombres ligeramente distintos (e.g., "Vijosa" vs "Laboratorios Vijosa").
  * **Mitigation:** Fomentar la búsqueda previa por NRC/NIT antes de crear nuevos registros y agregar advertencias de duplicidad por coincidencia de nombre.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/models/res_partner_vendor.py`.
* Archivo `custom_addons/caryvil_erp/views/res_partner_vendor_views.xml`.
* Registro del modelo en `models/__init__.py` y de la vista en `__manifest__.py`.

## 11. Definition of Done (DoD)
* [ ] Campos de proveedor (`vendor_type`, `nrc`, `commercial_terms`, etc.) implementados en `res.partner`.
* [ ] Vistas de lista, formulario y búsqueda creadas bajo el menú de Compras.
* [ ] Filtro de proveedores en órdenes de compra verificado.
* [ ] Pruebas unitarias aprobadas al 100%.
* [ ] Aprobación por la administración de Farmacia Caryvil.
