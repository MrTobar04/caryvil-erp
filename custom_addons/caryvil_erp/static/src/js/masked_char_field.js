/** @odoo-module **/

import { registry } from "@web/core/registry";
import { CharField, charField } from "@web/views/fields/char/char_field";
import { useEffect } from "@odoo/owl";

//  Formatea el TELÉFONO como 0000-0000 (4 dígitos, guion, 4 dígitos).
function formatTelefono(rawValue) {
    const digits = (rawValue || "").replace(/\D/g, "").slice(0, 8);
    const parte1 = digits.slice(0, 4);
    const parte2 = digits.slice(4, 8);
    return parte2 ? `${parte1}-${parte2}` : parte1;
}

//Formatea el NIT como 0000-000000-000-0
function formatNit(rawValue) {
    const digits = (rawValue || "").replace(/\D/g, "").slice(0, 14);
    const parte1 = digits.slice(0, 4);
    const parte2 = digits.slice(4, 10);
    const parte3 = digits.slice(10, 13);
    const parte4 = digits.slice(13, 14);
    let resultado = parte1;
    if (parte2) resultado += `-${parte2}`;
    if (parte3) resultado += `-${parte3}`;
    if (parte4) resultado += `-${parte4}`;
    return resultado;
}

// NRC no tiene un formato fijo, así que no se le aplica ninguna
function formatNrc(rawValue) {
    return rawValue || "";
}

// Widget base: engancha el evento "input" del campo y le aplica la función
// de formato que le corresponda. Cada campo (Teléfono, NIT, NRC) usa su propia función de arriba a través de "formatFn".
class BaseMaskedCharField extends CharField {
    setup() {
        super.setup();
        useEffect(
            (inputEl) => {
                if (inputEl) {
                    const handler = (ev) => {
                        ev.target.value = this.formatFn(ev.target.value);
                    };
                    inputEl.addEventListener("input", handler);
                    return () => inputEl.removeEventListener("input", handler);
                }
            },
            () => [this.input.el]
        );
    }

    parse(value) {
        return this.formatFn(value);
    }
}

// ============================================================================
//  widget="caryvil_phone_mask"
export class PhoneMaskedField extends BaseMaskedCharField {
    formatFn(value) {
        return formatTelefono(value);
    }
}
registry.category("fields").add("caryvil_phone_mask", {
    ...charField,
    component: PhoneMaskedField,
});

// ============================================================================
// widget="caryvil_nit_mask"
export class NitMaskedField extends BaseMaskedCharField {
    formatFn(value) {
        return formatNit(value);
    }
}
registry.category("fields").add("caryvil_nit_mask", {
    ...charField,
    component: NitMaskedField,
});

// ============================================================================
// widget="caryvil_nrc_mask"
export class NrcMaskedField extends BaseMaskedCharField {
    formatFn(value) {
        return formatNrc(value);
    }
}
registry.category("fields").add("caryvil_nrc_mask", {
    ...charField,
    component: NrcMaskedField,
});
