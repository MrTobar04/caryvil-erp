# Arquitectura y Flujo de Despliegue de Farmacia Caryvil ERP

## 1. Visión General

El proceso de despliegue de **Farmacia Caryvil ERP** implementa una canalización desacoplada y automatizada de Integración Continua y Despliegue Continuo (CI/CD), acompañada de Infraestructura como Código (IaC) gestionada con **Terraform** sobre el proveedor de nube **Render**.

> [!NOTE]
> **Entorno de Producción/Dev:** [https://caryvil-erp-dev.onrender.com](https://caryvil-erp-dev.onrender.com)
> **Registro de Contenedores:** GitHub Container Registry (`ghcr.io/mrtobar04/caryvil-erp`)

---

## 2. Diagrama de Contenedores de la Infraestructura (C4Container)

El siguiente diagrama representa los límites del sistema, servicios web, bases de datos y la orquestación de despliegue automatizado.

```mermaid
C4Container
  title Diagrama de Contenedores - Arquitectura de Despliegue Farmacia Caryvil ERP

  Person(developer, "Desarrollador / DevOps", "Realiza commits, PRs y libera código en el repositorio Git")
  Person(user, "Usuario Final / Farmacéutico", "Accede al sistema ERP a través del navegador web")

  System_Boundary(github_platform, "Ecosistema GitHub") {
    Container(repo, "Repositorio Git", "GitHub", "Almacena código fuente, manifiestos HCL y workflows")
    Container(ci_pipeline, "CI Pipeline (ci-validation)", "GitHub Actions", "Ejecuta linters, validación HCL, XML y build de prueba")
    Container(cd_pipeline, "CD Pipeline (cd-deploy)", "GitHub Actions", "Construye imagen Docker, publica en GHCR y dispara webhook")
    Container(ghcr, "Container Registry (GHCR)", "OCI / Docker Registry", "Almacena imágenes de Docker versionadas")
  }

  System_Boundary(render_platform, "Plataforma Render (Nube)") {
    Container(web_service, "Servicio Web Odoo 17", "Docker Container / Odoo 17 CE", "Ejecuta la aplicación ERP Farmacia Caryvil")
    ContainerDb(postgres_db, "Base de Datos PostgreSQL 16", "Render Managed Postgres", "Persiste datos de inventario, ventas y configuración Odoo")
  }

  Rel(developer, repo, "Push de código / Pull Request", "Git/HTTPS")
  Rel(repo, ci_pipeline, "Dispara análisis en PR / ramas dev")
  Rel(repo, cd_pipeline, "Dispara despliegue en push a main")
  Rel(cd_pipeline, ghcr, "Publica imagen caryvil-erp:latest", "Docker Push / HTTPS")
  Rel(cd_pipeline, web_service, "Invoca Deploy Webhook", "HTTP POST")
  Rel(web_service, ghcr, "Descarga imagen actualizada", "Docker Pull / HTTPS")
  Rel(web_service, postgres_db, "Conexión ORM / Consultas SQL", "TCP 5432 / TLS")
  Rel(user, web_service, "Acceso a la interfaz ERP", "HTTPS")
```

---

## 3. Infraestructura como Código (IaC con Terraform)

El aprovisionamiento de recursos en la nube se gestiona de forma declarativa mediante **Terraform** en la ruta `infra/terraform/`.

### Componentes Declarados (`main.tf`):
1. **Base de Datos Gestionada (`render_postgres.caryvil_db`):**
   - Motor: PostgreSQL 16.
   - Plan: Free / Región: Oregon (`us-west`).
2. **Servicio Web en Contenedor (`render_web_service.caryvil_odoo`):**
   - Origen de Runtime: Imagen Docker de GHCR (`ghcr.io/mrtobar04/caryvil-erp:latest`).
   - Inyección de Variables de Entorno:
     - `HOST`: Hostname privado interno de la BD extraído dinámicamente.
     - `DB_PORT`: Puerto 5432 (diferenciado del puerto reservado por Render para HTTP).
     - `USER` / `PASSWORD`: Credenciales provistas dinámicamente por la BD de Render.
     - `DB_NAME`: Nombre de la base de datos operativa (`caryvil_dev`).
     - `PROXY_MODE`: `True` para el funcionamiento correcto tras el Reverse Proxy de Render.
     - `ODOO_UPDATE_MODULES`: `caryvil_erp` para forzar la actualización idempotente de esquemas ORM en el arranque.

### Comandos de Gestión Terraform:
```bash
# Inicializar proveedores y backend
terraform -chdir=infra/terraform init

# Validar sintaxis y formato
terraform -chdir=infra/terraform fmt
terraform -chdir=infra/terraform validate

# Planificar y aplicar cambios de infraestructura
terraform -chdir=infra/terraform plan
terraform -chdir=infra/terraform apply
```

---

## 4. Diagrama de Despliegue (C4Deployment)

Representa la topología física y lógica de los nodos de infraestructura en ejecución.

```mermaid
C4Deployment
  title Diagrama de Despliegue - Entorno de Producción en Render

  Deployment_Node(github_cloud, "GitHub Infrastructure", "Cloud / SaaS") {
    Deployment_Node(actions_runner, "GitHub Actions Runner", "Ubuntu Latest") {
      Container(docker_builder, "Docker Buildx Agent", "Docker CLI", "Construye y empaqueta la imagen Odoo")
    }
    Deployment_Node(registry_node, "GitHub Container Registry", "GHCR") {
      Container(image_store, "caryvil-erp:latest", "Docker OCI Image", "Imagen de producción optimizada")
    }
  }

  Deployment_Node(render_cloud, "Render Cloud Infrastructure", "Region: Oregon (us-west)") {
    Deployment_Node(web_node, "Web Service Environment", "Linux Container Runtime") {
      Container(odoo_container, "Contenedor Odoo 17 CE", "Python 3.10 Runtime", "Servicio web ERP (Puerto HTTP 8069)")
    }
    Deployment_Node(db_node, "Managed Database Instance", "PostgreSQL 16 Engine") {
      ContainerDb(postgres_instance, "Instancia PostgreSQL", "PostgreSQL 16", "Base de datos relacional y esquemas ORM")
    }
  }

  Rel(docker_builder, image_store, "Publica imagen compilada", "HTTPS / Docker Registry API")
  Rel(odoo_container, image_store, "Pull de imagen en redespliegue", "HTTPS / OCI")
  Rel(odoo_container, postgres_instance, "Conexión de BD sobre red privada interna", "TCP 5432")
```

---

## 5. Diagrama Dinámico de la Canalización CI/CD (C4Dynamic)

Detalla la secuencia numerada de eventos que ocurren desde que un desarrollador publica un cambio hasta la verificación de salud del servicio.

```mermaid
C4Dynamic
  title Diagrama Dinámico - Flujo de Ejecución CI/CD y Despliegue

  Person(dev, "Desarrollador", "Publica commit en la rama main")
  Container(actions, "GitHub Actions (cd-deploy)", "Workflow Runner", "Orquestador de CD")
  Container(ghcr_registry, "GHCR Registry", "Container Registry", "Depósito de imágenes")
  Container(render_hook, "Render Webhook Service", "API Endpoint", "Gestor de redespliegues")
  Container(odoo_app, "Odoo 17 Web Service", "Render Web Service", "Runtime ERP")
  ContainerDb(db_system, "PostgreSQL 16", "Render Postgres", "Base de datos ERP")

  Rel(dev, actions, "1. Git Push a rama main", "HTTPS / Git")
  Rel(actions, ghcr_registry, "2. Compila y publica imagen Docker", "Docker Push / GHCR")
  Rel(actions, render_hook, "3. Emite solicitud POST al Deploy Webhook", "HTTP POST")
  Rel(render_hook, odoo_app, "4. Inicia descarga y reinicio de contenedor", "Internal Event")
  Rel(odoo_app, ghcr_registry, "5. Descarga caryvil-erp:latest", "Docker Pull")
  Rel(odoo_app, db_system, "6. Ejecuta entrypoint.sh y migra módulos (-u caryvil_erp)", "TCP 5432")
  Rel(actions, odoo_app, "7. Realiza sondeo HTTP (Health Check) en URL pública", "HTTPS GET")
```

---

## 6. Variables y Secretos Requeridos en GitHub Actions

Para asegurar la ejecución correcta de las canalizaciones CI/CD, el repositorio de GitHub debe configurar los siguientes secretos (`Settings > Secrets and variables > Actions`):

| Secreto / Variable | Tipo | Descripción | Obligatorio |
|-------------------|------|-------------|-------------|
| `GITHUB_TOKEN` | Nativo | Token automático de GitHub para autenticar y publicar en GHCR | Sí (Automático) |
| `RENDER_DEPLOY_HOOK_URL` | Secret | URL del webhook de despliegue generado por Render para el Web Service | Sí |
| `RENDER_SERVICE_URL` | Secret / Var | URL pública del servicio desplegado (`https://caryvil-erp-dev.onrender.com`) | Sí (Opcional / Fallback nativo) |

---

## 7. Estrategia de Resiliencia y Mantenibilidad

- **Idempotencia de Base de Datos:** Cada arranque de contenedor invoca `entrypoint.sh`, el cual evalúa `ODOO_UPDATE_MODULES`. Si la variable está presente, ejecuta la actualización del módulo `caryvil_erp`, asegurando que nuevos campos o vistas se sincronicen automáticamente sin requerir intervención manual.
- **Concurrencia Controlada:** El pipeline `cd-deploy.yml` configura `cancel-in-progress: false` para evitar abortar despliegues en curso, garantizando la consistencia de las imágenes publicadas.
- **Recuperación en Capa Gratuita:** El paso final del pipeline incluye un algoritmo de retardo progresivo (sondeo de hasta 12 intentos espaciados por 15 segundos) para mitigar falsos positivos producidos por el reinicio de instancias (*cold start*) en la capa gratuita de Render.
