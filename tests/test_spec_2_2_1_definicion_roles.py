# -*- coding: utf-8 -*-
"""Suite de pruebas automatizadas para SPEC-2.2.1: Definición de Roles y Grupos de Usuarios.

Valida el cumplimiento exhaustivo de los criterios de aceptación y Definition of Done (DoD):
1. Estructura y sintaxis XML de security/caryvil_security.xml.
2. Definición y configuración de la categoría de módulo 'module_category_caryvil_erp'.
3. Definición de los 3 grupos de seguridad jerárquicos:
   - group_caryvil_cashier (Cajero / Dependiente de Mostrador)
   - group_caryvil_inventory_purchases (Encargado de Compras e Inventario)
   - group_caryvil_manager (Administrador / Propietario)
4. Herencia de privilegios (implied_ids) transitiva y cumplimiento del principio de mínimo privilegio.
5. Inclusión obligatoria de caryvil_security.xml en __manifest__.py (sección data).
6. Coherencia de referencias de grupos en ir.model.access.csv y users_roles_data.xml.
7. Existencia y registro de la suite de pruebas Odoo TransactionCase (test_caryvil_security.py).
"""

import ast
import csv
import os
import xml.etree.ElementTree as ET

MODULE_ROOT = os.path.join("custom_addons", "caryvil_erp")
SECURITY_XML_PATH = os.path.join(MODULE_ROOT, "security", "caryvil_security.xml")
MANIFEST_PATH = os.path.join(MODULE_ROOT, "__manifest__.py")
ACCESS_CSV_PATH = os.path.join(MODULE_ROOT, "security", "ir.model.access.csv")
USERS_DATA_PATH = os.path.join(MODULE_ROOT, "data", "users_roles_data.xml")


def _load_manifest_dict():
    """Carga y parsea el archivo __manifest__.py de forma segura usando AST."""
    assert os.path.exists(MANIFEST_PATH), f"No se encontró el archivo {MANIFEST_PATH}"
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    tree = ast.parse(content, filename=MANIFEST_PATH)
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Dict):
            return ast.literal_eval(node.value)
    raise ValueError(f"No se pudo extraer el diccionario del manifiesto en {MANIFEST_PATH}")


def _load_security_xml_records():
    """Parsea caryvil_security.xml y retorna un diccionario con los registros indexados por ID."""
    assert os.path.exists(SECURITY_XML_PATH), f"No se encontró el archivo {SECURITY_XML_PATH}"
    tree = ET.parse(SECURITY_XML_PATH)
    root = tree.getroot()
    records = {}
    for record in root.findall(".//record"):
        rec_id = record.get("id")
        rec_model = record.get("model")
        fields = {}
        for field in record.findall("field"):
            field_name = field.get("name")
            field_ref = field.get("ref")
            field_eval = field.get("eval")
            field_text = field.text.strip() if field.text else ""
            fields[field_name] = {
                "ref": field_ref,
                "eval": field_eval,
                "text": field_text,
            }
        records[rec_id] = {
            "model": rec_model,
            "fields": fields,
        }
    return records


def test_security_xml_exists_and_in_manifest():
    """Valida que caryvil_security.xml exista y esté registrado en la lista data de __manifest__.py."""
    assert os.path.isfile(SECURITY_XML_PATH), f"Falta el archivo {SECURITY_XML_PATH}"
    manifest = _load_manifest_dict()
    data_files = manifest.get("data", [])
    assert "security/caryvil_security.xml" in data_files, (
        "security/caryvil_security.xml debe estar declarado en data del manifiesto"
    )
    # Debe cargarse antes que ir.model.access.csv y vistas
    sec_index = data_files.index("security/caryvil_security.xml")
    if "security/ir.model.access.csv" in data_files:
        csv_index = data_files.index("security/ir.model.access.csv")
        assert sec_index < csv_index, "caryvil_security.xml debe cargarse antes que ir.model.access.csv"


def test_module_category_definition():
    """Valida la definición de la categoría ir.module.category para Farmacia Caryvil."""
    records = _load_security_xml_records()
    assert "module_category_caryvil_erp" in records, "Falta la categoría module_category_caryvil_erp"
    cat = records["module_category_caryvil_erp"]
    assert cat["model"] == "ir.module.category"
    assert cat["fields"]["name"]["text"] == "Farmacia Caryvil"
    assert "Gestión de niveles de acceso" in cat["fields"]["description"]["text"]
    assert cat["fields"]["sequence"]["text"] == "10"


def test_group_caryvil_cashier_definition():
    """Valida la definición del rol Cajero / Dependiente de Mostrador."""
    records = _load_security_xml_records()
    assert "group_caryvil_cashier" in records, "Falta el rol group_caryvil_cashier"
    group = records["group_caryvil_cashier"]
    assert group["model"] == "res.groups"
    assert group["fields"]["name"]["text"] == "Cajero / Dependiente de Mostrador"
    assert group["fields"]["category_id"]["ref"] == "module_category_caryvil_erp"
    assert "base.group_user" in group["fields"]["implied_ids"]["eval"]
    assert bool(group["fields"]["comment"]["text"])


def test_group_caryvil_inventory_purchases_definition():
    """Valida la definición del rol Encargado de Compras e Inventario y su herencia."""
    records = _load_security_xml_records()
    assert "group_caryvil_inventory_purchases" in records, "Falta el rol group_caryvil_inventory_purchases"
    group = records["group_caryvil_inventory_purchases"]
    assert group["model"] == "res.groups"
    assert group["fields"]["name"]["text"] == "Encargado de Compras e Inventario"
    assert group["fields"]["category_id"]["ref"] == "module_category_caryvil_erp"

    eval_str = group["fields"]["implied_ids"]["eval"]
    assert "group_caryvil_cashier" in eval_str, "Debe heredar el grupo de cajero"
    assert "stock.group_stock_user" in eval_str, "Debe heredar stock.group_stock_user"
    assert "purchase.group_purchase_user" in eval_str, "Debe heredar purchase.group_purchase_user"
    assert bool(group["fields"]["comment"]["text"])


def test_group_caryvil_manager_definition():
    """Valida la definición del rol Administrador / Propietario y su herencia total."""
    records = _load_security_xml_records()
    assert "group_caryvil_manager" in records, "Falta el rol group_caryvil_manager"
    group = records["group_caryvil_manager"]
    assert group["model"] == "res.groups"
    assert group["fields"]["name"]["text"] == "Administrador / Propietario"
    assert group["fields"]["category_id"]["ref"] == "module_category_caryvil_erp"

    eval_str = group["fields"]["implied_ids"]["eval"]
    assert "group_caryvil_inventory_purchases" in eval_str, "Debe heredar group_caryvil_inventory_purchases"
    assert "stock.group_stock_manager" in eval_str, "Debe heredar stock.group_stock_manager"
    assert "purchase.group_purchase_manager" in eval_str, "Debe heredar purchase.group_purchase_manager"
    assert "sales_team.group_sale_manager" in eval_str, "Debe heredar sales_team.group_sale_manager"
    assert bool(group["fields"]["comment"]["text"])


def test_access_csv_consistency_with_groups():
    """Valida que ir.model.access.csv use los identificadores de grupo canónicos."""
    assert os.path.isfile(ACCESS_CSV_PATH), f"Falta el archivo {ACCESS_CSV_PATH}"
    valid_caryvil_groups = {
        "group_caryvil_cashier",
        "group_caryvil_inventory_purchases",
        "group_caryvil_manager",
        "base.group_user",
        "base.group_system",
    }
    with open(ACCESS_CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            group = row["group_id:id"].strip()
            if group:
                assert group in valid_caryvil_groups, f"Grupo '{group}' en ir.model.access.csv no es válido o canónico"


def test_users_roles_data_consistency():
    """Valida que los usuarios semilla de demostración usen los grupos canónicos."""
    assert os.path.isfile(USERS_DATA_PATH), f"Falta el archivo {USERS_DATA_PATH}"
    tree = ET.parse(USERS_DATA_PATH)
    root = tree.getroot()

    demo_users = root.findall(".//record[@model='res.users']")
    assert len(demo_users) >= 3, "Deben existir al menos 3 usuarios semilla para los 3 roles"

    for user in demo_users:
        groups_field = user.find("field[@name='groups_id']")
        assert groups_field is not None, f"El usuario {user.get('id')} debe tener configurado groups_id"
        eval_val = groups_field.get("eval", "")
        has_valid_group = (
            "group_caryvil_cashier" in eval_val
            or "group_caryvil_inventory_purchases" in eval_val
            or "group_caryvil_manager" in eval_val
        )
        assert has_valid_group, f"El usuario {user.get('id')} no tiene un grupo canónico de Caryvil asignado"


def test_odoo_unit_test_suite_presence():
    """Valida que el archivo de pruebas unitarias Odoo test_caryvil_security.py exista y esté importado."""
    test_file = os.path.join(MODULE_ROOT, "tests", "test_caryvil_security.py")
    test_init = os.path.join(MODULE_ROOT, "tests", "__init__.py")

    assert os.path.isfile(test_file), f"Falta el archivo de pruebas {test_file}"
    assert os.path.isfile(test_init), f"Falta el archivo {test_init}"

    with open(test_init, "r", encoding="utf-8") as f:
        init_content = f.read()
    assert "test_caryvil_security" in init_content, "test_caryvil_security debe ser importado en tests/__init__.py"


def test_menu_security_restrictions():
    """Valida que los menús de Compras, Configuración y Dashboard estén protegidos por grupos."""
    menus_file = os.path.join(MODULE_ROOT, "views", "caryvil_menus.xml")
    assert os.path.isfile(menus_file)
    tree = ET.parse(menus_file)
    root = tree.getroot()

    menus_by_id = {elem.get("id"): elem for elem in root.findall(".//menuitem")}

    # Compras y Proveedores debe estar restringido a compras e inventario
    assert "menu_caryvil_compras" in menus_by_id
    assert menus_by_id["menu_caryvil_compras"].get("groups") == "caryvil_erp.group_caryvil_inventory_purchases"

    # Dashboard y Configuración deben estar restringidos al administrador
    assert "menu_caryvil_dashboard" in menus_by_id
    assert menus_by_id["menu_caryvil_dashboard"].get("groups") == "caryvil_erp.group_caryvil_manager"

    assert "menu_caryvil_configuracion" in menus_by_id
    assert menus_by_id["menu_caryvil_configuracion"].get("groups") == "caryvil_erp.group_caryvil_manager"

    # Validar también menu_caryvil_proveedores en res_partner_vendor_views.xml
    vendor_views_file = os.path.join(MODULE_ROOT, "views", "res_partner_vendor_views.xml")
    assert os.path.isfile(vendor_views_file)
    tree_vendor = ET.parse(vendor_views_file)
    vendor_menus = {elem.get("id"): elem for elem in tree_vendor.findall(".//menuitem")}
    assert "menu_caryvil_proveedores" in vendor_menus
    assert vendor_menus["menu_caryvil_proveedores"].get("groups") == "caryvil_erp.group_caryvil_inventory_purchases"

