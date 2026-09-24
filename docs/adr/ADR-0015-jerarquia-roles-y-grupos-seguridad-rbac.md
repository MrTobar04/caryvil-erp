# [ADR-0015] Jerarquía de Roles de Usuario y Grupos de Seguridad RBAC en Farmacia Caryvil

## Status
Accepted

## Context
Para la operación farmacéutica de Farmacia Caryvil se requiere un esquema de control de acceso basado en roles (Role-Based Access Control - RBAC) que garantice la separación de responsabilidades, la protección de información sensible (como costos de adquisición a laboratorios) y la inmutabilidad de registros históricos según el principio de mínimo privilegio de ISO-27001 (Annex A.9).

Los perfiles operativos del personal abarcan:
1. Personal de mostrador (Cajeros / Dependientes): atención rápida, consulta de existencias, facturación a consumidor final.
2. Encargado de compras e inventario: abastecimiento a droguerías, recepción con lote/vencimiento, catálogo y conteos de stock.
3. Propietaria / Administrador General: acceso completo a costos, anulaciones, métricas financieras y configuración.

Este registro formaliza la arquitectura de seguridad definida en [spec-2.2.1-definicion-roles-usuarios.md](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-2.2.1-definicion-roles-usuarios.md) y se complementa con [spec-2.2.2-reglas-acceso-seguridad-modelos.md](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-2.2.2-reglas-acceso-seguridad-modelos.md).

## Decision
Hemos decidido implementar una jerarquía de grupos de seguridad estricta en `security/caryvil_security.xml` agrupada bajo la categoría de módulo `module_category_caryvil_erp` ("Farmacia Caryvil"):

1. **`group_caryvil_cashier` (Cajero / Dependiente de Mostrador):**
   - Herencia: `base.group_user` (Usuario Interno).
   - Alcance: Atención en mostrador, emisión de factura simple, búsqueda de medicamentos y registro de clientes. Oculta menús de compras, costos y administración.

2. **`group_caryvil_inventory_purchases` (Encargado de Compras e Inventario):**
   - Herencia (*implied groups*): `group_caryvil_cashier`, `stock.group_stock_user`, `purchase.group_purchase_user`.
   - Alcance: Gestión de compras a proveedores, recepción de albaranes, control de lotes/vencimientos y ajustes de stock.

3. **`group_caryvil_manager` (Administrador / Propietario):**
   - Herencia (*implied groups*): `group_caryvil_inventory_purchases`, `stock.group_stock_manager`, `purchase.group_purchase_manager`, `sales_team.group_sale_manager`.
   - Alcance: Acceso irrestricto a costos, reportes de margen, configuración avanzada y administración de usuarios.

## Consequences
### Positivas:
- **Cumplimiento ISO-27001:** Separación clara de deberes y protección de datos confidenciales de proveedores y costos.
- **Herencia Transitiva:** Los usuarios administradores o encargados reciben automáticamente los privilegios de los niveles inferiores sin requerir asignaciones redundantes manuales.
- **Simplicidad Administrativa:** La interfaz de configuración de usuarios en Odoo expone una sola categoría clara ("Farmacia Caryvil") para gestionar los permisos de los empleados.

### Negativas / Trade-offs:
- **Acoplamiento de Grupos Nativos:** La herencia de grupos de Odoo (`stock.group_stock_user`, `purchase.group_purchase_user`) asume que los módulos nativos correspondientes están instalados como dependencias obligatorias en el manifiesto.
