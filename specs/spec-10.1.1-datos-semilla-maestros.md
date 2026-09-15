# SPEC-10.1.1: Datos Semilla Maestros del Sistema

## 1. Objective
Construir, empaquetar y cargar los archivos de datos semilla maestros (*Master Seed Data*) en formato XML/CSV dentro de `custom_addons/caryvil_erp/data/` para inicializar automáticamente el sistema ERP de Farmacia Caryvil con la estructura corporativa, moneda oficial (USD), régimen fiscal salvadoreño (IVA 13%), catálogo de categorías terapéuticas, principios activos, unidades de medida farmacéuticas y usuarios base con sus respectivos roles de seguridad.

## 2. Scope
### 2.1. Included
* Creación de los archivos de datos maestros no actualizables por migración (`noupdate="1"`):
  * `company_data.xml`: Registro de la empresa principal "Farmacia Caryvil" con dirección en Soyapango, San Salvador, teléfono, moneda base USD y país El Salvador.
  * `tax_data.xml`: Configuración del impuesto salvadoreño IVA 13% aplicable a ventas y compras con sus respectivas cuentas contables.
  * `pharmacy_categories_data.xml`: Catálogo de 10 familias terapéuticas base (Analgésicos/Antiinflamatorios, Antibióticos, Antihistamínicos, Antihipertensivos, Gastrointestinales, Antidiabéticos, Vitaminas y Suplementos, Dermatológicos, Respiratorios, Oftálmicos).
  * `active_ingredients_data.xml`: Catálogo base de principios activos normalizados (Paracetamol, Ibuprofeno, Amoxicilina, Loratadina, Enalapril, Metformina, Omeprazol, Salbutamol, Complejo B, etc.).
  * `users_roles_data.xml`: Carga de usuarios de demostración y roles para pruebas locales (`admin_user`, `cashier_user`, `stock_user`).
* Carga ordenada en la sección `data` del manifiesto `__manifest__.py`.

### 2.2. Not Included (Out of Scope)
* Carga de existencias físicas de inventario o lotes operativos (cubierto en `SPEC-10.2.1`).
* Carga de la lista de clientes o proveedores de demostración (cubierto en `SPEC-10.2.1`).

## 3. Context and Restrictions
* **Context:** Permite que al inicializar una nueva base de datos en Docker o en Render, el sistema esté inmediatamente operativo con todas las tablas maestras y configuraciones legales sin requerir parametrización manual.
* **Restrictions:**
  * Los registros maestros deben utilizar identificadores externos (*External IDs* o `xml_id`) descriptivos y únicos para prevenir duplicaciones ante reinstalaciones.
  * La moneda del sistema debe fijarse estrictamente en Dólares Estadounidenses (USD - `$`).

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
  * `SPEC-2.2.1` (Definición de Roles y Grupos de Usuarios).
  * `SPEC-7.1.1` (Catálogo y Categorización de Medicamentos).
  * `SPEC-7.1.2` (Gestión de Unidades de Medida Farmacéuticas).
* **Definition of Ready (DoR):**
  * [x] Datos fiscales oficiales de Farmacia Caryvil recopilados.
  * [x] Listado de principios activos y familias terapéuticas prioritarias aprobado.

## 5. Design (Implementation Details)
* **Master Data Manifest Configuration (`__manifest__.py`):**
  ```python
  'data': [
      # Seguridad
      'security/caryvil_security.xml',
      'security/ir.model.access.csv',
      'security/caryvil_security_rules.xml',
      # Datos Maestros
      'data/company_data.xml',
      'data/pharmacy_uom_data.xml',
      'data/tax_data.xml',
      'data/pharmacy_categories_data.xml',
      'data/active_ingredients_data.xml',
      'data/invoice_sequence_data.xml',
      'data/users_roles_data.xml',
      # Vistas
      'views/caryvil_menus.xml',
  ],
  ```
* **Sample Data XML (`data/pharmacy_categories_data.xml`):**
  ```xml
  <?xml version="1.0" encoding="utf-8"?>
  <odoo>
      <data noupdate="1">
          <record id="cat_analgesicos" model="caryvil.therapeutic.category">
              <field name="name">Analgésicos y Antiinflamatorios</field>
              <field name="code">N02B</field>
              <field name="description">Medicamentos para el alivio del dolor y reducción de inflamación.</field>
          </record>
          <record id="cat_antibioticos" model="caryvil.therapeutic.category">
              <field name="name">Antibióticos y Antimicrobianos</field>
              <field name="code">J01C</field>
              <field name="description">Fármacos para el tratamiento de infecciones bacterianas.</field>
          </record>
      </data>
  </odoo>
  ```

## 6. Acceptance Criteria
* **Scenario 1: Inicialización de base de datos limpia**
  * **Given** Una base de datos PostgreSQL recién creada.
  * **When** Se instala el módulo `caryvil_erp`.
  * **Then** La compañía "Farmacia Caryvil" debe quedar establecida con moneda USD y las 10 familias terapéuticas base deben aparecer cargadas en el catálogo.
* **Scenario 2: Configuración automática del impuesto IVA (13%)**
  * **Given** El módulo `caryvil_erp` instalado.
  * **When** Se consulta la configuración de impuestos de venta y compra.
  * **Then** Debe existir el impuesto "IVA 13% Bienes Farmacéuticos" activo y configurado como predeterminado.
* **Scenario 3: Creación de usuarios de prueba por rol**
  * **Given** La base de datos inicializada en modo desarrollo.
  * **When** Se consultan los usuarios en `Ajustes > Usuarios`.
  * **Then** Deben existir los usuarios preconfigurados con sus credenciales y grupos de seguridad (`cajero_caryvil`, `compras_caryvil`, `admin_caryvil`).

## 7. Verification Plan
* **Automated Tests:**
  * Prueba unitaria en Python verificando la existencia de los registros por su `xml_id` mediante `env.ref('caryvil_erp.cat_analgesicos')` y `env.ref('caryvil_erp.tax_iva_13_sale')`.
* **Manual Verification:**
  * Instalar el módulo en un contenedor Docker limpio y comprobar que las listas desplegables de categorías y principios activos contengan datos desde el primer inicio.

## 8. Security and Privacy
* Las contraseñas de los usuarios semilla de prueba deben ser modificadas obligatoriamente al realizar el despliegue a producción.

## 9. Risks and Mitigation
* **Risk:** Sobreescritura accidental de personalizaciones manuales durante actualizaciones del módulo (`-u caryvil_erp`).
  * **Mitigation:** Uso estricto de la directiva `noupdate="1"` en los registros de datos maestros.

## 10. Deliverables & Config as Code
* Archivos XML en `custom_addons/caryvil_erp/data/` (`company_data.xml`, `tax_data.xml`, `pharmacy_categories_data.xml`, `active_ingredients_data.xml`, `users_roles_data.xml`).
* Registro de todos los archivos en `__manifest__.py`.

## 11. Definition of Done (DoD)
* [ ] Archivos de datos maestros creados con sintaxis XML válida.
* [ ] Carga exitosa verificada en una base de datos Odoo virgen.
* [ ] Impuesto IVA 13% y moneda USD parametrizados.
* [ ] Pruebas unitarias de carga de datos aprobadas al 100%.
* [ ] Aprobación de las categorías y datos corporativos por la farmacia.
