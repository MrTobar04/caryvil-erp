"""
Test Suite — SPEC-1.2.1: Aprovisionamiento en Render con Terraform

Verifica que los manifiestos HCL en infra/terraform/ cumplen con:
- Estructura de archivos requerida por el spec.
- Formato y sintaxis HCL válidos (variables, outputs, recursos declarados).
- Reglas de seguridad: terraform.tfvars excluido del repositorio Git.
- Variables sensibles marcadas como sensitive=true.
- Archivo .env y *.tfstate excluidos vía .gitignore.
"""
import os
import re
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
TERRAFORM_DIR = REPO_ROOT / "infra" / "terraform"
GITIGNORE_PATH = REPO_ROOT / ".gitignore"


# ===========================================================================
# Scenario: Estructura de archivos requerida (SPEC-1.2.1 §5)
# ===========================================================================
class TestTerraformFileStructure:
    """Todos los manifiestos definidos en el spec deben existir."""

    REQUIRED_FILES = [
        "main.tf",
        "variables.tf",
        "outputs.tf",
        "providers.tf",
        "versions.tf",
        "terraform.tfvars.example",
    ]

    @pytest.mark.parametrize("filename", REQUIRED_FILES)
    def test_required_file_exists(self, filename: str):
        """Given the terraform/ directory, each required file must be present."""
        target = TERRAFORM_DIR / filename
        assert target.exists(), (
            f"Falta el archivo requerido por SPEC-1.2.1 §5: {filename}"
        )

    def test_tfvars_real_not_committed(self):
        """
        terraform.tfvars NO debe estar rastreado en Git (es un secreto real).
        Se verifica indirectamente comprobando que .gitignore lo excluye.
        """
        gitignore_content = GITIGNORE_PATH.read_text(encoding="utf-8")
        assert "*.tfvars" in gitignore_content, (
            "El .gitignore debe excluir *.tfvars para proteger credenciales reales"
        )

    def test_tfstate_excluded_in_gitignore(self):
        """*.tfstate debe estar excluido en .gitignore (SPEC-1.2.1 §3)."""
        gitignore_content = GITIGNORE_PATH.read_text(encoding="utf-8")
        assert "*.tfstate" in gitignore_content, (
            "El .gitignore debe excluir *.tfstate para proteger el estado de Terraform"
        )

    def test_dot_terraform_excluded_in_gitignore(self):
        """.terraform/ debe estar excluido en .gitignore."""
        gitignore_content = GITIGNORE_PATH.read_text(encoding="utf-8")
        assert ".terraform/" in gitignore_content, (
            "El .gitignore debe excluir el directorio .terraform/"
        )


# ===========================================================================
# Scenario: versions.tf — versión y proveedor (SPEC-1.2.1 §5)
# ===========================================================================
class TestVersionsTf:
    """Verifica que versions.tf declara la versión mínima de Terraform y el provider."""

    def test_required_terraform_version(self):
        """Terraform debe requerir versión >= 1.5.0."""
        content = (TERRAFORM_DIR / "versions.tf").read_text(encoding="utf-8")
        assert ">= 1.5.0" in content, (
            "versions.tf debe declarar required_version = '>= 1.5.0'"
        )

    def test_render_provider_declared(self):
        """El provider render-oss/render debe estar declarado en required_providers."""
        content = (TERRAFORM_DIR / "versions.tf").read_text(encoding="utf-8")
        assert "render-oss/render" in content, (
            "versions.tf debe declarar el provider source = 'render-oss/render'"
        )

    def test_provider_version_pinned(self):
        """La versión del provider debe estar fijada con ~> 1.3.0."""
        content = (TERRAFORM_DIR / "versions.tf").read_text(encoding="utf-8")
        assert "~> 1.3.0" in content, (
            "La versión del provider debe estar fijada con '~> 1.3.0'"
        )


# ===========================================================================
# Scenario: providers.tf — configuración del proveedor (SPEC-1.2.1 §5)
# ===========================================================================
class TestProvidersTf:
    """Verifica que providers.tf configura el proveedor render correctamente."""

    def test_provider_render_block_exists(self):
        """providers.tf debe contener el bloque provider \"render\"."""
        content = (TERRAFORM_DIR / "providers.tf").read_text(encoding="utf-8")
        assert 'provider "render"' in content, (
            'providers.tf debe contener el bloque provider "render"'
        )

    def test_api_key_uses_variable(self):
        """La api_key debe referenciarse como variable, no estar hardcodeada."""
        content = (TERRAFORM_DIR / "providers.tf").read_text(encoding="utf-8")
        assert "var.render_api_key" in content, (
            "providers.tf debe usar var.render_api_key para la autenticación"
        )

    def test_owner_id_uses_variable(self):
        """El owner_id debe referenciarse como variable."""
        content = (TERRAFORM_DIR / "providers.tf").read_text(encoding="utf-8")
        assert "var.render_owner_id" in content, (
            "providers.tf debe usar var.render_owner_id para identificar el propietario"
        )


# ===========================================================================
# Scenario: variables.tf — declaración de variables sensibles (SPEC-1.2.1 §5)
# ===========================================================================
class TestVariablesTf:
    """Verifica que las variables críticas están declaradas correctamente."""

    REQUIRED_VARIABLES = [
        "render_api_key",
        "render_owner_id",
        "environment",
        "region",
        "db_name",
        "db_user",
        "odoo_admin_password",
    ]

    @pytest.mark.parametrize("varname", REQUIRED_VARIABLES)
    def test_variable_declared(self, varname: str):
        """Cada variable requerida debe estar declarada en variables.tf."""
        content = (TERRAFORM_DIR / "variables.tf").read_text(encoding="utf-8")
        assert f'variable "{varname}"' in content, (
            f"variables.tf debe declarar la variable '{varname}'"
        )

    def test_render_api_key_is_sensitive(self):
        """render_api_key debe marcarse como sensitive=true."""
        content = (TERRAFORM_DIR / "variables.tf").read_text(encoding="utf-8")
        # Buscar el bloque de render_api_key y verificar sensitive
        pattern = r'variable\s+"render_api_key"\s*\{[^}]*sensitive\s*=\s*true'
        assert re.search(pattern, content, re.DOTALL), (
            "La variable render_api_key debe tener sensitive = true"
        )

    def test_odoo_admin_password_is_sensitive(self):
        """odoo_admin_password debe marcarse como sensitive=true."""
        content = (TERRAFORM_DIR / "variables.tf").read_text(encoding="utf-8")
        pattern = r'variable\s+"odoo_admin_password"\s*\{[^}]*sensitive\s*=\s*true'
        assert re.search(pattern, content, re.DOTALL), (
            "La variable odoo_admin_password debe tener sensitive = true"
        )

    def test_render_owner_id_is_sensitive(self):
        """render_owner_id debe marcarse como sensitive=true."""
        content = (TERRAFORM_DIR / "variables.tf").read_text(encoding="utf-8")
        pattern = r'variable\s+"render_owner_id"\s*\{[^}]*sensitive\s*=\s*true'
        assert re.search(pattern, content, re.DOTALL), (
            "La variable render_owner_id debe tener sensitive = true"
        )

    def test_region_default_is_oregon(self):
        """La región por defecto debe ser 'oregon' según SPEC-1.2.1 §5."""
        content = (TERRAFORM_DIR / "variables.tf").read_text(encoding="utf-8")
        assert '"oregon"' in content, (
            "El valor por defecto de la variable region debe ser 'oregon'"
        )


# ===========================================================================
# Scenario: main.tf — recursos render_postgres y render_web_service (SPEC-1.2.1 §5)
# ===========================================================================
class TestMainTf:
    """Verifica que main.tf declara los dos recursos requeridos por el spec."""

    def test_render_postgres_resource_exists(self):
        """main.tf debe declarar el recurso render_postgres."""
        content = (TERRAFORM_DIR / "main.tf").read_text(encoding="utf-8")
        assert 'resource "render_postgres"' in content, (
            "main.tf debe declarar el recurso render_postgres"
        )

    def test_render_web_service_resource_exists(self):
        """main.tf debe declarar el recurso render_web_service."""
        content = (TERRAFORM_DIR / "main.tf").read_text(encoding="utf-8")
        assert 'resource "render_web_service"' in content, (
            "main.tf debe declarar el recurso render_web_service"
        )

    def test_postgres_plan_is_free(self):
        """El plan de PostgreSQL debe ser 'free' (SPEC-1.2.1 §5)."""
        content = (TERRAFORM_DIR / "main.tf").read_text(encoding="utf-8")
        assert re.search(r'plan\s*=\s*"free"', content), (
            "El recurso render_postgres debe usar plan = 'free'"
        )

    def test_postgres_version_is_16(self):
        """La versión de PostgreSQL debe ser '16' (ADR-0001)."""
        content = (TERRAFORM_DIR / "main.tf").read_text(encoding="utf-8")
        assert re.search(r'version\s*=\s*"16"', content), (
            "El recurso render_postgres debe usar version = '16' (ADR-0001)"
        )

    def test_web_service_uses_docker_image(self):
        """El Web Service debe usar runtime de imagen Docker (runtime_source.image)."""
        content = (TERRAFORM_DIR / "main.tf").read_text(encoding="utf-8")
        assert "image_url" in content, (
            "render_web_service debe usar runtime_source.image.image_url"
        )

    def test_web_service_references_ghcr_image(self):
        """La imagen Docker debe referenciarse desde GitHub Container Registry (GHCR)."""
        content = (TERRAFORM_DIR / "main.tf").read_text(encoding="utf-8")
        assert "ghcr.io" in content, (
            "La imagen de Odoo debe provenir de GitHub Container Registry (ghcr.io)"
        )

    def test_proxy_mode_env_var_set(self):
        """PROXY_MODE debe estar configurada como True (requerido detrás del proxy de Render)."""
        content = (TERRAFORM_DIR / "main.tf").read_text(encoding="utf-8")
        assert "PROXY_MODE" in content, (
            "El Web Service debe tener la variable de entorno PROXY_MODE configurada"
        )

    def test_admin_password_env_var_references_variable(self):
        """ADMIN_PASSWORD debe referenciarse desde var.odoo_admin_password, no hardcodeada."""
        content = (TERRAFORM_DIR / "main.tf").read_text(encoding="utf-8")
        assert "var.odoo_admin_password" in content, (
            "ADMIN_PASSWORD debe usar var.odoo_admin_password, no un valor hardcodeado"
        )

    def test_no_hardcoded_credentials(self):
        """main.tf NO debe contener contraseñas o tokens hardcodeados."""
        content = (TERRAFORM_DIR / "main.tf").read_text(encoding="utf-8")
        suspicious_patterns = [
            r'password\s*=\s*"[A-Za-z0-9@#$!%]{8,}"',
            r'api_key\s*=\s*"rnd_[A-Za-z0-9]+"',
        ]
        for pattern in suspicious_patterns:
            assert not re.search(pattern, content), (
                f"main.tf contiene credenciales hardcodeadas: {pattern}"
            )


# ===========================================================================
# Scenario: outputs.tf — salidas de infraestructura (SPEC-1.2.1 §5)
# ===========================================================================
class TestOutputsTf:
    """Verifica que outputs.tf declara las salidas requeridas por el spec."""

    def test_service_url_output_exists(self):
        """outputs.tf debe declarar la URL pública del servicio Odoo."""
        content = (TERRAFORM_DIR / "outputs.tf").read_text(encoding="utf-8")
        assert "odoo_service_url" in content, (
            "outputs.tf debe declarar el output 'odoo_service_url'"
        )

    def test_postgres_internal_host_output_exists(self):
        """outputs.tf debe declarar la cadena de conexión interna de PostgreSQL."""
        content = (TERRAFORM_DIR / "outputs.tf").read_text(encoding="utf-8")
        assert "postgres_internal_host" in content or "postgres_host" in content, (
            "outputs.tf debe declarar el output para el host interno de PostgreSQL"
        )

    def test_postgres_connection_output_is_sensitive(self):
        """El output de conexión PostgreSQL debe ser sensitive=true."""
        content = (TERRAFORM_DIR / "outputs.tf").read_text(encoding="utf-8")
        assert "sensitive   = true" in content or "sensitive = true" in content, (
            "Los outputs de conexión a PostgreSQL deben tener sensitive = true"
        )


# ===========================================================================
# Scenario: terraform.tfvars.example — plantilla de variables (SPEC-1.2.1 §10)
# ===========================================================================
class TestTfvarsExample:
    """Verifica que la plantilla .example contiene claves correctas y sin secretos reales."""

    EXPECTED_KEYS = [
        "render_api_key",
        "render_owner_id",
        "environment",
        "region",
        "db_name",
        "odoo_admin_password",
    ]

    @pytest.mark.parametrize("key", EXPECTED_KEYS)
    def test_example_contains_key(self, key: str):
        """La plantilla debe documentar cada variable requerida."""
        content = (TERRAFORM_DIR / "terraform.tfvars.example").read_text(
            encoding="utf-8"
        )
        assert key in content, (
            f"terraform.tfvars.example debe documentar la clave '{key}'"
        )

    def test_example_does_not_contain_real_token(self):
        """La plantilla NO debe contener tokens reales de Render (rnd_ seguido de chars reales)."""
        content = (TERRAFORM_DIR / "terraform.tfvars.example").read_text(
            encoding="utf-8"
        )
        # Un token real de Render tiene al menos 20 chars alfanuméricos tras rnd_
        real_token_pattern = r"rnd_[A-Za-z0-9]{20,}"
        assert not re.search(real_token_pattern, content), (
            "terraform.tfvars.example contiene lo que parece un token real de Render. "
            "Solo debe contener valores de ejemplo."
        )
