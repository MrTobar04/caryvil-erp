# [ADR-0002] Aprovisionamiento de Infraestructura con Terraform en Render y Pipeline CI/CD con GitHub Actions

## Status
Accepted

## Context
El despliegue del entorno de producción y staging del ERP requiere repetibilidad, auditoría de configuración y minimización de errores manuales en la nube. A la vez, el proyecto debe mantenerse dentro de un esquema de costos predecible y accesible para una microempresa, descartando la complejidad y costo de grandes proveedores como AWS ECS/EKS o Google Cloud Platform para la primera etapa.

Se necesita un flujo automatizado que construya las imágenes de contenedor de Odoo, ejecute pruebas automáticas y despliegue las actualizaciones de infraestructura y software de manera confiable ante cada merge a la rama principal.

Este registro se relaciona directamente con [spec-1.2.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-1.2.1-aprovisionamiento-render-terraform.md), [spec-1.2.2](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-1.2.2-gestion-variables-entorno-secretos.md) y [spec-1.3.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-1.3.1-pipeline-ci-cd-github-actions.md).

## Decision
Hemos decidido utilizar **Terraform** mediante el provider oficial de Render (`render-oss/render`) para aprovisionar declarativamente todos los recursos en la nube (Web Service Dockerizado para Odoo + Base de Datos Gestionada PostgreSQL 16 con discos persistentes).

Implementaremos un pipeline de **GitHub Actions** que ejecuta análisis estático (flake8), pruebas unitarias/integración en contenedor efímero, construye y publica la imagen Docker en GitHub Packages (GHCR), y dispara el webhook de despliegue en Render de manera continua.

## Consequences
### Positivas:
- **Infraestructura como Código (IaC):** La topología completa de servidores, variables de entorno no sensibles y discos está versionada en Git.
- **Despliegues Libres de Fricción:** El equipo entrega valor continuo haciendo push a `main`, sin necesidad de ingresar por SSH ni configurar servidores manualmente.
- **Trazabilidad y Pruebas Previas al Despliegue:** Ninguna versión con fallos en la suite de pruebas unitarias o errores de sintaxis llega al entorno productivo.

### Negativas / Trade-offs:
- **Manejo de Secretos en Estado de Terraform:** Requiere disciplina estricta para sincronizar variables sensibles mediante GitHub Secrets y Render Dashboard sin exponerlas en el `terraform.tfstate`.
- **Límites de Concurrencia en Capa Render:** Las instancias estándar de Render tienen capacidades de auto-escalado horizontal limitadas para cargas masivas no contempladas en el plan básico.
- **Dependencia de Proveedor Específico:** El provider de Terraform está fuertemente acoplado a la API de Render; una migración a otro cloud provider requerirá reescribir los módulos HCL.
