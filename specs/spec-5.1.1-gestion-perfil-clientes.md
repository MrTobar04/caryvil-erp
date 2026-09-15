# SPEC-5.1.1: Gestión del Perfil de Clientes

## 1. Objective
Personalizar y extender el modelo de contactos de Odoo (`res.partner`) para adaptar la gestión de clientes al contexto salvadoreño y a las necesidades operativas de Farmacia Caryvil. Esta especificación implementa la captura estructurada de los campos obligatorios del cliente (Nombre, Apellido, DUI con validación de formato `00000000-0`, Teléfono, Correo Electrónico y Dirección de residencia), garantizando la unicidad de registros, la integridad de los datos y la categorización automática como cliente de farmacia.

## 2. Scope
### 2.1. Included
* Extensión del modelo `res.partner` en `custom_addons/caryvil_erp/models/res_partner_customer.py` añadiendo:
  * `first_name` (Char): Nombre(s) del cliente.
  * `last_name` (Char): Apellido(s) del cliente.
  * `dui` (Char): Documento Único de Identidad salvadoreño con validación regex de 9 dígitos con guion (`^\d{8}-\d{1}$`).
  * `phone` / `mobile` (Char): Teléfono de contacto con validación de 8 dígitos.
  * `email` (Char): Correo electrónico para envío de facturas digitales o avisos.
  * `street` (Text): Dirección física o de residencia en Soyapango / San Salvador.
  * `is_pharmacy_customer` (Boolean): Bandera distintiva para clientes de mostrador.
* Restricción de unicidad (`@api.constrains('dui')` y `_sql_constraints`) para evitar la duplicidad de clientes registrados con el mismo número de DUI.
* Sincronización automática del campo compuesto `name` mediante cómputo de `first_name` y `last_name`.
* Extensión de la vista formulario (`views/res_partner_customer_views.xml`) reorganizando los campos de forma clara y accesible.

### 2.2. Not Included (Out of Scope)
* Funcionalidades avanzadas de marketing, segmentación o campañas automatizadas (excluido explícitamente en el alcance del proyecto).
* Búsqueda acelerada e indexada en el punto de venta (cubierto en `SPEC-5.2.1`).
* Despliegue del historial de compras acumulado (cubierto en `SPEC-5.2.2`).

## 3. Context and Restrictions
* **Context:** Permite formalizar la base de datos de compradores de Farmacia Caryvil, superando la limitación de la antigua app donde los datos estaban aislados y solo se usaban temporalmente para despachos.
* **Restrictions:**
  * El DUI debe ser validado antes de permitir guardar el registro en la base de datos.
  * El formato debe admitir la digitación con o sin guion, autocompletando el guion antes del dígito verificador si el usuario ingresa 9 dígitos continuos.
  * Los clientes pueden ser personas naturales; no se requiere información tributaria compleja de persona jurídica para este tipo de cliente.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
  * `SPEC-2.2.1` (Definición de Roles y Grupos de Usuarios).
* **Definition of Ready (DoR):**
  * [x] Formato estándar y algoritmo de validación de DUI salvadoreño definidos.
  * [x] Campos obligatorios acordados en el Sprint 2 del cronograma de planificación.

## 5. Design (Implementation Details)
* **Data Model (`models/res_partner_customer.py`):**
  ```python
  import re
  from odoo import models, fields, api, _
  from odoo.exceptions import ValidationError

  class ResPartnerCustomer(models.Model):
      _inherit = 'res.partner'

      first_name = fields.Char(string='Nombres', index=True)
      last_name = fields.Char(string='Apellidos', index=True)
      dui = fields.Char(string='DUI', size=10, index=True, help='Formato: 00000000-0')
      is_pharmacy_customer = fields.Boolean(string='Es Cliente de Farmacia', default=True)

      _sql_constraints = [
          ('dui_unique', 'unique(dui)', 'Ya existe un cliente registrado con este número de DUI.')
      ]

      @api.onchange('first_name', 'last_name')
      def _onchange_names(self):
          names = [self.first_name or '', self.last_name or '']
          full_name = ' '.join(filter(None, names)).strip()
          if full_name:
              self.name = full_name

      @api.constrains('dui')
      def _check_dui_format(self):
          for record in self:
              if record.dui:
                  # Limpiar y normalizar
                  clean_dui = record.dui.strip()
                  if re.match(r'^\d{9}$', clean_dui):
                      clean_dui = f"{clean_dui[:8]}-{clean_dui[8]}"
                      record.dui = clean_dui
                  
                  if not re.match(r'^\d{8}-\d{1}$', record.dui):
                      raise ValidationError(_('El DUI ingresado (%s) no es válido. Debe cumplir el formato 00000000-0.') % record.dui)
  ```
* **View Structure (`views/res_partner_customer_views.xml`):**
  * Formulario con tarjeta principal: Nombres, Apellidos, DUI destacado con icono de documento nacional, Teléfono principal, Correo y Dirección detallada.

## 6. Acceptance Criteria
* **Scenario 1: Registro exitoso de cliente con DUI válido**
  * **Given** El dependiente en la vista de clientes ingresando: Nombres "María Elena", Apellidos "López Rivas", DUI "04589632-1", Teléfono "7845-1234", Dirección "Col. San Antonio, Soyapango".
  * **When** Presiona "Guardar".
  * **Then** El registro se almacena exitosamente con el campo `name` calculado como "María Elena López Rivas" y `is_pharmacy_customer = True`.
* **Scenario 2: Rechazo de DUI con formato inválido**
  * **Given** Un usuario ingresando un DUI con letras o longitud incorrecta (e.g., "0458A-1" o "12345").
  * **When** Intenta guardar el cliente.
  * **Then** Odoo debe bloquear el guardado y mostrar una ventana emergente de error de validación (*ValidationError*) explicando el formato requerido `00000000-0`.
* **Scenario 3: Bloqueo de cliente duplicado por DUI**
  * **Given** Un cliente existente en la base de datos con DUI "01234567-8".
  * **When** Se intenta crear un segundo cliente con el mismo DUI "01234567-8".
  * **Then** El sistema debe rechazar la operación indicando que el DUI ya se encuentra registrado.

## 7. Verification Plan
* **Automated Tests:**
  * Prueba unitaria en Python probando creación de clientes con DUIs válidos, DUIs sin guion (autocorrección), DUIs inválidos (captura de excepción) y duplicados (captura de excepción SQL).
* **Manual Verification:**
  * Ingresar al menú `Clientes > Crear`, diligenciar los campos y validar el comportamiento reactivo del nombre completo y el bloqueo ante datos erróneos.

## 8. Security and Privacy
* Protección de datos personales (PII) bajo la normativa local salvadoreña.
* Acceso de lectura/escritura permitido a Cajeros y Administradores, pero eliminación física restringida exclusivamente a Administradores (`SPEC-2.2.2`).

## 9. Risks and Mitigation
* **Risk:** Resistencia de algunos clientes a proporcionar el número de DUI para compras menores de mostrador.
  * **Mitigation:** Permitir que el campo DUI sea opcional en transacciones rápidas de mostrador mediante el cliente genérico "Consumidor Final", pero obligatorio cuando se registre un perfil formal de cliente para seguimiento.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/models/res_partner_customer.py`.
* Archivo `custom_addons/caryvil_erp/views/res_partner_customer_views.xml`.
* Registro del modelo en `models/__init__.py` y de la vista en `__manifest__.py`.

## 11. Definition of Done (DoD)
* [ ] Campos salvadoreños (`first_name`, `last_name`, `dui`, dirección) implementados en `res.partner`.
* [ ] Validación de formato y unicidad de DUI probada con casos límite.
* [ ] Vista de clientes en Odoo adaptada con la nueva distribución de campos.
* [ ] Pruebas unitarias de validación en Python aprobadas al 100%.
* [ ] Aprobación funcional por el equipo del Sprint 2.
