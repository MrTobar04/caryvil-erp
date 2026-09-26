# [ADR-0018] Integración de Facturación Simple, Contabilización y Cobro en Caryvil

## Status

Accepted

## Context

La especificación `spec-9.2.1` requiere generar una factura simple para consumidor final a partir de las ventas realizadas en Farmacia Caryvil,
aplicando automáticamente IVA del 13%, utilizando una numeración correlativa y permitiendo registrar el cobro de la venta.

Los ADR existentes ya establecen dos decisiones relacionadas:

- [ADR-0005](ADR-0005-esquema-de-facturacion-simple-y-validacion-fiscal-salvadorena.md) define el esquema general de facturación simple, el uso del IVA del 13%,
  las secuencias correlativas y el uso de QWeb para los documentos.
- [ADR-0017](ADR-0017-estrategia-venta-mostrador-caryvil.md) establece que las ventas de mostrador se implementarán sobre `sale.order` y que el flujo
  de venta debe integrarse posteriormente con facturación e inventario.

Durante la implementación de `spec-9.2.1` fue necesario definir cómo se conectaría la factura con la configuración contable de Caryvil y cómo se
registraría automáticamente el cobro sin implementar un sistema contable paralelo al estándar de Odoo.

También se identificó que la configuración del impuesto debe formar parte de los datos del módulo y no modificarse dinámicamente cada vez que se publica una
factura.

## Decision

Se utilizarán los mecanismos contables estándar de Odoo 17 y se extenderán mediante ORM únicamente donde sea necesario para cumplir el flujo de
facturación de Caryvil.

### 1. Uso de `account.move` como factura

Las facturas de consumidor final se representarán mediante el modelo estándar `account.move` con `move_type = "out_invoice"`.

La personalización se implementará mediante `_inherit = "account.move"` para agregar únicamente la información específica requerida por Caryvil, evitando
crear un modelo de factura paralelo.

### 2. Numeración correlativa mediante `ir.sequence`

La numeración visible de las facturas será almacenada en el campo `simple_invoice_number`.

La numeración será generada mediante una secuencia de Odoo identificada por:

```text
caryvil.simple.invoice.sequence