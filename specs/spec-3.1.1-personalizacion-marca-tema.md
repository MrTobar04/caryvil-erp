# SPEC-3.1.1: Personalización de Marca y Tema Visual

## 1. Objective
Personalizar la identidad visual y la apariencia estética general del ERP Odoo para Farmacia Caryvil, aplicando con exactitud la paleta de colores, componentes y patrones visuales extraídos de los mockups de diseño de la aplicación (`docs/mockups/`). Esto incluye la barra lateral de navegación oscura en azul marino corporativo (`#002B49`), la barra superior en tono gris-azul acero (`#5C6F84`), los botones de acción principal en verde salud (`#22C55E` / `#28A745`), los estados/badges contextuales (Bajo stock, Por vencer, OK, Dañado), las tarjetas de métricas tipo KPI y la tipografía moderna y limpia (Inter / Roboto), garantizando una experiencia de usuario ergonómica, atractiva y profesional.

## 2. Scope
### 2.1. Included
* Creación y configuración del archivo de estilos SCSS `custom_addons/caryvil_erp/static/src/scss/custom_theme.scss`.
* Sobreescritura de variables CSS/SCSS de Odoo (`--o-brand-primary`, `--o-brand-secondary`, `--o-community-color`, colores de fondo, botones, tablas y badges).
* Definición de la estructura cromática basada en los mockups:
  * **Sidebar (Barra Lateral Izquierda):** Fondo azul marino profundo (`#002B49`), texto de marca superior "ERP FARMACIA" en blanco negrita, iconos de cuadrícula modular para cada sección, estado activo resaltado en color cian/turquesa (`#38B6FF` / `#00C2CB`) con barra indicadora vertical lateral derecha.
  * **Topbar (Barra Superior de Navegación):** Fondo gris-azul pizarra/acero (`#5C6F84`), títulos de sección y migas de pan (*breadcrumbs*) en blanco (`#FFFFFF`), icono de notificaciones tipo campana y perfil de usuario con avatar circular (`Administrador`).
  * **Botones de Acción Primarios:** Verde salud brillante (`#28A745` / `#22C55E`) con texto blanco y bordes redondeados (e.g., `Guardar`, `Cliente Nuevo`, `Nueva Compra`, `Crear`, `Proveedor Nuevo`, `Nueva Venta`).
  * **Botones Secundarios / Cancelar:** Fondo blanco/neutro con contorno gris (`#CED4DA` / `#6C757D`) y texto oscuro (`#495057`).
  * **Badges y Etiquetas de Estado:**
    * *Bajo stock:* Fondo amarillo/ámbar suave (`#FEF3C7` / `#FFF3CD`) con texto ámbar oscuro (`#856404` / `#B45309`).
    * *Por vencer:* Fondo rosa/rojo suave (`#FEE2E2` / `#F8D7DA`) con texto rojo (`#721C24` / `#DC3545`).
    * *OK / Pagado / Activo:* Fondo verde menta suave (`#DCFCE7` / `#D1E7DD`) con texto verde oscuro (`#0F5132` / `#15803D`).
    * *Dañado / Descartado:* Fondo gris neutro (`#E2E3E5` / `#E5E7EB`) con texto gris oscuro (`#383D41` / `#4B5563`).
  * **Barra de Búsqueda y Filtros:** Entrada con diseño tipo píldora en gris claro (`#E9ECEF` / `#F1F3F5`), icono de lupa integrado y botón de embudo para filtros.
  * **Tarjetas KPI y Formularios:** Tarjetas blancas con bordes redondeados (`8px`), sombras sutiles y líneas divisorias limpias.
* Registro del asset en el bundle `web.assets_backend` dentro de `__manifest__.py`.

### 2.2. Not Included (Out of Scope)
* Personalización de la pantalla de inicio de sesión (*Login*) (cubierto en `SPEC-3.1.2`).
* Reorganización jerárquica de menús y niveles de acceso (cubierto en `SPEC-3.2.1`).
* Plantillas QWeb de reportes impresos (cubierto en `SPEC-3.3.1` y `SPEC-3.3.2`).

## 3. Context and Restrictions
* **Context:** Proporciona un entorno visual altamente pulido, moderno y congruente con los prototipos aprobados en los mockups, facilitando la operación diaria de mostrador, inventario y compras.
* **Restrictions:**
  * Total compatibilidad con el framework web de Odoo 17 / Bootstrap 5 / SCSS.
  * Mantener diseño responsivo optimizado para resoluciones de 1366x768 (pantallas POS estándar) y superiores (Full HD 1920x1080).
  * Cumplir con los estándares de accesibilidad WCAG AA (ratio de contraste mínimo 4.5:1 para texto sobre fondo).

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
* **Definition of Ready (DoR):**
  * [x] Mockups de la aplicación analizados y verificados en `docs/mockups/` (`Inicio.png`, `Clientes.png`, `Inventario.png`, `Ventas.png`, `Compras.png`, `Proveedores.png`, etc.).
  * [x] Identidad de marca "ERP FARMACIA" / "Farmacia Caryvil" y paleta institucional documentada.
  * [x] Tokens de diseño y componentes UI estandarizados.

## 5. Design (Implementation Details)
* **Color Palette Tokens (`custom_theme.scss`):**
  ```scss
  :root {
      /* Paleta Institucional - Extraída de Mockups */
      --caryvil-sidebar-bg: #002B49;
      --caryvil-sidebar-hover: #003861;
      --caryvil-sidebar-active: #38B6FF;
      --caryvil-topbar-bg: #5C6F84;
      --caryvil-topbar-text: #FFFFFF;
      --caryvil-primary-green: #28A745;
      --caryvil-primary-green-hover: #218838;
      --caryvil-accent-cyan: #38B6FF;
      
      /* Fondos y Superficies */
      --caryvil-surface-bg: #F8F9FA;
      --caryvil-card-bg: #FFFFFF;
      --caryvil-card-border: #E5E7EB;
      --caryvil-search-bg: #E9ECEF;
      
      /* Tipografía y Textos */
      --caryvil-text-main: #212529;
      --caryvil-text-muted: #6C757D;
      --caryvil-text-light: #FFFFFF;

      /* Badges y Alertas */
      --caryvil-badge-low-stock-bg: #FEF3C7;
      --caryvil-badge-low-stock-text: #B45309;
      --caryvil-badge-expiring-bg: #FEE2E2;
      --caryvil-badge-expiring-text: #DC3545;
      --caryvil-badge-ok-bg: #DCFCE7;
      --caryvil-badge-ok-text: #15803D;
      --caryvil-badge-damaged-bg: #E2E3E5;
      --caryvil-badge-damaged-text: #383D41;

      /* Sobreescrituras de Variables del Sistema Odoo */
      --o-brand-primary: var(--caryvil-primary-green);
      --o-brand-odoo: var(--caryvil-sidebar-bg);
  }

  /* Barra Lateral de Navegación (Sidebar) */
  .o_main_navbar, .caryvil-sidebar {
      background-color: var(--caryvil-sidebar-bg) !important;
      
      .brand-title {
          font-weight: 700;
          font-size: 1.15rem;
          color: #FFFFFF;
          letter-spacing: 0.5px;
          text-transform: uppercase;
      }

      .nav-item {
          color: rgba(255, 255, 255, 0.85);
          font-weight: 500;
          
          &.active {
              color: var(--caryvil-sidebar-active) !important;
              font-weight: 700;
              position: relative;

              &::after {
                  content: "";
                  position: absolute;
                  right: 0;
                  top: 15%;
                  height: 70%;
                  width: 4px;
                  background-color: var(--caryvil-sidebar-active);
                  border-radius: 2px 0 0 2px;
              }
          }
      }
  }

  /* Barra Superior de Navegación (Topbar) */
  .caryvil-topbar, .o_control_panel_top {
      background-color: var(--caryvil-topbar-bg) !important;
      color: var(--caryvil-topbar-text) !important;
      
      .breadcrumb-item, .o_page_title {
          color: #FFFFFF !important;
          font-weight: 600;
      }
      
      .breadcrumb-item.active {
          color: rgba(255, 255, 255, 0.9) !important;
      }
  }

  /* Botones de Acción Primarios */
  .btn-primary, .btn-caryvil-success {
      background-color: var(--caryvil-primary-green) !important;
      border-color: var(--caryvil-primary-green) !important;
      color: #FFFFFF !important;
      font-weight: 600;
      border-radius: 8px;
      padding: 0.5rem 1.25rem;
      
      &:hover {
          background-color: var(--caryvil-primary-green-hover) !important;
          border-color: var(--caryvil-primary-green-hover) !important;
      }
  }

  /* Botones Secundarios y Cancelar */
  .btn-secondary, .btn-caryvil-cancel {
      background-color: #FFFFFF !important;
      border: 1px solid #CED4DA !important;
      color: #495057 !important;
      font-weight: 500;
      border-radius: 8px;
      padding: 0.5rem 1.25rem;

      &:hover {
          background-color: #F8F9FA !important;
          border-color: #ADB5BD !important;
      }
  }

  /* Badges de Estado */
  .badge-bajo-stock {
      background-color: var(--caryvil-badge-low-stock-bg) !important;
      color: var(--caryvil-badge-low-stock-text) !important;
      border-radius: 12px;
      padding: 4px 12px;
      font-weight: 600;
  }

  .badge-por-vencer {
      background-color: var(--caryvil-badge-expiring-bg) !important;
      color: var(--caryvil-badge-expiring-text) !important;
      border-radius: 12px;
      padding: 4px 12px;
      font-weight: 600;
  }

  .badge-ok, .badge-pagado {
      background-color: var(--caryvil-badge-ok-bg) !important;
      color: var(--caryvil-badge-ok-text) !important;
      border-radius: 12px;
      padding: 4px 12px;
      font-weight: 600;
  }

  .badge-danado {
      background-color: var(--caryvil-badge-damaged-bg) !important;
      color: var(--caryvil-badge-damaged-text) !important;
      border-radius: 12px;
      padding: 4px 12px;
      font-weight: 600;
  }
  ```

## 6. Acceptance Criteria
* **Scenario 1: Aplicación de la barra lateral azul marino y barra superior gris-azul**
  * **Given** El módulo `caryvil_erp` instalado en Odoo.
  * **When** Un usuario autenticado ingresa a cualquier sección del ERP.
  * **Then** La interfaz debe desplegar la barra lateral con fondo azul marino (`#002B49`), el título de marca "ERP FARMACIA", la barra superior gris-azul pizarra (`#5C6F84`) y el elemento de menú activo resaltado en color cian con su indicador lateral.
* **Scenario 2: Renderizado de botones de acción y botones de cancelar**
  * **Given** Un usuario creando o editando un registro (Cliente, Medicamento, Compra o Venta).
  * **When** Visualiza la barra de control superior.
  * **Then** El botón de confirmación ("Guardar", "Crear") debe mostrarse en verde salud (`#28A745`) y el botón "Cancelar" con contorno gris y fondo blanco.
* **Scenario 3: Despliegue de badges de estado en tablas y tarjetas**
  * **Given** Registros de lotes con estados de vencimiento o stock.
  * **When** Se renderizan en las vistas de lista o dashboard.
  * **Then** Los badges deben adoptar el color contextual exacto: "Bajo stock" en fondo amarillo suave, "Por vencer" en fondo rosado/rojo suave, "OK" en fondo verde menta y "Dañado" en fondo gris neutro.
* **Scenario 4: Accesibilidad y contraste tipográfico**
  * **Given** Personal operando el ERP en diferentes condiciones de iluminación.
  * **When** Se leen los datos en tablas, campos de formulario y tarjetas.
  * **Then** El contraste cromático cumple con el estándar WCAG AA (> 4.5:1).

## 7. Verification Plan
* **Automated Tests:**
  * Compilación y linting de SCSS en el pipeline de CI/CD para asegurar compatibilidad sintáctica con Odoo 17.
* **Manual Verification:**
  * Comparación lado a lado entre la interfaz del ERP y los mockups en `docs/mockups/` (`Inicio.png`, `Inventario.png`, `Ventas_Crear.png`, etc.).
  * Verificación de contrastes de color mediante la herramienta Lighthouse / Wave.

## 8. Security and Privacy
* Cumplimiento con CSP (Content Security Policy), sin dependencias de fuentes externas no seguras ni llamadas a servicios terceros sin cifrado.

## 9. Risks and Mitigation
* **Risk:** Incompatibilidad de selectores CSS ante actualizaciones del core de Odoo.
  * **Mitigation:** Uso estricto de variables CSS nativas (`:root`) y clases modulares con aislamiento de ámbito.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/static/src/scss/custom_theme.scss`.
* Declaración del recurso en el bundle `web.assets_backend` del manifiesto `__manifest__.py`.

## 11. Definition of Done (DoD)
* [ ] Archivo `custom_theme.scss` implementado y cargado en el bundle de Odoo.
* [ ] Barra lateral `#002B49`, barra superior `#5C6F84` y botones verdes `#28A745` reflejados con exactitud según los mockups.
* [ ] Badges de estado contextuales implementados y visibles en listados y dashboard.
* [ ] Pruebas de contraste WCAG AA superadas con ratio > 4.5:1.
* [ ] Verificación de fidelidad visual contra los mockups aprobada.

