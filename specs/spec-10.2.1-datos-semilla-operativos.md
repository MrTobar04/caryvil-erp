# SPEC-10.2.1: Datos Semilla Operativos y Demostración

## 1. Objective
Diseñar, estructurar y cargar el conjunto de **Datos Semilla Operativos y de Demostración** (*Operational & Demo Seed Data*) en Odoo para Farmacia Caryvil dentro de `custom_addons/caryvil_erp/demo/` o `data/`. Esta especificación puebla el sistema con un catálogo realista de más de 25 medicamentos de alta demanda con precios de venta, costos de compra, códigos de barras EAN-13, proveedores farmacéuticos salvadoreños (Laboratorios Vijosa, Laboratorios López, Droguería Santa Lucía), clientes de muestra con DUIs válidos y existencias iniciales asignadas a lotes con fechas de caducidad vigentes y en ventana de alerta para permitir la validación funcional inmediata de todos los módulos.

## 2. Scope
### 2.1. Included
* Creación de los archivos de datos operativos:
  * `demo_vendors_data.xml`: Registro de 4 proveedores farmacéuticos representativos (Laboratorios Vijosa, Laboratorios López, Droguería Santa Lucía, Droguería Americana) con NIT, NRC, plazos de entrega y datos de contacto de ventas.
  * `demo_customers_data.xml`: Registro de 10 perfiles de clientes de muestra con nombres salvadoreños, números de DUI con formato válido (`00000000-0`), teléfonos y direcciones en Soyapango.
  * `demo_medicines_data.xml`: Catálogo de 25 medicamentos cubriendo todas las familias terapéuticas, con códigos de barra EAN-13, principio activo, forma farmacéutica, costo de compra y precio de venta al público (e.g., Amoxicilina 500mg, Paracetamol 500mg, Ibuprofeno 400mg, Loratadina 10mg, Enalapril 20mg, Omeprazol 20mg, Complejo B inyectable, Jarabe para la Tos, etc.).
  * `demo_inventory_stock_data.xml`: Carga de saldos iniciales de existencias con asignación a números de lote específicos y fechas de caducidad:
    * Lotes con vencimiento a largo plazo (años 2027 y 2028) para rotación normal.
    * Lotes con vencimiento a mediano plazo (31 a 60 días) para validar la regla FEFO (`SPEC-9.3.2`).
    * Lotes con vencimiento crítico (<30 días) para validar las alertas del Dashboard (`SPEC-4.2.2`).
* Vinculación de los archivos en la sección `demo` o `data` del manifiesto `__manifest__.py`.

### 2.2. Not Included (Out of Scope)
* Datos contables transaccionales históricos de años anteriores (se inicia desde saldo cero en transacciones).
* Datos maestros estructurales de configuración base (cubierto en `SPEC-10.1.1`).

## 3. Context and Restrictions
* **Context:** Permite al equipo docente, a la propietaria y a los evaluadores del proyecto ejecutar de inmediato demostraciones completas de compra, venta en mostrador, despacho FEFO y monitoreo en dashboard sin necesidad de cargar manualmente decenas de productos.
* **Restrictions:**
  * Los códigos de barras EAN-13 generados deben ser válidos y numéricamente únicos.
  * Los precios y costos deben mantener márgenes comerciales lógicos de farmacia (margen bruto entre 25% y 40%).

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-5.1.1` (Gestión del Perfil de Clientes).
  * `SPEC-6.1.1` (Directorio y Gestión de Proveedores).
  * `SPEC-7.1.1` (Catálogo y Categorización de Medicamentos).
  * `SPEC-7.2.1` (Control de Stock, Lotes y Vencimientos).
  * `SPEC-10.1.1` (Datos Semilla Maestros del Sistema).
* **Definition of Ready (DoR):**
  * [x] Listado de 25 medicamentos más representativos de Farmacia Caryvil estructurado en hoja de cálculo.
  * [x] Modelos de datos y extensiones de Odoo previamente instalados y verificados.

## 5. Design (Implementation Details)
* **Demo File Structure (`demo/`):**
  ```
  custom_addons/caryvil_erp/demo/
  ├── demo_vendors_data.xml
  ├── demo_customers_data.xml
  ├── demo_medicines_data.xml
  └── demo_inventory_stock_data.xml
  ```
* **Sample Medicine XML Definition (`demo/demo_medicines_data.xml`):**
  ```xml
  <?xml version="1.0" encoding="utf-8"?>
  <odoo>
      <data noupdate="1">
          <!-- Medicamento 1: Amoxicilina 500mg -->
          <record id="med_amoxicilina_500" model="product.template">
              <field name="name">Amoxicilina Vijosa 500mg (Caja x 50)</field>
              <field name="detailed_type">product</field>
              <field name="tracking">lot</field>
              <field name="active_ingredient_id" ref="caryvil_erp.ing_amoxicilina"/>
              <field name="therapeutic_category_id" ref="caryvil_erp.cat_antibioticos"/>
              <field name="dosage_form">capsula</field>
              <field name="concentration">500 mg</field>
              <field name="barcode">7410001000012</field>
              <field name="standard_price">4.50</field>
              <field name="list_price">6.50</field>
              <field name="uom_id" ref="uom.product_uom_unit"/>
              <field name="uom_po_id" ref="uom.product_uom_unit"/>
          </record>

          <!-- Medicamento 2: Ibuprofeno 400mg -->
          <record id="med_ibuprofeno_400" model="product.template">
              <field name="name">Ibuprofeno MK 400mg (Caja x 100)</field>
              <field name="detailed_type">product</field>
              <field name="tracking">lot</field>
              <field name="active_ingredient_id" ref="caryvil_erp.ing_ibuprofeno"/>
              <field name="therapeutic_category_id" ref="caryvil_erp.cat_analgesicos"/>
              <field name="dosage_form">tableta</field>
              <field name="concentration">400 mg</field>
              <field name="barcode">7410001000029</field>
              <field name="standard_price">5.00</field>
              <field name="list_price">7.50</field>
          </record>
      </data>
  </odoo>
  ```

## 6. Acceptance Criteria
* **Scenario 1: Carga completa del catálogo de medicamentos operativos**
  * **Given** Una base de datos Odoo con datos demo cargados.
  * **When** El usuario navega a `Inventario > Medicamentos`.
  * **Then** Deben aparecer listados los 25 medicamentos con sus nombres, categorías terapéuticas, principios activos, códigos de barra y precios de venta al público.
* **Scenario 2: Consulta de proveedores y clientes muestra**
  * **Given** El sistema inicializado con datos operativos.
  * **When** Se consultan las listas de Clientes y Proveedores.
  * **Then** Deben visualizarse los 4 laboratorios y los 10 clientes con sus números de DUI formateados listos para transaccionar.
* **Scenario 3: Existencia de stock y lotes para pruebas del Dashboard y FEFO**
  * **Given** La carga de stock inicial ejecutada.
  * **When** La administradora abre el Dashboard de inicio.
  * **Then** El widget de alertas de vencimiento debe mostrar los lotes de prueba clasificados en las ventanas de <30 días y 31-60 días.

## 7. Verification Plan
* **Automated Tests:**
  * Prueba unitaria en Python verificando que el total de productos en catálogo sea `>= 25`, que existan al menos 4 proveedores y que existan registros en `stock.quant` con lotes asociados.
* **Manual Verification:**
  * Realizar un flujo completo de prueba en el entorno local (seleccionar cliente demo, escanear medicamento demo, cobrar e imprimir factura simple).

## 8. Security and Privacy
* Los datos de clientes y contactos en los archivos demo son ficticios (*mock data*) para evitar el uso de información personal sensible real en entornos de prueba o repositorios públicos.

## 9. Risks and Mitigation
* **Risk:** Confusión de datos de prueba con operaciones reales al momento de la puesta en producción.
  * **Mitigation:** Incluir los datos de demostración en un archivo separado bajo el bloque `demo` del manifiesto para que no se instalen en bases de datos de producción a menos que se active explícitamente el flag de datos demo.

## 10. Deliverables & Config as Code
* Archivos XML en `custom_addons/caryvil_erp/demo/` (`demo_vendors_data.xml`, `demo_customers_data.xml`, `demo_medicines_data.xml`, `demo_inventory_stock_data.xml`).
* Registro en la clave `'demo': [...]` de `__manifest__.py`.

## 11. Definition of Done (DoD)
* [ ] Catálogo de 25 medicamentos con datos farmacéuticos completos creado.
* [ ] 4 laboratorios y 10 clientes salvadoreños de muestra estructurados.
* [ ] Stock inicial por lotes con fechas de vencimiento cargado.
* [ ] Pruebas unitarias de verificación de datos aprobadas.
* [ ] Aprobación del conjunto de datos por el equipo del proyecto y la propietaria.
