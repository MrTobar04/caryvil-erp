# [ADR-0017] Estrategia de Venta de Mostrador y Cobro Unificado

## Status

Accepted

## Context

La operación de venta de Farmacia Caryvil requiere una interfaz de mostrador
rápida que permita registrar medicamentos, identificar clientes, gestionar el
cobro y posteriormente integrarse con la facturación y el despacho de
inventario.

Odoo 17 ya proporciona el modelo estándar `sale.order` y sus líneas de venta,
incluyendo soporte para búsqueda y lectura de productos mediante código de
barras.

La implementación de una solución paralela para ventas produciría duplicación
de lógica y dificultaría la integración posterior con facturación, inventario
y trazabilidad de lotes.

## Decision

Se utilizará el modelo nativo `sale.order` de Odoo como base para el flujo de
ventas de mostrador de Farmacia Caryvil.

La personalización se implementará mediante extensión ORM (`_inherit`) sobre
`sale.order` y `product.product`, junto con vistas XML heredadas del formulario
estándar de ventas.

La interfaz de mostrador incorporará:

- Forma de pago.
- Monto recibido en efectivo.
- Cálculo automático del cambio.
- Cliente "Consumidor Final" por defecto.
- Entrada rápida mediante código de barras.
- Búsqueda de productos por principio activo.
- Validación de disponibilidad antes de confirmar la venta.
- Acción unificada "Cobrar y Facturar".

El escaneo de código de barras aprovechará el widget nativo de Odoo siempre que
sea posible, evitando implementar un lector de códigos independiente mediante
JavaScript.

La lógica específica de selección FEFO y la deducción definitiva del stock se
mantendrán en sus respectivas especificaciones (`SPEC-9.3.1` y
`SPEC-9.3.2`) para mantener la separación de responsabilidades.

## Consequences

### Positivas

- Se reutiliza la infraestructura nativa de ventas de Odoo.
- Se reduce la cantidad de código personalizado.
- Se facilita la integración con `account.move`.
- Se facilita la integración posterior con inventario y lotes.
- Se mantiene la trazabilidad de la venta dentro de los modelos estándar de Odoo.

### Negativas / Trade-offs

- La interfaz está condicionada por la estructura base de `sale.order`.
- Algunas funcionalidades de mostrador requieren extensiones específicas del
  formulario estándar.
- La lógica de FEFO seguirá dependiendo de la integración con el módulo de
  inventario.

## Related Specifications

- `spec-9.1.1`
- `spec-9.2.1`
- `spec-9.3.1`
- `spec-9.3.2`
- `spec-3.3.1`
- `spec-11.1.2`