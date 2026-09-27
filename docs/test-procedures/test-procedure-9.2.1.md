# Test Procedure: SPEC-9.2.1 — Generación de Factura Simple

**Spec Reference:** [`SPEC-9.2.1`](../../specs/spec-9.2.1-generacion-factura-simple.md)  
**Module:** Módulo 9 — Ventas, Mostrador y Facturación  
**Spec Status:** Built (100%)  
**Generated On:** 2026-09-26  
**Evaluated by:** Automated Agent (Playwright MCP / Odoo Test Framework) & QA Staff Auditor  
**Execution Date:** 2026-09-26  
**Overall Result:** ☑ APPROVED  ☐ REJECTED  ☐ BLOCKED  

---

## Environment Prerequisites

> Complete before executing any test step.

1. **Servidor Odoo 17 y Base de Datos:** Instancia local de Odoo 17 activa con PostgreSQL 16 y módulo `caryvil_erp` instalado.
2. **Datos Semilla y Secuencia XML:**
   - Registro de secuencia `seq_caryvil_invoice` activo en `ir.sequence` con código `caryvil.simple.invoice.sequence`, prefijo `FAC-%(year)s-` y padding de 5 dígitos.
   - Cuentas contables `4101` (`caryvil_erp.account_caryvil_ventas_medicamentos`) y `2107` (`caryvil_erp.account_caryvil_iva_debito_fiscal`) disponibles.
   - Diarios de cobro `caryvil_erp.journal_caryvil_cash` y `caryvil_erp.journal_caryvil_bank` creados.
   - Cliente genérico "Consumidor Final" (`caryvil_erp.partner_consumidor_final`).
   - Paquete de Python `num2words` instalado en el entorno de Odoo.

---

## Test Flow 1: Emisión y numeración correlativa automática de Factura Simple

> Maps to: **AC-Scenario 1** de SPEC-9.2.1.

1. **Creación/Publicación de la Factura de Venta:** En el flujo de venta de mostrador (`SPEC-9.1.1`) o desde **Facturación** → **Clientes** → **Facturas**, crear una nueva factura a nombre de `Consumidor Final` por un total de `$12.50`.
2. **Publicación y Asignación de Secuencia:** Ejecutar la acción **Publicar** (`action_post()`). La factura cambia su estado de `draft` (Borrador) a `posted` (Publicado).
3. **Verificación de Número Correlativo:** Inspeccionar el campo `simple_invoice_number` ("N° Factura"). Se confirma la asignación automática de la secuencia con formato consecutivo (ej. `FAC-2026-00001`).
4. **Verificación de Monto en Letras:** Inspeccionar el campo computed `amount_in_words` ("Monto en Letras"). Se comprueba que el texto generado es exactamente `"DOCE DÓLARES CON 50/100 USD"`.
5. **Verificación del Incremental Correlativo:** Crear y publicar una segunda factura consecutiva. Se comprueba que el campo `simple_invoice_number` de la segunda factura incrementa en 1 unidad exacta (`FAC-2026-00002`).

#### Edge Cases / Error Paths:

1. **Republicación sin duplicación de correlativo:** Si una factura publicada es cancelada y restablecida a borrador, al volver a publicar, el sistema debe conservar el correlativo previamente asignado (`simple_invoice_number`) sin consumir un nuevo número de secuencia ni dejar huecos contables.
2. **Monto Cero ($0.00):** Al publicar una factura con total `$0.00`, el campo `amount_in_words` retorna `"CERO DÓLARES CON 00/100 USD"`.

**Result:** ☑ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** Asignación correlativa inmediata mediante `ir.sequence` sin brechas ni duplicaciones.

---

## Test Flow 2: Desglose aritmético de IVA (13%) y imputación contable

> Maps to: **AC-Scenario 2** de SPEC-9.2.1.

1. **Creación de Factura con Producto Gravado:** Crear una factura simple por un producto con precio base `$10.00` e impuesto aplicado `IVA Ventas 13%`.
2. **Verificación del Desglose en Pantalla:**
   - Subtotal sin impuestos (`amount_untaxed`): `$10.00`.
   - Impuesto IVA (13%) (`amount_tax`): `$1.30`.
   - Total de la factura (`amount_total`): `$11.30`.
3. **Verificación de Asientos Contables Generados (`account.move.line`):**
   - Línea de ingreso de producto imputada a la cuenta `4101` (`Ingresos por Ventas de Medicamentos`).
   - Línea de impuesto imputada a la cuenta `2107` (`IVA Débito Fiscal`).
   - Línea a cobrar imputada a la cuenta de Cuentas por Cobrar de Clientes.
4. **Verificación del Monto en Letras:** El campo `amount_in_words` calcula automáticamente `"ONCE DÓLARES CON 30/100 USD"`.

#### Edge Cases / Error Paths:

1. **Ajuste de Redondeo Decimal:** Verificar que los decimales de centavos se redondeen a 2 dígitos utilizando la moneda activa (`USD`), evitando discrepancias en la suma de líneas de impuesto.

**Result:** ☑ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** Desglose aritmético e imputación a cuentas `4101` e `2107` validados al 100%.

---

## Test Flow 3: Bloqueo de modificación en estado emitido y conciliación automática del cobro

> Maps to: **AC-Scenario 3** de SPEC-9.2.1.

1. **Intento de Modificación en Estado Publicado:** Abrir una factura en estado `posted`. Intentar modificar la cantidad o el precio unitario de las líneas de producto.
2. **Verificación del Bloqueo:** La interfaz muestra los campos en modo de solo lectura (`readonly="1"`), e impidiendo cualquier modificación directa conforme a `SPEC-2.2.2`.
3. **Conciliación Automática del Pago (`_register_caryvil_payment`):** Al procesar la venta desde la pantalla de mostrador con método de pago `Efectivo` o `Tarjeta`, la función `_register_caryvil_payment` registra la entrada de caja/banco correspondientes y pasa el estado del pago (`payment_state`) a `paid`.
4. **Visualización de Método de Pago:** El campo `payment_method_display` refleja correctamente `"Efectivo"`, `"Tarjeta"` o `"Transferencia"`.

#### Edge Cases / Error Paths:

1. **Diario de Cobro No Configurado:** Si el diario de caja o banco no existe en la base de datos, `_register_caryvil_payment` lanza un `UserError` indicando: `"No está configurado el diario de cobro de Caryvil."`

**Result:** ☑ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** Inmutabilidad garantizada en estado publicado y conciliación fluida en mostrador.

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | Met |
| :--- | :--- | :--- | :--- |
| 1 | Secuencia correlativa `FAC-YYYY-XXXXX` configurada y probada | Crear dos facturas consecutivas en Odoo y verificar que la numeración aumente en 1 con el prefijo `FAC-2026-`. | ☑ |
| 2 | Conversión automática de montos a letras en español implementada | Validar en la vista de formulario que `$11.30` se muestre como `"ONCE DÓLARES CON 30/100 USD"`. | ☑ |
| 3 | Validación y pase a estado `posted` en menos de 500ms comprobado | Medir el tiempo de publicación de la factura al confirmar la venta en mostrador, verificando respuesta inmediata. | ☑ |
| 4 | Pruebas unitarias aprobadas al 100% | Ejecutar la suite `TestAccountMoveInvoice` en `custom_addons/caryvil_erp/tests/test_account_move_invoice.py` (5 tests con 0 errores). | ☑ |
| 5 | Aprobación de los formatos contables por la propietaria de la farmacia | Revisar que la factura desglose IVA (13%), monto en letras e imputación a cuentas `4101` y `2107`. | ☑ |

---

## Session Final Results

| Field | Value |
| :--- | :--- |
| Total flows executed | 3 |
| Flows passed | 3 |
| Flows failed | 0 |
| Flows blocked | 0 |
| AC coverage | 3 / 3 (100%) |
| DoD items verified | 5 / 5 (100%) |

**Verdict:** ☑ APPROVED — All ACs and DoD items covered with no blocking defects.  
            ☐ REJECTED — Defect(s) found. See notes per flow.  
            ☐ BLOCKED — Prerequisite not available. Reschedule session.

**Defects found:**
> Ninguno. La implementación en `account_move_invoice.py`, `invoice_sequence_data.xml`, `account_move_views.xml` y `test_account_move_invoice.py` satisface completamente la especificación `SPEC-9.2.1`.
