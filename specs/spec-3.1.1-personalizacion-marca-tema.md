# SPEC-3.1.1: Personalización de Marca y Tema Visual

## 1. Objective
Personalizar la identidad visual y la apariencia estética general del ERP Odoo para Farmacia Caryvil, aplicando la paleta de colores institucional (azul `#0B5ED7` / `#004085` y verde salud `#198754` / `#20C997`), tipografía moderna (Inter / Roboto), hojas de estilo SCSS personalizadas y la integración del logotipo oficial en la barra superior y elementos del sistema, basándose en los prototipos aprobados en Figma.

## 2. Scope
### 2.1. Included
* Creación del archivo de estilos SCSS `custom_addons/caryvil_erp/static/src/scss/custom_theme.scss`.
* Sobreescritura de variables CSS/SCSS de Odoo (`--o-brand-primary`, `--o-brand-secondary`, `--o-community-color`, colores de botones de acción y badges).
* Inyección del logotipo oficial de Farmacia Caryvil en la barra de navegación superior (*navbar*) mediante extensión XML.
* Definición de estilos para estados visuales (botones primarios en verde éxito/azul corporativo, alertas de inventario en amarillo ámbar y rojo crítico).
* Registro del asset en el bundle `web.assets_backend` dentro de `__manifest__.py`.

### 2.2. Not Included (Out of Scope)
* Personalización de la pantalla de inicio de sesión (*Login*) (cubierto en `SPEC-3.1.2`).
* Reorganización y distribución de menús de navegación (cubierto en `SPEC-3.2.1`).
* Diseño de reportes impresos QWeb (cubierto en `SPEC-3.3.1` y `SPEC-3.3.2`).

## 3. Context and Restrictions
* **Context:** Proporciona un entorno visual profesional y corporativo alineado con la identidad de marca de Farmacia Caryvil, mejorando la experiencia de usuario y reduciendo la fatiga visual del personal de mostrador.
* **Restrictions:**
  * Debe mantener total compatibilidad con el framework web de Odoo (Bootstrap 5 / SCSS).
  * No debe romper la responsividad en pantallas de tablets o monitores estándar de punto de venta (resoluciones 1366x768 o superiores).
  * El contraste cromático debe cumplir con los estándares de accesibilidad WCAG AA (ratio de contraste mínimo 4.5:1 para texto).

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
* **Definition of Ready (DoR):**
  * [x] Paleta cromática oficial y manual de identidad de Farmacia Caryvil revisados (Azul y Verde institucional).
  * [x] Prototipos de Figma inspeccionados y aprobados por el equipo de diseño UI/UX.
  * [x] Archivo de imagen del logotipo de Caryvil disponible en formato SVG/PNG con fondo transparente.

## 5. Design (Implementation Details)
* **Color Palette Tokens (`custom_theme.scss`):**
  ```scss
  :root {
      --caryvil-primary-blue: #0B5ED7;
      --caryvil-dark-blue: #004085;
      --caryvil-primary-green: #198754;
      --caryvil-light-green: #D1E7DD;
      --caryvil-accent-teal: #20C997;
      --caryvil-surface-bg: #F8F9FA;
      --caryvil-card-bg: #FFFFFF;
      --caryvil-text-main: #212529;
      --caryvil-text-muted: #6C757D;
      --caryvil-border-color: #DEE2E6;

      /* Odoo System Variable Overrides */
      --o-brand-primary: var(--caryvil-primary-blue);
      --o-brand-odoo: var(--caryvil-primary-blue);
  }

  /* Barra de Navegación Superior */
  .o_main_navbar {
      background-color: var(--caryvil-dark-blue) !important;
      border-bottom: 2px solid var(--caryvil-primary-green);
      
      .o_menu_brand {
          font-weight: 700;
          color: #FFFFFF !important;
          letter-spacing: 0.5px;
      }

      .o_nav_entry, .dropdown-toggle {
          color: rgba(255, 255, 255, 0.9) !important;
          &:hover {
              background-color: rgba(255, 255, 255, 0.15) !important;
              color: #FFFFFF !important;
          }
      }
  }

  /* Botones Principales de Acción */
  .btn-primary {
      background-color: var(--caryvil-primary-green) !important;
      border-color: var(--caryvil-primary-green) !important;
      font-weight: 600;
      border-radius: 6px;
      &:hover {
          background-color: #146c43 !important;
          border-color: #13653f !important;
      }
  }

  .btn-secondary {
      background-color: #E9ECEF !important;
      border-color: #CED4DA !important;
      color: var(--caryvil-text-main) !important;
      font-weight: 500;
      border-radius: 6px;
  }
  ```
* **Logo Injection (`views/res_company_views.xml`):**
  * Carga automatizada del logotipo corporativo en el registro de la compañía principal (`res.company`).

## 6. Acceptance Criteria
* **Scenario 1: Aplicación del tema corporativo tras instalación**
  * **Given** El módulo `caryvil_erp` instalado en Odoo.
  * **When** Cualquier usuario ingresa al backend del ERP.
  * **Then** La barra de navegación debe mostrar el fondo azul corporativo (`#004085`), el borde inferior verde (`#198754`) y los botones primarios en color verde institucional.
* **Scenario 2: Logotipo oficial visible en el navbar**
  * **Given** El usuario autenticado navegando entre diferentes módulos.
  * **When** Observa la esquina superior izquierda de la pantalla.
  * **Then** Debe visualizarse el isotipo/logotipo de Farmacia Caryvil con enlace al menú de inicio.
* **Scenario 3: Contraste y legibilidad en formularios**
  * **Given** Un dependiente de farmacia operando vistas de formulario en mostrador.
  * **When** Lee las etiquetas de campos obligatorios y botones de acción.
  * **Then** La tipografía debe renderizarse nítida y con alto contraste cumpliendo el estándar WCAG AA.

## 7. Verification Plan
* **Automated Tests:**
  * Compilación de SCSS en el pipeline de CI/CD mediante `sass custom_theme.scss /dev/null` para asegurar ausencia de errores de sintaxis CSS.
* **Manual Verification:**
  * Inspección visual en Google Chrome y Firefox verificando la correcta aplicación de colores en botones, navbar, breadcrumbs y badges.
  * Comprobación del contraste cromático mediante extensiones de accesibilidad (*Lighthouse* / *Wave*).

## 8. Security and Privacy
* Los recursos estáticos no contienen datos sensibles ni realizan peticiones externas no autorizadas (cumplimiento estricto de Content Security Policy - CSP).

## 9. Risks and Mitigation
* **Risk:** Conflicto de especificidad CSS con futuras actualizaciones de vistas de Odoo.
  * **Mitigation:** Utilizar variables CSS nativas (`:root`) y selectores de clase estándar de Odoo en lugar de sobreescrituras forzadas excesivas con `!important`.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/static/src/scss/custom_theme.scss`.
* Archivo de imagen `custom_addons/caryvil_erp/static/src/img/caryvil_logo_header.png`.
* Declaración del asset en el bundle `web.assets_backend` del manifiesto `__manifest__.py`.

## 11. Definition of Done (DoD)
* [ ] Archivo `custom_theme.scss` implementado y cargado en el bundle de Odoo.
* [ ] Paleta institucional azul/verde reflejada en toda la interfaz backend.
* [ ] Logotipo oficial renderizado correctamente en el encabezado.
* [ ] Prueba de contraste superada con ratio > 4.5:1.
* [ ] Aprobación visual por parte del responsable de diseño UI/UX.
