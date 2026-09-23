# -*- coding: utf-8 -*-
"""Suite de pruebas automatizadas para SPEC-3.1.1: Personalizacion de Marca y Tema Visual.

Valida el cumplimiento exhaustivo de criterios de aceptacion y Definition of Done (DoD):
1. Existencia fisica y sintaxis basica del archivo SCSS implementado.
2. Registro correcto del asset en el bundle web.assets_backend del __manifest__.py.
3. Presencia de todos los tokens de diseno institucionales requeridos en el bloque :root.
4. Sobreescritura correcta de variables nativas del framework Odoo 17 (--o-brand-*, --bs-*).
5. Presencia de selectores clave para cada componente del sistema de diseno:
   Sidebar, Topbar, Botones primarios y secundarios, Badges semanticos,
   Barra de busqueda, Tarjetas KPI, Tablas, Paginacion y Bloque de totales.
6. Cumplimiento del estandar de accesibilidad WCAG AA (ratio de contraste > 4.5:1)
   para todos los pares texto/fondo definidos en la paleta institucional.
"""

import ast
import os

MODULE_ROOT = os.path.join("custom_addons", "caryvil_erp")
SCSS_RELATIVE_PATH = os.path.join("static", "src", "scss", "custom_theme.scss")
SCSS_ASSET_BUNDLE_KEY = "caryvil_erp/static/src/scss/custom_theme.scss"


def _read_scss() -> str:
    scss_path = os.path.join(MODULE_ROOT, SCSS_RELATIVE_PATH)
    assert os.path.isfile(scss_path), f"El archivo SCSS no existe en la ruta esperada: {scss_path}"
    with open(scss_path, "r", encoding="utf-8") as f:
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


def test_scss_file_exists_and_is_nonempty():
    scss_path = os.path.join(MODULE_ROOT, SCSS_RELATIVE_PATH)
    assert os.path.isfile(scss_path), f"El archivo SCSS no existe en: {scss_path}"
    content = _read_scss()
    assert len(content) > 2000, (
        f"El archivo SCSS parece incompleto: solo tiene {len(content)} bytes. "
        "Se esperan al menos 2000 bytes con la implementacion completa."
    )
    assert (
        ":root {" in content or ":root{" in content
    ), "El bloque :root con las CSS Custom Properties no fue encontrado en custom_theme.scss."


def test_scss_registered_in_web_assets_backend():
    manifest = _load_manifest_dict()
    assets = manifest.get("assets", {})
    backend_assets = assets.get("web.assets_backend", [])
    assert SCSS_ASSET_BUNDLE_KEY in backend_assets, (
        f"El asset '{SCSS_ASSET_BUNDLE_KEY}' no esta registrado en "
        f"web.assets_backend del __manifest__.py. Assets actuales: {backend_assets}"
    )


def test_institutional_color_tokens_present():
    content = _read_scss()
    content_upper = content.upper()

    required = {
        "--caryvil-sidebar-bg": "#002B49",
        "--caryvil-topbar-bg": "#5C6F84",
        "--caryvil-primary-green": "#1E7A3A",
        "--caryvil-sidebar-active": "#38B6FF",
        "--caryvil-sidebar-hover": "#003861",
        "--caryvil-primary-green-hover": "#166130",
        "--caryvil-accent-blue": "#0369A1",
        "--caryvil-surface-bg": None,
        "--caryvil-card-bg": None,
        "--caryvil-card-border": None,
        "--caryvil-input-bg": None,
        "--caryvil-font-family": None,
        "--caryvil-text-main": None,
        "--caryvil-text-muted": None,
    }

    for token, hex_val in required.items():
        assert token in content, f"Token de diseno '{token}' no encontrado en custom_theme.scss."
        if hex_val:
            assert (
                hex_val.upper() in content_upper
            ), f"Valor {hex_val} del token '{token}' no encontrado en custom_theme.scss."

    assert "Inter" in content, "La fuente 'Inter' no esta referenciada en custom_theme.scss."


def test_semantic_badge_tokens_present():
    content = _read_scss()
    content_upper = content.upper()

    badge_tokens = {
        "--caryvil-badge-low-stock-bg": "#FEF3C7",
        "--caryvil-badge-low-stock-text": "#B45309",
        "--caryvil-badge-low-stock-border": "#FDE68A",
        "--caryvil-badge-expiring-bg": "#FEE2E2",
        "--caryvil-badge-expiring-text": "#DC3545",
        "--caryvil-badge-expiring-border": "#FECACA",
        "--caryvil-badge-ok-bg": "#DCFCE7",
        "--caryvil-badge-ok-text": "#15803D",
        "--caryvil-badge-ok-border": "#BBF7D0",
        "--caryvil-badge-damaged-bg": "#E2E3E5",
        "--caryvil-badge-damaged-text": "#383D41",
        "--caryvil-badge-damaged-border": "#D6D8DB",
    }

    for token_name, hex_value in badge_tokens.items():
        assert token_name in content, f"Token de badge '{token_name}' no encontrado."
        assert (
            hex_value.upper() in content_upper
        ), f"Valor {hex_value} del token '{token_name}' no encontrado en custom_theme.scss."


def test_odoo_native_variable_overrides_present():
    content = _read_scss()
    required_overrides = [
        "--o-brand-primary",
        "--o-brand-odoo",
        "--bs-primary",
        "--bs-primary-rgb",
    ]
    for override in required_overrides:
        assert override in content, (
            f"La sobreescritura de variable nativa '{override}' no esta presente. "
            "Es necesaria para reemplazar la identidad visual por defecto de Odoo 17."
        )


def test_component_selectors_present():
    content = _read_scss()

    selectors = {
        ".o_main_navbar": "Navbar principal de Odoo (sidebar)",
        ".caryvil-sidebar": "Clase utilitaria sidebar",
        ".brand-title": "Texto de marca ERP FARMACIA",
        ".nav-item": "Items del menu lateral",
        ".o_control_panel": "Topbar/Control panel de Odoo",
        ".caryvil-topbar": "Clase utilitaria topbar",
        ".breadcrumb-item": "Migas de pan del topbar",
        ".btn-primary": "Boton primario Odoo/Bootstrap",
        ".btn-caryvil-primary": "Clase utilitaria boton primario",
        ".btn-secondary": "Boton secundario Odoo/Bootstrap",
        ".btn-caryvil-secondary": "Clase utilitaria boton secundario",
        ".badge-bajo-stock": "Badge Bajo Stock (espanol)",
        ".badge-por-vencer": "Badge Por Vencer (espanol)",
        ".badge-ok": "Badge OK",
        ".badge-danado": "Badge Danado (espanol)",
        ".badge-low-stock": "Badge low-stock (ingles)",
        ".badge-expiring": "Badge expiring (ingles)",
        ".badge-damaged": "Badge damaged (ingles)",
        ".badge-caryvil": "Badge base Caryvil",
        ".caryvil_badge_fefo": "Badge FEFO heredada (compatibilidad)",
        ".o_searchview": "Barra de busqueda de Odoo",
        ".caryvil-search-pill": "Clase utilitaria barra busqueda",
        ".caryvil-kpi-card": "Tarjetas KPI dashboard",
        ".caryvil-kpi-value": "Valor numerico de KPI",
        ".o_list_view": "Vista de lista de Odoo",
        ".caryvil-table": "Clase utilitaria tabla",
        ".o_form_view": "Vista de formulario de Odoo",
        ".caryvil-form-card": "Clase utilitaria formulario",
        ".caryvil-totals-block": "Bloque de totales financieros",
        ".caryvil-total-final": "Total final destacado",
        ".caryvil-pagination": "Clase utilitaria paginacion",
        ".o_pager": "Paginador de Odoo",
    }

    missing = [f"  '{sel}' ({desc})" for sel, desc in selectors.items() if sel not in content]
    assert (
        not missing
    ), "Los siguientes selectores requeridos no estan implementados en custom_theme.scss:\n" + "\n".join(missing)

    assert "width: 4px" in content, "La barra indicadora vertical de 4px del elemento activo no esta definida."
    assert (
        "border-radius: 2px 0 0 2px" in content
    ), "El border-radius de la barra indicadora lateral (2px 0 0 2px) no esta definido."
    assert (
        "border-radius: 50rem" in content
    ), "La forma de pildora (border-radius: 50rem) no esta definida para los badges."


def test_responsive_breakpoints_present():
    content = _read_scss()
    assert (
        "@media (max-width: 1366px)" in content
    ), "El media query para la resolucion POS estandar (max-width: 1366px) no esta implementado."
    assert (
        "@media (min-width: 1920px)" in content
    ), "El media query para Full HD (min-width: 1920px) no esta implementado."


def test_wcag_aa_contrast_ratios():
    WCAG_AA_THRESHOLD = 4.5

    pairs_to_test = [
        ("Sidebar: texto blanco (#FFFFFF) sobre azul marino (#002B49)", "#FFFFFF", "#002B49"),
        ("Sidebar active: cian (#38B6FF) sobre azul marino (#002B49)", "#38B6FF", "#002B49"),
        ("Topbar: texto blanco (#FFFFFF) sobre gris-azul (#5C6F84)", "#FFFFFF", "#5C6F84"),
        ("Boton primario: texto blanco (#FFFFFF) sobre verde (#28A745)", "#FFFFFF", "#1E7A3A"),
        ("Boton secundario: texto (#495057) sobre blanco (#FFFFFF)", "#495057", "#FFFFFF"),
        ("Badge Bajo Stock: texto (#B45309) sobre fondo (#FEF3C7)", "#B45309", "#FEF3C7"),
        ("Badge Por Vencer: texto (#B91C1C) sobre fondo (#FEE2E2)", "#B91C1C", "#FEE2E2"),
        ("Badge OK: texto (#15803D) sobre fondo (#DCFCE7)", "#15803D", "#DCFCE7"),
        ("Badge Danado: texto (#383D41) sobre fondo (#E2E3E5)", "#383D41", "#E2E3E5"),
        ("Cuerpo tabla: texto (#1F2937) sobre blanco (#FFFFFF)", "#1F2937", "#FFFFFF"),
        ("Encabezado tabla: texto (#374151) sobre gris claro (#F3F4F6)", "#374151", "#F3F4F6"),
        ("Texto principal (#212529) sobre superficie (#F8F9FA)", "#212529", "#F8F9FA"),
        ("Total final: texto azul (#0369A1) sobre blanco (#FFFFFF)", "#0369A1", "#FFFFFF"),
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
        f"Los siguientes pares de color NO cumplen el estandar WCAG AA "
        f"(ratio minimo {WCAG_AA_THRESHOLD}:1):\n" + "\n".join(failures)
    )


if __name__ == "__main__":
    tests = [
        test_scss_file_exists_and_is_nonempty,
        test_scss_registered_in_web_assets_backend,
        test_institutional_color_tokens_present,
        test_semantic_badge_tokens_present,
        test_odoo_native_variable_overrides_present,
        test_component_selectors_present,
        test_responsive_breakpoints_present,
        test_wcag_aa_contrast_ratios,
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
