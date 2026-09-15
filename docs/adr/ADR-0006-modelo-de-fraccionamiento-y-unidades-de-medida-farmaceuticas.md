# [ADR-0006] Modelo de Fraccionamiento y Unidades de Medida Farmacéuticas

## Status
Accepted

## Context
En las farmacias comunitarias, las compras a laboratorios y distribuidores mayoristas se realizan comúnmente en cajas contenedoras (ej. caja de 100 tabletas o caja de 10 blísteres), pero la venta a pacientes en mostrador con frecuencia se realiza fraccionada por blíster o por tableta individual para ajustarse al tratamiento prescrito o a la capacidad económica del cliente.

Si se crean productos separados para la "Caja" y la "Tableta", se duplica el catálogo, se fragmenta la trazabilidad del lote y la fecha de caducidad, y se requiere un proceso manual de manufactura o desempaque para transferir existencias entre ambos códigos.

Este registro se relaciona directamente con [spec-7.1.2](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-7.1.2-gestion-unidades-medida-farmaceuticas.md), [spec-8.2.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-8.2.1-recepcion-mercaderia-registro-lotes.md) y [spec-9.1.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-9.1.1-procesamiento-transacciones-ventas.md).

## Decision
Hemos decidido utilizar el sistema nativo de **Categorías de Unidades de Medida (`uom.category` y `uom.uom`)** de Odoo con una única unidad de referencia base (la unidad indivisible: "Tableta", "Cápsula", "Mililitro" o "Unidad"), asociando las unidades de compra y presentación comercial ("Caja x 100", "Caja x 30", "Blíster x 10") mediante factores de conversión decimales exactos dentro del mismo producto (`product.template`).

Las compras pueden recibirse en Cajas y las ventas despacharse en Blísteres o Unidades; el motor de inventario de Odoo convierte automáticamente los movimientos al stock base y mantiene la integridad del mismo lote físico (`stock.lot`).

## Consequences
### Positivas:
- **Trazabilidad Unificada de Lotes:** El mismo lote cubre tanto la venta de la caja completa como de sus fracciones individuales, garantizando auditorías precisas.
- **Catálogo Limpio:** No existe duplicidad de registros de productos en la base de datos para distintas presentaciones de un mismo fármaco.
- **Costeo Preciso:** El costo unitario promedio ponderado se calcula sobre la unidad base indivisible, evitando distorsiones al fraccionar.

### Negativas / Trade-offs:
- **Complejidad en la Parametrización Inicial:** Requiere definir cuidadosamente la unidad de medida base y los factores multiplicadores al dar de alta cada medicamento; un error en el ratio distorsionará el inventario teórico.
- **Redondeos en Cantidades Decimales:** Operaciones con empaques no estándar requieren configurar la precisión decimal de las unidades de medida en Odoo (`decimal.precision`) para evitar discrepancias de fracciones.
