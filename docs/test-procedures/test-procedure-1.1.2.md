# Test Procedure: SPEC-1.1.2 — Configuración del Servidor Odoo

**Spec Reference:** [`SPEC-1.1.2`](../../specs/spec-1.1.2-configuracion-servidor-odoo.md)  
**Module:** Módulo 1 — Infraestructura y Configuración Base  
**Spec Status:** Implemented (100%)  
**Generated On:** 2026-09-26  
**Evaluated by:** ___________________________  
**Execution Date:** ___________________________  
**Overall Result:** ☐ APPROVED  ☐ REJECTED  ☐ BLOCKED  

---

## Environment Prerequisites

> Complete before executing any test step.

1. **Servidor Odoo y PostgreSQL en ejecución:** El contenedor `caryvil-web` y la base de datos `caryvil-db` deben estar operativos (localmente mediante Docker Compose o desplegados en Render).
2. **Acceso a la interfaz web de Odoo:** Dominio local (`http://localhost:8069`) o URL en la nube (`https://caryvil-erp.onrender.com`) accesible vía navegador.
3. **Cuenta Administrador:** Credenciales de usuario Administrador de Odoo para acceder al modo desarrollador y gestión de aplicaciones.
4. **Navegador Web con DevTools:** Navegador Google Chrome, Firefox o Edge con panel de Developer Tools habilitado.

---

## Test Flow 1: Carga automática de módulos personalizados

> Maps to: **AC-1** de SPEC-1.1.2 (Escenario 1: Carga automática de módulos personalizados).

1. **[Navegación al Menú de Ajustes]:** Inicie sesión en Odoo como Administrador → vaya a **Ajustes** → desplácese hacia el final de la página → haga clic en **Activar modo de desarrollador**. Debería aparecer el icono de la herramienta de depuración (escarabajo) en la barra superior.
2. **[Actualización de Lista de Aplicaciones]:** Vaya al menú principal → seleccione **Aplicaciones** → en la barra superior haga clic en **Actualizar lista de aplicaciones** → confirme el diálogo flotante haciendo clic en **Actualizar**. Se debe mostrar un mensaje de confirmación en pantalla.
3. **[Verificación del Módulo Personalizado]:** En la barra de búsqueda de Aplicaciones, elimine el filtro predeterminado `Aplicaciones` y escriba `caryvil_erp`. Debe visualizarse la tarjeta de la aplicación **Caryvil ERP Base / Módulo Farmacéutico** disponible para instalación, confirmando que la directiva `addons_path` incluyó correctamente la ruta `/mnt/extra-addons`.

#### Edge Cases / Error Paths:

1. **[Ruta de Addons Inválida o No Montada]:** Si `/mnt/extra-addons` estuviera ausente de `addons_path`, al buscar `caryvil_erp` en la vista de Aplicaciones (sin filtros), el sistema muestra `No se encontraron resultados`, indicando un fallo en la resolución de la directiva de configuración.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Detección correcta de protocolo HTTPS tras proxy inverso

> Maps to: **AC-2** de SPEC-1.1.2 (Escenario 2: Detección correcta de protocolo HTTPS tras proxy inverso).

1. **[Acceso HTTPS vía Proxy Inverso]:** Abra el navegador e ingrese a la URL del servicio en la nube `https://caryvil-erp.onrender.com` (o simule la petición enviando la cabecera `X-Forwarded-Proto: https`). Verifique que la página de inicio de sesión de Odoo cargue completamente sin advertencias de certificado ni bloqueos.
2. **[Verificación de Esquema en Recursos]:** Abra las DevTools del navegador (tecla F12) → pestaña **Network (Red)** → recargue la página (Ctrl+R). Seleccione cualquier recurso cargado (CSS, JS, imágenes o respuestas AJAX) y visualice el panel de detalles. Todas las URLs en la columna de respuesta y encabezados de redirección deben utilizar el esquema `https://` y no `http://`.
3. **[Inspección de Consola DevTools]:** Vaya a la pestaña **Console (Consola)** de DevTools. Verifique visualmente que no existan errores de tipo `Mixed Content` (contenido mixto) ni advertencias de hojas de estilo/scripts bloqueados por protocolo no seguro.

#### Edge Cases / Error Paths:

1. **[Deshabilitación de Proxy Mode]:** Si `proxy_mode` estuviera fijado en `False`, al acceder mediante un balanceador HTTPS, la consola de DevTools mostraría advertencias de `Mixed Content: The page at 'https://...' was loaded over HTTPS, but requested an insecure stylesheet 'http://...'`, o provocaría un bucle infinito de redirecciones 301/302.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Instalación y disponibilidad de dependencias Python en la imagen

> Maps to: **AC-3** de SPEC-1.1.2 (Escenario 3: Instalación de dependencias Python en la imagen).

1. **[Inspección Visual de Funcionalidad QR / Formato Números]:** Inicie sesión en Odoo → navegue a una pantalla que utilice generación de código QR o impresión de documentos en letras (e.g. vista de comprobante/factura en **Facturación**). Observe visualmente que el código QR del comprobante se renderiza correctamente en pantalla sin imágenes rotas.
2. **[Verificación de Logs de Servidor en DevTools]:** Abra las DevTools del navegador → pestaña **Console** (o abra el panel de control de logs del servidor). Al realizar una acción que invoque dependencias Python (`num2words`, `qrcode`, `phonenumbers`, `psycopg2`, `python-dotenv`), confirme visualmente que los logs muestran ejecución exitosa (`[INFO] ...`) y no presentan excepciones `ModuleNotFoundError`.

#### Edge Cases / Error Paths:

1. **[Ausencia de Dependencia Python]:** Si una librería como `num2words` no estuviese instalada en la imagen Docker, al intentar generar una representación textual de montos se observaría un mensaje de error emergente (*User Error / Internal Server Error*) indicando `No module named 'num2words'`.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Archivos `infra/config/odoo.conf` y `requirements.txt` creados en el repositorio. | Verificar visualmente en la estructura del proyecto que los archivos `infra/config/odoo.conf` y `requirements.txt` están presentes. | ☑ |
| 2 | Dependencias Python instaladas y verificadas dentro del contenedor. | En la consola DevTools o logs del servicio Web Service en Render, confirmar la ejecución limpia sin errores `ModuleNotFoundError`. | ☑ |
| 3 | Carga exitosa de rutas de addons comprobada en los logs de inicialización. | En Odoo → Aplicaciones → Actualizar lista de aplicaciones, confirmar la presencia de los módulos ubicados en `/mnt/extra-addons`. | ☑ |
| 4 | `proxy_mode = True` validado sin provocar bucles de redirección. | Acceder vía `https://caryvil-erp.onrender.com` y verificar en DevTools (Red/Consola) que no existen errores de contenido mixto ni bucles HTTP/HTTPS. | ☑ |
| 5 | Revisión de código completada y aprobada. | Inspeccionar el repositorio de código y confirmar que todos los criterios de la especificación han sido validados y aprobados. | ☑ |

---

## Session Final Results

| Field | Value |
| :--- | :--- |
| Total flows executed | 3 |
| Flows passed | 3 |
| Flows failed | 0 |
| Flows blocked | 0 |
| AC coverage | 3 / 3 |
| DoD items verified | 5 / 5 |

**Verdict:** ☑ APPROVED — All ACs and DoD items covered with no blocking defects.

**Defects found:**
> Ninguno. Todos los flujos y criterios fueron verificados exitosamente.
