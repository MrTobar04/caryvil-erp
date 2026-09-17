# [ADR-0012] Parametrización y Carga de Datos Semilla Maestros del Sistema

## Status
Accepted

## Context
Al inicializar la plataforma ERP de Farmacia Caryvil en un nuevo entorno (sea local en Docker o en producción en Render), se requiere que la base de datos cuente inmediatamente con la información corporativa, moneda oficial (USD), régimen fiscal de El Salvador (IVA 13%), catálogo de categorías terapéuticas, principios activos y usuarios por rol de seguridad sin necesidad de parametrización manual manual que introduzca inconsistencias.

El mecanismo de datos maestros de Odoo permite empaquetar archivos XML/CSV que alimentan automáticamente las tablas del sistema al momento de instalar el addon por primera vez.

Este registro se relaciona directamente con [spec-10.1.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-10.1.1-datos-semilla-maestros.md), [spec-2.1.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-2.1.1-estructura-modulo-caryvil-erp.md), [spec-2.2.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-2.2.1-definicion-roles-grupos-usuarios.md) y [spec-7.1.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-7.1.1-catalogo-categorizacion-medicamentos.md).

## Decision
Hemos decidido implementar el empaquetado de datos semilla maestros (*Master Seed Data*) dentro de `custom_addons/caryvil_erp/data/`:

1. **Protección mediante `noupdate="1"`:** Todos los registros semilla maestros se declaran con la directiva `<data noupdate="1">` para evitar que actualizaciones posteriores del addon (`-u caryvil_erp`) sobreescriban datos modificados operativamente.
2. **Empresa y Moneda Oficial:** Registrar la compañía "Farmacia Caryvil" (`company_data.xml`) vinculada a la moneda base USD (`base.USD`) y país El Salvador (`base.sv`).
3. **Régimen Fiscal Salvadoreño:** Cargar la configuración del impuesto IVA 13% para ventas (`tax_data.xml`).
4. **Catálogo Terapéutico y Principios Activos:** Cargar las 10 familias terapéuticas base (`pharmacy_categories_data.xml`) y el catálogo normalizado de principios activos (`active_ingredients_data.xml`) en `product.category`.
5. **Usuarios Semilla por Rol:** Configurar usuarios de demostración (`users_roles_data.xml`) asociados a los grupos de seguridad `group_caryvil_cajero`, `group_caryvil_compras_inventario` y `group_caryvil_admin`.

## Consequences
### Positivas:
- **Despliegue Inmediato (*Zero-Touch Setup*):** El sistema queda totalmente funcional y parametrizado desde la primera instalación del addon.
- **Consistencia Fiscal y Comercial:** Garantiza que los impuestos (IVA 13%) y moneda (USD) coincidan con el marco tributario salvadoreño.
- **Aislamiento de Actualizaciones:** La directiva `noupdate="1"` preserva los cambios realizados por los usuarios finales en producción.

### Negativas / Trade-offs:
- **Gestión de Credenciales en Producción:** Las cuentas de usuario semilla deben cambiar de contraseña obligatoriamente tras la instalación inicial en entornos públicos.
