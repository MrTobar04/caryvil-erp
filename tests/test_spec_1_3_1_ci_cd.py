"""
Test Suite — SPEC-1.3.1: Pipeline CI/CD con GitHub Actions y Render

Verifica de manera automatizada:
- Estructura y existencia de flujos de trabajo (.github/workflows/) y configuración (.flake8, .yamllint, etc.).
- Parseo y validez sintáctica de los manifiestos YAML de GitHub Actions.
- Configuración de eventos disparadores (pull_request, push, workflow_dispatch).
- Presencia y completitud de jobs de validación estática (Flake8, Black, Yamllint, Terraform, XML).
- Presencia y completitud de jobs de compilación Docker con almacenamiento en caché (type=gha).
- Integración segura con Render (Deploy Hook y Health Check) respetando ISO-27001 (sin secretos expuestos).
- Parámetros de calidad en .flake8 y .yamllint.
"""
import re
from pathlib import Path
import pytest
import yaml

# ---------------------------------------------------------------------------
# Constantes de Rutas
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
WORKFLOWS_DIR = REPO_ROOT / ".github" / "workflows"
CI_VALIDATION_FILE = WORKFLOWS_DIR / "ci-validation.yml"
CD_DEPLOY_FILE = WORKFLOWS_DIR / "cd-deploy.yml"
FLAKE8_CONFIG_FILE = REPO_ROOT / ".flake8"
YAMLLINT_CONFIG_FILE = REPO_ROOT / ".yamllint"
PYPROJECT_CONFIG_FILE = REPO_ROOT / "pyproject.toml"


# ===========================================================================
# 1. Verificación de Entregables y Archivos de Configuración (SPEC-1.3.1 §10)
# ===========================================================================
class TestDeliverablesAndConfigFiles:
    """Verifica la existencia y configuración base de todos los archivos requeridos."""

    @pytest.mark.parametrize(
        "file_path,description",
        [
            (CI_VALIDATION_FILE, "Workflow de CI (ci-validation.yml)"),
            (CD_DEPLOY_FILE, "Workflow de CD (cd-deploy.yml)"),
            (FLAKE8_CONFIG_FILE, "Configuración de Flake8 (.flake8)"),
            (YAMLLINT_CONFIG_FILE, "Configuración de Yamllint (.yamllint)"),
            (PYPROJECT_CONFIG_FILE, "Configuración de Black y Pytest (pyproject.toml)"),
        ],
    )
    def test_required_file_exists(self, file_path: Path, description: str):
        """Given el repositorio, cada archivo de configuración y workflow debe existir."""
        assert file_path.exists(), f"Falta el archivo requerido por SPEC-1.3.1: {description} en {file_path}"
        assert file_path.stat().st_size > 0, f"El archivo {file_path.name} no debe estar vacío"

    def test_flake8_configuration_parameters(self):
        """Verifica que .flake8 define las reglas PEP8 requeridas para Odoo 17."""
        content = FLAKE8_CONFIG_FILE.read_text(encoding="utf-8")
        assert "max-line-length = 120" in content, "Flake8 debe configurar max-line-length = 120"
        assert "max-complexity = 10" in content, "Flake8 debe limitar max-complexity = 10"
        assert "exclude =" in content, "Flake8 debe definir exclusiones"
        assert "__pycache__" in content, "Flake8 debe excluir __pycache__"
        assert "show-source = True" in content, "Flake8 debe activar show-source para logs descriptivos"

    def test_yamllint_configuration_parameters(self):
        """Verifica que .yamllint define reglas válidas de validación YAML."""
        content = YAMLLINT_CONFIG_FILE.read_text(encoding="utf-8")
        assert "extends: default" in content, "Yamllint debe extender el perfil default"
        assert "line-length:" in content, "Yamllint debe configurar longitud de línea"
        assert "truthy:" in content, "Yamllint debe configurar regla truthy"

    def test_pyproject_toml_parameters(self):
        """Verifica que pyproject.toml configure Black con longitud de línea 120."""
        content = PYPROJECT_CONFIG_FILE.read_text(encoding="utf-8")
        assert "line-length = 120" in content, "Black debe estar configurado con line-length = 120"
        assert "target-version = ['py310']" in content or 'target-version = ["py310"]' in content


# ===========================================================================
# 2. Validación de Sintaxis y Estructura del Workflow de CI (SPEC-1.3.1 §5)
# ===========================================================================
class TestCIValidationWorkflow:
    """Verifica que el workflow de CI cumple con los triggers, jobs y steps requeridos."""

    @pytest.fixture(scope="class")
    def ci_yaml(self):
        """Carga y parsea el archivo YAML de validación de CI."""
        assert CI_VALIDATION_FILE.exists()
        with open(CI_VALIDATION_FILE, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data

    @pytest.fixture(scope="class")
    def ci_content(self):
        """Lee el contenido crudo del archivo de validación de CI."""
        return CI_VALIDATION_FILE.read_text(encoding="utf-8")

    def test_ci_yaml_valid_syntax(self, ci_yaml):
        """El archivo ci-validation.yml debe tener una sintaxis YAML 100% válida."""
        assert isinstance(ci_yaml, dict), "El archivo YAML debe parsear a un diccionario válido"
        assert "name" in ci_yaml, "El workflow de CI debe tener un nombre asignado"
        assert "jobs" in ci_yaml, "El workflow de CI debe contener la sección 'jobs'"

    def test_ci_trigger_events(self, ci_yaml):
        """Verifica que los triggers de CI cubran pull_request en main/develop y push en develop."""
        triggers = ci_yaml.get("on") or ci_yaml.get(True, {})
        # Verifica pull_request
        assert "pull_request" in triggers, "CI debe dispararse en eventos pull_request"
        pr_branches = triggers["pull_request"].get("branches", [])
        assert "main" in pr_branches, "pull_request debe monitorear la rama 'main'"
        assert "develop" in pr_branches, "pull_request debe monitorear la rama 'develop'"

    def test_ci_required_jobs_present(self, ci_yaml):
        """Verifica la presencia de los jobs 'lint-and-static-analysis' y 'docker-build-test'."""
        jobs = ci_yaml.get("jobs", {})
        assert "lint-and-static-analysis" in jobs, "Falta el job de análisis estático 'lint-and-static-analysis'"
        assert "docker-build-test" in jobs, "Falta el job de compilación Docker 'docker-build-test'"

    def test_ci_job_dependencies(self, ci_yaml):
        """docker-build-test debe requerir que lint-and-static-analysis sea exitoso."""
        docker_job = ci_yaml["jobs"]["docker-build-test"]
        needs = docker_job.get("needs")
        valid_needs = needs == "lint-and-static-analysis" or (
            isinstance(needs, list) and "lint-and-static-analysis" in needs
        )
        assert valid_needs, "docker-build-test debe depender de lint-and-static-analysis"

    def test_ci_static_analysis_steps(self, ci_content):
        """Verifica que el job de análisis estático incluya todas las herramientas requeridas."""
        # Python setup con caché
        assert "actions/setup-python" in ci_content, "Debe utilizar actions/setup-python"
        assert "cache: \"pip\"" in ci_content or "cache: 'pip'" in ci_content, "Debe configurar caché de pip"

        # Herramientas de calidad
        assert "flake8" in ci_content, "Debe ejecutar análisis estático con flake8"
        assert "black --check" in ci_content, "Debe ejecutar verificación de formato con black"
        assert "yamllint" in ci_content, "Debe ejecutar verificación con yamllint"

        # Terraform lint & validate
        assert "hashicorp/setup-terraform" in ci_content, "Debe utilizar setup-terraform"
        assert "terraform" in ci_content and "fmt -check" in ci_content, (
            "Debe verificar formato con terraform fmt -check"
        )
        assert "validate" in ci_content, "Debe validar sintaxis con terraform validate"

        # Verificación XML de Odoo
        assert "xml.etree.ElementTree" in ci_content or "xmllint" in ci_content, (
            "Debe incluir paso de validación de sintaxis XML para vistas de Odoo"
        )

    def test_ci_docker_build_caching(self, ci_content):
        """Verifica que el build de Docker utilice docker/build-push-action con caché de GitHub Actions."""
        assert "docker/setup-buildx-action" in ci_content, "Debe configurar buildx para soporte de caché avanzada"
        assert "docker/build-push-action" in ci_content, "Debe utilizar docker/build-push-action"
        assert "type=gha" in ci_content, "Debe configurar caché de capas Docker en GitHub Actions (type=gha)"
        assert "push: false" in ci_content, "En la etapa de CI de validación push debe ser false"


# ===========================================================================
# 3. Validación de Sintaxis y Estructura del Workflow de CD (SPEC-1.3.1 §5)
# ===========================================================================
class TestCDDeployWorkflow:
    """Verifica que el workflow de CD cumple con la compilación, publicación y despliegue a Render."""

    @pytest.fixture(scope="class")
    def cd_yaml(self):
        """Carga y parsea el archivo YAML de despliegue CD."""
        assert CD_DEPLOY_FILE.exists()
        with open(CD_DEPLOY_FILE, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data

    @pytest.fixture(scope="class")
    def cd_content(self):
        """Lee el contenido crudo del archivo de despliegue CD."""
        return CD_DEPLOY_FILE.read_text(encoding="utf-8")

    def test_cd_yaml_valid_syntax(self, cd_yaml):
        """El archivo cd-deploy.yml debe tener una sintaxis YAML 100% válida."""
        assert isinstance(cd_yaml, dict), "El archivo YAML debe parsear a un diccionario válido"
        assert "name" in cd_yaml, "El workflow de CD debe tener un nombre asignado"
        assert "jobs" in cd_yaml, "El workflow de CD debe contener la sección 'jobs'"

    def test_cd_trigger_events(self, cd_yaml):
        """Verifica que el CD se active únicamente ante push en main o workflow_dispatch."""
        triggers = cd_yaml.get("on") or cd_yaml.get(True, {})
        assert "push" in triggers, "CD debe dispararse en eventos push"
        push_branches = triggers["push"].get("branches", [])
        assert "main" in push_branches, "CD push debe ejecutarse exclusivamente en la rama 'main'"
        assert "workflow_dispatch" in triggers, "CD debe soportar ejecución manual vía workflow_dispatch"

    def test_cd_required_jobs_present(self, cd_yaml):
        """Verifica la presencia de los 3 jobs del pipeline de CD."""
        jobs = cd_yaml.get("jobs", {})
        assert "build-and-publish" in jobs, "Falta el job 'build-and-publish'"
        assert "deploy-to-render" in jobs, "Falta el job 'deploy-to-render'"
        assert "health-check" in jobs, "Falta el job 'health-check'"

    def test_cd_job_chain_dependencies(self, cd_yaml):
        """Verifica la secuencialidad: build-and-publish -> deploy-to-render -> health-check."""
        deploy_job = cd_yaml["jobs"]["deploy-to-render"]
        assert deploy_job.get("needs") == "build-and-publish", "deploy-to-render debe depender de build-and-publish"

        health_job = cd_yaml["jobs"]["health-check"]
        assert health_job.get("needs") == "deploy-to-render", "health-check debe depender de deploy-to-render"

    def test_cd_docker_registry_publication(self, cd_content):
        """Verifica autenticación y publicación en GitHub Packages / GHCR."""
        assert "docker/login-action" in cd_content, "Debe iniciar sesión en el registro Docker"
        assert "ghcr.io" in cd_content, "Debe utilizar el registro ghcr.io"
        assert "GITHUB_TOKEN" in cd_content, "Debe usar el GITHUB_TOKEN para autenticación en GHCR"
        assert "push: true" in cd_content, "En CD la imagen debe ser publicada (push: true)"
        assert "type=gha" in cd_content, "Debe usar caché de capas en CD para optimizar tiempo de compilación"

    def test_cd_render_deploy_hook_and_retries(self, cd_content):
        """Verifica la invocación segura del Deploy Hook de Render y su lógica de reintentos (SPEC-1.3.1 §9)."""
        assert "RENDER_DEPLOY_HOOK_URL" in cd_content, "Debe referenciar el secreto RENDER_DEPLOY_HOOK_URL"
        assert "curl" in cd_content, "Debe invocar el webhook mediante curl"
        assert "MAX_RETRIES" in cd_content or "retry" in cd_content.lower(), (
            "Debe incluir política de reintentos para mitigar fallos transitorios en el webhook"
        )
        assert "200" in cd_content and "201" in cd_content, (
            "Debe verificar respuestas HTTP de éxito (200 o 201) de Render"
        )

    def test_cd_health_check_confirmation(self, cd_content):
        """Verifica que se ejecute la comprobación de estado de salud del servicio (SPEC-1.3.1 §6 Escenario 3)."""
        assert "http_code" in cd_content or "curl" in cd_content, "Debe consultar el endpoint público del servicio"
        assert "200" in cd_content, "Debe esperar confirmación HTTP 200/303 en el health check"


# ===========================================================================
# 4. Seguridad, Secretos y Principio de Menor Privilegio (ISO-27001)
# ===========================================================================
class TestSecurityAndSecretsEnforcement:
    """Garantiza el cumplimiento estricto de seguridad en el pipeline CI/CD."""

    @pytest.mark.parametrize("workflow_file", [CI_VALIDATION_FILE, CD_DEPLOY_FILE])
    def test_no_hardcoded_secrets_in_workflows(self, workflow_file: Path):
        """Ningún token real, API key o contraseña debe figurar en texto plano en los workflows."""
        content = workflow_file.read_text(encoding="utf-8")
        # Patrones de tokens de Render o GitHub
        assert not re.search(r"rnd_[A-Za-z0-9]{20,}", content), (
            f"Se detectó un token potencial de Render hardcodeado en {workflow_file.name}"
        )
        assert not re.search(r"ghp_[A-Za-z0-9]{20,}", content), (
            f"Se detectó un token personal de GitHub hardcodeado en {workflow_file.name}"
        )

    @pytest.mark.parametrize("workflow_file", [CI_VALIDATION_FILE, CD_DEPLOY_FILE])
    def test_secrets_masked_via_context(self, workflow_file: Path):
        """Todas las variables sensibles deben ser inyectadas únicamente mediante ${{ secrets.* }}."""
        content = workflow_file.read_text(encoding="utf-8")
        if "RENDER_" in content:
            assert "${{ secrets.RENDER_" in content, (
                f"Las variables de Render en {workflow_file.name} deben usar el contexto ${{ secrets.* }}"
            )

    @pytest.mark.parametrize("workflow_file", [CI_VALIDATION_FILE, CD_DEPLOY_FILE])
    def test_least_privilege_permissions_declared(self, workflow_file: Path):
        """Los workflows deben declarar explícitamente permisos mínimos (Least Privilege)."""
        content = workflow_file.read_text(encoding="utf-8")
        assert "permissions:" in content, (
            f"El archivo {workflow_file.name} debe definir la sección de permisos mínimos"
        )
        assert "contents: read" in content, (
            f"El archivo {workflow_file.name} debe declarar 'contents: read'"
        )
