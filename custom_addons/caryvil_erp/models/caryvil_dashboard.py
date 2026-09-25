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
from odoo.exceptions import AccessError


class CaryvilSalesDashboard(models.TransientModel):
    """Modelo transaccional y servicio de agregación para el Dashboard de Ventas."""

    _name = "caryvil.dashboard.sales"
    _description = "Dashboard Analítico de Ventas Caryvil"

    name = fields.Char(string="Nombre", default="Dashboard de Ventas Caryvil", readonly=True)
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
