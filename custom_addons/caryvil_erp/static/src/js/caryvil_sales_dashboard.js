/** @odoo-module **/

import { loadBundle } from "@web/core/assets";
import { registry } from "@web/core/registry";
import { Component, onWillStart, useEffect, useRef, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

/**
 * Componente OWL para el Dashboard de KPIs de Ventas de Farmacia Caryvil.
 * Cumple con SPEC-4.1.1:
 * - Tarjetas interactivas de ventas del día, transacciones, ticket promedio y acumulado mensual.
 * - Gráfico de tendencia de ventas de los últimos 7 días con Chart.js.
 * - Tabla ranking con el Top 5 de medicamentos más vendidos.
 * - Botón de actualización rápida en tiempo real.
 */
export class CaryvilSalesDashboard extends Component {
    static template = "caryvil_erp.CaryvilSalesDashboard";

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.canvasRef = useRef("salesChartCanvas");
        this.chart = null;

        this.state = useState({
            kpiData: {
                total_sales_today: 0.0,
                tx_count_today: 0,
                avg_ticket: 0.0,
                sales_this_month: 0.0,
                sales_last_month: 0.0,
                growth_rate_month: 0.0,
                sales_last_7_days: [],
                top_5_medicines: [],
                currency: "$ USD",
            },
            loading: true,
        });

        onWillStart(async () => {
            await loadBundle("web.chartjs_lib");
            await this.loadDashboardData();
        });

        useEffect(() => {
            this.renderChart();
            return () => {
                if (this.chart) {
                    this.chart.destroy();
                    this.chart = null;
                }
            };
        });
    }

    /**
     * Formatea valores monetarios a estilo salvadoreño/USD ($ 0,000.00).
     */
    formatMoney(val) {
        const num = Number(val || 0);
        return "$" + num.toLocaleString("en-US", {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
        });
    }

    /**
     * Carga de datos de KPIs llamando al servicio backend caryvil.dashboard.sales.
     */
    async loadDashboardData() {
        this.state.loading = true;
        try {
            const data = await this.orm.call("caryvil.dashboard.sales", "get_sales_kpis", []);
            Object.assign(this.state.kpiData, data);
        } catch (error) {
            console.error("Error al cargar KPIs de ventas:", error);
            this.notification.add("No se pudieron cargar los datos del dashboard de ventas.", {
                type: "danger",
            });
        } finally {
            this.state.loading = false;
        }
    }

    /**
     * Manejador del botón de refresco en tiempo real con protección contra doble clic.
     */
    async onRefresh() {
        if (this.state.loading) {
            return;
        }
        await this.loadDashboardData();
    }

    /**
     * Renderiza el gráfico interactivo de tendencia de ventas de los últimos 7 días.
     */
    renderChart() {
        if (!this.canvasRef.el || typeof Chart === "undefined") {
            return;
        }

        if (this.chart) {
            this.chart.destroy();
            this.chart = null;
        }

        const series = this.state.kpiData.sales_last_7_days || [];
        const labels = series.map((d) => d.day_name + " (" + (d.formatted_date || d.date) + ")");
        const dataValues = series.map((d) => d.total);

        const ctx = this.canvasRef.el.getContext("2d");
        const gradient = ctx.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, "rgba(0, 168, 150, 0.35)");
        gradient.addColorStop(1, "rgba(0, 91, 96, 0.0)");

        const config = {
            type: "line",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: "Ventas Diarias ($)",
                        data: dataValues,
                        borderColor: "#005b60",
                        backgroundColor: gradient,
                        borderWidth: 3,
                        pointBackgroundColor: "#00a896",
                        pointBorderColor: "#ffffff",
                        pointBorderWidth: 2,
                        pointRadius: 5,
                        pointHoverRadius: 7,
                        tension: 0.35,
                        fill: true,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false,
                    },
                    tooltip: {
                        backgroundColor: "#0f172a",
                        titleFont: { size: 13, weight: "bold" },
                        bodyFont: { size: 12 },
                        padding: 10,
                        cornerRadius: 8,
                        callbacks: {
                            label: (context) => {
                                const val = context.parsed.y || 0;
                                return " Ventas: " + this.formatMoney(val);
                            },
                        },
                    },
                },
                scales: {
                    x: {
                        grid: {
                            display: false,
                        },
                        ticks: {
                            color: "#64748b",
                            font: { size: 11, weight: "500" },
                        },
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: "#f1f5f9",
                        },
                        ticks: {
                            color: "#64748b",
                            font: { size: 11 },
                            callback: (value) => "$" + value,
                        },
                    },
                },
            },
        };

        this.chart = new Chart(this.canvasRef.el, config);
    }
}

registry.category("actions").add("caryvil_sales_dashboard", CaryvilSalesDashboard);
