# SPEC-ISSUE-67: Corrección de Fecha de Vencimiento en Recepciones y Restablecimiento de Interfaz de Facturación en Compras

## 1. Objective
Resolver y subsanar dos defectos operativos críticos identificados en el flujo de compras e inventario de Farmacia Caryvil reportados en el Issue #67:
1. **Recepción de Productos (`stock.picking`):** Corregir la disponibilidad y usabilidad del campo "Fecha de Vencimiento" (`expiration_date`) en la vista de operaciones detalladas de albaranes de entrada (`stock.move.line`), garantizando el uso de datepicker interactivo, corrigiendo la condición de visibilidad basada en el seguimiento de lote del producto (`tracking in ('lot', 'serial')`), y asegurando que la fecha digitada se guarde y sincronice de forma persistente en el registro del lote (`stock.lot`).
2. **Órdenes de Compra (`purchase.order`):** Restablecer la interfaz y flujo estándar nativo de Odoo para la generación de Facturas de Proveedor eliminando el ocultamiento forzado del botón "Crear Factura" (`action_create_invoice`) y asegurando la total operatividad del botón inteligente (stat button) de facturas vinculadas (`action_view_invoice` / `invoice_ids`), permitiendo al usuario la transición natural de la Orden de Compra hacia el borrador de Factura de Proveedor (`account.move`).

---

## 2. Scope

### 2.1. Included
* **Módulo de Inventario / Recepciones (`stock.picking`, `stock.move.line`):**
  * Corrección de la vista XML `view_stock_move_line_operation_tree_caryvil` en `custom_addons/caryvil_erp/views/stock_picking_views.xml`:
    * Sustituir la condición inválida `column_invisible="parent.has_tracking == 'none'"` por la expresión correcta evaluada en la línea: `column_invisible="tracking in ('none', False)"`.
    * Configurar widget de selección de fecha (`widget="date"`) en el campo `expiration_date` para facilitar la captura ágil en mostrador/bodega.
  * Extensión en `custom_addons/caryvil_erp/models/stock_picking_reception.py`:
    * Asegurar que tras la validación del albarán (`button_validate`), cualquier fecha de caducidad ingresada en la línea de movimiento (`stock.move.line.expiration_date`) se sincronice y propague formalmente al lote correspondiente (`stock.lot.expiration_date`), disparando el recalculo de `alert_date` y `removal_date`.
* **Módulo de Compras / Facturación (`purchase.order`):**
  * Corrección de la vista XML `view_purchase_order_form_caryvil` en `custom_addons/caryvil_erp/views/purchase_order_views.xml`:
    * Remover el nodo `<attribute name="invisible">1</attribute>` aplicado sobre el botón nativo `action_create_invoice`.
    * Garantizar visibilidad del botón nativo "Crear Factura" cuando la orden esté en estado confirmado (`purchase`) o recibido/bloqueado (`done`) y existan líneas facturables pendientes según la política de facturación.
    * Habilitar y comprobar el funcionamiento del botón inteligente (*stat button*) nativo de facturas vinculadas (`action_view_invoice` con conteo `invoice_count` / `invoice_ids`).
    * Armonizar la convivencia entre el flujo nativo de facturación de Odoo y la funcionalidad complementaria de `action_generar_factura_final_caryvil` y gestión de abonos.
* **Pruebas Automatizadas:**
  * Actualización e incorporación de casos de prueba unitarios en `tests/test_stock_picking_reception.py` y `tests/test_purchase_order_medicine.py` para validar la sincronización de lotes y la generación fluida de facturas desde la orden de compra.

### 2.2. Not Included (Out of Scope)
* Modificaciones al motor de salida de inventario por política FEFO (`SPEC-9.3.2`).
* Cambios en la estructura de datos fiscales de facturación hacia el Ministerio de Hacienda (DTE).
* Alteración del modelo de abonos informales `purchase.order.abono` más allá de su coexistencia armónica con las facturas nativas.

---

## 3. Context and Restrictions
* **Context:**
  * En la operación real de Farmacia Caryvil, cuando se reciben medicamentos enviados por laboratorios o droguerías, es mandatorio registrar el número de lote y su fecha de caducidad en el albarán de entrada antes de guardar las existencias en las estanterías de bodega. Un input de fecha invisible o defectuoso detiene el ingreso de mercadería.
  * Por otra parte, el proceso de compras requiere conciliar la orden de compra con la factura física entregada por el transportista del laboratorio mediante la generación de la Factura de Proveedor en Odoo (`in_invoice`), permitiendo cargar los pagos y retenciones fiscales sin restricciones artificiales.
* **Restrictions:**
  * **Odoo 17 ORM:** En vistas `tree` anidadas o de operaciones detalladas (`stock.move.line`), el acceso al modelo padre mediante `parent.` solo debe referenciar campos existentes en la vista del modelo primario. El modelo `stock.picking` no posee el atributo `has_tracking`; el tracking reside en `product_id.tracking` y se proyecta en la línea como `tracking`.
  * **Integridad de datos de lotes:** Todo medicamento con seguimiento por lote (`tracking='lot'`) debe quedar vinculado a un registro de `stock.lot` cuya `expiration_date` coincida con la digitada en la recepción.
  * **Flujo contable nativo:** No se debe sobreescribir ni deshabilitar destructivamente la lógica del módulo core `purchase` y `purchase_stock`.

---

## 4. Dependencias y Definición de Preparación (DoR)

### 4.1. Dependencias Previas
* `SPEC-8.1.1` (Gestión de Órdenes de Compra).
* `SPEC-8.1.2` (Abonos y Pagos a Proveedores).
* `SPEC-8.2.1` (Recepción de Mercadería y Registro de Lotes).
* Módulos base instalados: `stock`, `purchase`, `purchase_stock`, `product_expiry`, `account`.

### 4.2. Definition of Ready (DoR) Checklist
* [x] Issue #67 analizado y reproducido en el código actual de `custom_addons/caryvil_erp/`.
* [x] Causa raíz identificada en `stock_picking_views.xml` (`parent.has_tracking == 'none'`).
* [x] Causa raíz identificada en `purchase_order_views.xml` (ocultamiento forzado de `action_create_invoice`).
* [x] Rama de trabajo `fix/issue-67-vencimiento-recepciones-facturacion-compra` creada a partir de `dev`.

---

## 5. Design (Implementation Details)

### 5.1. Vistas XML

#### A. Recepción de Lotes (`custom_addons/caryvil_erp/views/stock_picking_views.xml`)
Se corrige la herencia sobre `stock.view_stock_move_line_operation_tree`:
```xml
<record id="view_stock_move_line_operation_tree_caryvil" model="ir.ui.view">
    <field name="name">stock.move.line.operations.tree.caryvil</field>
    <field name="model">stock.move.line</field>
    <field name="inherit_id" ref="stock.view_stock_move_line_operation_tree"/>
    <field name="arch" type="xml">
        <field name="lot_name" position="attributes">
            <attribute name="string">Código de Lote</attribute>
        </field>
        <field name="lot_name" position="after">
            <!-- tracking proviene de stock.move.line (related a product_id.tracking) -->
            <field name="tracking" column_invisible="True"/>
            <field name="expiration_date" string="Fecha de Vencimiento"
                   widget="date"
                   column_invisible="tracking in ('none', False)"
                   readonly="tracking in ('none', False)"/>
        </field>
        <field name="quantity" position="attributes">
            <attribute name="string">Stock Ingresado</attribute>
        </field>
    </field>
</record>
```

#### B. Órdenes de Compra (`custom_addons/caryvil_erp/views/purchase_order_views.xml`)
Se retira el atributo `invisible="1"` sobre `action_create_invoice` y se asegura la visibilidad de los botones inteligentes:
```xml
<!-- En view_purchase_order_form_caryvil: -->
<!-- 1. Se remueve el xpath que forzaba invisible="1" sobre action_create_invoice -->
<!-- 2. Se conserva action_create_invoice con sus condiciones nativas de visualización -->
<!-- 3. Se asegura que el stat button action_view_invoice (Vendor Bills) esté disponible -->
```

### 5.2. Modelos Python

#### A. Sincronización de Lote y Vencimiento (`custom_addons/caryvil_erp/models/stock_picking_reception.py`)
En el método `button_validate` de `stock.picking`:
```python
def button_validate(self):
    # Validaciones existentes de lotes requeridos y fechas caducadas
    ...
    res = super().button_validate()

    # Sincronización post-validación: asegurar que los lotes creados o asignados
    # tomen la fecha de vencimiento ingresada en stock.move.line
    for picking in self:
        if picking.picking_type_code == "incoming":
            for line in picking.move_line_ids:
                if line.lot_id and line.expiration_date:
                    if not line.lot_id.expiration_date or line.lot_id.expiration_date != line.expiration_date:
                        line.lot_id.write({"expiration_date": line.expiration_date})
    return res
```

#### B. Soporte de Facturación en Compras (`custom_addons/caryvil_erp/models/purchase_order_medicine.py`)
* Garantizar que `action_create_invoice` genere la factura y redireccione al formulario borrador de la factura creada (`account.move`) cuando se invoque desde la interfaz.
* Verificar compatibilidad con `action_view_invoice` y el conteo de facturas (`invoice_count`).

---

## 6. Acceptance Criteria (Gherkin Syntax)

### Escenario 1: Captura interactiva de fecha de vencimiento al recepcionar medicamentos
* **Given** una orden de compra confirmada a un laboratorio con 20 unidades del medicamento con seguimiento por lotes "Amoxicilina 500mg".
* **When** el encargado de bodega abre el albarán de entrada (`stock.picking`), hace clic en Operaciones Detalladas y agrega una línea con Lote "LOT-AMOX-2027" y selecciona mediante el widget de calendario la fecha de vencimiento "2027-12-31".
* **Then** la columna "Fecha de Vencimiento" es completamente visible, editable y permite seleccionar la fecha sin errores de interfaz.
* **And** al presionar "Validar", el albarán cambia a estado `done` y el lote "LOT-AMOX-2027" en `stock.lot` queda guardado con `expiration_date = 2027-12-31`.

### Escenario 2: Ocultamiento automático de vencimiento en productos sin seguimiento
* **Given** una orden de compra confirmada con un insumo médico o producto con `tracking = 'none'`.
* **When** el usuario abre la tabla de operaciones detalladas en la recepción.
* **Then** la columna "Fecha de Vencimiento" permanece oculta de manera no intrusiva (`column_invisible = True`), sin generar errores de evaluación de campos inexistentes en el modelo padre.

### Escenario 3: Restablecimiento del botón "Crear Factura" en Orden de Compra
* **Given** una orden de compra en estado `purchase` (confirmada) o `done` (recibida).
* **When** el encargado de compras visualiza el formulario de la orden.
* **Then** el botón "Crear Factura" es claramente visible en la barra de botones del encabezado.
* **When** el usuario hace clic en "Crear Factura".
* **Then** Odoo genera el registro borrador de Factura de Proveedor (`account.move`, `in_invoice`) con las líneas y montos de la orden y redirige al usuario a la vista de edición de dicha factura.

### Escenario 4: Conteo y navegación mediante Stat Button de Facturas
* **Given** una orden de compra que ya cuenta con una o más facturas de proveedor generadas.
* **When** el usuario consulta la orden de compra.
* **Then** el stat button de facturas muestra el conteo exacto de facturas asociadas (`invoice_count`).
* **And** al hacer clic en el stat button, Odoo abre la vista de lista/formulario de las facturas vinculadas a dicha orden.

---

## 7. Verification Plan

### 7.1. Automated Tests (`odoo-bin --test-enable`)
* Ejecutar la suite de pruebas unitarias de inventario y compras:
  ```bash
  python -m unittest custom_addons.caryvil_erp.tests.test_stock_picking_reception
  python -m unittest custom_addons.caryvil_erp.tests.test_purchase_order_medicine
  ```
* Casos específicos a validar:
  1. `test_recepcion_sincroniza_expiration_date_en_stock_lot`: Validar que tras `picking.button_validate()`, `line.lot_id.expiration_date` coincida exactamente con la fecha suministrada.
  2. `test_crear_factura_desde_orden_compra`: Validar que al ejecutar `orden.action_create_invoice()`, se genere un `account.move` borrador enlazado en `orden.invoice_ids`.

### 7.2. Manual Verification Checklist
1. **Verificación de Recepción e Input Datepicker:**
   * Crear y confirmar una Orden de Compra de medicamento con lote.
   * Entrar a la Recepción de inventario -> pestaña "Operaciones Detalladas".
   * Comprobar que aparece el campo "Fecha de Vencimiento" con selector de fecha calendario.
   * Seleccionar fecha y presionar "Validar".
   * Ir al menú Inventario -> Productos -> Lotes/Números de Serie y verificar que el lote tenga la fecha asignada.
2. **Verificación de Factura de Compra:**
   * Abrir la Orden de Compra confirmada.
   * Verificar presencia visible del botón "Crear Factura".
   * Pulsar "Crear Factura" y comprobar apertura de la Factura de Proveedor en estado borrador.
   * Regresar a la Orden de Compra y comprobar que el stat button muestra "1 Factura".

---

## 8. Security and Privacy
* La edición de fechas de vencimiento en recepciones está restringida a los grupos `group_caryvil_inventory_purchases` y `group_caryvil_admin`.
* La creación de facturas de proveedor desde la orden de compra respeta las listas de control de acceso de Odoo para el grupo `account.group_account_invoice` y compras.
* No se exponen datos sensibles de clientes ni credenciales.

---

## 9. Risks and Mitigation
* **Riesgo:** Conflicto entre la creación nativa de facturas y el botón custom `action_generar_factura_final_caryvil`.
  * **Mitigación:** Ambos mecanismos pueden coexistir de forma no destructiva: `action_create_invoice` permite el flujo formal nativo de Odoo en cualquier momento para usuarios contables, mientras que la interfaz de abonos continúa funcionando para control de saldos diarios.
* **Riesgo:** Incompatibilidad de versión en atributos XML de vista tree (`column_invisible` vs `invisible`).
  * **Mitigación:** En Odoo 17, `column_invisible` es la sintaxis oficial para ocultar columnas completas en vistas `tree`; se valida la sintaxis con el linter y pruebas de carga de vistas.

---

## 10. Deliverables & Config as Code
* **Especificación:**
  * `specs/spec-issue-67-vencimiento-recepciones-facturacion-compra.md`
* **Vistas XML:**
  * `custom_addons/caryvil_erp/views/stock_picking_views.xml`
  * `custom_addons/caryvil_erp/views/purchase_order_views.xml`
* **Modelos Python:**
  * `custom_addons/caryvil_erp/models/stock_picking_reception.py`
  * `custom_addons/caryvil_erp/models/purchase_order_medicine.py`
* **Pruebas Automatizadas:**
  * `custom_addons/caryvil_erp/tests/test_stock_picking_reception.py`
  * `custom_addons/caryvil_erp/tests/test_purchase_order_medicine.py`

---

## 11. Definition of Done (DoD)
* [x] Especificación técnica `spec-issue-67-vencimiento-recepciones-facturacion-compra.md` revisada y aprobada.
* [x] Rama `fix/issue-67-vencimiento-recepciones-facturacion-compra` creada a partir de `dev`.
* [x] Campo `expiration_date` visible con datepicker en operaciones detalladas para productos con lote.
* [x] Sincronización automática de `expiration_date` hacia `stock.lot` probada.
* [x] Botón nativo "Crear Factura" y stat button de facturas restablecidos y funcionales en `purchase.order`.
* [x] Pruebas unitarias ejecutadas con 0 fallos y 0 errores.
* [x] Estilo de código conforme a PEP8/Flake8.
