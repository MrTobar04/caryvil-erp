# [ADR-0014] Desacoplamiento de Precio Bruto y Gestión de Descuentos en Catálogo de Proveedores

## Status
Accepted

## Context
Durante la auditoría técnica de la especificación `SPEC-6.2.1` (Catálogo de Precios y Códigos de Proveedor) y su implementación en el modelo `product.supplierinfo`, se identificó una vulnerabilidad de degradación compuesta en la función de recálculo `_onchange_discount_percentage`. 

En la versión inicial, la modificación del campo `discount_percentage` sobreescribía directamente el valor neto en `price`. Si el usuario ingresaba un precio base de $10.00 y aplicaba un 10%, `price` pasaba a $9.00; si posteriormente corregía a 20%, el cálculo se aplicaba sobre $9.00 resultando en $7.20 (28% acumulado) en vez de los $8.00 esperados. Asimismo, al revertir el descuento a 0%, el precio original no se recuperaba.

Adicionalmente, se requería garantizar la confidencialidad de los costos de adquisición farmacéutica restringiendo su visibilidad frente a usuarios con roles operativos en mostrador (`group_caryvil_cajero`), alineándose con el principio de mínimo privilegio bajo ISO-27001.

## Decision
Hemos decidido implementar las siguientes modificaciones arquitectónicas en `product.supplierinfo`:

1. **Introducción del Campo `gross_price`:** Agregamos el campo `gross_price` (Monetary) para almacenar el precio de catálogo de lista oficial provisto por el laboratorio antes de cualquier deducción comercial.
2. **Cálculo Determinista y No Destructivo:** Establecemos la regla de cálculo:
   $$\text{price} = \text{gross\_price} \times \left(1 - \frac{\text{discount\_percentage}}{100}\right)$$
   garantizando que cambios sucesivos en el porcentaje de descuento se apliquen siempre sobre la base inmutable de `gross_price`. Si el usuario digita directamente `price` sin descuento, `gross_price` se sincroniza automáticamente para mantener total retrocompatibilidad.
3. **Control de Acceso y Visibilidad:** Los campos `gross_price`, `discount_percentage`, `product_presentation` y `price` se restringen explícitamente al grupo de seguridad `caryvil_erp.group_caryvil_compras_inventario` en las vistas XML.
4. **Visibilidad de Escalas por Volumen:** Se activa la visibilidad por defecto (`optional="show"`) para `min_qty` (Cantidad Mínima) en la tabla de proveedores para facilitar la comparativa de escalas de precios.

## Consequences
### Positivas:
* **Integridad Matemática y de Costos:** Se elimina el error de descuentos compuestos en la interfaz web de Odoo, garantizando exactitud contable en las órdenes de compra.
* **Trazabilidad Comercial:** El equipo de compras puede visualizar simultáneamente el precio de lista del laboratorio, el descuento pactado y el costo unitario neto resultante.
* **Seguridad y Confidencialidad:** Se resguardan los márgenes y precios de compra frente al personal de caja sin impedir su operativa diaria de venta.
* **Validación E2E:** Permite verificar de forma automatizada los Criterios de Aceptación CA-1, CA-2 y CA-3 de `SPEC-6.2.1`.

### Negativas / Trade-offs:
* **Sobrecarga de Campos en Base de Datos:** Se añade una columna adicional (`gross_price`) en la tabla `product_supplierinfo` de PostgreSQL.
* **Mantenimiento en Vistas Heredadas:** Cualquier módulo que personalice la vista de lista de `product.supplierinfo` debe considerar la presencia y grupos de seguridad de `gross_price` y `discount_percentage`.
