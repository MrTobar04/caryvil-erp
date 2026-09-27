# Índice de Registros de Decisiones de Arquitectura (ADR) - Farmacia Caryvil ERP

Este directorio contiene los **Architecture Decision Records (ADR)** que formalizan las decisiones técnicas, arquitectónicas y metodológicas más trascendentes tomadas durante el diseño e implementación del ERP para Farmacia Caryvil, de acuerdo con la metodología Spec-Driven Development (SDD) y el estándar estipulado en `.agents/rules/adr-writter.md`.

---

## Registro de Decisiones

| ID | Título | Estado | Fecha | Especificaciones Relacionadas |
|---|---|:---:|:---:|---|
| [ADR-0001](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/docs/adr/ADR-0001-adopcion-odoo-17-community-y-postgresql-16.md) | Adopción de Odoo 17.0 Community y PostgreSQL 16 como Plataforma ERP Base | `Accepted` | 2026-09-14 | `spec-1.1.1`, `spec-1.1.2`, `spec-2.1.1` |
| [ADR-0002](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/docs/adr/ADR-0002-aprovisionamiento-iac-terraform-en-render-con-github-actions.md) | Aprovisionamiento de Infraestructura con Terraform en Render y CI/CD con GitHub Actions | `Accepted` | 2026-09-14 | `spec-1.2.1`, `spec-1.2.2`, `spec-1.3.1` |
| [ADR-0003](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/docs/adr/ADR-0003-arquitectura-modular-de-extension-sin-bifurcacion-modulo-caryvil-erp.md) | Arquitectura Modular de Extensión sin Bifurcación (Módulo Único caryvil_erp) | `Accepted` | 2026-09-14 | `spec-2.1.1`, `spec-2.2.1`, `spec-2.2.2`, `spec-7.1.1` |
| [ADR-0004](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/docs/adr/ADR-0004-estrategia-de-remocion-estricta-fefo-para-trazabilidad-farmaceutica.md) | Estrategia de Remoción Estricta FEFO para Trazabilidad Farmacéutica | `Accepted` | 2026-09-14 | `spec-7.2.1`, `spec-9.3.2`, `spec-11.1.2` |
| [ADR-0005](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/docs/adr/ADR-0005-esquema-de-facturacion-simple-y-validacion-fiscal-salvadorena.md) | Esquema de Facturación Simple y Validación Fiscal Salvadoreña | `Accepted` | 2026-09-14 | `spec-3.3.1`, `spec-5.1.1`, `spec-9.2.1`, `spec-11.1.3` |
| [ADR-0006](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/docs/adr/ADR-0006-modelo-de-fraccionamiento-y-unidades-de-medida-farmaceuticas.md) | Modelo de Fraccionamiento y Unidades de Medida Farmacéuticas | `Accepted` | 2026-09-14 | `spec-7.1.2`, `spec-8.2.1`, `spec-9.1.1` |
| [ADR-0007](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/docs/adr/ADR-0007-estrategia-de-testing-automatizado-con-odoo-test-framework.md) | Estrategia de Testing Automatizado con Odoo Test Framework en Contenedores Efímeros | `Accepted` | 2026-09-14 | `spec-1.3.1`, `spec-11.1.1`, `spec-11.1.2`, `spec-11.1.3` |
| [ADR-0008](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/docs/adr/ADR-0008-gestion-perfil-clientes-y-validacion-identidad-salvadorena.md) | Gestión del Perfil de Clientes y Validación de Identidad Salvadoreña (DUI) | `Accepted` | 2026-09-16 | `spec-5.1.1`, `spec-5.2.1`, `spec-9.2.1` |
| [ADR-0009](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/docs/adr/ADR-0009-busqueda-rapida-multicampo-e-indexacion-de-clientes-en-caja.md) | Búsqueda Rápida Multicampo e Indexación de Clientes en Caja | `Accepted` | 2026-09-16 | `spec-5.2.1`, `spec-5.1.1`, `spec-9.1.1` |
| [ADR-00010](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/docs/adr/ADR-00010-gestion-de-compras-con-abonos-y-totales-calculados-en-cliente.md) | Gestión de Órdenes de Compra con Abonos y Totales Calculados | `Accepted` | 2026-09-16 | `spec-8.1.1`, `spec-8.2.1`, `spec-8.2.2`, `spec-8.2.3`, `spec-3.3.2` |
| [ADR-0011](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/docs/adr/ADR-0011-historial-compras-y-trazabilidad-transaccional-clientes.md) | Historial de Compras y Trazabilidad Transaccional de Clientes | `Accepted` | 2026-09-16 | `spec-5.2.2`, `spec-5.1.1`, `spec-5.2.1`, `spec-9.1.1` |
| [ADR-0012](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/docs/adr/ADR-0012-parametrizacion-y-carga-de-datos-semilla-maestros.md) | Parametrización y Carga de Datos Semilla Maestros del Sistema | `Accepted` | 2026-09-16 | `spec-10.1.1`, `spec-2.1.1`, `spec-2.2.1`, `spec-7.1.1` |
| [ADR-0013](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/docs/adr/ADR-0013-datos-semilla-operativos-y-lotes-de-demostracion.md) | Datos Semilla Operativos y Lotes de Demostración | `Accepted` | 2026-09-16 | `spec-10.2.1`, `spec-5.1.1`, `spec-6.1.1`, `spec-7.1.1`, `spec-7.2.1`, `spec-10.1.1` |
| [ADR-0014](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/docs/adr/ADR-0014-desacoplamiento-precio-bruto-y-gestion-descuentos-proveedores.md) | Desacoplamiento de Precio Bruto y Gestión de Descuentos en Catálogo de Proveedores | `Accepted` | 2026-09-20 | `spec-6.2.1`, `spec-6.1.1`, `spec-8.1.1` |
| [ADR-0015](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/docs/adr/ADR-0015-jerarquia-roles-y-grupos-seguridad-rbac.md) | Jerarquía de Roles de Usuario y Grupos de Seguridad RBAC en Farmacia Caryvil | `Accepted` | 2026-09-21 | `spec-2.2.1`, `spec-2.2.2` |
| [ADR-0016](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/docs/adr/ADR-0016-reglas-acceso-y-seguridad-a-nivel-de-modelo-y-registro.md) | Reglas de Acceso Granular y Seguridad a Nivel de Modelo y Registro en Farmacia Caryvil | `Accepted` | 2026-09-21 | `spec-2.2.2`, `spec-2.2.1` |
| [ADR-0017](ADR-0017-estrategia-venta-mostrador-caryvil.md) | Estrategia de Venta de Mostrador y Cobro Unificado | `Accepted` | 2026-09-24 | `spec-9.1.1`, `spec-9.2.1`, `spec-9.3.1`, `spec-9.3.2`, `spec-11.1.2` |


---

## Ciclo de Vida de un ADR
Los ADRs son **inmutables**. Si una decisión arquitectónica cambia en el futuro, se creará un nuevo ADR con estado `Accepted` que marcará al registro previo como `Superseded by ADR-XXXX`.
