# SPEC-3.1.2: Personalización de Pantalla de Autenticación

## 1. Objective
Personalizar visual y estructuralmente la pantalla de inicio de sesión (*Login*) de Odoo para Farmacia Caryvil mediante la sobreescritura de la plantilla QWeb `web.login`. Esta especificación proporciona una interfaz de bienvenida corporativa, moderna y limpia que proyecta la identidad institucional de la farmacia, incorporando el logotipo oficial, mensaje descriptivo de la sucursal de Soyapango, formulario estilizado y pie de página institucional.

## 2. Scope
### 2.1. Included
* Creación del archivo de vista XML `custom_addons/caryvil_erp/views/web_login_templates.xml` extendiendo la plantilla `web.login`.
* Creación de los estilos asociados en `custom_addons/caryvil_erp/static/src/scss/custom_login.scss` vinculado a `web.assets_frontend`.
* Integración del logotipo principal de Farmacia Caryvil en alta resolución sobre la tarjeta de autenticación.
* Inclusión del subtítulo institucional: "Sistema Integral de Gestión ERP • Farmacia Caryvil • Soyapango".
* Personalización de los campos de entrada (*inputs*) de correo/usuario y contraseña con iconos descriptivos, foco resaltado en azul corporativo y botón de ingreso en verde institucional.
* Inclusión de pie de página discreto con créditos de la Universidad Don Bosco (UDB) y aviso de confidencialidad.

### 2.2. Not Included (Out of Scope)
* Mecanismos de autenticación federada o single sign-on (SSO/OAuth) (fuera de alcance del proyecto).
* Personalización de la interfaz backend post-login (cubierto en `SPEC-3.1.1` y `SPEC-3.2.1`).

## 3. Context and Restrictions
* **Context:** Es el primer punto de contacto visual para los usuarios (propietaria, cajeros y encargados de compras) al ingresar al sistema desde cualquier dispositivo en la farmacia o de forma remota.
* **Restrictions:**
  * Debe mantener intacta la lógica de seguridad CSRF y el flujo de autenticación nativo de Odoo (`/web/login`).
  * Debe ser completamente responsivo, adaptándose con elegancia tanto a pantallas móviles como a monitores de escritorio.
  * No debe depender de CDNs externos para permitir arranque rápido en redes locales o con baja latencia.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-2.1.1` (Estructura del Módulo Personalizado caryvil_erp).
  * `SPEC-3.1.1` (Personalización de Marca y Tema Visual).
* **Definition of Ready (DoR):**
  * [x] Logotipo oficial en alta resolución optimizado para fondos claros/oscuros.
  * [x] Prototipo de pantalla de login en Figma validado.

## 5. Design (Implementation Details)
* **Template Extension (`views/web_login_templates.xml`):**
  ```xml
  <?xml version="1.0" encoding="utf-8"?>
  <odoo>
      <template id="caryvil_web_login" inherit_id="web.login" name="Farmacia Caryvil Login">
          <xpath expr="//div[hasclass('card-body')]" position="before">
              <div class="text-center py-3 caryvil-login-header">
                  <img src="/caryvil_erp/static/src/img/caryvil_logo_full.png" 
                       alt="Farmacia Caryvil" 
                       class="img-fluid caryvil-login-logo mb-2" 
                       style="max-height: 80px;"/>
                  <h4 class="fw-bold text-primary mb-1">Farmacia Caryvil</h4>
                  <p class="text-muted small mb-0">Sistema de Gestión Farmacéutica • Soyapango</p>
              </div>
          </xpath>
          <xpath expr="//div[hasclass('card-body')]" position="after">
              <div class="text-center py-2 text-muted small border-top">
                  <span>© 2026 Farmacia Caryvil • Universidad Don Bosco</span>
              </div>
          </xpath>
      </template>
  </odoo>
  ```
* **Styles (`static/src/scss/custom_login.scss`):**
  ```scss
  body.o_home_menu_background, .oe_website_login_container {
      background: linear-gradient(135deg, #EBF3FB 0%, #D8EAF8 100%) !important;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
  }

  .card.oe_login_form {
      border: none !important;
      border-radius: 12px !important;
      box-shadow: 0 10px 25px rgba(0, 64, 133, 0.12) !important;
      overflow: hidden;
      max-width: 420px;
      width: 100%;
  }

  .btn-primary.btn-block {
      background-color: #198754 !important;
      border-color: #198754 !important;
      font-size: 1rem;
      padding: 10px 0;
      font-weight: 600;
      border-radius: 6px;
      &:hover {
          background-color: #146c43 !important;
      }
  }
  ```

## 6. Acceptance Criteria
* **Scenario 1: Acceso a la ruta `/web/login`**
  * **Given** Un usuario navegando a la URL del ERP `http://localhost:8069/web/login`.
  * **When** La página carga completamente.
  * **Then** Debe mostrarse la tarjeta de inicio de sesión con el logotipo oficial de Farmacia Caryvil, el subtítulo de Soyapango y el degradado azul suave de fondo.
* **Scenario 2: Autenticación exitosa con credenciales válidas**
  * **Given** Un usuario ingresando su correo y contraseña correctos.
  * **When** Hace clic en el botón "Iniciar Sesión" (color verde).
  * **Then** El sistema debe autenticar la sesión, validar el token CSRF y redirigir al usuario al backend de Odoo.
* **Scenario 3: Manejo de errores con credenciales inválidas**
  * **Given** Un usuario ingresando una contraseña incorrecta.
  * **When** Presiona ingresar.
  * **Then** La pantalla debe mostrar el mensaje de alerta nativo de Odoo "Contraseña/Usuario incorrecto" con formato estilizado sin romper el layout corporativo.

## 7. Verification Plan
* **Automated Tests:**
  * Prueba de renderizado de la plantilla XML en el test suite de Odoo (`test_web_login_render`).
* **Manual Verification:**
  * Abrir la pantalla de login en modo incógnito desde desktop y dispositivo móvil.
  * Validar la correcta carga de imágenes y estilos sin advertencias en la consola del navegador.

## 8. Security and Privacy
* Preservación del campo oculto `csrf_token` generado por el controlador web de Odoo.
* Protección contra visualización de contraseñas mediante campos de tipo `password`.

## 9. Risks and Mitigation
* **Risk:** Ruptura visual del login en pantallas de baja resolución (smartphones o POS compactos).
  * **Mitigation:** Uso de clases responsivas de Bootstrap (`img-fluid`, `max-width: 420px`) y contenedor flexible centrado.

## 10. Deliverables & Config as Code
* Archivo `custom_addons/caryvil_erp/views/web_login_templates.xml`.
* Archivo `custom_addons/caryvil_erp/static/src/scss/custom_login.scss`.
* Archivo de imagen `custom_addons/caryvil_erp/static/src/img/caryvil_logo_full.png`.
* Declaración del bundle `web.assets_frontend` en `__manifest__.py`.

## 11. Definition of Done (DoD)
* [ ] Plantilla XML `web_login_templates.xml` extendida e integrada en el manifiesto.
* [ ] Hoja de estilos `custom_login.scss` aplicada y verificada.
* [ ] Imagen del logotipo visible y escalada correctamente.
* [ ] Flujo de autenticación y manejo de errores de credenciales probado.
* [ ] Aprobación de diseño UI/UX confirmada.
