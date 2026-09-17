# [ADR-0013] Datos Semilla Operativos y Lotes de Demostración

## Status
Accepted

## Context
Para permitir la validación funcional, pruebas de aceptación por parte del usuario (UAT) y demostraciones operativas completas del ERP de Farmacia Caryvil, se requiere poblar la base de datos con un conjunto de datos realista de productos, clientes, proveedores y saldos de existencias por lote.

La carga manual individual de productos y lotes durante demostraciones resulta propensa a omisiones y ralentiza el proceso de prueba de reglas complejas como FEFO y alertas de vencimiento en el Dashboard.

Este registro se relaciona directamente con [spec-10.2.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-10.2.1-datos-semilla-operativos.md), [spec-5.1.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-5.1.1-gestion-perfil-clientes.md), [spec-6.1.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-6.1.1-directorio-proveedores.md), [spec-7.1.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-7.1.1-catalogo-categorizacion-medicamentos.md), [spec-7.2.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-7.2.1-control-stock-lotes-vencimientos.md) y [spec-10.1.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-10.1.1-datos-semilla-maestros.md).

## Decision
Hemos decidido implementar el empaquetado de datos semilla de demostración (*Operational Demo Data*) en el directorio `custom_addons/caryvil_erp/demo/`:

1. **Declaración en Manifiesto:** Declarar los archivos XML demo en la clave `'demo': [...]` del manifiesto `__manifest__.py` para que solo se carguen cuando la base de datos esté configurada en modo demostración/desarrollo.
2. **Catálogo de 25 Medicamentos con EAN-13:** Registrar 25 medicamentos (`demo_medicines_data.xml`) cubriendo todas las familias terapéuticas con códigos de barras EAN-13 válidos, seguimiento activado por lote (`tracking = 'lot'`), costos de compra y precios de venta al público.
3. **Proveedores y Clientes de Muestra:** Registrar 4 laboratorios/droguerías salvadoreñas (`demo_vendors_data.xml`) y 10 clientes con formato sintáctico de DUI salvadoreño válido (`demo_customers_data.xml`).
4. **Lotes de Prueba para FEFO y Alertas:** Cargar lotes de existencias (`demo_inventory_stock_data.xml`) clasificados en vencimiento crítico (<30 días), vencimiento medio (31-60 días) y largo plazo (2027-2028).

## Consequences
### Positivas:
- **Demostración Operativa Inmediata:** Permite simular de inmediato órdenes de compra, recepciones, ventas en mostrador y reportes sin configuración manual.
- **Validación de FEFO y Dashboard:** Proveer lotes con fechas de vencimiento cercanas permite verificar el funcionamiento de las sugerencias FEFO y los widgets del dashboard.
- **Aislamiento en Producción:** La separación en el bloque `'demo'` previene la contaminación de bases de datos de producción reales.

### Negativas / Trade-offs:
- **Mantenimiento de IDs de Referencia:** Los archivos demo requieren mantener referencias exactas a las categorías e impuestos cargados en los datos semilla maestros (`SPEC-10.1.1`).
