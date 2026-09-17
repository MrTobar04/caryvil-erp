# [ADR-0008] Gestión de Órdenes de Compra con Abonos y Totales Calculados en Cliente

## Status
Accepted

## Context
SPEC-8.1.1 (Gestión de Órdenes de Compra) requería extender el modelo nativo `purchase.order` de Odoo para el flujo farmacéutico de Caryvil: separación entre Nombre Vendedor (`partner_id`) y Proveedor/Laboratorio (`laboratory_id`, derivado del contacto comercial), códigos correlativos propios (`PE0001...`), estado simplificado en español (Pendiente/Recibido/Cancelado) y un IVA del 13%.

Durante la implementación surgieron dos problemas de fondo que obligaron a decisiones de arquitectura no anticipadas en la spec original:

1. **Seguimiento de pagos parciales.** El flujo nativo de Odoo exige crear una Factura de Proveedor (`account.move`) formal y registrar un pago. Proceso sin utilidad para el día a día de la farmacia, donde los abonos a un pedido se negocian de forma flexible con el vendedor.

2. **Reactividad del resumen de totales.** Los campos calculados a nivel de encabezado (`Subtotal`, `Descuento`, `IVA`, `Total`) dependientes de `order_line` se quedaban en `$0.00` en el navegador al agregar una línea de producto nueva. Se confirmó mediante inspección de las peticiones XHR que el webclient de Odoo 17 dispara el `onchange` de `purchase.order.line` para una fila one2many recién creada, pero **no** dispara de forma confiable el `onchange` del modelo padre (`purchase.order`) en ese mismo ciclo. Esto es una limitación del webclient, no un error de la implementación: cualquier campo `Monetary` computado en el encabezado y dependiente de las líneas queda visualmente desactualizado hasta que un campo no relacionado fuerza un `onchange` completo del registro.

Este registro se relaciona con `spec-8.1.1` (Gestión de Órdenes de Compra), `spec-8.2.1`/`spec-8.2.2`/`spec-8.2.3` (recepción, actualización de stock y discrepancias) y `spec-3.3.2` (reporte PDF de orden de compra).

## Decision

### 1. Abonos en vez de Factura de Proveedor por cada pago
Se implementó un modelo nuevo y simple, `purchase.order.abono` (fecha, monto, nota), como línea `One2many` directamente en la Orden de Compra, sin ningún asiento contable. Los campos computados `monto_abonado`, `saldo_abonos_pendiente` y `abono_status_label` (`pendiente`/`parcial`/`pagado`) se derivan exclusivamente de `abono_ids` y del total final de la orden.

Cuando `abono_status_label == 'pagado'` (100% abonado), se habilita un único botón, **"Generar Factura Final"**, que en un solo clic:
- Crea y postea la Factura de Proveedor (`account.move`) formal.
- Registra automáticamente el pago completo, vía el wizard nativo `account.payment.register`.

El botón nativo "Crear Factura" se oculta (`invisible="1"`) para que el flujo diario de caja no pase por Contabilidad. Se verificó explícitamente que el bloqueo automático de la orden (`Bloqueada`, al alcanzar 100% de recepción) **no** impide registrar abonos ni generar la factura final.

### 2. Totales del encabezado calculados en el navegador (widget OWL), no en el servidor
En vez de depender del `onchange` del servidor para refrescar `Subtotal`/`Descuento`/`IVA (13%)`/`IVA Percibido`/`Total`, se implementó un campo widget personalizado (`caryvil_purchase_live_totals`, componente OWL en `purchase_live_totals.js`/`.xml`) que lee directamente `props.record.data.order_line.records` — el estado ya reactivo del formulario en el cliente — y calcula todo localmente:

- Subtotal neto = `Σ (cantidad × precio_unitario × (1 − descuento/100))`.
- Descuento = bruto − neto.
- IVA = `neto × 13%` (tasa fija, independiente del campo `taxes_id` nativo por línea, que se oculta de la grilla).
- IVA Percibido (1%) = autosugerido cuando el subtotal con IVA supera $100, pero editable manualmente vía checkbox (`iva_percibido_check`).
- Total = subtotal con IVA + IVA percibido.

Este enfoque evita por completo el problema de sincronización servidor/cliente: los totales se ven correctos desde la primera línea de producto agregada, sin necesidad de tocar un segundo campo como workaround. 

## Consequences

### Positivas:
- **Flujo de caja simplificado:** el encargado de compras negocia y anota abonos parciales sin fricción contable, reflejando cómo realmente opera la farmacia con sus proveedores.
- **Trazabilidad diferida pero completa:** la Factura de Proveedor y su pago siguen generándose y quedando reconciliados en Contabilidad, solo que en el momento correcto (100% abonado) y en un solo paso.
- **Totales siempre correctos en pantalla:** el widget cliente elimina la clase entera de bugs de "$0.00 hasta tocar otro campo", sin recurrir a workarounds que introducen otros efectos secundarios (como la sobrescritura de precio).

### Negativas / Trade-offs:
- **Lógica de negocio duplicada en el cliente:** el cálculo de Subtotal/Descuento/IVA/Total vive ahora en JavaScript (OWL) además de (potencialmente) en Python, por lo que cualquier cambio futuro a la fórmula de IVA o descuento debe actualizarse en ambos lugares o se corre el riesgo de que diverjan.
- **Ausencia temporal de control contable durante los abonos:** mientras no se genera la Factura Final, los montos abonados no existen en los libros contables ni en los reportes financieros nativos de Odoo, solo en el registro informal `purchase.order.abono`.
- **Integración formal con otros módulos:** estas funcionalidades fueron creadas antes de sus dependencias requeridas por lo que su integración deberá comprobarse rigurosamente para evitar fallos en producción.
