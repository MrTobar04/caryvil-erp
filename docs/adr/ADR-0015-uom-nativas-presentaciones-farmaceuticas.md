# [ADR-0015] Uso de Unidades de Medida Nativas de Odoo para Presentaciones Farmacéuticas

## Status

Accepted

## Context

Durante la implementación de la especificación `SPEC-7.1.2` (Gestión de Unidades de Medida Farmacéuticas), se requirió soportar diferentes presentaciones comerciales de medicamentos, permitiendo adquirir productos en cajas o blísteres y mantener el inventario en una unidad base farmacéutica.

Odoo proporciona de forma nativa los campos `uom_id` y `uom_po_id` en `product.template`, así como el mecanismo de conversión entre unidades pertenecientes a una misma categoría de unidades de medida.

Se identificó que agregar campos personalizados para representar la unidad de compra y la unidad de inventario duplicaría funcionalidad existente en Odoo y requeriría implementar lógica adicional para realizar las conversiones de cantidades.

Por lo tanto, se requirió definir una estrategia única para representar las presentaciones farmacéuticas sin modificar el mecanismo estándar de conversión de Odoo.

## Decision

Hemos decidido utilizar las unidades de medida nativas de Odoo para gestionar las presentaciones farmacéuticas:

1. **Unidad base farmacéutica:** Se establece `Unidad / Pastilla` como unidad de referencia para la categoría `Presentaciones Farmacéuticas`.

2. **Unidades comerciales:** Se definen unidades superiores dentro de la misma categoría para representar las presentaciones habituales de medicamentos:
   - `Blíster x 4 unidades`
   - `Blíster x 10 unidades`
   - `Caja x 20 unidades`
   - `Caja x 50 unidades`
   - `Caja x 100 unidades`

3. **Separación entre inventario y compra:** Se utilizan los campos nativos `uom_id` y `uom_po_id` de `product.template`. El `uom_id` representa la unidad utilizada para inventario y ventas, mientras que `uom_po_id` representa la unidad utilizada para compras.

4. **Conversión nativa:** Las conversiones entre presentaciones se delegan al mecanismo estándar de Odoo mediante las relaciones de conversión de `uom.uom`, evitando implementar lógica personalizada para convertir cantidades.

5. **Restricción de modificaciones:** La modificación de las unidades de medida y sus factores de conversión queda restringida mediante los permisos existentes de Odoo, permitiendo escritura al Administrador y evitando modificaciones por parte de los roles operativos.

## Consequences

### Positivas:

* **Reutilización del estándar de Odoo:** Se aprovechan `uom_id`, `uom_po_id` y el mecanismo nativo de conversión sin duplicar funcionalidad.

* **Conversión automática:** Una compra expresada en una presentación comercial puede convertirse automáticamente a la unidad base de inventario. Por ejemplo, `1 Caja x 100 unidades` se registra como `100 Unidad / Pastilla`.

* **Integración con Compras e Inventario:** La solución utiliza los mecanismos estándar de Odoo, facilitando su integración con los flujos existentes.

* **Consistencia de cantidades:** Las presentaciones farmacéuticas pertenecientes a la misma categoría mantienen relaciones numéricas definidas respecto a la unidad base.

* **Control administrativo:** La modificación de las unidades y factores de conversión no queda disponible para los usuarios operativos.

### Negativas / Trade-offs:

* **Dependencia del modelo estándar de Odoo:** La implementación depende del comportamiento de `uom.uom`, `uom_id` y `uom_po_id` proporcionado por Odoo.

* **Restricción para productos con historial:** Odoo no permite cambiar la unidad de medida de productos que ya poseen movimientos de inventario, por lo que la UoM debe definirse correctamente antes de comenzar a utilizar un producto en operaciones de inventario.

* **Presentaciones no discretas:** Las presentaciones líquidas o semisólidas requieren una definición de conversión compatible con la categoría farmacéutica antes de incorporarse como unidades convertibles.