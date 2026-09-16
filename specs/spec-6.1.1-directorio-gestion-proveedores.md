# SPEC-6.1.1: Directorio y Gestión de Proveedores

## 1. Objective
Implementar y estructurar el catálogo centralizado de proveedores, laboratorios farmacéuticos, distribuidoras y droguerías dentro de Odoo (`res.partner`) para Farmacia Caryvil. Un mismo laboratorio puede tener **varios vendedores/representantes** visitando la farmacia, por lo que el modelo separa la **Empresa** (datos fiscales: NIT, NRC, tipo) de sus **Vendedores** (contactos individuales, hijos de la empresa), sirviendo como base indispensable para el módulo de compras y abastecimiento.

## 2. Scope
### 2.1. Included
* Extensión del modelo `res.partner` en `custom_addons/caryvil_erp/models/res_partner_vendor.py` añadiendo:
  * `is_pharmacy_vendor` (Boolean): Bandera distintiva para proveedores y laboratorios farmacéuticos (aplica tanto a la Empresa como a cada Vendedor hijo).
  * `vendor_code` (Char, autogenerado): Código correlativo `P0001`, `P0002`... asignado automáticamente al crear cualquier registro marcado como proveedor, vía secuencia `caryvil.vendor.code`.
  * `vendor_type` (Selection): Clasificación de la Empresa (`laboratorio`, `distribuidora`, `drogueria`).
  * `nit` (Char, opcional): Número de Identificación Tributaria salvadoreño, formato `0000-000000-000-0`, validado por expresión regular si se llena.
  * `nrc` (Char, **obligatorio** para la Empresa): Número de Registro de Contribuyente. Sin formato fijo definido por el negocio.
* **Modelo de datos padre-hijo** (usando el mecanismo nativo `parent_id` de `res.partner`, sin campo nuevo):
  * **Empresa** (`is_company = True`): registro con Nombre, Tipo de Proveedor, NIT, NRC.
  * **Vendedor** (`is_company = False`, `parent_id` = la Empresa): registro con Código, Nombre, Teléfono, Email. Es la pantalla principal de uso diario.
* Formulario emergente para crear/editar la Empresa (`view_res_partner_laboratorio_quick_form`), sin los campos genéricos de contacto de Odoo (dirección, sitio web, tags). Se usa tanto al crear la Empresa desde el dropdown del Vendedor como al editar una ya existente (vía `get_formview_id`/`get_formview_action` sobrescritos en el modelo).
* Máscaras de formato en tiempo real (JavaScript, `static/src/js/masked_char_field.js`):
  * `caryvil_phone_mask`: formatea Teléfono como `0000-0000` mientras se escribe.
  * `caryvil_nit_mask`: formatea NIT como `0000-000000-000-0` mientras se escribe.
  * `caryvil_nrc_mask`: sin formato (placeholder de referencia únicamente).
* Validaciones de respaldo en Python (`@api.constrains`, no dependen del JS):
  * NIT: formato `0000-000000-000-0` si se llena.
  * NRC: obligatorio en toda Empresa marcada como proveedor farmacéutico.
  * Teléfono: formato `0000-0000` si se llena.
* Creación de la vista de lista, formulario y búsqueda para Vendedores en `views/res_partner_vendor_views.xml`.
* Creación del menú de acceso "Proveedores y Laboratorios" bajo el menú "Compras y Proveedores".

### 2.2. Not Included (Out of Scope)
* Gestión de catálogos de precios y códigos de artículo del proveedor (cubierto en `SPEC-6.2.1`).
* Emisión y validación de órdenes de compra formales (cubierto en `SPEC-8.1.1`).
* Historial de compras por vendedor (se agregará como pestaña cuando exista `SPEC-8.1.1`).
* Condiciones de pago (`commercial_terms`) y tiempo de entrega (`delivery_lead_time`): se evaluó incluirlos, pero el negocio decidió no manejarlos en esta iteración.

## 3. Context and Restrictions
* **Context:** Permite a la propietaria y al encargado de compras mantener una base de datos unificada de distribuidores (e.g., Laboratorios Vijosa, Droguería Santa Lucía, Laboratorios López) y de las personas que los representan, para cotizar y emitir pedidos de forma ágil y formal.
* **Restrictions:**
  * Un proveedor no debe confundirse con un cliente en las listas de selección del punto de venta.
  * El NIT/NRC debe ser validado para evitar registros incompletos en compras formales — NRC es obligatorio; NIT valida formato solo si se llena.
  * Un Laboratorio puede tener múltiples Vendedores asociados; los datos fiscales (NIT/NRC) viven únicamente en el registro de la Empresa, nunca duplicados en cada Vendedor.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
  * `SPEC-2.2.1` (Definición de Roles y Grupos de Usuarios).
* **Definition of Ready (DoR):**
  * [x] Listado de laboratorios y distribuidores habituales de Farmacia Caryvil recopilado.
  * [x] Tipología de proveedores acordada con la administración (Laboratorio / Distribuidora / Droguería).
  * [x] Confirmado con la administración: un laboratorio puede tener varios vendedores; no se manejan condiciones de pago ni tiempo de entrega en esta iteración.

## 5. Design (Implementation Details)
* **Data Model (`models/res_partner_vendor.py`):**
  ```python
  import re
  from odoo import models, fields, api, _
  from odoo.exceptions import ValidationError

  NIT_RE = re.compile(r'^\d{4}-\d{6}-\d{3}-\d{1}$')
  PHONE_RE = re.compile(r'^\d{4}-\d{4}$')

  class ResPartnerVendor(models.Model):
      _inherit = 'res.partner'

      is_pharmacy_vendor = fields.Boolean(string='Es Proveedor Farmacéutico', default=False)
      vendor_code = fields.Char(string='Código', readonly=True, copy=False)
      vendor_type = fields.Selection([
          ('laboratorio', 'Laboratorio'),
          ('distribuidora', 'Distribuidora'),
          ('drogueria', 'Droguería'),
      ], string='Tipo de Proveedor', default='laboratorio')
      nit = fields.Char(string='NIT', size=17, help='Formato: 0000-000000-000-0')
      nrc = fields.Char(string='NRC', size=10, help='Formato: 00000-0')

      # Asigna el código autogenerado (P0001, P0002...) a proveedores/vendedores nuevos.
      @api.model_create_multi
      def create(self, vals_list): ...

      # Fuerza que al abrir un Laboratorio existente se use el formulario simplificado.
      def get_formview_id(self, access_uid=None): ...

      # Hace que ese formulario simplificado se abra en ventana emergente, igual que al crear.
      def get_formview_action(self, access_uid=None): ...

      # Valida formato de NIT, NRC obligatorio, y formato de Teléfono.
      @api.constrains(...) ...
  ```
* **View Structure (`views/res_partner_vendor_views.xml`)** — organizada en 5 secciones:
  1. Lista de Vendedores: Código, Nombre, Proveedor (empresa), Teléfono.
  2. Formulario del Vendedor: Código, Nombre, Proveedor (dropdown con creación rápida de Empresa), Teléfono (con máscara), Email.
  3. Búsqueda con filtros: Laboratorios / Distribuidoras / Droguerías (filtra por `parent_id.vendor_type`).
  4. Acción de ventana + menú "Proveedores y Laboratorios" bajo "Compras y Proveedores".
  5. Formulario rápido de la Empresa: Nombre, Tipo de Proveedor, NIT (con máscara), NRC (obligatorio).

## 6. Acceptance Criteria
* **Scenario 1: Creación de un Vendedor y su Laboratorio**
  * **Given** El encargado de compras en `Compras y Proveedores > Proveedores y Laboratorios > Nuevo`.
  * **When** Escribe el nombre del vendedor "Carlos Méndez", y en el campo "Proveedor" crea "Laboratorios Vijosa S.A. de C.V." con NIT `0614-123456-001-2` y NRC `12345-6`, y llena el Teléfono `7788-9900`.
  * **Then** El Vendedor se guarda con un código autogenerado (`P0001`), vinculado como hijo de la Empresa "Laboratorios Vijosa", y ambos quedan marcados con `is_pharmacy_vendor = True`.
* **Scenario 2: Un mismo Laboratorio con varios Vendedores**
  * **Given** Un Laboratorio ya registrado ("Laboratorios Vijosa").
  * **When** Se crea un segundo Vendedor eligiendo el mismo Laboratorio en el dropdown "Proveedor".
  * **Then** Ambos Vendedores aparecen en la lista principal, cada uno con su propio código, teléfono y nombre, compartiendo el mismo Laboratorio.
* **Scenario 3: Validación de formato y campo obligatorio**
  * **Given** El formulario de creación de un Laboratorio.
  * **When** El usuario intenta guardar sin NRC, o con un NIT/Teléfono que no cumple el formato de guiones.
  * **Then** Odoo rechaza el guardado con un mensaje de error específico por campo.
* **Scenario 4: Edición de un Laboratorio existente**
  * **Given** Un Laboratorio ya creado, accedido desde la flechita del campo "Proveedor" en la ficha de un Vendedor.
  * **Then** Se abre en ventana emergente, mostrando el mismo formulario simplificado usado al crearlo (no el formulario genérico de contactos de Odoo).

## 7. Verification Plan
* **Automated Tests** (`tests/test_res_partner_vendor.py`, pendiente de escribir):
  * Crear un Vendedor y verificar que se le asigna `vendor_code` automáticamente.
  * Crear una Empresa sin NRC y verificar que lanza `ValidationError`.
  * Crear un NIT/Teléfono con formato inválido y verificar que lanza `ValidationError`.
  * Crear dos Vendedores con el mismo `parent_id` y verificar que ambos quedan asociados correctamente.
* **Manual Verification:**
  * Navegar a `Compras y Proveedores > Proveedores y Laboratorios`, registrar un vendedor y su laboratorio, y validar la máscara de NIT/Teléfono en pantalla.

## 8. Security and Privacy
* La creación y edición de Proveedores está disponible para los roles `Encargado de Compras e Inventario` y `Administrador General` (heredado del acceso general a `res.partner` ya definido en `SPEC-2.2.2`).

## 9. Risks and Mitigation
* **Risk:** Registros duplicados del mismo laboratorio bajo nombres ligeramente distintos (e.g., "Vijosa" vs "Laboratorios Vijosa").
  * **Mitigation:** Fomentar la búsqueda previa por NRC/NIT antes de crear nuevos registros. (Detectado en pruebas manuales: se crearon "Laboratio Vijosa" y "Laboratorio Vijosa" por error de tipeo — pendiente limpieza de datos de prueba antes de producción).

## 10. Deliverables & Config as Code
* `custom_addons/caryvil_erp/models/res_partner_vendor.py`
* `custom_addons/caryvil_erp/views/res_partner_vendor_views.xml`
* `custom_addons/caryvil_erp/data/res_partner_vendor_sequence.xml` (secuencia del código autogenerado)
* `custom_addons/caryvil_erp/static/src/js/masked_char_field.js` (máscaras de Teléfono/NIT)
* Registro del modelo en `models/__init__.py` y de la vista/data/assets en `__manifest__.py`.
* `custom_addons/caryvil_erp/tests/test_res_partner_vendor.py` (pendiente).

## 11. Definition of Done (DoD)
* [x] Campos de proveedor (`vendor_code`, `vendor_type`, `nit`, `nrc`) implementados en `res.partner`.
* [x] Modelo padre-hijo Empresa/Vendedor funcionando (un laboratorio, múltiples vendedores).
* [x] Vistas de lista, formulario y búsqueda creadas bajo el menú de Compras.
* [x] Formulario emergente simplificado de Empresa, tanto al crear como al editar.
* [x] Máscaras de formato para NIT y Teléfono, y validaciones de respaldo en Python.
* [ ] Filtro de proveedores en órdenes de compra verificado (bloqueado hasta `SPEC-8.1.1`).
* [x] Pruebas unitarias aprobadas al 100%.
* [ ] Aprobación por la administración de Farmacia Caryvil.
