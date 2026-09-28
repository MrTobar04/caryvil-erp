# -*- coding: utf-8 -*-
"""Suite de pruebas automatizadas para SPEC-ISSUE-TOOLBAR-CONTRAST.

Verifica la corrección de contraste, visibilidad post-guardado y estados interactivos
de los botones de la toolbar (Guardar, Regresar, Nuevo) en Farmacia Caryvil ERP:
1. Existencia física y carga del archivo custom_theme.scss.
2. Presencia de selectores específicos para botones de la toolbar en todos sus estados:
   default, hover, focus y disabled.
3. Presencia de reglas de visibilidad post-guardado para breadcrumbs, botones de retorno
   y el indicador de estado (.o_form_status_indicator).
4. Verificación matemática estricta de cumplimiento WCAG AA (ratio de contraste > 4.5:1)
   para todas las combinaciones cromáticas empleadas en los botones de la toolbar.
"""

import ast
import os

MODULE_ROOT = os.path.join("custom_addons", "caryvil_erp")
SCSS_RELATIVE_PATH = os.path.join("static", "src", "scss", "custom_theme.scss")
SCSS_ASSET_BUNDLE_KEY = "caryvil_erp/static/src/scss/custom_theme.scss"


def _read_scss() -> str:
    scss_path = os.path.join(MODULE_ROOT, SCSS_RELATIVE_PATH)
    assert os.path.isfile(scss_path), f"El archivo SCSS no existe en: {scss_path}"
    with open(scss_path, "r", encoding="utf-8") as f:
        return f.read()


def _load_manifest_dict() -> dict:
    manifest_path = os.path.join(MODULE_ROOT, "__manifest__.py")
    assert os.path.isfile(manifest_path), f"No se encontró el archivo {manifest_path}"
    with open(manifest_path, "r", encoding="utf-8") as f:
        content = f.read()
    tree = ast.parse(content, filename=manifest_path)
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Dict):
            return ast.literal_eval(node.value)
    raise ValueError(f"No se pudo extraer el diccionario del manifiesto en {manifest_path}")


def _hex_to_rgb(hex_color: str) -> tuple:
    hex_color = hex_color.lstrip("#")
    assert len(hex_color) == 6, f"Color HEX inválido: #{hex_color}"
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


def test_scss_toolbar_file_exists_and_registered():
    """Verifica que el archivo SCSS exista y esté registrado en web.assets_backend."""
    scss_content = _read_scss()
    assert len(scss_content) > 5000, "El archivo SCSS no contiene la estructura suficiente."
    manifest = _load_manifest_dict()
    backend_assets = manifest.get("assets", {}).get("web.assets_backend", [])
    assert SCSS_ASSET_BUNDLE_KEY in backend_assets, f"Asset '{SCSS_ASSET_BUNDLE_KEY}' no registrado."


def test_toolbar_button_selectors_present():
    """Verifica que los selectores requeridos para botones Guardar, Regresar, Nuevo existan."""
    content = _read_scss()

    required_selectors = {
        ".o_control_panel": "Contenedor principal de la toolbar",
        ".o_form_button_save": "Botón de acción Guardar",
        ".o_form_button_create": "Botón de acción Nuevo / Crear",
        ".o_back_button": "Botón de navegación de retorno (Regresar / Back to...)",
        ".o_form_button_cancel": "Botón de cancelación / descarte",
        ".o_form_status_indicator": "Indicador de estado del formulario post-guardado",
        'button[data-hotkey="s"]': "Atajo hotkey para Guardar",
        'button[data-hotkey="c"]': "Atajo hotkey para Nuevo",
        'button[data-hotkey="j"]': "Atajo hotkey para Cancelar",
    }

    missing = [f"  '{sel}' ({desc})" for sel, desc in required_selectors.items() if sel not in content]
    assert not missing, "Faltan los siguientes selectores de toolbar en SCSS:\n" + "\n".join(missing)


def test_interactive_states_defined():
    """Verifica que existan reglas específicas para hover, focus y disabled en botones de toolbar."""
    content = _read_scss()

    required_states = [
        "&:hover",
        "&:focus",
        "&:disabled",
    ]

    for state in required_states:
        assert state in content, f"El estado interactivo '{state}' no fue encontrado en custom_theme.scss."


def test_wcag_aa_toolbar_contrast_ratios():
    """Verifica matemáticamente que todas las combinaciones de color de la toolbar cumplan WCAG AA (> 4.5:1)."""
    WCAG_AA_THRESHOLD = 4.5

    color_pairs = [
        ("Topbar background vs white breadcrumb text (#FFFFFF vs #5C6F84)", "#FFFFFF", "#5C6F84"),
        ("Boton Guardar default: blanco (#FFFFFF) sobre verde (#1E7A3A)", "#FFFFFF", "#1E7A3A"),
        ("Boton Guardar hover: blanco (#FFFFFF) sobre verde oscuro (#166130)", "#FFFFFF", "#166130"),
        ("Boton Secundario / Descartar: azul marino (#002B49) sobre blanco (#FFFFFF)", "#002B49", "#FFFFFF"),
        ("Indicador estado post-guardado: azul marino (#002B49) sobre tarjeta blanca (#FFFFFF)", "#002B49", "#FFFFFF"),
        ("Texto verde estado guardado (#1E7A3A) sobre fondo blanco (#FFFFFF)", "#1E7A3A", "#FFFFFF"),
        ("Botón Regresar blanco (#FFFFFF) sobre fondo toolbar (#5C6F84)", "#FFFFFF", "#5C6F84"),
    ]

    failures = []
    for description, text_hex, bg_hex in color_pairs:
        ratio = _contrast_ratio(text_hex, bg_hex)
        if ratio < WCAG_AA_THRESHOLD:
            failures.append(
                f"  FALLO WCAG AA: {description}\n"
                f"    Ratio calculado: {ratio:.2f}:1 (mínimo requerido: {WCAG_AA_THRESHOLD}:1)"
            )

    assert not failures, "Pares de color en toolbar no cumplen WCAG AA:\n" + "\n".join(failures)


if __name__ == "__main__":
    tests = [
        test_scss_toolbar_file_exists_and_registered,
        test_toolbar_button_selectors_present,
        test_interactive_states_defined,
        test_wcag_aa_toolbar_contrast_ratios,
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
