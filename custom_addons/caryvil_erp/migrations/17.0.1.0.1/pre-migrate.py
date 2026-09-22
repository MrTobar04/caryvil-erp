# -*- coding: utf-8 -*-
"""Script de pre-migración para SPEC-2.2.1: Sincronización de XML IDs de grupos de seguridad.

Mapea los identificadores XML previos en ir_model_data hacia los identificadores
canónicos de SPEC-2.2.1 para evitar la colisión con la restricción de unicidad
res_groups_name_uniq de PostgreSQL.
"""


def migrate(cr, version):
    if not version:
        return

    # 1. Renombrar XML IDs existentes de grupos en ir_model_data
    cr.execute("""
        UPDATE ir_model_data
        SET name = 'group_caryvil_cashier'
        WHERE module = 'caryvil_erp' AND name = 'group_caryvil_cajero';

        UPDATE ir_model_data
        SET name = 'group_caryvil_inventory_purchases'
        WHERE module = 'caryvil_erp' AND name = 'group_caryvil_compras_inventario';

        UPDATE ir_model_data
        SET name = 'group_caryvil_manager'
        WHERE module = 'caryvil_erp' AND name = 'group_caryvil_admin';
    """)

    # 2. Si el grupo ya existía en base de datos pero no estaba vinculado al nuevo ID, vincularlo
    cr.execute("""
        INSERT INTO ir_model_data (name, module, model, res_id, noupdate)
        SELECT 'group_caryvil_inventory_purchases', 'caryvil_erp', 'res.groups', g.id, false
        FROM res_groups g
        WHERE (g.name->>'en_US' = 'Encargado de Compras e Inventario' OR g.name->>'es_ES' = 'Encargado de Compras e Inventario')
          AND NOT EXISTS (
              SELECT 1 FROM ir_model_data
              WHERE module = 'caryvil_erp' AND name = 'group_caryvil_inventory_purchases'
          )
        LIMIT 1;

        INSERT INTO ir_model_data (name, module, model, res_id, noupdate)
        SELECT 'group_caryvil_cashier', 'caryvil_erp', 'res.groups', g.id, false
        FROM res_groups g
        WHERE (g.name->>'en_US' LIKE '%Cajero%' OR g.name->>'es_ES' LIKE '%Cajero%')
          AND NOT EXISTS (
              SELECT 1 FROM ir_model_data
              WHERE module = 'caryvil_erp' AND name = 'group_caryvil_cashier'
          )
        LIMIT 1;

        INSERT INTO ir_model_data (name, module, model, res_id, noupdate)
        SELECT 'group_caryvil_manager', 'caryvil_erp', 'res.groups', g.id, false
        FROM res_groups g
        WHERE (g.name->>'en_US' LIKE '%Administrador%' OR g.name->>'es_ES' LIKE '%Administrador%')
          AND NOT EXISTS (
              SELECT 1 FROM ir_model_data
              WHERE module = 'caryvil_erp' AND name = 'group_caryvil_manager'
          )
        LIMIT 1;
    """)
