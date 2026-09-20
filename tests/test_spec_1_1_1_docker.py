# -*- coding: utf-8 -*-
"""Suite de pruebas automatizadas para SPEC-1.1.1: Configuración del Entorno Docker.

Valida el cumplimiento de criterios de aceptación y Definition of Done:
1. Validación sintáctica de docker-compose.yml.
2. Estado de salud de los contenedores (caryvil-db y caryvil-web).
3. Disponibilidad del endpoint HTTP de Odoo (puerto 8069).
4. Montaje en caliente de /mnt/extra-addons.
5. Ejecución del runtime bajo usuario no privilegiado odoo (UID 101).
6. Aislamiento y conectividad de red interna caryvil-net.
"""

import subprocess
import urllib.request


def test_docker_compose_syntax_config():
    """Valida que la configuración de Docker Compose sea sintácticamente válida."""
    cmd = ["docker", "compose", "-f", "infra/compose/docker-compose.yml", "config"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Error en validación de compose: {result.stderr}"
    assert "caryvil-db" in result.stdout
    assert "caryvil-web" in result.stdout
    assert "odoo-db-data" in result.stdout
    assert "odoo-web-data" in result.stdout
    assert "caryvil-net" in result.stdout


def test_containers_running_status():
    """Valida que los contenedores caryvil-db y caryvil-web estén en ejecución."""
    cmd = ["docker", "compose", "-f", "infra/compose/docker-compose.yml", "ps", "--format", "{{.Name}} {{.Status}}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Error al consultar estado de contenedores: {result.stderr}"
    assert "caryvil-db" in result.stdout
    assert "caryvil-web" in result.stdout


def test_odoo_http_endpoint_accessible():
    """Valida que la interfaz web de Odoo responda en http://localhost:8069."""
    url = "http://localhost:8069"
    req = urllib.request.Request(url, headers={"User-Agent": "Caryvil-QA-Test/1.0"})
    with urllib.request.urlopen(req, timeout=10) as response:
        assert response.status in [200, 303], f"Código HTTP inesperado: {response.status}"
        headers = dict(response.headers)
        assert "Server" in headers or "Set-Cookie" in headers


def test_volume_mount_extra_addons():
    """Valida que /mnt/extra-addons esté montado y sincronizado con custom_addons."""
    cmd = [
        "docker",
        "compose",
        "-f",
        "infra/compose/docker-compose.yml",
        "exec",
        "-T",
        "web",
        "ls",
        "-la",
        "/mnt/extra-addons",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Error al acceder a /mnt/extra-addons: {result.stderr}"
    assert "caryvil_erp" in result.stdout


def test_non_root_runtime_user():
    """Valida que el proceso Odoo se ejecute bajo el usuario seguro sin privilegios 'odoo'."""
    cmd = ["docker", "compose", "-f", "infra/compose/docker-compose.yml", "exec", "-T", "web", "whoami"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Error al ejecutar whoami en contenedor: {result.stderr}"
    assert result.stdout.strip() == "odoo"


def test_postgres_internal_healthcheck():
    """Valida que PostgreSQL esté disponible y responda al comando pg_isready."""
    cmd = [
        "docker",
        "compose",
        "-f",
        "infra/compose/docker-compose.yml",
        "exec",
        "-T",
        "db",
        "pg_isready",
        "-U",
        "odoo",
        "-d",
        "postgres",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"PostgreSQL no está listo: {result.stderr}"
    assert "accepting connections" in result.stdout
