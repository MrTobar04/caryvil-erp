# [ADR-0007] Estrategia de Testing Automatizado con Odoo Test Framework en Contenedores Efímeros

## Status
Accepted

## Context
Para asegurar la estabilidad de la lógica de negocio farmacéutica (FEFO, cálculo de impuestos, fraccionamiento de UoM, validaciones de documentos de identidad salvadoreños) y prevenir regresiones durante el desarrollo ágil, se requiere una suite de pruebas automatizada ejecutable localmente y en el pipeline de CI/CD.

Los tests que dependen de una base de datos estática persistente tienden a fallar por contaminación de datos residuales entre ejecuciones, o requieren costosos scripts de reseteo manual. Además, herramientas externas como Selenium/Playwright resultan lentas para validar reglas puras del ORM de Odoo.

Este registro se relaciona directamente con [spec-1.3.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-1.3.1-pipeline-ci-cd-github-actions.md), [spec-11.1.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-11.1.1-pruebas-flujo-compras-inventario.md), [spec-11.1.2](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-11.1.2-pruebas-flujo-ventas-fefo-facturacion.md) y [spec-11.1.3](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-11.1.3-pruebas-validaciones-datos-locales.md).

## Decision
Hemos decidido utilizar el framework de pruebas nativo de Odoo (**`odoo.tests.common.TransactionCase`** y **`SingleTransactionCase`**) como la herramienta estándar de pruebas unitarias y de integración del backend.

Las pruebas se ejecutarán mediante el comando `odoo-bin --test-enable -i caryvil_erp --stop-after-init` dentro de contenedores Docker efímeros creados dinámicamente en GitHub Actions con bases de datos PostgreSQL temporales en memoria / tempfs, garantizando que cada corrida de pruebas inicie desde un estado limpio y aislado.

## Consequences
### Positivas:
- **Aislamiento Total de Transacciones:** `TransactionCase` realiza rollback automático al finalizar cada método de test, impidiendo contaminación de estado entre pruebas.
- **Acceso Directo al ORM y Contexto:** Permite crear datos de prueba, validar métodos calculados, disparar wizards y simular flujos de compras/ventas directamente en Python sin sobrecarga HTTP.
- **Ejecución Automatizada en CI:** La suite corre de forma desatendida en GitHub Actions antes de autorizar cualquier pull request o despliegue a producción.

### Negativas / Trade-offs:
- **Tiempo de Inicialización del Entorno de Test:** Inicializar el entorno completo de Odoo (`--test-enable`) carga todos los módulos base (`base`, `mail`, `stock`, `account`), lo que toma entre 20 a 45 segundos por corrida en CI.
- **Limitación en Pruebas de Interfaz de Usuario:** `TransactionCase` valida lógica de modelos y controladores Python, pero no valida interacciones visuales en OWL del frontend sin el uso adicional de `HttpCase` o tours de JavaScript.
