# Diagrama C4 - Nivel 4: Despliegue (Deployment Diagram)

Este documento ilustra la arquitectura de infraestructura física y virtualizada donde se despliega **Farmacia Caryvil ERP**, abarcando tanto el entorno de desarrollo local orquestado con Docker Compose como la infraestructura cloud de producción aprovisionada en Render mediante Terraform.

## Diagrama de Despliegue C4

```mermaid
C4Deployment
  title Diagrama de Despliegue - Entornos Local y Producción (Render Cloud)

  Deployment_Node(clientDevice, "Dispositivo POS / PC", "Windows / Linux") {
    Deployment_Node(browserNode, "Navegador Web", "Chrome / Edge") {
      Container(clientSpa, "Cliente ERP", "OWL JS", "Interfaz de ventas y gestión.")
    }
  }

  Deployment_Node(githubCloud, "GitHub", "GitHub Actions & GHCR") {
    Deployment_Node(cicdRunner, "CI/CD Runner", "Ubuntu") {
      Container(cicdPipeline, "Pipeline CI/CD", "Actions", "Linting, tests y build de imagen.")
    }
    Deployment_Node(registryNode, "Registry GHCR", "ghcr.io") {
      Container(dockerImage, "Imagen Docker", "Odoo 17", "ghcr.io/mrtobar04/caryvil-erp:latest")
    }
  }

  Deployment_Node(renderCloud, "Render Cloud", "Región US West") {
    Deployment_Node(renderWebNode, "Web Service", "Docker Container") {
      Container(prodOdoo, "caryvil-web", "Odoo 17.0", "Servidor Odoo en producción.")
    }
    Deployment_Node(renderDbNode, "Managed DB", "Postgres 16") {
      ContainerDb(prodPostgres, "caryvil-postgres", "PostgreSQL", "Base de datos persistente.")
    }
  }

  Deployment_Node(localDockerHost, "Entorno Local", "Docker Compose") {
    Deployment_Node(localWebNode, "Web Local", "caryvil-web") {
      Container(devOdoo, "Odoo Dev", "Odoo 17.0", "Servidor local :8069.")
    }
    Deployment_Node(localDbNode, "DB Local", "caryvil-db") {
      ContainerDb(devPostgres, "Postgres Dev", "PostgreSQL", "BD local :5432.")
    }
  }

  Rel_R(clientSpa, prodOdoo, "Acceso usuario", "HTTPS:443")
  Rel_D(clientSpa, devOdoo, "Acceso dev", "HTTP:8069")

  Rel_D(cicdPipeline, dockerImage, "Publica imagen", "Docker Push")
  Rel_L(prodOdoo, dockerImage, "Descarga imagen", "Docker Pull")

  Rel_D(prodOdoo, prodPostgres, "Conexión interna", "TLS:5432")
  Rel_D(devOdoo, devPostgres, "Red bridge", "SQL:5432")
```

## Infraestructura como Código (IaC con Terraform)

El aprovisionamiento de la infraestructura en producción está automatizado mediante **Terraform** dentro del directorio `infra/terraform/`:

1. **`render_postgres.caryvil_db`**: Instancia gestionada de PostgreSQL 16 en Render con aprovisionamiento automatizado y almacenamiento persistente.
2. **`render_web_service.caryvil_odoo`**: Contenedor basado en la imagen inmutable de GHCR.
   - **Inyección de Secretos:** Configura `HOST`, `USER`, `PASSWORD`, `DB_NAME` y `ADMIN_PASSWORD` desde variables de entorno.
   - **Reverse Proxy:** Habilita `PROXY_MODE=True` para manejar de forma segura las terminaciones TLS.
   - **Actualización Automática:** Emplea `ODOO_UPDATE_MODULES=caryvil_erp` para aplicar migraciones de esquema (`ALTER TABLE`) de forma idempotente durante el arranque.

## Entorno Local (Docker Compose)

En local (`infra/compose/docker-compose.yml`), los servicios se comunican a través de la red `caryvil_network`:
- **`caryvil-db`**: Contenedor `postgres:16-alpine` con healthcheck activo.
- **`caryvil-web`**: Contenedor Odoo 17 con volumen montado para desarrollo ágil en `/mnt/extra-addons`.
