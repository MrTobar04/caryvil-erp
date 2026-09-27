# -*- coding: utf-8 -*-
"""Suite de pruebas estáticas para SPEC-4.2.2: Dashboard de Alertas de Vencimiento de Lotes.

Valida:
1. Métodos backend en `caryvil_dashboard.py` (get_expiring_lots_data, action_view_lot_traceability, etc.).
2. Integración en el componente JS OWL `caryvil_sales_dashboard.js`.
3. Presencia de tarjetas de conteo tripartito (<30d, 31-60d, 61-90d) y tabla en `caryvil_sales_dashboard.xml`.
4. Estilos SCSS en `caryvil_sales_dashboard.scss`.
5. Cobertura de pruebas en `test_caryvil_dashboard.py` para los escenarios AC-1, AC-2 y AC-3.
"""

import ast
import os

MODULE_ROOT = os.path.join("custom_addons", "caryvil_erp")


def test_backend_methods_exist_in_dashboard_model():
    """Valida que los métodos de backend requeridos para SPEC-4.2.2 estén definidos en caryvil_dashboard.py."""
    file_path = os.path.join(MODULE_ROOT, "models", "caryvil_dashboard.py")
    assert os.path.exists(file_path), f"No existe el archivo {file_path}"

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    tree = ast.parse(content, filename=file_path)
    method_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            method_names.add(node.name)

    required_methods = {
        "get_expiring_lots_data",
        "action_view_lot_traceability",
        "action_transfer_to_quarantine",
    }
    for method in required_methods:
        assert method in method_names, f"El método '{method}' no está definido en {file_path}"


def test_js_component_includes_expiring_lots_logic():
    """Valida que caryvil_sales_dashboard.js llame a get_expiring_lots_data y gestione handlers de lote."""
    file_path = os.path.join(MODULE_ROOT, "static", "src", "js", "caryvil_sales_dashboard.js")
    assert os.path.exists(file_path), f"No existe el archivo {file_path}"

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "get_expiring_lots_data" in content
    assert "expiringLotsData" in content
    assert "onSelectLotTab" in content
    assert "onViewLotTraceability" in content
    assert "onTransferToQuarantine" in content


def test_xml_template_includes_expiring_lots_panel():
    """Valida que el template XML caryvil_sales_dashboard.xml contenga el panel visual de vencimiento de lotes."""
    file_path = os.path.join(MODULE_ROOT, "static", "src", "xml", "caryvil_sales_dashboard.xml")
    assert os.path.exists(file_path), f"No existe el archivo {file_path}"

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "panel_expiring_lots" in content
    assert "count_critical_30" in content
    assert "count_warning_60" in content
    assert "count_notice_90" in content
    assert "expiring_lots_table" in content
    assert "onTransferToQuarantine" in content
    assert "onViewLotTraceability" in content


def test_scss_styles_include_expiring_lots_rules():
    """Valida que caryvil_sales_dashboard.scss contenga las reglas CSS para el panel de vencimiento de lotes."""
    file_path = os.path.join(MODULE_ROOT, "static", "src", "scss", "caryvil_sales_dashboard.scss")
    assert os.path.exists(file_path), f"No existe el archivo {file_path}"

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "panel_expiring_lots" in content
    assert "expiring_cards_grid" in content
    assert "expiring_card" in content
    assert "lot_badge" in content


def test_unit_test_suite_covers_spec_4_2_2():
    """Valida que test_caryvil_dashboard.py contenga los test cases para SPEC-4.2.2 (Escenarios 1, 2 y 3)."""
    file_path = os.path.join(MODULE_ROOT, "tests", "test_caryvil_dashboard.py")
    assert os.path.exists(file_path), f"No existe el archivo {file_path}"

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "test_11_expiring_lots_tripartite_classification" in content
    assert "test_12_scenario_1_critical_expiring_lot" in content
    assert "test_13_scenario_2_exclusion_of_depleted_lots" in content
    assert "test_14_scenario_3_transfer_to_quarantine_action" in content
    assert "test_15_expiring_lots_access_control" in content
