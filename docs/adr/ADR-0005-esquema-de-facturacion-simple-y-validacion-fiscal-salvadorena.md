# [ADR-0005] Esquema de Facturación Simple y Validación Fiscal Salvadoreña

## Status
Accepted

## Context
El marco tributario de El Salvador administrado por el Ministerio de Hacienda exige que toda transacción comercial compute correctamente el Impuesto a la Transferencia de Bienes Muebles y a la Prestación de Servicios (IVA del 13%) y valide identificadores fiscales (DUI de 9 dígitos y NIT de 9 o 14 dígitos).

La integración completa con la API de Facturación Electrónica (DTE) de Hacienda implica procesos de certificación de emisor, firma digital con certificados X.509 y un API Gateway que exceden el alcance y plazo de la primera fase del proyecto. No obstante, la farmacia requiere emitir tickets térmicos físicos de 80mm y facturas simples legalmente consistentes con correlativos internos y desglose de IVA para sus clientes de mostrador.

Este registro se relaciona directamente con [spec-3.3.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-3.3.1-plantilla-reporte-factura-ticket.md), [spec-5.1.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-5.1.1-gestion-perfil-clientes.md), [spec-9.2.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-9.2.1-generacion-factura-simple.md) y [spec-11.1.3](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-11.1.3-pruebas-validaciones-datos-locales.md).

## Decision
Hemos decidido implementar un **esquema de facturación simple local** que maneja la tasa estándar de IVA (13%), retenciones aplicables y secuencias correlativas de documentos en Odoo (`account.move`), junto con un motor de validación sintáctica por expresiones regulares para DUI (`^\d{8}-\d{1}$`) y NIT (`^\d{4}-\d{6}-\d{3}-\d{1}$` o formato unificado de 9 dígitos).

Las impresiones de venta se realizarán mediante plantillas QWeb optimizadas para papel continuo térmico de 80mm (impresora POS). Se aplaza la interconexión directa con el webservice DTE de Hacienda para una fase posterior, dejando la estructura de datos preparada con campos de control (UUID, sello de recepción).

## Consequences
### Positivas:
- **Operación Ininterrumpida en Caja:** La generación de facturas y tickets no depende de la disponibilidad o latencia de servicios web externos del Ministerio de Hacienda.
- **Cumplimiento Tributario de Cálculo:** Los libros de ventas a consumidor final y el cálculo de débitos fiscales reflejan el 13% de IVA exacto sin inconsistencias de redondeo.
- **Velocidad de Impresión:** Reportes QWeb ligeros renderizados directamente en HTML/PDF para impresoras térmicas estándar.

### Negativas / Trade-offs:
- **Deuda Técnica para DTE Oficial:** La transición futura a DTE exigirá desarrollar un módulo puente de firma JSON/JWS y sincronización asíncrona con el Ministerio de Hacienda.
- **Manejo Manual de Contingencias Fiscales:** Las anulaciones de documentos y notas de crédito operan bajo control interno del ERP sin transmisión automática a entes reguladores.
