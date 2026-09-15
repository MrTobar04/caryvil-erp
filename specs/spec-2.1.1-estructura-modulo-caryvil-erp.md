# SPEC-2.1.1: Estructura del Módulo Personalizado caryvil_erp

## 1. Objective
Definir, estructurar y crear el andamiaje (*scaffolding*) del módulo personalizado de Odoo denominado `caryvil_erp` dentro del directorio `custom_addons/`. Esta especificación establece la arquitectura modular estándar de Odoo, el archivo manifiesto `__manifest__.py`, los enlaces de inicialización `__init__.py` y las dependencias base requeridas (`sale_management`, `purchase`, `stock`, `contacts`, `account`) para soportar todas las extensiones funcionales de Farmacia Caryvil.

## 2. Scope
### 2.1. Included
* Creación de la estructura de carpetas estándar del addon `custom_addons/caryvil_erp/`:
  * `models/`: Clases y extensiones ORM de Python.
  * `views/`: Vistas XML (formularios, árboles/listas, búsquedas, menús y acciones).
  * `security/`: Definición de grupos, reglas de registro y archivo `ir.model.access.csv`.
  * `data/`: Archivos XML/CSV con secuencias, categorías y datos maestros.
  * `reports/`: Plantillas de reportes QWeb y acciones de impresión.
  * `static/`: Recursos estáticos (CSS, SCSS, JavaScript, imágenes y logotipos).
  * `demo/`: Datos de demostración y pruebas operativas.
* Definición exhaustiva del manifiesto `__manifest__.py` con metadatos del proyecto, autoría, versión semántica (1.0.0), categoría, dependencias base y lista de carga de archivos `data`.
* Configuración de la bandera `application = True` e `installable = True` para que el módulo aparezca como una aplicación principal en el catálogo de Odoo.

### 2.2. Not Included (Out of Scope)
* Definición detallada de grupos y permisos de usuario (cubierto en `SPEC-2.2.1` y `SPEC-2.2.2`).
* Implementación de los modelos específicos de clientes, medicamentos o ventas (cubierto en los Dominios 5, 7, 8 y 9).

## 3. Context and Restrictions
* **Context:** Actúa como el contenedor central donde se implementará toda la lógica de negocio y personalizaciones requeridas para Farmacia Caryvil, desacoplándola del núcleo de Odoo para facilitar futuras actualizaciones sin pérdida de código.
* **Restrictions:**
  * Debe apegarse a la guía de estilo oficial de desarrollo de Odoo (PEP8 para Python, nombres de vistas XML descriptivos).
  * Compatibilidad asegurada con Odoo 16.0 y 17.0 Community Edition bajo licencia LGPL-3.
  * No debe sobreescribir métodos nativos sin invocar adecuadamente `super()`.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-1.1.1` (Configuración del Entorno Docker).
  * `SPEC-1.1.2` (Configuración del Servidor Odoo).
* **Definition of Ready (DoR):**
  * [x] Ruta de addons `/mnt/extra-addons` montada y verificada en el contenedor.
  * [x] Identificación de los módulos oficiales de Odoo necesarios como dependencias (`base`, `sale_management`, `purchase`, `stock`, `contacts`, `account`).

## 5. Design (Implementation Details)
* **Directory Tree:**
  ```
  custom_addons/caryvil_erp/
  ├── __init__.py
  ├── __manifest__.py
  ├── models/
  │   └── __init__.py
  ├── views/
  │   └── caryvil_menus.xml
  ├── security/
  │   ├── caryvil_security.xml
  │   └── ir.model.access.csv
  ├── data/
  ├── reports/
  ├── static/
  │   ├── description/
  │   │   ├── icon.png
  │   │   └── index.html
  │   └── src/
  │       └── scss/
  │           └── custom_theme.scss
  └── demo/
  ```
* **Manifest (`__manifest__.py`):**
  ```python
  # -*- coding: utf-8 -*-
  {
      'name': 'Farmacia Caryvil ERP',
      'version': '1.0.0',
      'category': 'Pharmacy/ERP',
      'summary': 'Sistema integral de gestión farmacéutica: Inventario, Ventas, Compras y Clientes',
      'description': """
          Personalización y extensión de Odoo ERP para Farmacia Caryvil.
          Incluye:
          - Control estricto de lotes y fechas de vencimiento.
          - Venta en mostrador con deducción automática y política FEFO.
          - Facturación simple para consumidor final.
          - Registro de clientes con validación de DUI salvadoreño.
          - Gestión de compras y abastecimiento con actualización de stock.
          - Dashboard gerencial de KPIs.
      """,
      'author': 'Equipo de Desarrollo Caryvil - UDB',
      'website': 'https://github.com/MelissaFloresA/Odoo_ERP_Farmacia',
      'license': 'LGPL-3',
      'depends': [
          'base',
          'contacts',
          'stock',
          'purchase',
          'sale_management',
          'account',
      ],
      'data': [
          'security/caryvil_security.xml',
          'security/ir.model.access.csv',
          'views/caryvil_menus.xml',
      ],
      'demo': [],
      'assets': {
          'web.assets_backend': [
              'caryvil_erp/static/src/scss/custom_theme.scss',
          ],
      },
      'installable': True,
      'application': True,
      'auto_install': False,
  }
  ```

## 6. Acceptance Criteria
* **Scenario 1: Reconocimiento e instalación limpia del módulo**
  * **Given** El módulo `caryvil_erp` colocado en `custom_addons/`.
  * **When** El administrador actualiza la lista de aplicaciones e instala "Farmacia Caryvil ERP".
  * **Then** Odoo debe instalar el módulo sin errores, cargando automáticamente todas sus dependencias (`stock`, `purchase`, `sale_management`, `contacts`, `account`).
* **Scenario 2: Creación del menú raíz en la barra de navegación**
  * **Given** El módulo `caryvil_erp` instalado exitosamente.
  * **When** Un usuario autenticado accede a la interfaz principal de Odoo.
  * **Then** Debe visualizarse el icono y acceso a la aplicación "Farmacia Caryvil" con su estructura de menús base.
* **Scenario 3: Desinstalación sin residuos ni errores de integridad**
  * **Given** El módulo `caryvil_erp` instalado en una base de datos de pruebas.
  * **When** El administrador solicita desinstalar la aplicación.
  * **Then** Odoo debe desinstalar el módulo de forma limpia sin corromper los módulos nativos del sistema.

## 7. Verification Plan
* **Automated Tests:**
  * Ejecutar el comando de test de Odoo: `odoo -u caryvil_erp --test-enable --stop-after-init -d test_db`.
  * Validación de sintaxis con `flake8 custom_addons/caryvil_erp` y `xmllint` para archivos XML.
* **Manual Verification:**
  * Instalar el módulo desde la interfaz web en una base de datos limpia y validar la creación de tablas y menús.

## 8. Security and Privacy
* El manifiesto no debe contener llaves API, credenciales ni tokens de servicios externos.
* Los archivos `__init__.py` deben controlar de forma estricta la exportación de modelos para evitar importar código inseguro.

## 9. Risks and Mitigation
* **Risk:** Conflicto de dependencias si se especifica un módulo no presente en la edición Community.
  * **Mitigation:** Utilizar exclusivamente módulos oficiales incluidos en la distribución base de Odoo Community.

## 10. Deliverables & Config as Code
* Estructura completa de carpetas del addon `custom_addons/caryvil_erp/`.
* Archivo `custom_addons/caryvil_erp/__init__.py`.
* Archivo `custom_addons/caryvil_erp/__manifest__.py`.
* Archivo `custom_addons/caryvil_erp/views/caryvil_menus.xml`.
* Archivo de icono `custom_addons/caryvil_erp/static/description/icon.png`.

## 11. Definition of Done (DoD)
* [ ] Estructura de carpetas y archivos base creada bajo estándares Odoo.
* [ ] Manifiesto `__manifest__.py` configurado con todas las dependencias requeridas.
* [ ] Instalación y desinstalación del módulo verificada en Odoo sin errores en logs.
* [ ] Menú raíz de Farmacia Caryvil visible en el backend.
* [ ] Revisión de código completada y fusionada en la rama principal.
