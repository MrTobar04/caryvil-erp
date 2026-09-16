/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { formatMonetary } from "@web/views/fields/formatters";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

// Resumen de la Orden de Compra (Subtotal/Descuento/IVA 13%/IVA Percibido/Total)
// calculado DIRECTO en el navegador a partir de las líneas ya cargadas en pantalla,
// sin esperar una llamada al servidor. Esto evita que el resumen se quede en $0.00
// cuando Odoo no dispara a tiempo el recálculo del encabezado al agregar un producto.
export class PurchaseLiveTotals extends Component {
    static template = "caryvil_erp.PurchaseLiveTotals";
    static props = { ...standardFieldProps };

    get currencyId() {
        const currency = this.props.record.data.currency_id;
        return currency ? currency[0] : undefined;
    }

    get lines() {
        const o2m = this.props.record.data.order_line;
        return o2m && o2m.records ? o2m.records.filter((l) => !l.data.display_type) : [];
    }

    get gross() {
        return this.lines.reduce((sum, l) => sum + (l.data.product_qty || 0) * (l.data.price_unit || 0), 0);
    }

    get net() {
        return this.lines.reduce((sum, l) => {
            const qty = l.data.product_qty || 0;
            const price = l.data.price_unit || 0;
            const disc = l.data.discount || 0;
            return sum + qty * price * (1 - disc / 100);
        }, 0);
    }

    get discount() {
        return this.gross - this.net;
    }

    get iva() {
        return this.net * 0.13;
    }

    get subtotalConIva() {
        return this.net + this.iva;
    }

    get ivaPercibidoCheck() {
        return !!this.props.record.data.iva_percibido_check;
    }

    get ivaPercibido() {
        return this.ivaPercibidoCheck && this.subtotalConIva > 100 ? this.subtotalConIva * 0.01 : 0;
    }

    get total() {
        return this.subtotalConIva + this.ivaPercibido;
    }

    fmt(value) {
        return formatMonetary(value, { currencyId: this.currencyId });
    }

    onToggleIvaPercibido(ev) {
        this.props.record.update({ iva_percibido_check: ev.target.checked });
    }
}

registry.category("fields").add("caryvil_purchase_live_totals", {
    component: PurchaseLiveTotals,
});
