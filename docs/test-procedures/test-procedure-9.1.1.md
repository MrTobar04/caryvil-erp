# Test Procedure: SPEC-9.1.1 — Procesamiento de Transacciones de Ventas

**Spec Reference:** [`SPEC-9.1.1`](../../specs/spec-9.1.1-procesamiento-transacciones-ventas.md)
**Module:** Módulo 9 — Ventas, Mostrador y Facturación
**Spec Status:** Built (100%)
**Generated On:** 2026-09-26
**Evaluated by:** Automated Agent (Playwright MCP / Browser Subagent) & QA Staff Auditor
**Execution Date:** 2026-09-26
**Overall Result:** ☑ APPROVED  ☐ REJECTED  ☐ BLOCKED

---

## Environment Prerequisites

> Complete before executing any test step.

1. **Servidor Odoo 17 y Base de Datos:** Instancia local de Odoo 17 activa con PostgreSQL 16 y módulo `caryvil_erp` instalado y actualizado.
2. **Datos Semilla y Maestros:**
   - Usuario de prueba con rol Cajero/Mostrador (`cajero@caryvil.com` / contraseña configurada) perteneciente al grupo `caryvil_erp.group_caryvil_cashier`.
   - Cliente genérico "Consumidor Final" (`caryvil_erp.partner_consumidor_final`) registrado con `is_pharmacy_customer = True`.
   - Cliente frecuente con DUI registrado (ej. "04589632-1", "Juan Pérez") con `is_pharmacy_customer = True`.
   - Medicamento "Amoxicilina 500mg" con código de barras EAN-13 `7412345678901`, principio activo "Amoxicilina", precio de lista `$4.50`, e inventario disponible de al menos 10 unidades.
   - Medicamento "Jarabe 120ml" con inventario físico restringido exactamente a 2 unidades disponibles en mostrador.
   - Impuesto de ventas `caryvil_erp.tax_caryvil_iva_ventas_13` (IVA 13%) configurado y asignado.

---

## Test Flow 1: Venta rápida con escaneo de código de barras EAN-13 y cobro en efectivo

> Maps to: **AC-Scenario 1** de SPEC-9.1.1.

1. **Acceso a la Interfaz de Mostrador:** Iniciar sesión con el usuario cajero en Odoo, abrir el menú superior **Farmacia Caryvil** → **Ventas y Caja** → **Venta de Mostrador**, y hacer clic en el botón **Nuevo**. Se despliega el formulario de venta rápida mostrando por defecto el cliente `Consumidor Final` y la Forma de Pago seleccionada como `Efectivo`.
2. **Escaneo de Código de Barras EAN-13:** En el campo `caryvil_barcode_input` ("Escanear EAN-13"), ingresar el código `7412345678901` y presionar `Enter`. Se observa que el campo de escaneo se limpia de inmediato, se inserta una nueva línea en la tabla de productos con el producto "Amoxicilina 500mg", cantidad `1.0`, precio unitario `$4.50`, impuesto `IVA 13%`, subtotal sin impuestos `$4.50`, IVA `$0.59` y total calculado `$5.09`.
3. **Escaneo Consecutivo / Incremento de Cantidad:** Volver a posicionar el cursor en `caryvil_barcode_input`, ingresar nuevamente `7412345678901` y presionar `Enter`. Se verifica que no se crea una línea duplicada, sino que la línea existente actualiza su cantidad de `1.0` a `2.0`, calculando el total de la orden en `$10.17`.
4. **Cálculo Reactivo de Cambio en Efectivo:** En la sección **Cobro en mostrador**, ingresar en el campo `amount_tendered` ("Efectivo Recibido ($)") el monto `15.00`. Se observa que el campo de solo lectura `amount_change` ("Cambio / Vuelto ($)") calcula reactivamente `$4.83` (`$15.00 - $10.17`).
5. **Ejecución de Cobro y Emisión:** Hacer clic en el botón principal **Cobrar y Facturar** ubicado en el encabezado. La orden cambia automáticamente su estado a `sale` (Orden de Venta confirmada), se descuenta el stock en el almacén de mostrador, se genera y valida el comprobante `account.move` en estado `posted`, y se abre la vista previa/diálogo de impresión del ticket de venta.

#### Edge Cases / Error Paths:

1. **Efectivo Recibido Insuficiente:** En una orden con total `$10.17`, ingresar en `amount_tendered` el valor `5.00` y hacer clic en **Cobrar y Facturar**. El sistema bloquea la operación y despliega un mensaje modal de error: `UserError: El monto en efectivo recibido ($5.00) es menor al total a pagar ($10.17).`
2. **Código EAN-13 Inválido o No Numérico:** Escribir en `caryvil_barcode_input` el texto `74123ABC` o un código de menos de 13 dígitos y presionar `Enter`. El sistema despliega una advertencia en pantalla: `El código de barras debe contener exactamente 13 dígitos (EAN-13).`
3. **Código EAN-13 Inexistente en Catálogo:** Escribir el código `9999999999999` y presionar `Enter`. Se muestra una notificación de advertencia: `No se encontró un medicamento activo con el código de barras "9999999999999".`

**Result:** ☑ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** Flujo verificado exitosamente. El escaneo rápido y el cálculo reactivo de vuelto operan con tiempos de respuesta menores a 100ms.

---

## Test Flow 2: Bloqueo estricto de venta ante stock insuficiente

> Maps to: **AC-Scenario 2** de SPEC-9.1.1.

1. **Creación de Orden y Selección de Medicamento con Stock Limitado:** En el formulario de Venta de Mostrador, agregar el producto "Jarabe 120ml" (el cual cuenta únicamente con 2 unidades en existencias físicas).
2. **Ingreso de Cantidad Excedente:** Modificar manualmente la columna cantidad (`product_uom_qty`) a `5.0` unidades.
3. **Intento de Cobro y Validación:** Configurar Forma de Pago `Efectivo`, ingresar `amount_tendered` suficiente y presionar **Cobrar y Facturar**.
4. **Verificación del Bloqueo:** El sistema intercepta la confirmación antes de modificar el inventario o la contabilidad, lanzando un `UserError` bloqueante con el texto explicativo: `Stock insuficiente para "Jarabe 120ml". Cantidad solicitada: 5.0 Unidades, Cantidad disponible: 2.0 Unidades.` La orden permanece en estado borrador (`draft`).

#### Edge Cases / Error Paths:

1. **Validación Multi-línea Acumulada:** Agregar dos líneas separadas del mismo producto "Jarabe 120ml" con cantidades `1.0` y `2.0` (total 3 unidades solicitadas). Al presionar **Cobrar y Facturar**, la validación interna agrupa las cantidades por producto (`_get_caryvil_requested_quantities`) y bloquea la transacción al detectar que el acumulado (3.0) excede el stock disponible (2.0).

**Result:** ☑ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** La validación de stock previene sobreventas y descuadres físicos en mostrador.

---

## Test Flow 3: Asignación inmediata de cliente registrado mediante búsqueda por DUI

> Maps to: **AC-Scenario 3** de SPEC-9.1.1.

1. **Apertura de Nueva Venta:** Hacer clic en **Nuevo** en la pantalla de Venta de Mostrador. Se comprueba que el campo `partner_id` inicia con "Consumidor Final".
2. **Búsqueda Rápida por DUI:** En el selector de cliente (`partner_id`), escribir el DUI del cliente frecuente `04589632-1`.
3. **Asignación Automática:** El autocompletado despliega al cliente asociado "Juan Pérez [04589632-1]". Al seleccionarlo, la orden se vincula de inmediato a dicho registro, conservando su historial y datos fiscales.
4. **Cobro con Métodos Electrónicos (Tarjeta / Transferencia QR):**
   - Cambiar **Forma de Pago** a `Tarjeta de Débito / Crédito` o `Transferencia / Pago QR`.
   - Verificar que los campos `amount_tendered` y `amount_change` se ocultan de la interfaz (`invisible="payment_method != 'efectivo'"`), y el cálculo de cambio se fija automáticamente en `$0.00`.
5. **Confirmación:** Presionar **Cobrar y Facturar**. La transacción se postea sin exigir efectivo recibido.

#### Edge Cases / Error Paths:

1. **Filtro Estricto de Clientes Farmacéuticos:** En el selector de cliente, intentar buscar un proveedor o contacto que no tenga activo `is_pharmacy_customer`. El dominio `[('is_pharmacy_customer', '=', True)]` restringe la lista garantizando que solo clientes válidos de mostrador sean seleccionables.

**Result:** ☑ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** La búsqueda por DUI se integra limpiamente con SPEC-5.2.1 y la vista simplificada de caja.

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | Met |
| :--- | :--- | :--- | :--- |
| 1 | Formulario de venta rápida en mostrador implementado | Abrir menú **Farmacia Caryvil** → **Ventas y Caja** → **Venta de Mostrador** y verificar la vista simplificada con botón de escaneo y bloque de cobro integrado. | ☑ |
| 2 | Escaneo de código de barras y cálculo automático de cambio validados | Escanear un código EAN-13 en la interfaz, ingresar efectivo y verificar que la adición de línea y el cálculo de vuelto en `amount_change` ocurren en tiempo real. | ☑ |
| 3 | Bloqueo de venta ante stock insuficiente verificado | Intentar facturar una cantidad mayor a las existencias físicas y corroborar que el modal de `UserError` bloquea la transacción informando la cantidad disponible. | ☑ |
| 4 | Pruebas unitarias aprobadas al 100% | Verificar la ejecución de la suite de pruebas unitarias `TestSaleOrderMedicine` (9 tests ejecutados con 0 fallos). | ☑ |
| 5 | Validación de experiencia de usuario en mostrador aprobada | Medir el tiempo de ejecución del ciclo completo de escaneo, cobro y facturación, confirmando que la transacción se completa en menos de 15 segundos en un solo clic. | ☑ |

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
> Ninguno. La implementación en `sale_order_medicine.py`, `sale_order_views.xml` y `test_sale_order_medicine.py` cumple exhaustivamente con todos los criterios de aceptación y restricciones de negocio.
