# [ADR-0001] Adopción de Odoo 17.0 Community y PostgreSQL 16 como Plataforma ERP Base

## Status
Accepted

## Context
Farmacia Caryvil requiere un sistema de planificación de recursos empresariales (ERP) para gestionar sus operaciones comerciales, compras a laboratorios, control de inventario farmacéutico, facturación de mostrador y administración de clientes. El proyecto cuenta con un límite de presupuesto de infraestructura cero/mínimo durante la fase de desarrollo, un equipo reducido de desarrollo de software para el ciclo lectivo y una fecha de entrega límite estricta.

Desarrollar un sistema ERP desde cero requeriría modelar flujos contables, motores de inventario, seguridad por roles, ORM y generación de reportes, lo cual excede la capacidad temporal del equipo. Por otro lado, soluciones propietarias (SAP, Odoo Enterprise, NetSuite) implican costos de licenciamiento inviables para el perfil de microempresa farmacéutica.

Este registro se relaciona directamente con los requerimientos definidos en [spec-1.1.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-1.1.1-configuracion-entorno-docker.md), [spec-1.1.2](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-1.1.2-configuracion-servidor-odoo.md) y [spec-2.1.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-2.1.1-estructura-modulo-caryvil-erp.md).

## Decision
Hemos decidido adoptar **Odoo 17.0 Community Edition** ejecutado sobre **Python 3.10+** con **PostgreSQL 16** como la plataforma tecnológica y motor ERP central del sistema.

Utilizaremos el ecosistema modular nativo de Odoo (`base`, `sale`, `purchase`, `stock`, `account`) como infraestructura transaccional y construiremos un módulo de personalización dedicado denominado `caryvil_erp` para encapsular la lógica de negocio farmacéutica salvadoreña.

## Consequences
### Positivas:
- **Reducción del Time-to-Market:** Aprovechamiento inmediato de módulos maduros y auditados para ventas, compras, inventario valorizado y catálogo de contactos.
- **Cero Costo de Licenciamiento:** Odoo Community bajo licencia LGPLv3 elimina costos recurrentes por usuario o terminal.
- **Riqueza de ORM y Framework Web:** ORM robusto con control de concurrencia, transaccionalidad ACID en PostgreSQL 16 y renderizado QWeb nativo para reportes.
- **Extensibilidad:** Capacidad de extender modelos existentes mediante herencia sin modificar el código fuente base del framework.

### Negativas / Trade-offs:
- **Curva de Aprendizaje del Framework:** El equipo de desarrollo debe familiarizarse con la arquitectura interna de Odoo (ORM, vistas XML, controladores OWL, QWeb, decoradores `@api.depends`/`@api.onchange`).
- **Consumo de Recursos en Servidor:** La arquitectura de Odoo en Python requiere un mínimo de 1 GB a 2 GB de memoria RAM para ejecución estable con múltiples workers, limitando el uso de capas gratuitas mínimas sin swap.
- **Ausencia de Módulos Enterprise:** Características como contabilidad avanzada completa, escaneo de código de barras nativo de mobile y POS Enterprise no están disponibles de forma predeterminada, requiriendo implementaciones custom en el módulo local.
