# -*- coding: utf-8 -*-
"""Modelo y servicio de analítica de KPIs de ventas para Farmacia Caryvil ERP.

Cumple con SPEC-4.1.1:
- Agregación de volumen diario facturado, transacciones y ticket promedio.
- Comparativa mensual e índice de crecimiento.
- Tendencia histórica de ventas de los últimos 7 días.
- Ranking Top 5 de medicamentos más vendidos.
- Restricción de acceso estricta para group_caryvil_manager.
"""

from datetime import timedelta
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, ValidationError


class CaryvilSalesDashboard(models.TransientModel):
    """Modelo transaccional y servicio de agregación para el Dashboard de Ventas e Inventario."""

    _name = "caryvil.dashboard.sales"
    _description = "Dashboard Analítico y Alertas Caryvil"

    name = fields.Char(string="Nombre", default="Dashboard de Ventas y Alertas", readonly=True)
    total_sales_today = fields.Float(string="Ventas del Día ($)", readonly=True)
    tx_count_today = fields.Integer(string="Transacciones de Hoy", readonly=True)
    avg_ticket = fields.Float(string="Ticket Promedio ($)", readonly=True)
    sales_this_month = fields.Float(string="Ventas del Mes ($)", readonly=True)
    sales_last_month = fields.Float(string="Ventas Mes Anterior ($)", readonly=True)
    growth_rate_month = fields.Float(string="Crecimiento Mensual (%)", readonly=True)
    currency_id = fields.Many2one(
        "res.currency",
        string="Moneda",
        default=lambda self: self.env.company.currency_id,
        readonly=True,
    )

    def _check_manager_access(self):
        """Verifica que el usuario actual posea el rol de Administrador / Propietario."""
        if not self.env.user.has_group("caryvil_erp.group_caryvil_manager"):
            raise AccessError(
                _("No tiene permisos para acceder al dashboard de ventas. Se requiere rol de Administrador.")
            )

    def _check_inventory_access(self):
        """Verifica que el usuario posea el rol de Compras/Inventario o Administrador."""
        user = self.env.user
        is_inventory = user.has_group("caryvil_erp.group_caryvil_inventory_purchases")
        is_manager = user.has_group("caryvil_erp.group_caryvil_manager")
        if not (is_inventory or is_manager):
            raise AccessError(
                _(
                    "No tiene permisos para acceder a las alertas de stock crítico. "
                    "Se requiere rol de Compras e Inventario o Administrador."
                )
            )

    def _get_today_sales_metrics(self, today):
        """Calcula el total de ventas, conteo de transacciones y ticket promedio del día."""
        invoices = self.env["account.move"].search(
            [
                ("move_type", "=", "out_invoice"),
                ("state", "=", "posted"),
                ("invoice_date", "=", today),
                ("company_id", "=", self.env.company.id),
            ]
        )
        total_sales_today = sum(invoices.mapped("amount_total"))
        tx_count_today = len(invoices)
        avg_ticket = (total_sales_today / tx_count_today) if tx_count_today > 0 else 0.0
        return total_sales_today, tx_count_today, avg_ticket

    def _get_monthly_sales_metrics(self, today):
        """Calcula el acumulado del mes en curso, mes previo y tasa de crecimiento."""
        first_day_this_month = today.replace(day=1)
        last_day_last_month = first_day_this_month - timedelta(days=1)
        first_day_last_month = last_day_last_month.replace(day=1)

        invoices_this_month = self.env["account.move"].search(
            [
                ("move_type", "=", "out_invoice"),
                ("state", "=", "posted"),
                ("invoice_date", ">=", first_day_this_month),
                ("invoice_date", "<=", today),
                ("company_id", "=", self.env.company.id),
            ]
        )
        sales_this_month = sum(invoices_this_month.mapped("amount_total"))

        invoices_last_month = self.env["account.move"].search(
            [
                ("move_type", "=", "out_invoice"),
                ("state", "=", "posted"),
                ("invoice_date", ">=", first_day_last_month),
                ("invoice_date", "<=", last_day_last_month),
                ("company_id", "=", self.env.company.id),
            ]
        )
        sales_last_month = sum(invoices_last_month.mapped("amount_total"))

        if sales_last_month > 0:
            growth_rate_month = ((sales_this_month - sales_last_month) / sales_last_month) * 100.0
        else:
            growth_rate_month = 100.0 if sales_this_month > 0 else 0.0

        return sales_this_month, sales_last_month, growth_rate_month

    def _get_last_7_days_sales(self, today):
        """Calcula la serie temporal de ventas de los últimos 7 días con nombres en español."""
        start_7_days = today - timedelta(days=6)
        self.env.cr.execute(
            """
            SELECT
                invoice_date,
                COALESCE(SUM(amount_total), 0) AS total_amount,
                COUNT(id) AS tx_count
            FROM account_move
            WHERE move_type = 'out_invoice'
              AND state = 'posted'
              AND invoice_date >= %s
              AND invoice_date <= %s
              AND company_id = %s
            GROUP BY invoice_date
            ORDER BY invoice_date ASC
            """,
            (start_7_days, today, self.env.company.id),
        )
        sales_by_date = {row[0]: {"total": float(row[1]), "tx_count": int(row[2])} for row in self.env.cr.fetchall()}
        day_names_es = {0: "Lun", 1: "Mar", 2: "Mié", 3: "Jue", 4: "Vie", 5: "Sáb", 6: "Dom"}

        sales_last_7_days = []
        curr = start_7_days
        while curr <= today:
            day_info = sales_by_date.get(curr, {"total": 0.0, "tx_count": 0})
            sales_last_7_days.append(
                {
                    "date": curr.strftime("%Y-%m-%d"),
                    "day_name": day_names_es[curr.weekday()],
                    "formatted_date": curr.strftime("%d/%m"),
                    "total": round(day_info["total"], 2),
                    "tx_count": day_info["tx_count"],
                }
            )
            curr += timedelta(days=1)
        return sales_last_7_days

    def _get_top_5_medicines(self):
        """Obtiene los 5 medicamentos más vendidos en unidades con sus respectivos ingresos."""
        lines = self.env["account.move.line"].read_group(
            domain=[
                ("move_id.move_type", "=", "out_invoice"),
                ("move_id.state", "=", "posted"),
                ("move_id.company_id", "=", self.env.company.id),
                ("product_id", "!=", False),
                ("display_type", "in", ("product", False)),
            ],
            fields=["product_id", "quantity:sum", "price_total:sum"],
            groupby=["product_id"],
            orderby="quantity desc",
            limit=5,
        )
        top_5 = []
        for line in lines:
            prod_id = line["product_id"][0]
            prod_name = line["product_id"][1]
            prod = self.env["product.product"].browse(prod_id)
            top_5.append(
                {
                    "product_id": prod_id,
                    "name": prod_name,
                    "code": prod.default_code or "",
                    "qty_sold": float(line["quantity"]),
                    "total_amount": round(float(line["price_total"]), 2),
                }
            )
        return top_5

    @api.model
    def get_sales_kpis(self):
        """Retorna las métricas y agregaciones de ventas para alimentar el Dashboard."""
        self._check_manager_access()

        today = fields.Date.context_today(self)
        total_sales_today, tx_count_today, avg_ticket = self._get_today_sales_metrics(today)
        sales_this_month, sales_last_month, growth_rate_month = self._get_monthly_sales_metrics(today)
        sales_last_7_days = self._get_last_7_days_sales(today)
        top_5_medicines = self._get_top_5_medicines()

        currency_symbol = self.env.company.currency_id.symbol or "$"
        currency_name = self.env.company.currency_id.name or "USD"

        return {
            "total_sales_today": round(float(total_sales_today or 0.0), 2),
            "tx_count_today": int(tx_count_today or 0),
            "avg_ticket": round(float(avg_ticket or 0.0), 2),
            "sales_this_month": round(float(sales_this_month or 0.0), 2),
            "sales_last_month": round(float(sales_last_month or 0.0), 2),
            "growth_rate_month": round(float(growth_rate_month or 0.0), 2),
            "sales_last_7_days": sales_last_7_days,
            "top_5_medicines": top_5_medicines,
            "currency": "$ USD",
            "currency_symbol": currency_symbol,
            "currency_name": currency_name,
            "company_name": self.env.company.name,
            "today_date": today.strftime("%Y-%m-%d"),
            "today_formatted": today.strftime("%d/%m/%Y"),
        }

    @api.model
    def get_critical_stock_data(self):
        """Retorna el conteo total y listado de los productos almacenables en situación
        de stock crítico (qty_available <= orderpoint_min_qty).
        """
        self._check_inventory_access()

        critical_products = self.env["product.product"].search([
            ("detailed_type", "=", "product"),
            ("active", "=", True),
            ("orderpoint_min_qty", ">", 0),
        ]).filtered(lambda p: p.qty_available <= p.orderpoint_min_qty)

        sorted_critical = sorted(
            critical_products,
            key=lambda p: (p.orderpoint_min_qty - p.qty_available),
            reverse=True,
        )

        results = []
        for prod in sorted_critical[:10]:
            active_ingredient = (
                getattr(prod, "active_ingredient_id", False)
                and prod.active_ingredient_id.name
                or (
                    getattr(prod.product_tmpl_id, "active_ingredient_id", False)
                    and prod.product_tmpl_id.active_ingredient_id.name
                    or "N/A"
                )
            )
            therapeutic_category = (
                getattr(prod, "therapeutic_category_id", False)
                and prod.therapeutic_category_id.name
                or (
                    getattr(prod.product_tmpl_id, "therapeutic_category_id", False)
                    and prod.product_tmpl_id.therapeutic_category_id.name
                    or "N/A"
                )
            )

            supplier_name = "Sin Asignar"
            supplier_id = False
            if prod.seller_ids:
                supplier_name = prod.seller_ids[0].partner_id.name
                supplier_id = prod.seller_ids[0].partner_id.id
            elif prod.product_tmpl_id.seller_ids:
                supplier_name = prod.product_tmpl_id.seller_ids[0].partner_id.name
                supplier_id = prod.product_tmpl_id.seller_ids[0].partner_id.id

            min_qty = prod.orderpoint_min_qty
            qty_available = prod.qty_available
            deficit = max(min_qty - qty_available, 0.0)

            results.append(
                {
                    "product_id": prod.id,
                    "name": prod.name,
                    "default_code": prod.default_code or "",
                    "active_ingredient": active_ingredient,
                    "therapeutic_category": therapeutic_category,
                    "qty_available": qty_available,
                    "min_qty": min_qty,
                    "deficit": deficit,
                    "uom": prod.uom_id.name or "",
                    "supplier_name": supplier_name,
                    "supplier_id": supplier_id,
                }
            )

        return {
            "critical_count": len(critical_products),
            "critical_list": results,
        }

    @api.model
    def action_reorder_product(self, product_id):
        """Abre un borrador de Orden de Compra precargado con el proveedor,
        medicamento y cantidad sugerida de reposición.
        """
        self._check_inventory_access()
        product = self.env["product.product"].browse(product_id)
        if not product.exists():
            raise ValidationError(_("El medicamento seleccionado no existe."))

        orderpoint = product.orderpoint_ids[:1]
        if orderpoint and orderpoint.suggested_replenishment_qty > 0:
            qty_to_order = orderpoint.suggested_replenishment_qty
        else:
            qty_to_order = max(product.orderpoint_min_qty - product.qty_available, 1.0)

        vendor = False
        seller = False
        if orderpoint and orderpoint.supplier_id:
            vendor = orderpoint.supplier_id
        elif product.seller_ids:
            seller = product.seller_ids[0]
            vendor = seller.partner_id
        elif product.product_tmpl_id.seller_ids:
            seller = product.product_tmpl_id.seller_ids[0]
            vendor = seller.partner_id

        vendor_id = vendor.id if vendor else False

        domain = [("state", "=", "draft")]
        if vendor_id:
            domain.append(("partner_id", "=", vendor_id))

        po = self.env["purchase.order"].search(domain, limit=1)
        if not po and vendor_id:
            po = self.env["purchase.order"].create(
                {
                    "partner_id": vendor_id,
                    "origin": "Reabastecimiento Caryvil - Dashboard",
                    "company_id": self.env.company.id,
                }
            )

        price_unit = seller.price if seller else (product.standard_price or 0.0)
        po_uom = product.uom_po_id or product.uom_id

        if po:
            order_line = po.order_line.filtered(lambda l_item: l_item.product_id == product)
            if order_line:
                order_line.write({"product_qty": qty_to_order})
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

            return {
                "type": "ir.actions.act_window",
                "name": _("Orden de Compra"),
                "res_model": "purchase.order",
                "res_id": po.id,
                "view_mode": "form",
                "views": [(False, "form")],
                "target": "current",
            }
        else:
            return {
                "type": "ir.actions.act_window",
                "name": _("Solicitud de Presupuesto"),
                "res_model": "purchase.order",
                "view_mode": "form",
                "views": [(False, "form")],
                "target": "current",
                "context": {
                    "default_partner_id": vendor_id,
                    "default_origin": "Reabastecimiento Caryvil - Dashboard",
                    "default_order_line": [
                        (
                            0,
                            0,
                            {
                                "product_id": product.id,
                                "name": product.display_name,
                                "product_qty": qty_to_order,
                                "product_uom": po_uom.id,
                                "price_unit": price_unit,
                                "date_planned": fields.Datetime.now(),
                            },
                        )
                    ],
                },
            }

    @api.model
    def action_get_orderpoint_view(self):
        """Retorna la acción de ventana para ver el catálogo completo de reglas de reabastecimiento."""
        self._check_inventory_access()
        action = self.env.ref("stock.action_orderpoint").read()[0]
        action["name"] = _("Productos con Reglas de Reabastecimiento")
        return action
