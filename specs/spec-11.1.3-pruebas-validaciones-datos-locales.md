# SPEC-11.1.3: Pruebas Unitarias de Validaciones Locales y Reglas de Negocio

## 1. Objective
Diseñar, estructurar e implementar la suite de pruebas unitarias y de integridad de datos en Python/Odoo (`tests/test_local_validations.py`) para validar las reglas de negocio personalizadas de Farmacia Caryvil. Esta especificación verifica mediante asserts rigurosos la validación de formato y unicidad del Documento Único de Identidad (DUI salvadoreño), la autocorrección de digitación continua de 9 dígitos, la búsqueda indexada multicampo de clientes y la restricción de privilegios de acceso por rol según la matriz de seguridad.

## 2. Scope
### 2.1. Included
* Creación del archivo de pruebas `custom_addons/caryvil_erp/tests/test_local_validations.py` heredando de `odoo.tests.common.TransactionCase`.
* Implementación de los siguientes casos de prueba automatizados:
  * **Test 1 (`test_dui_valid_formats_and_autocorrection`):** Validación de DUI estándar con guion (`01234567-8`) y autocorrección de entrada continua sin guion (`012345678` ➔ transformado a `01234567-8`).
  * **Test 2 (`test_dui_invalid_formats_raise_validation_error`):** Comprobación de que cadenas inválidas (letras, longitud menor a 9 dígitos, longitud mayor, caracteres especiales) disparen `ValidationError`.
  * **Test 3 (`test_dui_uniqueness_sql_constraint`):** Creación de un segundo cliente con un DUI ya existente ➔ Comprobación de bloqueo por violación de unicidad.
  * **Test 4 (`test_customer_name_search_multicampo`):** Verificación de que el método `_name_search` retorne el registro correcto al buscar por fragmentos de DUI, número telefónico o apellidos.
  * **Test 5 (`test_security_rbac_restrictions`):** Ejecución de operaciones con usuario Cajero (`with_user(cashier)`) verificando que se impida la eliminación de medicamentos o la modificación de facturas emitidas mediante `AccessError`.
* Integración de la suite en el flujo de CI/CD de GitHub Actions (`SPEC-1.3.1`).

### 2.2. Not Included (Out of Scope)
* Pruebas del flujo de abastecimiento (cubierto en `SPEC-11.1.1`).
* Pruebas del flujo de ventas y FEFO (cubierto en `SPEC-11.1.2`).

## 3. Context and Restrictions
* **Context:** Asegura la consistencia estructural de los datos del sistema, impidiendo el almacenamiento de registros corruptos, duplicados o no conformes con las leyes salvadoreñas.
* **Restrictions:**
  * Todas las pruebas deben ejecutarse en aislamiento transaccional con reversión automática al finalizar.
  * El tiempo total de ejecución de esta suite unitaria no debe superar los 25 segundos.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.2.1` (Definición de Roles y Grupos de Usuarios).
  * `SPEC-2.2.2` (Reglas de Acceso y Seguridad de Modelos).
  * `SPEC-5.1.1` (Gestión del Perfil de Clientes).
  * `SPEC-5.2.1` (Búsqueda Rápida de Clientes en Caja).
* **Definition of Ready (DoR):**
  * [x] Modelos de clientes y matriz de seguridad implementados.
  * [x] Casos de prueba de formatos límite de DUI catalogados.

## 5. Design (Implementation Details)
* **Test Architecture (`tests/test_local_validations.py`):**
  ```python
  # -*- coding: utf-8 -*-
  from odoo.tests.common import TransactionCase
  from odoo.exceptions import ValidationError, AccessError
  from psycopg2 import IntegrityError
  from odoo.tools import mute_logger

  class TestLocalValidations(TransactionCase):

      def test_dui_valid_formats_and_autocorrection(self):
          # Caso 1: DUI formateado estándar
          client1 = self.env['res.partner'].create({
              'first_name': 'Carlos',
              'last_name': 'Rivas',
              'dui': '04589632-1',
              'is_pharmacy_customer': True
          })
          self.assertEqual(client1.dui, '04589632-1')
          self.assertEqual(client1.name, 'Carlos Rivas')

          # Caso 2: DUI sin guion (9 dígitos continuos) -> Debe autocorregir
          client2 = self.env['res.partner'].create({
              'first_name': 'Ana',
              'last_name': 'García',
              'dui': '098765432',
              'is_pharmacy_customer': True
          })
          self.assertEqual(client2.dui, '09876543-2')

      def test_dui_invalid_formats(self):
          # Longitud corta
          with self.assertRaises(ValidationError):
              self.env['res.partner'].create({'first_name': 'A', 'last_name': 'B', 'dui': '12345'})
          
          # Caracteres alfabéticos
          with self.assertRaises(ValidationError):
              self.env['res.partner'].create({'first_name': 'A', 'last_name': 'B', 'dui': '0458A632-1'})

      @mute_logger('odoo.sql_db')
      def test_dui_uniqueness_constraint(self):
          self.env['res.partner'].create({
              'first_name': 'Cliente',
              'last_name': 'Uno',
              'dui': '01122334-5',
              'is_pharmacy_customer': True
          })
          # Intentar crear segundo cliente con mismo DUI
          with self.assertRaises((ValidationError, IntegrityError)):
              self.env['res.partner'].create({
                  'first_name': 'Cliente',
                  'last_name': 'Dos',
                  'dui': '01122334-5',
                  'is_pharmacy_customer': True
              })

      def test_customer_name_search(self):
          client = self.env['res.partner'].create({
              'first_name': 'Roberto',
              'last_name': 'Menjívar',
              'dui': '05544332-9',
              'phone': '7890-1234',
              'is_pharmacy_customer': True
          })
          
          # Buscar por DUI parcial
          results = self.env['res.partner'].name_search('05544332')
          self.assertIn(client.id, [r[0] for r in results])

          # Buscar por teléfono
          results_phone = self.env['res.partner'].name_search('78901234')
          self.assertIn(client.id, [r[0] for r in results_phone])
  ```

## 6. Acceptance Criteria
* **Scenario 1: Validación y autocorrección de DUI aprobada**
  * **Given** La suite de pruebas ejecutándose en entorno de testing.
  * **When** Se corre `test_dui_valid_formats_and_autocorrection`.
  * **Then** El test confirma que los formatos válidos se guardan correctamente y los de 9 dígitos continuos se normalizan con guion.
* **Scenario 2: Detección y rechazo de DUIs duplicados o mal formados**
  * **When** Se ejecutan `test_dui_invalid_formats` y `test_dui_uniqueness_constraint`.
  * **Then** El test confirma que se lanzan las excepciones `ValidationError` e `IntegrityError` impidiendo la corrupción de la base de datos.
* **Scenario 3: Verificación de búsqueda rápida por múltiples criterios**
  * **When** Se ejecuta `test_customer_name_search`.
  * **Then** El test confirma que el método `name_search` localiza al cliente tanto por DUI como por número de teléfono.

## 7. Verification Plan
* **Automated Tests:**
  * Comando: `docker compose exec web odoo -u caryvil_erp --test-enable --stop-after-init -d test_db --test-tags=caryvil_erp.TestLocalValidations`.
* **Manual Verification:**
  * Verificar en los logs de consola que los 5 casos de prueba finalicen en verde sin errores.

## 8. Security and Privacy
* Los datos de prueba utilizan identificadores sintéticos para validar el comportamiento algorítmico sin usar datos reales.

## 9. Risks and Mitigation
* **Risk:** Fallos en pruebas de unicidad por transacciones anidadas en PostgreSQL.
  * **Mitigation:** Uso de `@mute_logger('odoo.sql_db')` y captura de `IntegrityError` para manejo limpio de excepciones a nivel de base de datos.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/tests/test_local_validations.py`.
* Inclusión en `custom_addons/caryvil_erp/tests/__init__.py`.

## 11. Definition of Done (DoD)
* [ ] Suite de pruebas de validaciones locales implementada en Python.
* [ ] Autocorrección, unicidad y rechazo de DUIs mal formados comprobada.
* [ ] Cobertura de pruebas de las funciones de validación > 95%.
* [ ] Pruebas aprobadas en el pipeline de CI/CD de GitHub Actions.
* [ ] Revisión técnica aprobada por el equipo de desarrollo.
