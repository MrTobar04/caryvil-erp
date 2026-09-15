# [ADR-0003] Arquitectura Modular de Extensión sin Bifurcación (Módulo Único caryvil_erp)

## Status
Accepted

## Context
Al personalizar un ERP monolítico como Odoo, existen dos enfoques principales: bifurcar (hacer fork) el código fuente del núcleo modificando archivos base directamente, o mantener el núcleo intacto e implementar todas las reglas de negocio, modelos, campos extendidos, vistas y seguridad dentro de un módulo personalizado desacoplado.

Bifurcar el código base genera una deuda técnica inmanejable, impidiendo la actualización de parches de seguridad de Odoo, dificultando la migración entre versiones menores/mayores y violando las directrices de Spec-Driven Development.

Este registro se relaciona directamente con [spec-2.1.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-2.1.1-estructura-modulo-caryvil-erp.md), [spec-2.2.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-2.2.1-definicion-roles-usuarios.md), [spec-2.2.2](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-2.2.2-reglas-acceso-seguridad-modelos.md) y [spec-7.1.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-7.1.1-catalogo-categorizacion-medicamentos.md).

## Decision
Hemos decidido implementar una **arquitectura de extensión estricta sin bifurcación (No-Fork Architecture)** concentrada en un módulo principal denominado `caryvil_erp`.

Extenderemos los modelos estándar de Odoo (`res.partner`, `product.template`, `product.product`, `stock.lot`, `purchase.order`, `sale.order`, `account.move`) utilizando exclusivamente herencia clásica de Python (`_inherit = '...'`) y herencia de vistas XML mediante XPath (`<xpath expr="..." position="...">`), asegurando que el código fuente de Odoo se mantenga 100% puro e inalterado.

## Consequences
### Positivas:
- **Facilidad de Actualización y Parches:** Las actualizaciones de seguridad de Odoo se pueden aplicar sin riesgo de sobrescribir personalizaciones locales.
- **Aislamiento de Lógica Farmacéutica:** Toda la lógica de negocio, validaciones fiscales salvadoreñas y campos específicos reside en un único repositorio auditable.
- **Portabilidad:** El módulo puede ser empaquetado, instalado o desinstalado de manera limpia a través del gestor de aplicaciones de Odoo.

### Negativas / Trade-offs:
- **Sobrecarga de Especificidad en Selectores XPath:** Las vistas heredadas dependen de selectores XPath que pueden romperse si la estructura de vistas de Odoo sufre cambios en futuras versiones.
- **Acoplamiento de Dominio en Módulo Único:** Concentrar todas las extensiones (ventas, compras, inventario, reportes) en `caryvil_erp` simplifica el despliegue para una microempresa, pero reduce la granularidad de despliegue independiente entre áreas funcionales.
