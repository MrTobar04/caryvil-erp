# SPEC-1.3.1: Pipeline CI/CD con GitHub Actions

## 1. Objective
Implementar el pipeline automatizado de Integración Continua y Despliegue Continuo (CI/CD) para el proyecto Caryvil ERP utilizando GitHub Actions. Este flujo de trabajo automatiza la verificación de sintaxis y estándares de código (Python, XML de Odoo, Terraform HCL), la compilación y prueba de la imagen Docker del sistema, y el despliegue automático hacia la infraestructura de Render tras la integración aprobada de cambios en la rama principal (`main`).

## 2. Scope
### 2.1. Included
* Creación de los archivos de flujo de trabajo en `.github/workflows/`:
  * `ci-validation.yml`: Validación de sintaxis en Pull Requests (Flake8, Black check, `yamllint`, `terraform fmt/validate`).
  * `cd-deploy.yml`: Compilación de la imagen Docker y disparo del despliegue en Render (mediante Terraform Apply o Render Deploy Hook) al realizar merge a la rama `main`.
* Configuración de matriz de ejecución con runners de Ubuntu (`ubuntu-latest`).
* Configuración del almacenamiento en caché (*cache*) de capas Docker y paquetes pip para acelerar la ejecución del pipeline.
* Notificación del estado de compilación y despliegue directamente en los Pull Requests de GitHub.

### 2.2. Not Included (Out of Scope)
* Creación de pruebas unitarias específicas de los módulos de negocio (cubierto en `Dominio 11`).
* Modificación de la arquitectura de contenedores Docker local (cubierto en `SPEC-1.1.1`).

## 3. Context and Restrictions
* **Context:** Asegura la calidad y estabilidad del código fuente antes de que llegue a producción, eliminando pasos manuales de despliegue y reduciendo el riesgo de caídas del sistema en Farmacia Caryvil.
* **Restrictions:**
  * Debe operar dentro de la cuota gratuita de minutos de GitHub Actions (2,000 minutos/mes para repositorios públicos o privados en free tier).
  * El tiempo total de ejecución de la suite CI/CD no debe superar los 8 minutos por corrida.
  * Ningún cambio puede ser desplegado a `main` sin haber superado previamente todas las etapas de validación de CI.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-1.1.1` (Configuración del Entorno Docker).
  * `SPEC-1.1.2` (Configuración del Servidor Odoo).
  * `SPEC-1.2.1` (Aprovisionamiento en Render con Terraform).
  * `SPEC-1.2.2` (Gestión de Variables de Entorno y Secretos).
* **Definition of Ready (DoR):**
  * [x] Repositorio Git configurado en GitHub con permisos de administrador.
  * [x] Secretos del repositorio (`RENDER_API_KEY`, `RENDER_OWNER_ID`, `RENDER_DEPLOY_HOOK_URL`) identificados.
  * [x] Estructura de carpetas base del proyecto confirmada.

## 5. Design (Implementation Details)
* **Architecture:**
  * **Pipeline Workflow Diagram:**
    ```
    [Pull Request / Push]
             │
             ▼
    ┌────────────────────────────────────────┐
    │  Job 1: Lint & Static Code Analysis    │
    │  - Python: flake8, black --check       │
    │  - Terraform: fmt -check, validate     │
    │  - XML: xmllint check                  │
    └──────────────────┬─────────────────────┘
                       │ (Success)
                       ▼
    ┌────────────────────────────────────────┐
    │  Job 2: Docker Build & Test            │
    │  - Build Docker image                  │
    │  - Test Odoo dependencies imports      │
    └──────────────────┬─────────────────────┘
                       │ (Success & Merge to Main)
                       ▼
    ┌────────────────────────────────────────┐
    │  Job 3: CD Deploy to Render            │
    │  - Trigger Render Deploy Hook /        │
    │    Terraform Apply Cloud Deployment    │
    │  - Health Check Confirmation           │
    └────────────────────────────────────────┘
    ```
* **Workflow Configuration (`.github/workflows/ci-cd.yml`):**
  * **Eventos disparadores:**
    * `pull_request`: Ramas `main` y `develop` (Ejecuta Jobs 1 y 2).
    * `push`: Rama `main` (Ejecuta Jobs 1, 2 y 3).
  * **Etapa de Despliegue (Deploy Step):**
    * Invocación segura mediante `curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK_URL }}` o ejecución desatendida de `terraform apply -auto-approve` utilizando `hashicorp/setup-terraform@v3`.

## 6. Acceptance Criteria
* **Scenario 1: Rechazo de Pull Request con errores de sintaxis**
  * **Given** Un desarrollador enviando un Pull Request con errores de formato o sintaxis en Python/Terraform.
  * **When** GitHub Actions ejecuta el workflow `ci-validation`.
  * **Then** El job `Lint & Static Analysis` debe fallar, bloquear el merge del Pull Request e indicar la línea exacta del error en los logs.
* **Scenario 2: Validación exitosa de Pull Request conforme**
  * **Given** Un Pull Request con código limpio y manifiestos válidos.
  * **When** GitHub Actions ejecuta el pipeline de CI.
  * **Then** Todos los jobs de validación y compilación de Docker deben finalizar en verde (código `0`) en menos de 5 minutos.
* **Scenario 3: Despliegue automático a Render tras merge en main**
  * **Given** Un Pull Request aprobado que se integra a la rama `main`.
  * **When** El evento `push: main` se dispara en GitHub Actions.
  * **Then** El pipeline debe activar el job de despliegue, notificar a Render y confirmar que el servicio web responda con estado `HTTP 200` en su URL pública.

## 7. Verification Plan
* **Automated Tests:**
  * Validación local de workflows con herramientas de emulación como `act` (opcional).
  * Prueba real enviando un commit de prueba a una rama de desarrollo para verificar la activación del pipeline.
* **Manual Verification:**
  * Revisar la pestaña *Actions* en GitHub para comprobar que los jobs se visualicen organizados y con logs descriptivos.
  * Verificar en el dashboard de Render que el evento de despliegue se registre automáticamente tras un merge a `main`.

## 8. Security and Privacy
* Uso estricto de secretos enmascarados de GitHub (`secrets.RENDER_API_KEY`, etc.).
* Permisos mínimos de token en el workflow (`permissions: contents: read`, `pull-requests: write`).
* Protección contra inyección de comandos en variables de entorno de los steps.

## 9. Risks and Mitigation
* **Risk:** Fallo de despliegue por expiración o invalidación del Deploy Hook de Render.
  * **Mitigation:** Incluir paso de reintento automático (*retry*) y verificación de código de respuesta HTTP del webhook (`HTTP 200/201`).
* **Risk:** Consumo excesivo de minutos en GitHub Actions por reconstrucciones completas de imágenes Docker.
  * **Mitigation:** Implementar `actions/cache` y `docker/build-push-action` con caché de capas de Docker en GitHub (`type=gha`).

## 10. Deliverables & Config as Code
* Archivo `.github/workflows/ci-cd.yml` completo y operativo.
* Archivo `.flake8` con configuración de estilo PEP8 compatible con Odoo (longitud de línea 100/120, exclusiones).
* Archivo `.yamllint` para validación de sintaxis de manifiestos YAML.

## 11. Definition of Done (DoD)
* [ ] Workflows de GitHub Actions implementados en el repositorio.
* [ ] Pipeline de CI validado exitosamente en un Pull Request de prueba.
* [ ] Flujo de CD a Render verificado y enlazado con los secretos del repositorio.
* [ ] Documentación del flujo de contribución y branching model añadida al repositorio.
* [ ] Aprobación de la configuración por el responsable de DevOps y arquitectura.
