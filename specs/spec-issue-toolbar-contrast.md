# SPEC-ISSUE-TOOLBAR-CONTRAST: Corrección de Contraste y Visibilidad en Botones de Toolbar (Guardar, Regresar, Nuevo) — **Status: Implemented** ✅

## 1. Objective
Corregir integralmente el contraste de color, los estados interactivos (`default`, `hover`, `focus`, `disabled`) y la visibilidad post-guardado de la barra de herramientas superior (*toolbar / control panel*) en Odoo 17 para la aplicación Farmacia Caryvil ERP. Se garantiza que los botones de acción principal (**Guardar**, **Nuevo**), los botones de navegación de retorno (**Regresar / Back to...**, **Descartar**) y las migas de pan (*breadcrumbs*) permanezcan legibles con un contraste superior al estándar WCAG AA (> 4.5:1) en todo momento y tras el evento de guardado en el módulo de medicamentos y vistas relacionadas.

---

## 2. Scope

### 2.1. Included
* **Ajuste de SCSS (`custom_addons/caryvil_erp/static/src/scss/custom_theme.scss`):**
  * Definición y refinamiento de reglas CSS para `.o_control_panel`, `.o_control_panel_breadcrumbs`, `button.o_back_button`, `a.o_back_button`, `.o_form_button_save`, `.o_form_button_create`, `.o_form_button_cancel`, `.o_form_status_indicator` y `.o_cp_buttons`.
  * Garantizar cumplimiento estricto del estándar de accesibilidad WCAG AA (ratio de contraste mínimo 4.5:1 para texto normal e íconos).
  * Soporte completo para los cuatro estados interactivos: `default`, `hover`, `focus` y `disabled` en todos los botones de la toolbar.
  * Preservar la visibilidad de los botones de retorno ("Back to medicamentos" / "Regresar") y acciones secundarias tras el evento de guardado en la vista de detalle de medicamentos y formularios generales.
* **Pruebas Automatizadas (`tests/test_spec_issue_toolbar_contrast.py`):**
  * Validación programática de la presencia y sintaxis de los selectores SCSS para botones de toolbar.
  * Verificación matemática del ratio de contraste WCAG AA (> 4.5:1) para cada combinación de color texto/fondo en todos los estados.
* **Procedimiento de Prueba Manual (`docs/test-procedures/test-procedure-issue-toolbar-contrast.md`):**
  * Documentación detallada paso a paso de verificación visual sin código para 100% de los Criterios de Aceptación (CAs) y la Definition of Done (DoD).

### 2.2. Not Included (Out of Scope)
* Rediseño de la estructura HTML o JavaScript del control panel nativo de Odoo 17.
* Cambios en la lógica de negocio de guardado u operaciones de servidor ORM.
* Modificaciones a temas globales no relacionados con la toolbar o botones de acción de formularios.

---

## 3. Context and Restrictions

* **Context:**
  * Al aplicar el tema personalizado de Farmacia Caryvil ERP (`SPEC-3.1.1`), la barra superior (*control panel*) adopta un fondo gris-azul acero (`#5C6F84`). En ciertos estados del formulario (especialmente post-guardado o al pasar el cursor), el texto o los íconos de botones secundarios y de navegación de retorno ("Back to...", "Regresar") se tornaban blancos sobre fondos claros o grises oscuros sobre fondos oscuros, perdiendo contraste y legibilidad.
* **Restrictions:**
  * Compatibilidad estricta con Odoo 17 Web Client / Bootstrap 5 / SCSS.
  * WCAG AA Compliance: Todos los elementos interactivos y textos de la toolbar deben superar el ratio de contraste 4.5:1 contra sus fondos respectivos.

---

## 4. Dependencias y Definición de Preparación (DoR)

### 4.1. Dependencias Previas
* `SPEC-3.1.1` (Personalización de Marca y Tema Visual).
* `SPEC-7.1.1` (Catálogo y Categorización de Medicamentos).

### 4.2. Definition of Ready (DoR) Checklist
* [x] Defectos visuales del issue analizados y reproducidos en la interfaz de Odoo 17.
* [x] Combinaciones de color evaluadas matemáticamente según el estándar WCAG 2.1 AA.
* [x] Estrategia de selectores CSS aislados en `custom_theme.scss` definida.

---

## 5. Acceptance Criteria (CAs)

* **CA1 (Contraste visual de texto e íconos):** Los botones de **Guardar**, **Regresar** y **Nuevo** en la toolbar superior deben cumplir con un contraste mínimo legible (ratio > 4.5:1) respecto al fondo de la barra en todo momento.
* **CA2 (Visibilidad post-guardado):** Al hacer clic en **Guardar**, los botones de navegación de retorno (ej. "Back to medicamentos") y acciones secundarias deben permanecer claramente visibles y no desaparecer o camuflarse con el fondo del tema.
* **CA3 (Estados interactivos):** Los botones deben mantener estados claramente diferenciados e identificables para `default`, `hover`, `focus` y `disabled`.
* **CA4 (Consistencia en módulos):** Los estilos ajustados deben aplicarse de forma consistente en la vista de detalle de medicamentos y formularios generales de la aplicación.

---

## 6. Definition of Done (DoD)

- [x] Estilos CSS/SCSS en `custom_theme.scss` actualizados y verificados.
- [x] Pruebas automatizadas de contraste y selectores implementadas y ejecutadas exitosamente.
- [x] Documento de procedimiento de prueba manual `docs/test-procedures/test-procedure-issue-toolbar-contrast.md` generado.
- [x] Verificación de los criterios de aceptación realizada.

---
