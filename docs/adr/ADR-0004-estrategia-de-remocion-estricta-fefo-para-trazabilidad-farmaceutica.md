# [ADR-0004] Estrategia de Remoción Estricta FEFO para Trazabilidad Farmacéutica

## Status
Accepted

## Context
En el sector farmacéutico salvadoreño (regulado por la Dirección Nacional de Medicamentos - DNM), dispensar medicamentos vencidos o próximos a vencer representa una infracción sanitaria grave y un riesgo crítico para la salud pública de los pacientes. 

El modelo de inventario tradicional FIFO (First In, First Out) basa las salidas en la fecha de recepción física en bodega. En farmacia, un lote recibido recientemente de un distribuidor puede tener una fecha de caducidad más cercana que un lote recibido semanas atrás. Utilizar FIFO provocaría pérdidas financieras por vencimiento en estantería (mermas) y potencial dispensación indebida.

Este registro se relaciona directamente con [spec-7.2.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-7.2.1-control-stock-lotes-vencimientos.md), [spec-9.3.2](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-9.3.2-estrategia-salida-fefo-lotes.md) y [spec-11.1.2](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-11.1.2-pruebas-flujo-ventas-fefo-facturacion.md).

## Decision
Hemos decidido configurar e imponer la estrategia de remoción estricta **FEFO (First Expired, First Out / Primero en Vencer, Primero en Salir)** como la regla global predeterminada en todas las ubicaciones y categorías de productos farmacéuticos.

Configuraremos el módulo `stock` para que todo movimiento de salida (`stock.move.line`) priorice automáticamente la reserva de lotes ordenados ascendentemente por el campo `use_date` / `expiration_date` de `stock.lot`. Adicionalmente, el sistema bloqueará la reserva o dispensación de lotes cuya fecha de vencimiento sea menor o igual a la fecha actual.

## Consequences
### Positivas:
- **Cumplimiento Normativo Sanitario:** Garantiza el apego estricto a las regulaciones de la DNM evitando multas y sanciones legales.
- **Reducción Drástica de Mermas:** Minimiza el riesgo de que medicamentos caduquen en bodega o mostrador al rotar primero las existencias con vida útil más corta.
- **Automatización en Caja:** El cajero/farmacéutico no necesita calcular manualmente qué lote despachar; el sistema propone y reserva el lote óptimo en la orden de venta.

### Negativas / Trade-offs:
- **Rigidez Operativa:** Si físicamente un blíster o caja de lote más antiguo está en el fondo del estante, el operador debe buscarlo para coincidir con la sugerencia del sistema, o realizar una reasignación manual justificada.
- **Obligatoriedad de Registro Exhaustivo en Recepción:** Cada recepción de compra exige ingresar obligatoriamente número de lote y fecha de vencimiento; omitir estos datos bloquea el flujo de entrada al inventario.
