# [ADR-0008] Gestión del Perfil de Clientes y Validación de Identidad Salvadoreña (DUI)

## Status
Accepted

## Context
Farmacia Caryvil requiere formalizar el registro y seguimiento de su cartera de clientes en el ERP Odoo 17. En El Salvador, la identificación de personas naturales con fines comerciales y de comprobación fiscal se realiza mediante el Documento Único de Identidad (DUI), el cual consta de 9 dígitos numéricos en formato `00000000-0`.

El modelo estándar de contactos de Odoo (`res.partner`) maneja un único campo genérico `name` y no incluye validación de formato ni restricciones de unicidad para documentos de identidad nacionales de El Salvador. Esto originaba registros duplicados e inconsistencias de datos en la operación anterior.

Este registro se relaciona directamente con [spec-5.1.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-5.1.1-gestion-perfil-clientes.md), [spec-5.2.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-5.2.1-busqueda-rapida-clientes-caja.md) y [spec-9.2.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-9.2.1-generacion-factura-simple.md).

## Decision
Hemos decidido extender el modelo base `res.partner` en el módulo `caryvil_erp` mediante el modelo heredado `ResPartnerCustomer`:

1. **Campos de Identidad Salvadoreña:** Añadir `first_name` (Char), `last_name` (Char), `dui` (Char, size 10), `is_pharmacy_customer` (Boolean, default True) y autonumeración secuencial de referencia (`CL0001`, `CL0002`, ...).
2. **Validación Sintáctica y Autocorrección:** Implementar la validación con expresión regular `^\d{8}-\d{1}$` en el método `@api.constrains('dui')`. Si el usuario ingresa 9 dígitos continuos sin guion (`000000000`), el sistema autocompleta el guion canónico antes del dígito verificador.
3. **Restricción de Unicidad:** Imponer una restricción SQL a nivel de PostgreSQL (`_sql_constraints`) en la columna `dui` de `res.partner` para impedir la existencia de múltiples clientes con el mismo número de DUI.
4. **Sincronización Compuesta del Nombre:** Mantener sincronizado el campo estándar `name` a través de los eventos `@api.onchange('first_name', 'last_name')`.

## Consequences
### Positivas:
- **Calidad e Integridad de Datos:** Garantiza la unicidad y validez del DUI a nivel de base de datos y modelo ORM.
- **Estandarización de Nombres:** Evita discrepancias en el registro al separar nombres y apellidos para reportes y facturación.
- **Trazabilidad:** Código interno autogenerado (`CL0000`) para cada cliente registrado.

### Negativas / Trade-offs:
- **Flexibilidad en Transacciones Anónimas:** Para ventas de mostrador a clientes que no desean proporcionar DUI, se requiere el uso de un registro comodín ("Consumidor Final") sin DUI.
