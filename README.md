# Farmacia Caryvil ERP

Sistema integral de gestión de recursos empresariales (ERP) especializado para **Farmacia Caryvil**, desarrollado sobre **Odoo 17.0 Community Edition**, **Python 3.10+** y **PostgreSQL 16**.

---

## 📁 Estructura del Proyecto

El repositorio sigue una arquitectura modular y desacoplada bajo metodología **Spec-Driven Development (SDD)**, centralizando la infraestructura dentro del directorio `infra/`:

```text
caryvil-erp/
├── .github/                      # Automatización CI/CD
│   └── workflows/
│       └── ci-cd.yml             # Pipeline de Linting, Testing, Build Docker y Deploy
├── custom_addons/                # 📦 Aplicación y Módulos Farmacéuticos
│   └── caryvil_erp/              # Módulo central de extensión de negocio
│       ├── controllers/          # Endpoints HTTP y rutas web
│       ├── data/                 # Datos maestros, categorías fiscales e inicializaciones
│       ├── demo/                 # Datos de prueba para entornos de desarrollo
│       ├── models/               # Modelos ORM extendidos (Clientes, Productos, Lotes, etc.)
│       ├── reports/              # Plantillas QWeb de tickets y órdenes de compra
│       ├── security/             # Grupos de seguridad y reglas de acceso ACL
│       ├── static/               # Assets estáticos (SCSS, JS, imágenes de branding)
│       ├── tests/                # Suite de pruebas automatizadas (TransactionCase)
│       ├── views/                # Vistas XML (Formularios, Árboles, Menús de navegación)
│       ├── wizards/              # Asistentes interactivos de recepción y conteo
│       ├── __init__.py           # Enrutamiento de paquetes Python
│       └── __manifest__.py       # Manifiesto y dependencias del addon
├── docs/                         # 📚 Documentación Técnica y de Gestión
│   ├── adr/                      # Architecture Decision Records (ADRs)
│   └── gestion/                  # Planificación y alcance (EDT/WBS)
├── infra/                        # 🛠️ Infraestructura Desacoplada
│   ├── compose/                  # Orquestación de contenedores multi-servicio
│   │   ├── docker-compose.yml
│   │   └── docker-compose.override.yml.example
│   ├── config/                   # Configuración del servidor Odoo
│   │   └── odoo.conf             # Parámetros de ejecución y límites de recursos
│   ├── docker/                   # Definición de contenedores y runtime
│   │   ├── Dockerfile            # Imagen base optimizada de Odoo 17
│   │   └── entrypoint.sh         # Script de inicio y conexión con base de datos
│   └── terraform/                # Infraestructura como Código (IaC) para Render
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       ├── versions.tf
│       └── terraform.tfvars.example
├── specs/                        # 📋 Ecosistema SDD (40 especificaciones detalladas)
│   └── spec-plan.md              # Plan maestro de especificaciones
├── .dockerignore                 # Exclusiones de contexto Docker
├── .gitignore                    # Exclusiones de control de versiones Git
├── requirements.txt              # Dependencias de Python fijadas
└── README.md                     # Guía principal del repositorio
```

---

## 🚀 Inicio Rápido en Entorno Local

### Prerrequisitos
- [Docker](https://www.docker.com/) y [Docker Compose](https://docs.docker.com/compose/) v2.0+
- [Git](https://git-scm.com/)

### 1. Clonar el repositorio
```bash
git clone https://github.com/MelissaFloresA/Odoo_ERP_Farmacia.git caryvil-erp
cd caryvil-erp
```

### 2. Iniciar los servicios con Docker Compose
```bash
docker compose -f infra/compose/docker-compose.yml up -d --build
```

### 3. Acceder al sistema
Una vez que los contenedores estén en estado `healthy`:
- **Interfaz Web de Odoo:** [http://localhost:8069](http://localhost:8069)
- **Base de Datos por defecto:** `caryvil_dev`
- **Usuario administrador:** `admin`

### 4. Monitoreo de logs
```bash
docker compose -f infra/compose/docker-compose.yml logs -f web
```

---

## 🧪 Pruebas Automatizadas y Calidad de Código

### Ejecución de Linter (Flake8):
```bash
flake8 custom_addons/caryvil_erp
```

### Ejecución del Suite de Tests de Odoo:
```bash
docker compose -f infra/compose/docker-compose.yml exec web odoo --test-enable -i caryvil_erp --stop-after-init -d caryvil_dev
```

---

## 📄 Metodología y Documentación
- **Especificaciones Funcionales:** Consulta [specs/spec-plan.md](specs/spec-plan.md) para el catálogo de requerimientos.
- **Decisiones de Arquitectura:** Consulta [docs/adr/README.md](docs/adr/README.md) para los registros ADR inmutables.
- **Licencia:** LGPL-3.0.
