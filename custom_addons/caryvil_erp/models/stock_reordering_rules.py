# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, ValidationError


class StockWarehouseOrderpointMedicine(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    suggested_replenishment_qty = fields.Float(
        string="Cantidad Sugerida a Comprar",
        compute="_compute_suggested_qty",
        store=False,
        help="Cantidad calculada automáticamente para alcanzar el nivel máximo objetivo, "
        "respetando el stock actual proyectado y los múltiplos de compra del proveedor.",
    )

    @api.depends(
        "product_id",
        "location_id",
        "product_min_qty",
        "product_max_qty",
        "qty_multiple",
    )
    def _compute_suggested_qty(self):
        for rule in self:
            if not rule.product_id or not rule.location_id:
                rule.suggested_replenishment_qty = 0.0
                continue

            # Evalúa el stock virtual proyectado considerando la ubicación específica del almacén
            virtual_stock = rule.product_id.with_context(location=rule.location_id.id).virtual_available

            if virtual_stock < rule.product_min_qty:
                needed = rule.product_max_qty - virtual_stock

                # Respetar el múltiplo de compra o lote mínimo si aplica (> 0)
                if rule.qty_multiple > 0:
                    remainder = needed % rule.qty_multiple
                    if remainder > 1e-6:
                        needed += rule.qty_multiple - remainder

                rule.suggested_replenishment_qty = max(needed, 0.0)
            else:
                rule.suggested_replenishment_qty = 0.0

    @api.constrains("product_min_qty", "product_max_qty")
    def _check_min_max_quantities(self):
        for rule in self:
            if rule.product_min_qty < 0:
                raise ValidationError(_("El stock mínimo de seguridad (Punto de Reorden) no puede ser negativo."))
            if rule.product_max_qty < rule.product_min_qty:
                raise ValidationError(
                    _(
                        "El nivel máximo objetivo (%(max).2f) no puede "
                        "ser inferior al stock mínimo de seguridad (%(min).2f)."
                    )
                    % {"max": rule.product_max_qty, "min": rule.product_min_qty}
                )

    @api.constrains("qty_multiple")
    def _check_qty_multiple(self):
        for rule in self:
            if rule.qty_multiple <= 0:
                raise ValidationError(
                    _("El múltiplo de compra / empaque debe ser " "un valor positivo estrictamente superior a 0.")
                )

    def _check_reordering_security(self):
        """Verifica que el usuario actual tenga permisos de gestión de inventario/compras o administrador."""
        if self.env.is_superuser() or self.env.su:
            return
        user = self.env.user
        is_inventory_purchases = user.has_group("caryvil_erp.group_caryvil_inventory_purchases")
        is_manager = user.has_group("caryvil_erp.group_caryvil_manager")
        if not (is_inventory_purchases or is_manager):
            raise AccessError(
                _(
                    "Solo los usuarios con rol 'Encargado de Compras e Inventario' o 'Administrador' "
                    "pueden configurar reglas de reabastecimiento."
                )
            )

    @api.model_create_multi
    def create(self, vals_list):
        self._check_reordering_security()
        return super().create(vals_list)

    def write(self, vals):
        self._check_reordering_security()
        return super().write(vals)

    def unlink(self):
        self._check_reordering_security()
        return super().unlink()

    def _get_vendor_for_rule(self, rule):
        product = rule.product_id
        vendor = rule.supplier_id
        seller = False
        if not vendor and product.seller_ids:
            seller = product.seller_ids[0]
            vendor = seller.partner_id

        if not vendor:
            return None, None

        if not (vendor.is_pharmacy_vendor or vendor.commercial_partner_id.is_pharmacy_vendor):
            return None, None

        return vendor, seller

    def _get_unit_price_for_vendor(self, product, vendor, seller):
        price_unit = 0.0
        if seller:
            price_unit = seller.price or seller.gross_price
        elif product.seller_ids:
            matching_sellers = product.seller_ids.filtered(lambda line: line.partner_id == vendor)
            if matching_sellers:
                price_unit = matching_sellers[0].price or matching_sellers[0].gross_price
        if not price_unit:
            price_unit = product.standard_price
        return price_unit

    def _get_or_create_draft_po(self, orders_by_vendor, vendor, company_id):
        if vendor.id not in orders_by_vendor:
            existing_po = self.env["purchase.order"].search(
                [
                    ("partner_id", "=", vendor.id),
                    ("state", "=", "draft"),
                    ("origin", "=", "Reabastecimiento Caryvil"),
                ],
                limit=1,
            )

            if not existing_po:
                existing_po = self.env["purchase.order"].create(
                    {
                        "partner_id": vendor.id,
                        "origin": "Reabastecimiento Caryvil",
                        "company_id": company_id or self.env.company.id,
                    }
                )
            orders_by_vendor[vendor.id] = existing_po
        return orders_by_vendor[vendor.id]

    def action_calculate_replenishment_caryvil(self):
        """
        Calcula el reorden de compras para medicamentos que están por debajo del mínimo,
        agrupando los pedidos sugeridos en Solicitudes de Presupuesto (RFQ) en estado borrador
        por cada proveedor habitual (cumpliendo Escenario 2 de SPEC-7.2.2).
        """
        self._check_reordering_security()

        rules = self if self else self.search([("active", "=", True)])
        rules_to_reorder = rules.filtered(lambda r: r.suggested_replenishment_qty > 0)

        if not rules_to_reorder:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Reabastecimiento Caryvil"),
                    "message": _("No hay medicamentos con existencias por debajo del stock mínimo."),
                    "type": "info",
                    "sticky": False,
                },
            }

        orders_by_vendor = {}

        for rule in rules_to_reorder:
            product = rule.product_id
            vendor, seller = self._get_vendor_for_rule(rule)
            if not vendor:
                continue

            po = self._get_or_create_draft_po(orders_by_vendor, vendor, rule.company_id.id)

            # Calcular cantidad en la unidad de medida de compra (uom_po_id)
            qty_stock = rule.suggested_replenishment_qty
            po_uom = product.uom_po_id or product.uom_id
            if product.uom_po_id and product.uom_po_id != product.uom_id:
                qty_to_order = product.uom_id._compute_quantity(qty_stock, product.uom_po_id)
            else:
                qty_to_order = qty_stock

            price_unit = self._get_unit_price_for_vendor(product, vendor, seller)

            existing_line = po.order_line.filtered(lambda line: line.product_id == product)
            if existing_line:
                existing_line.write({"product_qty": qty_to_order})
            else:
                self.env["purchase.order.line"].create(
                    {
                        "order_id": po.id,
                        "product_id": product.id,
                        "name": product.display_name,
                        "product_qty": qty_to_order,
                        "product_uom": po_uom.id,
                        "price_unit": price_unit,
                        "date_planned": fields.Datetime.now(),
                    }
                )

        generated_pos = (
            self.env["purchase.order"]
            .browse([po_record.id for po_record in orders_by_vendor.values() if po_record])
            .exists()
        )

        if len(generated_pos) == 1:
            return {
                "type": "ir.actions.act_window",
                "res_model": "purchase.order",
                "res_id": generated_pos.id,
                "view_mode": "form",
                "views": [(False, "form")],
                "target": "current",
            }
        elif len(generated_pos) > 1:
            return {
                "type": "ir.actions.act_window",
                "name": _("Solicitudes de Presupuesto Generadas"),
                "res_model": "purchase.order",
                "domain": [("id", "in", generated_pos.ids)],
                "view_mode": "tree,form",
                "target": "current",
            }
        else:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Reabastecimiento Caryvil"),
                    "message": _(
                        "No se generaron solicitudes de presupuesto "
                        "(verifique que los medicamentos tengan proveedores farmacéuticos configurados)."
                    ),
                    "type": "warning",
                    "sticky": False,
                },
            }


class ProductTemplateOrderpoint(models.Model):
    _inherit = "product.template"

    orderpoint_ids = fields.One2many(
        "stock.warehouse.orderpoint",
        compute="_compute_orderpoint_ids",
        inverse="_set_orderpoint_ids",
        string="Reglas de Reabastecimiento",
        help="Reglas de stock mínimo y reabastecimiento parametrizadas para este medicamento.",
    )

    @api.depends("product_variant_ids.orderpoint_ids")
    def _compute_orderpoint_ids(self):
        for tmpl in self:
            tmpl.orderpoint_ids = tmpl.product_variant_ids.orderpoint_ids

    def _set_orderpoint_ids(self):
        for tmpl in self:
            for rule in tmpl.orderpoint_ids:
                if not rule.product_id and tmpl.product_variant_id:
                    rule.product_id = tmpl.product_variant_id.id
