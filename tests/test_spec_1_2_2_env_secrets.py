"""
Test Suite — SPEC-1.2.2: Gestión de Variables de Entorno y Secretos

Verifica el cumplimiento estricto de los criterios de aceptación y Definition of Done:
1. Existencia, sintaxis e integridad de plantillas .env.example (raíz e infra/compose/).
2. Verificación de catálogo de variables (§5) y ausencia de credenciales reales.
3. Reglas de exclusión en .gitignore para archivos sensibles (.env, .env.local, *.tfvars).
4. Comportamiento activo de Git Ignore ante archivos de credenciales reales.
5. Marcado de variables sensibles (sensitive = true) en Terraform.
6. Interpolación correcta y libre de errores en Docker Compose.
7. Disponibilidad de la guía técnica de documentación de variables y secretos.
"""

import re
import subprocess
from pathlib import Path
import pytest

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
ROOT_ENV_EXAMPLE = REPO_ROOT / ".env.example"
COMPOSE_ENV_EXAMPLE = REPO_ROOT / "infra" / "compose" / ".env.example"
COMPOSE_FILE = REPO_ROOT / "infra" / "compose" / "docker-compose.yml"
GITIGNORE_FILE = REPO_ROOT / ".gitignore"
TERRAFORM_DIR = REPO_ROOT / "infra" / "terraform"
DOCS_GUIDE_FILE = REPO_ROOT / "docs" / "guias" / "guia-variables-entorno-secretos.md"


# ===========================================================================
# Scenario 1: Plantillas Seguras y Catálogo de Variables (SPEC-1.2.2 §5, DoD #1)
# ===========================================================================
class TestEnvExampleTemplates:
    """Valida la existencia, completitud y seguridad de los archivos .env.example."""

    CATALOG_KEYS = [
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "POSTGRES_HOST",
        "POSTGRES_PORT",
        "ADMIN_PASSWORD",
        "PROXY_MODE",
        "ODOO_STAGE",
        "RENDER_API_KEY",
        "RENDER_OWNER_ID",
        "RENDER_SERVICE_NAME",
    ]

    def test_root_env_example_exists(self):
        """El archivo .env.example debe existir en la raíz del repositorio."""
        assert ROOT_ENV_EXAMPLE.exists(), "Falta el archivo .env.example en la raíz del proyecto."

    def test_compose_env_example_exists(self):
        """El archivo .env.example debe existir en infra/compose/."""
        assert COMPOSE_ENV_EXAMPLE.exists(), "Falta infra/compose/.env.example."

    @pytest.mark.parametrize("key", CATALOG_KEYS)
    def test_root_env_example_contains_key(self, key: str):
        """La plantilla .env.example debe documentar cada clave del catálogo (§5)."""
        content = ROOT_ENV_EXAMPLE.read_text(encoding="utf-8")
        assert f"{key}=" in content, f".env.example debe contener la variable '{key}'."

    def test_env_example_has_odoo_db_name(self):
        """.env.example debe documentar DB_NAME u ODOO_DB_NAME para la base de datos de Odoo."""
        content = ROOT_ENV_EXAMPLE.read_text(encoding="utf-8")
        assert "DB_NAME=" in content or "ODOO_DB_NAME=" in content

    def test_passwords_meet_minimum_length_placeholder(self):
        """Las contraseñas de ejemplo deben ser placeholders de al menos 16 caracteres (§3)."""
        content = ROOT_ENV_EXAMPLE.read_text(encoding="utf-8")
        for line in content.splitlines():
            if line.startswith("POSTGRES_PASSWORD=") or line.startswith("ADMIN_PASSWORD="):
                val = line.split("=", 1)[1].strip()
                assert len(val) >= 16, f"La contraseña de ejemplo '{line}' debe tener al menos 16 caracteres."

    def test_no_real_render_tokens_in_templates(self):
        """Ninguna plantilla debe contener tokens reales de Render API."""
        real_token_pattern = r"rnd_[A-Za-z0-9]{20,}"
        for template in [ROOT_ENV_EXAMPLE, COMPOSE_ENV_EXAMPLE]:
            content = template.read_text(encoding="utf-8")
            assert not re.search(
                real_token_pattern, content
            ), f"{template.name} contiene lo que parece un token real de Render."


# ===========================================================================
# Scenario 2: Detección y Bloqueo en Git (SPEC-1.2.2 §6, DoD #2)
# ===========================================================================
class TestGitignoreSecurityRules:
    """Valida que .gitignore bloquee efectivamente archivos con credenciales reales."""

    def test_gitignore_contains_required_rules(self):
        """.gitignore debe contener reglas explícitas para .env, .env.local y *.tfvars."""
        assert GITIGNORE_FILE.exists(), "Falta el archivo .gitignore en la raíz."
        content = GITIGNORE_FILE.read_text(encoding="utf-8")
        assert ".env" in content
        assert ".env.local" in content
        assert "*.tfvars" in content
        assert "*.tfstate" in content

    def test_gitignore_allows_example_files(self):
        """.gitignore debe excluir explícitamente las plantillas .example con negación (!)."""
        content = GITIGNORE_FILE.read_text(encoding="utf-8")
        assert "!.env.example" in content
        assert "!terraform.tfvars.example" in content

    def test_git_check_ignore_blocks_sensitive_files(self):
        """Verifica mediante git check-ignore que los archivos con secretos son ignorados."""
        test_files = [
            ".env",
            ".env.local",
            ".env.staging",
            ".env.production",
            "infra/terraform/terraform.tfvars",
            "infra/terraform/custom.tfvars.json",
        ]
        cmd = ["git", "check-ignore"] + test_files
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT)
        assert result.returncode == 0, f"git check-ignore falló: {result.stderr}"
        for f in test_files:
            assert f in result.stdout, f"El archivo sensible '{f}' NO fue ignorado por Git."

    def test_git_check_ignore_does_not_block_example_templates(self):
        """Verifica que git check-ignore NO ignore los archivos .example."""
        allowed_files = [
            ".env.example",
            "infra/compose/.env.example",
            "infra/terraform/terraform.tfvars.example",
        ]
        for f in allowed_files:
            cmd = ["git", "check-ignore", f]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT)
            assert result.returncode == 1, f"La plantilla requerida '{f}' está siendo erróneamente ignorada por Git."

    def test_no_real_secret_files_tracked_in_git(self):
        """Verifica que ningún archivo .env o .tfvars real esté actualmente rastreado en Git."""
        cmd = ["git", "ls-files", ".env", "*.tfvars", "*.tfstate"]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT)
        assert result.returncode == 0
        tracked_files = [f for f in result.stdout.splitlines() if not f.endswith(".example")]
        assert len(tracked_files) == 0, f"Archivos sensibles rastreados en Git: {tracked_files}"


# ===========================================================================
# Scenario 3: Secretos en Terraform (SPEC-1.2.2 §6 Scenario 3, DoD #3)
# ===========================================================================
class TestTerraformSecretsConfiguration:
    """Verifica que las variables de secretos en Terraform estén marcadas como sensibles."""

    SENSITIVE_VARIABLES = [
        "render_api_key",
        "render_owner_id",
        "odoo_admin_password",
    ]

    @pytest.mark.parametrize("varname", SENSITIVE_VARIABLES)
    def test_variable_is_flagged_sensitive(self, varname: str):
        """Cada variable de secreto en variables.tf debe tener sensitive = true."""
        variables_content = (TERRAFORM_DIR / "variables.tf").read_text(encoding="utf-8")
        pattern = rf'variable\s+"{varname}"\s*\{{[^}}]*sensitive\s*=\s*true'
        assert re.search(
            pattern, variables_content, re.DOTALL
        ), f"La variable de secreto '{varname}' debe tener 'sensitive = true' en variables.tf."

    def test_terraform_no_hardcoded_secrets_in_manifests(self):
        """Ningún manifiesto HCL en infra/terraform/ debe contener contraseñas quemadas."""
        for tf_file in TERRAFORM_DIR.glob("*.tf"):
            content = tf_file.read_text(encoding="utf-8")
            assert not re.search(
                r'password\s*=\s*"[A-Za-z0-9@#$!%]{8,}"', content
            ), f"Posible contraseña quemada en {tf_file.name}"


# ===========================================================================
# Scenario 4: Interpolación en Docker Compose (SPEC-1.2.2 §6 Scenario 1, DoD #1)
# ===========================================================================
class TestDockerComposeInterpolation:
    """Valida que docker-compose.yml interprete correctamente las variables de entorno."""

    def test_compose_config_validates_successfully(self):
        """docker compose config debe ejecutarse sin errores de sintaxis o variables no resueltas."""
        cmd = ["docker", "compose", "-f", str(COMPOSE_FILE), "config"]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT)
        assert result.returncode == 0, f"Error en validación de compose config: {result.stderr}"
        assert "caryvil-db" in result.stdout
        assert "caryvil-web" in result.stdout

    def test_compose_uses_db_port_to_prevent_render_conflict(self):
        """El servicio web de Docker Compose debe usar DB_PORT para no colisionar con PORT."""
        content = COMPOSE_FILE.read_text(encoding="utf-8")
        assert "DB_PORT" in content, "docker-compose.yml debe configurar DB_PORT para el puerto de PostgreSQL."

    def test_compose_exposes_standard_odoo_ports(self):
        """docker-compose.yml debe mapear los puertos 8069 y 8072."""
        content = COMPOSE_FILE.read_text(encoding="utf-8")
        assert '"8069:8069"' in content
        assert '"8072:8072"' in content


# ===========================================================================
# Scenario 5: Documentación Técnica de Variables y Secretos (DoD #3)
# ===========================================================================
class TestDocumentationDeliverable:
    """Valida la existencia y contenido de la guía técnica de variables y secretos."""

    def test_technical_guide_exists(self):
        """La guía de variables y secretos debe existir en docs/guias/."""
        assert (
            DOCS_GUIDE_FILE.exists()
        ), "Falta la guía técnica docs/guias/guia-variables-entorno-secretos.md requerida por el DoD."

    def test_technical_guide_documents_all_environments(self):
        """La guía debe documentar los entornos Local, CI/CD y Render."""
        content = DOCS_GUIDE_FILE.read_text(encoding="utf-8")
        assert "Local" in content
        assert "CI/CD" in content
        assert "Render" in content
        assert "POSTGRES_PASSWORD" in content
        assert "ADMIN_PASSWORD" in content
        assert "RENDER_API_KEY" in content
