# SPEC-5.2.1: Búsqueda Rápida de Clientes en Caja

## 1. Objective
Optimizar los mecanismos de búsqueda, indexación y selección ágil de clientes dentro del flujo de ventas y atención en mostrador de Farmacia Caryvil. Esta especificación sobreescribe los métodos de búsqueda del ORM de Odoo (`_name_search`) y personaliza el formato de visualización (`display_name`) en el modelo `res.partner`, permitiendo a los cajeros y dependientes localizar a cualquier cliente en menos de 2 segundos mediante la digitación parcial o total de su número de DUI (con o sin guion), número telefónico o apellidos, así como habilitar un formulario de alta exprés en mostrador.

## 2. Scope
### 2.1. Included
* Sobreescritura del método `_name_search` en `custom_addons/caryvil_erp/models/res_partner_customer.py` para admitir operadores de coincidencia multicampo:
  * Búsqueda por DUI (ejemplo: escribir `0458` o `04589632-1`).
  * Búsqueda por Teléfono o Celular (ejemplo: escribir `7845` o `7845-1234`).
  * Búsqueda por Apellidos o Nombres.
* Personalización del formato de etiqueta en listas desplegables (`display_name`): `[DUI] Nombre Completo - Tel: XXXXXXXX`.
* Creación de índices de base de datos B-Tree en PostgreSQL para las columnas `dui`, `phone`, `mobile` y `name` en la tabla `res_partner`.
* Optimización de la vista rápida de creación modal (*Quick Create View*) para permitir dar de alta a un cliente nuevo en caja en menos de 15 segundos sin salir del formulario de venta.

### 2.2. Not Included (Out of Scope)
* Procesamiento y cálculo de la transacción de venta (cubierto en `SPEC-9.1.1`).
* Almacenamiento de historiales de compras (cubierto en `SPEC-5.2.2`).

## 3. Context and Restrictions
* **Context:** Durante las horas pico de atención en la farmacia, la lentitud en la selección o alta del cliente genera filas y demoras; esta especificación minimiza los tiempos de atención en caja.
* **Restrictions:**
  * La consulta de búsqueda debe devolver resultados en menos de 200ms sobre una base de datos de hasta 50,000 contactos.
  * Si no se encuentra el cliente, el sistema debe ofrecer inmediatamente la opción "Crear y Editar..." sin borrar el texto digitado.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-5.1.1` (Gestión del Perfil de Clientes).
* **Definition of Ready (DoR):**
  * [x] Campos de DUI y nombres estructurados en `res.partner`.
  * [x] Flujo de atención en mostrador analizado con el equipo de farmacia.

## 5. Design (Implementation Details)
* **Search Overriding (`models/res_partner_customer.py`):**
  ```python
  from odoo import models, api

  class ResPartnerCustomerSearch(models.Model):
      _inherit = 'res.partner'

      @api.depends('name', 'dui', 'phone')
      def _compute_display_name(self):
          for partner in self:
              if partner.is_pharmacy_customer and partner.dui:
                  phone_part = f" - Tel: {partner.phone}" if partner.phone else ""
                  partner.display_name = f"[{partner.dui}] {partner.name}{phone_part}"
              else:
                  super(ResPartnerCustomerSearch, partner)._compute_display_name()

      @api.model
      def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
          args = list(args or [])
          if name:
              # Limpiar posibles guiones y espacios
              clean_term = name.replace('-', '').strip()
              domain = [
                  '|', '|', '|',
                  ('name', operator, name),
                  ('dui', operator, name),
                  ('dui', operator, clean_term),
                  ('phone', operator, name)
              ]
              return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
          return super(ResPartnerCustomerSearch, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)
  ```
* **Database Indexes:**
  * Creación de índices en PostgreSQL mediante `index=True` en campos `dui`, `phone`, `first_name`, `last_name`.

## 6. Acceptance Criteria
* **Scenario 1: Búsqueda por número de DUI en el campo de cliente**
  * **Given** El dependiente en el formulario de ventas en mostrador.
  * **When** Digita en el campo de cliente "04589632".
  * **Then** La lista desplegable debe mostrar de inmediato `[04589632-1] María Elena López Rivas - Tel: 7845-1234` para selección con la tecla Enter.
* **Scenario 2: Búsqueda por número de teléfono**
  * **Given** Un cliente que no recuerda su DUI pero proporciona su teléfono "78451234".
  * **When** El cajero ingresa dicho número en el buscador.
  * **Then** El sistema debe localizar y autocompletar la ficha de dicho cliente.
* **Scenario 3: Alta rápida de cliente nuevo desde el desplegable**
  * **Given** Un cliente nuevo que no existe en el sistema.
  * **When** El cajero escribe su nombre o DUI y presiona "Crear y Editar...".
  * **Then** Se despliega una ventana modal simplificada con solo los campos indispensables (Nombre, DUI, Teléfono) y, al guardar, el cliente queda automáticamente asignado a la venta en curso.

## 7. Verification Plan
* **Automated Tests:**
  * Test unitario en Python ejecutando `env['res.partner'].name_search()` pasando únicamente fragmentos de DUI, teléfonos y nombres, verificando que los IDs correctos sean retornados.
* **Manual Verification:**
  * Simular una venta en el navegador, digitar un DUI de prueba y verificar el autocompletado en menos de 1 segundo.

## 8. Security and Privacy
* Los cajeros solo acceden a información de contacto requerida para la facturación y despacho, sin acceso a historiales clínicos sensibles.

## 9. Risks and Mitigation
* **Risk:** Múltiples clientes con nombres similares que dificulten la selección correcta.
  * **Mitigation:** Incluir siempre el prefijo de DUI entre corchetes `[00000000-0]` en el `display_name` para desambiguación inequívoca.

## 10. Deliverables & Config as Code
* Métodos `_compute_display_name` y `_name_search` implementados en `models/res_partner_customer.py`.
* Vista simplificada `view_partner_simple_form_caryvil` para creación rápida en mostrador.

## 11. Definition of Done (DoD)
* [ ] Búsqueda multicampo (DUI, teléfono, nombre) implementada y testeada.
* [ ] Formato `display_name` con DUI visible en todos los selectores de cliente.
* [ ] Tiempo de respuesta de búsqueda < 200ms comprobado.
* [ ] Pruebas unitarias en Python aprobadas.
* [ ] Validación de experiencia de usuario en mostrador aprobada.
