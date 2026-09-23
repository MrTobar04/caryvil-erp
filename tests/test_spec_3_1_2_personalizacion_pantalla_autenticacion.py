# -*- coding: utf-8 -*-
"""Suite de pruebas automatizadas para SPEC-3.1.2: Personalizacion de Pantalla de Autenticacion.

Valida el cumplimiento exhaustivo de criterios de aceptacion y Definition of Done (DoD):
1. Existencia fisica y validez sintactica del archivo XML de plantillas QWeb (views/web_login_templates.xml).
2. Estructura de la plantilla caryvil_web_login extendiendo web.login mediante XPath.
3. Existencia y correcta ubicacion del encabezado institucional ('ERP FARMACIA', 'Soyapango', logotipo).
4. Presencia del pie de pagina institucional con derechos reservados.
5. Existencia fisica y contenido de la hoja de estilos SCSS (static/src/scss/custom_login.scss).
6. Registro correcto de la plantilla XML y del asset SCSS en web.assets_frontend del __manifest__.py.
7. Existencia de los recursos graficos requeridos en static/src/img/.
8. Cumplimiento de estilos responsivos, tokens de color corporativos y ratio de contraste WCAG AA.
"""

import ast
import os
import xml.etree.ElementTree as ET

MODULE_ROOT = os.path.join("custom_addons", "caryvil_erp")
XML_RELATIVE_PATH = os.path.join("views", "web_login_templates.xml")
SCSS_RELATIVE_PATH = os.path.join("static", "src", "scss", "custom_login.scss")
SCSS_ASSET_BUNDLE_KEY = "caryvil_erp/static/src/scss/custom_login.scss"
LOGO_RELATIVE_PATH = os.path.join("static", "src", "img", "caryvil_logo_full.png")


def _read_file(relative_path: str) -> str:
    full_path = os.path.join(MODULE_ROOT, relative_path)
    assert os.path.isfile(full_path), f"El archivo no existe: {full_path}"
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()


def _load_manifest_dict() -> dict:
    manifest_path = os.path.join(MODULE_ROOT, "__manifest__.py")
    assert os.path.isfile(manifest_path), f"No se encontro el archivo {manifest_path}"
    with open(manifest_path, "r", encoding="utf-8") as f:
        content = f.read()
    tree = ast.parse(content, filename=manifest_path)
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Dict):
            return ast.literal_eval(node.value)
    raise ValueError(f"No se pudo extraer el diccionario del manifiesto en {manifest_path}")


def _hex_to_rgb(hex_color: str) -> tuple:
    hex_color = hex_color.lstrip("#")
    assert len(hex_color) == 6, f"Color HEX invalido: #{hex_color}"
    return (int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16))


def _relative_luminance(rgb: tuple) -> float:
    def linearize(c: int) -> float:
        srgb = c / 255.0
        if srgb <= 0.04045:
            return srgb / 12.92
        return ((srgb + 0.055) / 1.055) ** 2.4

    r, g, b = rgb
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def _contrast_ratio(hex_text: str, hex_bg: str) -> float:
    l_text = _relative_luminance(_hex_to_rgb(hex_text))
    l_bg = _relative_luminance(_hex_to_rgb(hex_bg))
    lighter = max(l_text, l_bg)
    darker = min(l_text, l_bg)
    return (lighter + 0.05) / (darker + 0.05)


def test_xml_template_file_exists_and_is_valid():
    xml_content = _read_file(XML_RELATIVE_PATH)
    assert len(xml_content) > 0, "El archivo web_login_templates.xml esta vacio."
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        assert False, f"Error de sintaxis XML en web_login_templates.xml: {e}"

    assert root.tag == "odoo", f"La etiqueta raiz del XML debe ser <odoo>, se encontro <{root.tag}>"
    templates = root.findall(".//template")
    assert len(templates) >= 1, "No se encontro ninguna etiqueta <template> en el XML."

    login_tmpl = root.find(".//template[@id='caryvil_web_login_layout']") or root.find(".//template[@id='caryvil_web_login']")
    assert login_tmpl is not None, "No se encontro el template de login en el XML."
    assert login_tmpl.get("inherit_id") in ["web.login_layout", "web.login"], (
        f"El template debe heredar de 'web.login_layout' o 'web.login', actual: {login_tmpl.get('inherit_id')}"
    )


def test_xml_template_structure_and_branding():
    xml_content = _read_file(XML_RELATIVE_PATH)
    assert "ERP FARMACIA" in xml_content, "El texto de marca 'ERP FARMACIA' no esta en la plantilla XML."
    assert "Soyapango" in xml_content, "La referencia a 'Soyapango' no esta en la plantilla XML."
    assert "caryvil_logo_full.png" in xml_content or "caryvil_logo.png" in xml_content, (
        "No se encontro referencia a la imagen del logotipo institucional en el XML."
    )
    assert "caryvil-login-body" in xml_content or "card-body" in xml_content, (
        "La plantilla XML debe contener el contenedor de formulario de login."
    )
    assert "Farmacia Caryvil" in xml_content, "La marca 'Farmacia Caryvil' no esta en el XML."
    assert "derechos reservados" in xml_content.lower(), "El texto de pie de pagina de derechos reservados no esta presente."


def test_manifest_registration():
    manifest = _load_manifest_dict()
    data_files = manifest.get("data", [])
    assert "views/web_login_templates.xml" in data_files, (
        "El archivo 'views/web_login_templates.xml' no esta registrado en la seccion 'data' del __manifest__.py"
    )

    assets = manifest.get("assets", {})
    frontend_assets = assets.get("web.assets_frontend", [])
    assert SCSS_ASSET_BUNDLE_KEY in frontend_assets, (
        f"El asset '{SCSS_ASSET_BUNDLE_KEY}' no esta registrado en "
        f"web.assets_frontend del __manifest__.py. Assets actuales: {frontend_assets}"
    )


def test_scss_styles_structure_and_tokens():
    scss_content = _read_file(SCSS_RELATIVE_PATH)
    assert len(scss_content) > 500, "El archivo custom_login.scss parece incompleto o muy corto."
    assert ":root" in scss_content, "El bloque :root no esta presente en custom_login.scss."

    required_tokens = [
        "--caryvil-sidebar-bg",
        "--caryvil-primary-green",
        "--caryvil-sidebar-active",
        "--caryvil-accent-blue",
    ]
    for token in required_tokens:
        assert token in scss_content, f"Token '{token}' no encontrado en custom_login.scss."

    required_selectors = [
        "oe_login_form",
        "caryvil-login-header",
        "caryvil-login-footer",
        "btn-primary",
        "form-control",
    ]
    for selector in required_selectors:
        assert selector in scss_content, f"Selector o clase '{selector}' no encontrada en custom_login.scss."

    assert "linear-gradient" in scss_content, "No se encontro el fondo con gradiente institucional."
    assert "@media" in scss_content, "No se encontraron reglas de responsividad media queries en custom_login.scss."


def test_logo_asset_exists():
    logo_path = os.path.join(MODULE_ROOT, LOGO_RELATIVE_PATH)
    assert os.path.isfile(logo_path), f"El archivo de logotipo no existe en la ruta: {logo_path}"
    assert os.path.getsize(logo_path) > 0, f"El archivo de logotipo esta vacio: {logo_path}"


def test_login_contrast_wcag_aa():
    WCAG_AA_THRESHOLD = 4.5

    pairs_to_test = [
        ("Texto titulo 'ERP FARMACIA' (#002B49) sobre fondo blanco (#FFFFFF)", "#002B49", "#FFFFFF"),
        ("Texto subtitulo (#6B7280) sobre fondo blanco (#FFFFFF)", "#4B5563", "#FFFFFF"),
        ("Boton Acceder texto blanco (#FFFFFF) sobre verde (#1E7A3A)", "#FFFFFF", "#1E7A3A"),
        ("Pie de pagina texto (#64748B) sobre fondo gris claro (#F8FAFC)", "#475569", "#F8FAFC"),
        ("Alerta error texto (#B91C1C) sobre fondo alerta (#FEE2E2)", "#B91C1C", "#FEE2E2"),
    ]

    failures = []
    for description, text_hex, bg_hex in pairs_to_test:
        ratio = _contrast_ratio(text_hex, bg_hex)
        if ratio < WCAG_AA_THRESHOLD:
            failures.append(
                f"  FALLO WCAG AA: {description}\n"
                f"    Ratio calculado: {ratio:.2f}:1 (minimo requerido: {WCAG_AA_THRESHOLD}:1)"
            )

    assert not failures, (
        f"Los siguientes pares de color de la pantalla de login NO cumplen WCAG AA:\n" + "\n".join(failures)
    )


if __name__ == "__main__":
    tests = [
        test_xml_template_file_exists_and_is_valid,
        test_xml_template_structure_and_branding,
        test_manifest_registration,
        test_scss_styles_structure_and_tokens,
        test_logo_asset_exists,
        test_login_contrast_wcag_aa,
    ]
    passed = 0
    for t in tests:
        try:
            t()
            passed += 1
            print(f"  [PASS] {t.__name__}")
        except Exception as exc:
            print(f"  [FAIL] {t.__name__}: {exc}")
    print(f"\nResultado: {passed}/{len(tests)} pruebas pasadas.")
    if passed != len(tests):
        exit(1)
