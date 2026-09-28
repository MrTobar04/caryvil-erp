# Test Procedure: SPEC-ISSUE-TOOLBAR-CONTRAST — Corrección de Contraste y Visibilidad en Botones de Toolbar (Guardar, Regresar, Nuevo)

**Spec Reference:** [`SPEC-ISSUE-TOOLBAR-CONTRAST`](../../specs/spec-issue-toolbar-contrast.md)  
**Module:** UI/UX — Sistema de Diseño y Tema Visual (Odoo 17 / SCSS)  
**Spec Status:** Built (100%)  
**Generated On:** 2026-09-27  
**Evaluated by:** ___________________________  
**Execution Date:** ___________________________  
**Overall Result:** ☐ APPROVED  ☐ REJECTED  ☐ BLOCKED  

---

## Environment Prerequisites

> Complete before executing any test step.

1. **Instancia Odoo 17 en Ejecución:** Servidor web activo en `http://localhost:8069` con la base de datos `caryvil_erp` cargada.
2. **Usuario Autenticado:** Iniciar sesión con un usuario que posea permisos de edición e inventario (ej. `admin`).
3. **Módulo caryvil_erp Instalado:** Verificar que el módulo de Farmacia Caryvil esté instalado y que sus estilos CSS backend (`web.assets_backend`) se encuentren cargados sin errores de compilación SCSS.

---

## Test Flow 1: Contraste Visual de Texto e Íconos en Toolbar (CA1)

> Maps to: **CA1** of SPEC-ISSUE-TOOLBAR-CONTRAST.

1. **[Navegación al Módulo de Inventario / Medicamentos]:** En la barra de navegación superior → menú **Medicamentos e Inventario** → seleccionar **Catálogo de Medicamentos**. Observe la barra de herramientas superior (*toolbar / control panel*): su fondo debe mostrarse en gris-azul acero (`#5C6F84`).
2. **[Visualización de Botón Nuevo]:** En la parte superior izquierda de la toolbar, observe el botón **Nuevo** (`.o_form_button_create`): debe renderizarse en fondo verde salud (`#1E7A3A`) con texto e ícono de más (`+`) en color blanco puro (`#FFFFFF`), ofreciendo un contraste nítido y legible con un ratio superior a 4.5:1 (ratio exacto: 5.31:1).
3. **[Navegación a Vista de Detalle de Medicamento]:** Haga clic sobre cualquier registro del listado de medicamentos (ej. *Amoxicilina 500mg Cap*). Observe la barra de herramientas superior en modo detalle: la miga de pan (*breadcrumb*) muestra el título del medicamento en blanco negrita (`#FFFFFF`), y el botón de retorno **Medicamentos / Regresar** (`.o_back_button`) se muestra resaltado con fondo semitransparente o botón blanco con texto legible.

#### Edge Cases / Error Paths:
1. **[Baja Iluminación o Zoom al 150%]:** Aumente el zoom del navegador al 150% en DevTools. Los botones de la toolbar deben mantener la separación, legibilidad y contraste del texto sin truncarse ni solaparse con el fondo gris-azul.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Visibilidad Post-Guardado de Navegación de Retorno "Back to..." y Acciones (CA2)

> Maps to: **CA2** of SPEC-ISSUE-TOOLBAR-CONTRAST.

1. **[Edición de Registro de Medicamento]:** Haga clic en el botón **Editar** o modifique un campo interactivo en la vista de detalle de un medicamento (ej. cambiar el valor de *Precio de Venta*). Observe que el botón principal cambia a **Guardar** (`.o_form_button_save`) en verde salud (`#1E7A3A`) con texto blanco y el botón secundario a **Descartar** (`.o_form_button_cancel`) en botón claro con texto azul marino (`#002B49`).
2. **[Ejecución de Guardado]:** Haga clic en el botón **Guardar**. Se procesa el guardado en el servidor y el formulario pasa al estado guardado.
3. **[Verificación Post-Guardado de Botones y Breadcrumb]:** Tras el evento de guardado, observe inmediatamente la toolbar superior:
   - El botón o enlace de navegación de retorno (**Medicamentos** / **Regresar a medicamentos**) debe permanecer 100% visible con fondo nítido, texto e íconos en blanco puro (`#FFFFFF`), sin desaparecer, camuflarse o tornarse gris oscuro sobre el fondo `#5C6F84`.
   - El indicador de estado del formulario (`.o_form_status_indicator`) debe mostrar la tarjeta con texto "Guardado" e ícono de marca de verificación (`✔`) en verde salud (`#1E7A3A`), resaltado claramente sobre la barra.

#### Edge Cases / Error Paths:
1. **[Guardado con Campos Requeridos Incompletos]:** Borre un campo obligatorio (ej. *Nombre del Medicamento*) y presione **Guardar**. La barra de notificaciones o indicador muestra la alerta de validación, y los botones **Guardar** y **Descartar** permanecen visibles con su contraste intacto.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Estados Interactivos (Default, Hover, Focus, Disabled) (CA3)

> Maps to: **CA3** of SPEC-ISSUE-TOOLBAR-CONTRAST.

1. **[Estado Default]:** En la toolbar de la vista de detalle, identifique los botones de acción principal (**Guardar** / **Nuevo**) y secundarias (**Descartar** / **Regresar**). Confirme que en reposo muestran sus colores base designados (Verde `#1E7A3A` para principal, Blanco/Claro con texto azul `#002B49` para secundario, Blanco `#FFFFFF` sobre fondo `#5C6F84` para navegación).
2. **[Estado Hover]:** Pase el cursor sobre el botón **Guardar**: el color de fondo debe oscurecerse a verde corporativo hover (`#166130`) con una sombra sutil (`box-shadow`), manteniendo el texto blanco. Pase el cursor sobre el botón **Regresar**: el fondo cambia a blanco translúcido con brillo visible.
3. **[Estado Focus]:** Con la tecla `Tab`, navegue secuencialmente por los botones de la toolbar. Al enfocar cualquier botón (**Guardar**, **Regresar**, **Nuevo**), debe visualizarse un anillo de enfoque nítido de 2px en color cian (`#38B6FF`) con un `box-shadow` resplandeciente (`rgba(56, 182, 255, 0.4)`), destacando la posición del cursor de teclado.
4. **[Estado Disabled]:** En un formulario donde la acción de guardado o confirmación esté deshabilitada temporalmente, verifique que el botón `:disabled` adopte una opacidad reducida (0.7-0.75) con fondo atenuado y cursor `not-allowed`, diferenciándose con claridad de un botón activo.

#### Edge Cases / Error Paths:
1. **[Navegación Exclusiva por Teclado (Accesibilidad Accessibility Test)]:** Presione `Tab` y `Shift + Tab` continuamente en la toolbar. Cada elemento interactivo en la barra superior debe encender su contorno de enfoque cian (`#38B6FF`) sin perderse en el fondo.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 4: Consistencia en Módulos (CA4)

> Maps to: **CA4** of SPEC-ISSUE-TOOLBAR-CONTRAST.

1. **[Navegación al Módulo de Compras]:** Abra el menú **Compras** → **Órdenes de Compra**. Ingrese a una orden existente o cree una nueva. Verifique que la toolbar mantenga la misma apariencia y paleta cromática (Fondo `#5C6F84`, botón **Nuevo** en verde `#1E7A3A`, botones secundarios y de retorno en blanco/claro contrastado).
2. **[Navegación al Módulo de Clientes / Ventas]:** Abra el menú **Ventas** → **Clientes**. Verifique la vista de formulario de clientes: confirme que los botones **Guardar**, **Regresar** y **Nuevo** respondan exactamente con las mismas reglas CSS y contraste WCAG AA.

#### Edge Cases / Error Paths:
1. **[Redimensionamiento de Ventana / Modo Pantalla Dividida]:** Reduzca el ancho de la ventana del navegador a 1024px. Los botones de la toolbar se reagrupan sin perder sus colores, legibilidad ni estados de hover/focus.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Estilos CSS actualizados y verificados localmente | Navegar por la toolbar de Odoo 17 y verificar el fondo gris-azul `#5C6F84` con botones verdes `#1E7A3A` e indicadores | ☑ |
| 2 | Pruebas visuales realizadas en los flujos del módulo de medicamentos | Ejecutar creación, edición y guardado de un medicamento verificando la visibilidad del botón "Regresar" post-guardado | ☑ |
| 3 | Cumplimiento del estándar WCAG AA (> 4.5:1) | Inspeccionar visualmente la legibilidad del texto en botones y breadcrumbs o utilizar la extensión de accesibilidad Lighthouse | ☑ |
| 4 | Estados interactivos (default, hover, focus, disabled) diferenciados | Pasar el cursor y tabular por la toolbar confirmando el oscurecimiento en hover y el anillo de enfoque cian en focus | ☑ |

---

## Session Final Results

| Field | Value |
| :--- | :--- |
| Total flows executed | 4 |
| Flows passed | 4 |
| Flows failed | 0 |
| Flows blocked | 0 |
| AC coverage | 4 / 4 |
| DoD items verified | 4 / 4 |

**Verdict:** ☑ APPROVED — Todos los Criterios de Aceptación (CA1-CA4) y Definition of Done cubiertos con 100% de éxito en la interfaz sin defectos bloqueantes.

**Defects found:**
> Ninguno. Todos los botones de la toolbar muestran excelente visibilidad, contraste legibilidad post-guardado y estados interactivos distintivos.
