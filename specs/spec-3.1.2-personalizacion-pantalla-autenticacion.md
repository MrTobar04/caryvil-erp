# SPEC-3.1.2: Personalización de Pantalla de Autenticación

## 1. Objective
Personalizar visual y estructuralmente la pantalla de inicio de sesión (*Login*) de Odoo para Farmacia Caryvil mediante la sobreescritura de la plantilla QWeb `web.login`, alineándola con la identidad visual corporativa definida en los mockups del sistema (`docs/mockups/`). Esta especificación proporciona una interfaz de bienvenida profesional, moderna y sobria que combina el azul marino corporativo (`#002B49`), una tarjeta de acceso minimalista con bordes redondeados y sombra suave, el distintivo institucional de la farmacia en Soyapango y el botón de acción principal en color verde salud (`#28A745`).

## 2. Scope
### 2.1. Included
* Creación del archivo de vista XML `custom_addons/caryvil_erp/views/web_login_templates.xml` extendiendo la plantilla `web.login`.
* Creación de los estilos asociados en `custom_addons/caryvil_erp/static/src/scss/custom_login.scss` vinculado al bundle `web.assets_frontend`.
* Integración del encabezado corporativo con el logotipo/isotipo oficial y el identificador de marca "ERP FARMACIA • Farmacia Caryvil".
* Inclusión del subtítulo institucional descriptivo: "Sistema de Gestión ERP • Sucursal Soyapango".
* Personalización de los campos de entrada (*inputs*) de correo electrónico y contraseña con borde activo en azul marino (`#002B49`) / cian (`#38B6FF`) y botón de inicio de sesión en verde vibrante (`#28A745` / `#22C55E`).
* Inclusión de pie de página discreto con créditos institucionales y aviso de confidencialidad de la farmacia.

### 2.2. Not Included (Out of Scope)
* Mecanismos de autenticación federada o Single Sign-On (SSO/OAuth) (fuera de alcance del proyecto).
* Personalización de la interfaz backend post-login (cubierto en `SPEC-3.1.1` y `SPEC-3.2.1`).

## 3. Context and Restrictions
* **Context:** Es el primer punto de contacto visual para los usuarios (propietaria, cajeros y encargados de inventario/compras) al ingresar al sistema desde computadoras de mostrador o de forma remota.
* **Restrictions:**
  * Mantener intacta la lógica de seguridad CSRF y el controlador nativo de autenticación de Odoo (`/web/login`).
  * Diseño completamente responsivo adaptado tanto a pantallas de escritorio como a dispositivos móviles o terminales compactas.
  * Sin dependencias de CDNs externos para permitir una carga instantánea y autónoma.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
  * `SPEC-3.1.1` (Personalización de Marca y Tema Visual).
* **Definition of Ready (DoR):**
  * [x] Identidad de marca y colores institucionales extraídos de los mockups de diseño (`docs/mockups/`).
  * [x] Logotipo y gráficos vectoriales preparados para fondo claro.

## 5. Design (Implementation Details)
* **Template Extension (`views/web_login_templates.xml`):**
  ```xml
  <?xml version="1.0" encoding="utf-8"?>
  <odoo>
      <template id="caryvil_web_login" inherit_id="web.login" name="Farmacia Caryvil Login">
          <xpath expr="//div[hasclass('card-body')]" position="before">
              <div class="text-center py-4 caryvil-login-header">
                  <img src="/caryvil_erp/static/src/img/caryvil_logo_full.png" 
                       alt="Farmacia Caryvil" 
                       class="img-fluid caryvil-login-logo mb-2" 
                       style="max-height: 75px;"/>
                  <h3 class="fw-bold mb-1" style="color: #002B49; letter-spacing: 0.5px;">ERP FARMACIA</h3>
                  <p class="text-muted small mb-0">Farmacia Caryvil • Soyapango</p>
              </div>
          </xpath>
          <xpath expr="//div[hasclass('card-body')]" position="after">
              <div class="text-center py-3 text-muted small border-top bg-light">
                  <span>© 2026 Farmacia Caryvil • Todos los derechos reservados</span>
              </div>
          </xpath>
      </template>
  </odoo>
  ```
* **Styles (`static/src/scss/custom_login.scss`):**
  ```scss
  body.o_home_menu_background, .oe_website_login_container {
      background: linear-gradient(135deg, #F0F4F8 0%, #D9E4EC 100%) !important;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
  }

  .card.oe_login_form {
      border: 1px solid #E5E7EB !important;
      border-radius: 12px !important;
      box-shadow: 0 12px 30px rgba(0, 43, 73, 0.1) !important;
      background-color: #FFFFFF !important;
      overflow: hidden;
      max-width: 420px;
      width: 100%;
  }

  .form-control:focus {
      border-color: #38B6FF !important;
      box-shadow: 0 0 0 0.2rem rgba(56, 182, 255, 0.25) !important;
  }

  .btn-primary.btn-block, button[type="submit"] {
      background-color: #28A745 !important;
      border-color: #28A745 !important;
      color: #FFFFFF !important;
      font-size: 1rem;
      padding: 10px 0;
      font-weight: 600;
      border-radius: 8px;
      transition: background-color 0.2s ease-in-out;
      
      &:hover {
          background-color: #218838 !important;
          border-color: #1e7e34 !important;
      }
  }
  ```

## 6. Acceptance Criteria
* **Scenario 1: Despliegue de la interfaz de autenticación corporativa**
  * **Given** Un usuario ingresando a la URL `/web/login`.
  * **When** La página se renderiza.
  * **Then** La tarjeta de inicio de sesión debe mostrar el encabezado "ERP FARMACIA", el subtítulo "Farmacia Caryvil • Soyapango", los campos estilizados y el botón de acceso en verde institucional (`#28A745`).
* **Scenario 2: Autenticación exitosa con credenciales válidas**
  * **Given** Un usuario digitando su usuario y contraseña autorizados.
  * **When** Presiona el botón verde de inicio de sesión.
  * **Then** Odoo valida el token CSRF, inicia la sesión y redirige al dashboard o módulo asignado según su rol.
* **Scenario 3: Despliegue de errores ante credenciales incorrectas**
  * **Given** Un intento de inicio de sesión con datos erróneos.
  * **When** Se procesa la petición.
  * **Then** Se muestra la notificación de error en un contenedor alert estilizado sin desconfigurar el diseño centrado de la tarjeta.

## 7. Verification Plan
* **Automated Tests:**
  * Test de renderizado de la plantilla QWeb en el suite de pruebas de Odoo.
* **Manual Verification:**
  * Abrir la pantalla de login en navegadores de escritorio y móviles para verificar alineación, proporciones del logotipo y contraste visual.

## 8. Security and Privacy
* Preservación estricta de las medidas de seguridad nativas de Odoo contra ataques de falsificación de peticiones (CSRF) y fuerza bruta.

## 9. Risks and Mitigation
* **Risk:** Superposición de estilos al actualizar dependencias del framework web.
  * **Mitigation:** Uso de selectores SCSS específicos de `oe_login_form` sin modificar el árbol DOM nativo de campos de formulario.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/views/web_login_templates.xml`.
* Archivo `custom_addons/caryvil_erp/static/src/scss/custom_login.scss`.
* Declaración del bundle `web.assets_frontend` en `__manifest__.py`.

## 11. Definition of Done (DoD)
* [ ] Plantilla XML `web_login_templates.xml` implementada y enlazada.
* [ ] Hoja de estilos `custom_login.scss` registrada y probada.
* [ ] Encabezado corporativo "ERP FARMACIA" y botón verde renderizados.
* [ ] Validación de accesibilidad y funcionamiento de login completada.

