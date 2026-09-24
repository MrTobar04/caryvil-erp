# [ADR-0016] Reglas de Acceso Granular y Seguridad a Nivel de Modelo y Registro en Farmacia Caryvil

## Status
Accepted

## Context
Tras la definición de la jerarquía de roles RBAC en [ADR-0015](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/docs/adr/ADR-0015-jerarquia-roles-y-grupos-seguridad-rbac.md) y [spec-2.2.1-definicion-roles-usuarios.md](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-2.2.1-definicion-roles-usuarios.md), Farmacia Caryvil requiere la parametrización exhaustiva de los permisos de acceso CRUD (Create, Read, Update, Delete) a nivel de modelo de datos (`ir.model.access.csv`) y la imposición de restricciones transaccionales a nivel de registro (`ir.rule` en `caryvil_security_rules.xml`).

El negocio farmacéutico exige:
1. **Inmutabilidad de datos fiscales e históricos:** Las facturas emitidas y publicadas (`posted`) y los albaranes validados (`done`) no deben ser modificados ni eliminados por personal operativo (cajeros o encargados de compras).
2. **Protección del catálogo de medicamentos y clientes:** Prevenir la eliminación accidental o no autorizada (`perm_unlink = 0`) de medicamentos y clientes por parte de cajeros y encargados de inventario, restringiendo la eliminación física exclusivamente al Administrador General.
3. **Aislamiento de sesiones de venta en mostrador:** Garantizar que los cajeros únicamente gestionen las ventas correspondientes a su usuario/sesión o ventas no asignadas.

Este registro formaliza las decisiones técnicas de [spec-2.2.2-reglas-acceso-seguridad-modelos.md](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-2.2.2-reglas-acceso-seguridad-modelos.md).

## Decision
Hemos implementado una arquitectura de seguridad de dos niveles dentro de `custom_addons/caryvil_erp/security/`:

1. **Control de Acceso a Nivel de Modelo (ACL - `ir.model.access.csv`):**
   - **`product.template` / `product.product`:** Cajeros tienen solo lectura (`1,0,0,0`), Encargados de Inventario tienen lectura/escritura/creación (`1,1,1,0`), Administrador tiene control total (`1,1,1,1`).
   - **`res.partner`:** Cajeros y Encargados tienen permiso de lectura, escritura y creación (`1,1,1,0`) para registrar pacientes y clientes en mostrador, reservando la eliminación (`1,1,1,1`) exclusivamente al Administrador.
   - **`sale.order` / `account.move`:** Cajeros pueden emitir y consultar transacciones (`1,1,1,0`), sin permisos de eliminación física.

2. **Reglas de Seguridad a Nivel de Registro (`ir.rule` en `caryvil_security_rules.xml`):**
   - **`rule_caryvil_sale_order_cashier`:** Filtra las órdenes de venta visibles para el Cajero a `['|', ('user_id', '=', user.id), ('user_id', '=', False)]`.
   - **`rule_caryvil_posted_invoices_readonly` & `rule_caryvil_invoices_cashier_write_draft`:** Restringe la modificación de facturas para cajeros exclusivamente a estados de borrador (`['draft', 'cancel']`), garantizando que toda factura publicada (`posted`) quede en modo solo lectura.
   - **`rule_caryvil_sale_order_unlink_draft_only`:** Bloquea la eliminación de órdenes de venta confirmadas para usuarios no administradores.
   - **`rule_caryvil_stock_picking_unlink_non_done`:** Bloquea la eliminación de albaranes de recepción en estado validado (`done`) para el rol de inventario.

3. **Carga Segura con `noupdate="1"`:**
   - Las reglas de registro se cargan con la bandera `noupdate="1"` para permitir personalizaciones locales seguras sin ser sobreescritas en migraciones estándar.

## Consequences
### Positivas:
- **Cumplimiento ISO-27001:** Protección de la integridad y trazabilidad de registros contables, de inventario y transaccionales.
- **Seguridad en Profundidad:** El motor ORM de Odoo evalúa automáticamente tanto las listas de control de acceso (ACLs) como las reglas de registro SQL en cada operación ORM (`create`, `write`, `unlink`, `search`).
- **Resiliencia Operativa:** Los cajeros pueden atender y registrar clientes al vuelo sin riesgo de borrar el historial de pacientes ni el catálogo de precios o medicamentos.

### Negativas / Trade-offs:
- **Sobrecarga de Evaluación SQL:** Cada consulta de búsqueda o lectura a modelos protegidos por `ir.rule` añade cláusulas `WHERE` adicionales evaluadas en la base de datos PostgreSQL.
