# Manual Verification Runbook: Catálogo de Precios y Códigos de Proveedor (SPEC-6.2.1)

## 1. Pre-requisites & Environment Setup
* **Branch/Environment:** Entorno local Docker (`docker compose -f infra/compose/docker-compose.yml up -d`) o staging en Render con módulo `caryvil_erp` actualizado.
* **Feature Flags / Módulos:** `purchase`, `stock`, `product` y `caryvil_erp` instalados y actualizados.
* **Test Data Required:**
  * Al menos 2 Laboratorios/Proveedores creados (e.g., "Laboratorios Vijosa S.A. de C.V." y "Droguería Santa Lucía").
  * Al menos 1 Medicamento registrado en `product.template` (e.g., "Amoxicilina 500mg (Caja x 50)").
  * 1 Usuario de prueba con rol `Encargado de Compras e Inventario` (`compras@caryvil.com` / `compras123`).
  * 1 Usuario de prueba con rol exclusivo `Cajero / Mostrador` (`cajero@caryvil.com` / `cajero123`).

---

## 2. Happy Path Verification (Acceptance Criteria Match)

* **Step 1: Acceso a la ficha técnica del medicamento**
  * *Acción:* Iniciar sesión como `compras@caryvil.com`, navegar a **Farmacia Caryvil** -> **Inventario y Medicamentos** -> **Medicamentos** (o catálogo de productos) y seleccionar "Amoxicilina 500mg (Caja x 50)".
  * *Expected Result:* Se despliega el formulario del producto mostrando la pestaña **Compras**.
* **Step 2: Registro del Primer Laboratorio con Descuento Determinista (CA-1)**
  * *Acción:* En la pestaña **Compras**, presionar "Agregar una línea" en la tabla de proveedores.
    - Proveedor: `Laboratorios Vijosa S.A. de C.V.`
    - Código Proveedor: `VIJ-AMX-500`
    - Presentación Proveedor: `Caja con 50 tabletas`
    - Cantidad Mínima (`min_qty`): `1.0`
    - Plazo de entrega (`delay`): `2`
    - Precio Bruto (`gross_price`): `5.00`
    - % Descuento (`discount_percentage`): `10.0`
  * *Expected Result:* El campo **Precio Neto** (`price`) se actualiza automáticamente en pantalla a `$4.50`. Al guardar el producto, la línea queda registrada en base de datos.
* **Step 3: Registro de Múltiples Proveedores para Comparativa de Costos (CA-1)**
  * *Acción:* Agregar una segunda línea en la misma tabla:
    - Proveedor: `Droguería Santa Lucía`
    - Código Proveedor: `DSL-AMX-50`
    - Presentación Proveedor: `Caja x 50 cápsulas`
    - Cantidad Mínima (`min_qty`): `1.0`
    - Plazo de entrega (`delay`): `1`
    - Precio Bruto: `4.80`
    - % Descuento: `0.0`
  * *Expected Result:* Ambas líneas coexisten en la tabla permitiendo al encargado de compras comparar de inmediato tiempos de entrega ($4.50 a 2 días vs $4.80 a 1 día).
* **Step 4: Configuración de Escala de Precios por Volumen (CA-3)**
  * *Acción:* Para `Laboratorios Vijosa S.A. de C.V.`, agregar una segunda línea con Cantidad Mínima `10.0`, Precio Bruto `5.00` y % Descuento `16.0` (Precio Neto `$4.20`).
  * *Expected Result:* Quedan configuradas dos escalas de compra para el mismo laboratorio: < 10 unidades a $4.50 y >= 10 unidades a $4.20.
* **Step 5: Autocompletado Automático en Orden de Compra (CA-2 y CA-3)**
  * *Acción:* Navegar a **Farmacia Caryvil** -> **Compras y Proveedores** -> **Órdenes de Compra**, hacer clic en **Nuevo**, seleccionar proveedor asociado a "Laboratorios Vijosa" y agregar en la tabla de productos "Amoxicilina 500mg (Caja x 50)":
    - Caso A: Cantidad = `5.0`
    - Caso B: Cantidad = `12.0`
  * *Expected Result:*
    - En Caso A: El precio unitario se autocompleta automáticamente en `$4.50` (escala normal).
    - En Caso B: El precio unitario se autocompleta automáticamente en `$4.20` (escala por volumen).
* *Pass/Fail:* [ ]

---

## 3. Unhappy Paths & Error Handling

* **Scenario A: Modificación sucesiva del porcentaje de descuento comercial**
  * *Pasos:* En una línea con Precio Bruto `$10.00`, ingresar `% Desc.` = `10.0` (calcula `$9.00`). Posteriormente cambiar `% Desc.` a `20.0`, y finalmente a `0.0`.
  * *Expected Result:* Al cambiar a `20.0`, el precio neto debe ser `$8.00` (no `$7.20`). Al cambiar a `0.0`, el precio neto debe retornar a `$10.00` íntegramente.
* **Scenario B: Descuento comercial mayor al 100% o negativo**
  * *Pasos:* Ingresar en `% Desc.` un valor de `150.0` o `-10.0`.
  * *Expected Result:* La función `_onchange_pricing_caryvil` acota el descuento entre `0.0` y `100.0`, evitando precios unitarios negativos o inconsistencias contables.
* **Scenario C: Incompatibilidad de Proveedor no Farmacéutico**
  * *Pasos:* Intentar crear una orden de compra seleccionando un contacto genérico que no tenga activo `is_pharmacy_vendor`.
  * *Expected Result:* El sistema bloquea la orden arrojando un error de validación `ValidationError: El proveedor "..." no está catalogado como proveedor farmacéutico.`

---

## 4. State & Security Edge Cases (The "Gotchas")

* **Test 1 (Confidencialidad de Costos - Perfil Cajero):**
  * *Pasos:* Cerrar sesión e ingresar con el usuario `cajero@caryvil.com` / `cajero123`. Abrir el catálogo de productos o medicamentos y revisar la pestaña de compras.
  * *Expected Result:* Las columnas `Precio Bruto`, `% Desc.`, `Presentación Proveedor` y `Precio Neto` se encuentran totalmente ocultas para el rol Cajero por las reglas de grupo `caryvil_erp.group_caryvil_compras_inventario`.
* **Test 2 (Idempotencia en Guardado de Lista de Precios):**
  * *Pasos:* Modificar el descuento comercial y guardar el formulario del producto repetidas veces (`Ctrl + S` o botón guardar).
  * *Expected Result:* El precio neto almacenado en base de datos es exactamente el valor calculado sin desviaciones por redondeo o transacciones concurrentes.
* **Test 3 (Persistencia de Vigencia de Precios):**
  * *Pasos:* Asignar fechas `date_start` y `date_end` a una lista de precios, guardar y recargar la página (`F5`).
  * *Expected Result:* Las fechas y condiciones persisten en la tabla `product_supplierinfo` de PostgreSQL.

---

## 5. Audit Findings & Loopholes Discovered

* **Critical:** Ninguno.
* **Warning:** Ninguno tras la introducción de `gross_price` (resuelto en ADR-0014).
* **Verified:**
  1. `product.supplierinfo` desacopla el precio de lista bruto del precio neto final.
  2. La vista XML extiende la tabla con visibilidad de `min_qty`, `gross_price` y `discount_percentage`.
  3. La suite de pruebas unitarias (`test_product_supplierinfo.py`) valida los criterios CA-1, CA-2 y CA-3 al 100%.
  4. Los costos de compra permanecen confidenciales ante el rol de Cajero.
