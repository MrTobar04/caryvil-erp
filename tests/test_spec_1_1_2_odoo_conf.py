# -*- coding: utf-8 -*-
"""Suite de pruebas automatizadas para SPEC-1.1.2: Configuración del Servidor Odoo.

Valida el cumplimiento de criterios de aceptación y Definition of Done:
1. Existencia y montaje del archivo odoo.conf y plantilla parametrizada.
2. Configuración correcta de addons_path (/mnt/extra-addons y addons base).
3. Habilitación de proxy_mode = True para soporte de proxy inverso en Render.
4. Parámetros de límites de recursos y optimización (workers, CPU, memoria, hilos cron).
5. Instalación y disponibilidad de librerías Python (num2words, phonenumbers, qrcode, psycopg2, dotenv).
6. Funcionamiento del endpoint HTTP bajo cabeceras de proxy inverso (X-Forwarded-Proto, X-Forwarded-For).
"""

import os
import subprocess
import urllib.request


def test_odoo_conf_files_exist_locally():
    """Valida que los archivos odoo.conf y plantilla existan en la ruta canónica infra/config/."""
    infra_conf = os.path.join("infra", "config", "odoo.conf")
    infra_template = os.path.join("infra", "config", "odoo.conf.template")

    assert os.path.exists(infra_conf), f"No se encontró {infra_conf}"
    assert os.path.exists(infra_template), f"No se encontró {infra_template}"

    with open(infra_template, "r", encoding="utf-8") as f:
        template_content = f.read()
    assert "$ADMIN_PASSWORD" in template_content
    assert "$DB_HOST" in template_content or "$HOST" in template_content


def test_odoo_conf_mounted_in_container():
    """Valida que /etc/odoo/odoo.conf exista dentro del contenedor caryvil-web."""
    cmd = [
        "docker", "compose", "-f", "infra/compose/docker-compose.yml",
        "exec", "-T", "web", "cat", "/etc/odoo/odoo.conf"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Error al leer /etc/odoo/odoo.conf en el contenedor: {result.stderr}"

    conf_content = result.stdout
    assert "addons_path" in conf_content
    assert "proxy_mode = True" in conf_content
    assert "workers = 0" in conf_content


def test_odoo_conf_addons_path_includes_extra_addons():
    """Valida que la directiva addons_path incluya la ruta de módulos personalizados /mnt/extra-addons."""
    cmd = [
        "docker", "compose", "-f", "infra/compose/docker-compose.yml",
        "exec", "-T", "web", "cat", "/etc/odoo/odoo.conf"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0

    lines = result.stdout.splitlines()
    addons_line = next((item for item in lines if item.strip().startswith("addons_path")), None)
    assert addons_line is not None, "Directiva addons_path no encontrada en odoo.conf"
    assert "/mnt/extra-addons" in addons_line
    assert "/usr/lib/python3/dist-packages/odoo/addons" in addons_line


def test_odoo_conf_resource_and_worker_limits():
    """Valida las directivas de consumo de memoria, límites de tiempo de CPU y trabajadores."""
    cmd = [
        "docker", "compose", "-f", "infra/compose/docker-compose.yml",
        "exec", "-T", "web", "cat", "/etc/odoo/odoo.conf"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0

    conf_text = result.stdout
    assert "workers = 0" in conf_text
    assert "max_cron_threads = 1" in conf_text
    assert "limit_time_cpu = 120" in conf_text
    assert "limit_time_real = 240" in conf_text
    assert "limit_memory_soft = 671088640" in conf_text
    assert "limit_memory_hard = 805306368" in conf_text
    assert "log_level = info" in conf_text


def test_python_dependencies_import_and_execution():
    """Valida que las librerías num2words, phonenumbers, qrcode, psycopg2 y dotenv funcionen en el runtime."""
    python_eval_script = (
        "import num2words\n"
        "import phonenumbers\n"
        "import qrcode\n"
        "import psycopg2\n"
        "import dotenv\n"
        "text_num = num2words.num2words(123.45, lang='es')\n"
        "assert 'ciento' in text_num\n"
        "qr = qrcode.QRCode(box_size=10, border=4)\n"
        "qr.add_data('https://caryvil-erp.onrender.com')\n"
        "qr.make(fit=True)\n"
        "assert qr.modules_count > 0\n"
        "print('PYTHON_DEPS_OK')\n"
    )
    cmd = [
        "docker", "compose", "-f", "infra/compose/docker-compose.yml",
        "exec", "-T", "web", "python3", "-c", python_eval_script
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Error al validar dependencias Python: {result.stderr}"
    assert "PYTHON_DEPS_OK" in result.stdout


def test_http_proxy_mode_reverse_proxy_headers():
    """Valida que Odoo procese peticiones HTTP simulando el proxy inverso de Render (HTTPS / Forwarded).

    Comprueba que con proxy_mode = True, Odoo respeta X-Forwarded-Proto y X-Forwarded-Host
    generando redirecciones con esquema https:// y host adecuado.
    """
    class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
        def http_error_301(self, req, fp, code, msg, hdrs):
            return fp

        def http_error_302(self, req, fp, code, msg, hdrs):
            return fp

        def http_error_303(self, req, fp, code, msg, hdrs):
            return fp

        def http_error_307(self, req, fp, code, msg, hdrs):
            return fp

    opener = urllib.request.build_opener(NoRedirectHandler)
    url = "http://localhost:8069/"
    headers = {
        "User-Agent": "Caryvil-Render-Proxy-Test/1.0",
        "X-Forwarded-Proto": "https",
        "X-Forwarded-For": "190.86.100.25",
        "X-Forwarded-Host": "caryvil-erp.onrender.com",
    }
    req = urllib.request.Request(url, headers=headers)
    response = opener.open(req, timeout=10)

    code = response.status if hasattr(response, "status") else response.code
    assert code in [200, 301, 302, 303, 307], f"Código HTTP inesperado: {code}"

    if code in [301, 302, 303, 307]:
        location = response.headers.get("Location", "")
        assert location.startswith("https://caryvil-erp.onrender.com"), (
            f"El encabezado Location ({location}) no respeta el esquema HTTPS del proxy inverso"
        )


def test_custom_module_caryvil_erp_discoverable():
    """Valida que el módulo custom caryvil_erp sea accesible dentro del path /mnt/extra-addons."""
    cmd = [
        "docker", "compose", "-f", "infra/compose/docker-compose.yml",
        "exec", "-T", "web", "test", "-f", "/mnt/extra-addons/caryvil_erp/__manifest__.py"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, (
        f"El manifiesto de caryvil_erp no está presente en /mnt/extra-addons: {result.stderr}"
    )
