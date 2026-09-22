# -*- coding: utf-8 -*-
"""Suite de pruebas automatizadas para SPEC-2.1.1: Estructura del Módulo Personalizado caryvil_erp.

Valida el cumplimiento exhaustivo de criterios de aceptación y Definition of Done (DoD):
1. Integridad del andamiaje de directorios estándar de Odoo (models, views, security, data, etc.).
2. Validez sintáctica y completitud del archivo manifiesto (__manifest__.py).
3. Declaración de dependencias base obligatorias (base, contacts, stock, purchase, sale_management, account).
4. Configuración de flags de aplicación principal (installable=True, application=True).
5. Existencia y sintaxis de los archivos de inicialización (__init__.py).
6. Definición correcta del menú raíz y submenús en views/caryvil_menus.xml.
7. Presencia y validez técnica de los assets visuales (icon.png e index.html).
8. Consistencia de archivos declarados en el manifiesto con el sistema de archivos.
"""

import ast
import os
import xml.etree.ElementTree as ET
from PIL import Image

MODULE_ROOT = os.path.join("custom_addons", "caryvil_erp")


def _load_manifest_dict():
    """Carga y parsea el archivo __manifest__.py de forma segura usando AST."""
    manifest_path = os.path.join(MODULE_ROOT, "__manifest__.py")
    assert os.path.exists(manifest_path), f"No se encontró el archivo {manifest_path}"
    with open(manifest_path, "r", encoding="utf-8") as f:
        content = f.read()
    tree = ast.parse(content, filename=manifest_path)
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Dict):
            return ast.literal_eval(node.value)
    raise ValueError(f"No se pudo extraer el diccionario del manifiesto en {manifest_path}")


def test_standard_directory_scaffolding():
    """Valida que todos los directorios estándar de la arquitectura de Odoo estén presentes."""
    expected_dirs = [
        "models",
        "views",
        "security",
        "data",
        "reports",
        "static",
        "static/description",
        "static/src",
        "demo",
        "controllers",
        "wizards",
        "tests",
    ]
    for rel_dir in expected_dirs:
        dir_path = os.path.join(MODULE_ROOT, rel_dir.replace("/", os.sep))
        assert os.path.isdir(dir_path), f"El directorio requerido '{rel_dir}' no existe en {MODULE_ROOT}"


def test_init_files_presence_and_syntax():
    """Valida la presencia y sintaxis de los archivos __init__.py en la raíz y submódulos Python."""
    init_paths = [
        os.path.join(MODULE_ROOT, "__init__.py"),
        os.path.join(MODULE_ROOT, "models", "__init__.py"),
        os.path.join(MODULE_ROOT, "controllers", "__init__.py"),
        os.path.join(MODULE_ROOT, "wizards", "__init__.py"),
        os.path.join(MODULE_ROOT, "tests", "__init__.py"),
    ]
    for init_file in init_paths:
        assert os.path.isfile(init_file), f"Falta el archivo {init_file}"
        with open(init_file, "r", encoding="utf-8") as f:
            content = f.read()
        # Verificar que sea código Python sintácticamente válido
        ast.parse(content, filename=init_file)


def test_manifest_metadata_and_flags():
    """Valida que los metadatos requeridos y las banderas de aplicación estén configurados en __manifest__.py."""
    manifest = _load_manifest_dict()

    assert manifest.get("name") == "Farmacia Caryvil ERP", "Nombre del módulo incorrecto"
    assert "17.0" in manifest.get("version", ""), "La versión debe apuntar al ciclo Odoo 17.0"
    assert manifest.get("category") == "Pharmacy/ERP", "Categoría del módulo incorrecta"
    assert manifest.get("license") == "LGPL-3", "La licencia debe ser LGPL-3"
    assert manifest.get("installable") is True, "El módulo debe tener 'installable': True"
    assert manifest.get("application") is True, "El módulo debe tener 'application': True para ser app principal"
    assert manifest.get("auto_install") is False, "El módulo debe tener 'auto_install': False"
    assert bool(manifest.get("summary")), "El resumen (summary) no debe estar vacío"
    assert bool(manifest.get("description")), "La descripción (description) no debe estar vacía"


def test_manifest_required_dependencies():
    """Valida que todas las dependencias base requeridas por el spec estén presentes."""
    manifest = _load_manifest_dict()
    depends = manifest.get("depends", [])

    required_modules = [
        "base",
        "contacts",
        "stock",
        "purchase",
        "sale_management",
        "account",
    ]
    for req in required_modules:
        assert req in depends, f"El módulo '{req}' es obligatorio en la lista 'depends' del manifiesto"


def test_manifest_declared_data_files_exist():
    """Valida que todos los archivos listados en 'data' y 'demo' existan físicamente en el disco."""
    manifest = _load_manifest_dict()
    data_files = manifest.get("data", []) + manifest.get("demo", [])

    for rel_path in data_files:
        full_path = os.path.join(MODULE_ROOT, rel_path.replace("/", os.sep))
        assert os.path.isfile(full_path), f"El archivo declarado en el manifiesto '{rel_path}' no existe en {full_path}"


def test_root_menu_xml_structure():
    """Valida que views/caryvil_menus.xml defina el menú raíz de Farmacia Caryvil y sus submenús."""
    menus_file = os.path.join(MODULE_ROOT, "views", "caryvil_menus.xml")
    assert os.path.isfile(menus_file), f"No se encontró {menus_file}"

    tree = ET.parse(menus_file)
    root = tree.getroot()

    # Buscar menú raíz
    root_menus = [
        elem for elem in root.iter("menuitem")
        if elem.get("id") == "menu_caryvil_root"
    ]
    assert len(root_menus) == 1, "Debe existir exactamente un menú con id='menu_caryvil_root'"
    root_menu = root_menus[0]

    assert root_menu.get("name") == "Farmacia Caryvil"
    assert "caryvil_erp,static/description/icon.png" in root_menu.get("web_icon", "")

    # Validar existencia de submenús clave
    menu_ids = [elem.get("id") for elem in root.iter("menuitem")]
    assert "menu_caryvil_inventario" in menu_ids or "menu_caryvil_dashboard" in menu_ids
    assert "menu_caryvil_ventas" in menu_ids or "menu_caryvil_compras" in menu_ids


def test_static_description_icon_and_index():
    """Valida que icon.png e index.html existan en static/description/ y sean válidos."""
    icon_path = os.path.join(MODULE_ROOT, "static", "description", "icon.png")
    index_path = os.path.join(MODULE_ROOT, "static", "description", "index.html")

    assert os.path.isfile(icon_path), f"El icono {icon_path} no existe"
    assert os.path.isfile(index_path), f"La descripción HTML {index_path} no existe"

    # Validar formato y dimensiones de la imagen PNG
    with Image.open(icon_path) as img:
        assert img.format == "PNG", f"El icono debe ser formato PNG, encontrado: {img.format}"
        width, height = img.size
        assert width >= 128 and height >= 128, f"Dimensiones mínimas 128x128, encontradas: {width}x{height}"


def test_security_scaffolding_files():
    """Valida la presencia y estructura básica de los archivos de seguridad."""
    sec_xml = os.path.join(MODULE_ROOT, "security", "caryvil_security.xml")
    sec_csv = os.path.join(MODULE_ROOT, "security", "ir.model.access.csv")

    assert os.path.isfile(sec_xml), f"Falta {sec_xml}"
    assert os.path.isfile(sec_csv), f"Falta {sec_csv}"

    # Validar sintaxis XML de seguridad
    ET.parse(sec_xml)

    # Validar cabeceras CSV de seguridad
    with open(sec_csv, "r", encoding="utf-8") as f:
        header_line = f.readline().strip()
    expected_header = "id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink"
    assert header_line == expected_header, f"Cabecera CSV incorrecta: {header_line}"
