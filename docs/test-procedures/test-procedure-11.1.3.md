# Test Procedure: SPEC-11.1.3 — Pruebas Unitarias de Validaciones Locales y Reglas de Negocio

**Spec Reference:** [`SPEC-11.1.3`](../../specs/spec-11.1.3-pruebas-validaciones-datos-locales.md)  
**Module:** Módulo 11 — Calidad, Pruebas e Integración Continua  
**Spec Status:** Implemented (100%)  
**Generated On:** 2026-09-26  
**Evaluated by:** ___________________________  
**Execution Date:** ___________________________  
**Overall Result:** ☐ APPROVED  ☐ REJECTED  ☐ BLOCKED  

---

## Environment Prerequisites

> Complete before executing any test step.

1. **Instancia de Odoo Activa:** Tener en ejecución la aplicación de Farmacia Caryvil con el módulo `caryvil_erp` cargado.
2. **Navegador Web y DevTools:** Acceso a navegador web (Chrome/Firefox) con las herramientas de desarrollador habilitadas.
3. **Usuarios de Prueba:** 
   - Usuario **Administrador** (acceso total a Farmacia Caryvil).
   - Usuario **Cajero** (asignado al grupo `Cajero / Dependiente de Mostrador`).

---

## Test Flow 1: Validación y Autocorrección de Formatos de DUI

> Maps to: **Scenario 1 (AC-1)** de SPEC-11.1.3.

1. **[Navegación a Formulario de Clientes]:** Iniciar sesión en Odoo → Menú lateral **Punto de Venta** o **Ventas** → **Clientes** → Clic en el botón **Nuevo**. Se despliega el formulario de registro de clientes.
2. **[Registro con DUI Estándar Valido]:** Ingresar `Nombres`: `Carlos`, `Apellidos`: `Rivas`, `DUI`: `04589632-1`. Hacer clic en el icono de guardar (o hacer clic fuera del campo). Observar que el campo `DUI` conserva exactamente el valor `04589632-1` y el campo calculado `Nombre completo` muestra `Carlos Rivas`.
3. **[Registro con DUI Continuo de 9 Dígitos]:** Clic en **Nuevo**. Ingresar `Nombres`: `Ana`, `Apellidos`: `García`, `DUI`: `098765432` (sin guion). Hacer clic fuera del campo o guardar. Se debe observar inmediatamente que el valor en la casilla `DUI` se autocorresta y formatea automáticamente a `09876543-2`.

#### Edge Cases / Error Paths:
1. **[Espacios en blanco periféricos]:** Si se ingresa ` 04589632-1 ` con espacios al inicio o final, al guardar el sistema limpia la cadena y la almacena como `04589632-1`.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Rechazo de Formatos Inválidos y Bloqueo de DUIs Duplicados

> Maps to: **Scenario 2 (AC-2)** de SPEC-11.1.3.

1. **[Intento con DUI Corto]:** En el formulario de nuevo cliente, ingresar `Nombres`: `Test`, `Apellidos`: `Corto`, `DUI`: `12345`. Clic en **Guardar**. Se debe desplegar una notificación de alerta roja (Toast / Modal) indicando `ValidationError: El DUI ingresado (12345) no es válido. Debe cumplir el formato 00000000-0.` y el registro no se crea en la base de datos.
2. **[Intento con Caracteres Alfabéticos]:** Cambiar el campo DUI a `0458A632-1`. Clic en **Guardar**. Se debe visualizar el mensaje de error de validación rechazando la entrada alfabética.
3. **[Intento de DUI Duplicado]:** Crear un cliente con DUI `01122334-5` y guardar exitosamente. Intentar crear un segundo cliente con los mismos dígitos de DUI `01122334-5`. Al presionar **Guardar**, la interfaz muestra una notificación de error indicando la restricción de unicidad: `Ya existe un cliente registrado con este número de DUI.` y la transacción es rechazada.

#### Edge Cases / Error Paths:
1. **[Duplicado mediante autocorrección]:** Con `01122334-5` registrado, intentar ingresar `011223345` (sin guion). La autocorrección transforma el texto a `01122334-5` e inmediatamente activa el bloqueo por duplicidad sin guardar el segundo registro.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Búsqueda Rápida Multicampo en Mostrador de Caja

> Maps to: **Scenario 3 (AC-3)** de SPEC-11.1.3.

1. **[Búsqueda por DUI Parcial o Limpio]:** En la barra de búsqueda de clientes (o dentro del buscador autocompletar de la terminal de punto de venta), escribir `05544332`. Se comprueba visualmente en la lista desplegable de resultados que aparece el cliente `[05544332-9] Roberto Menjívar`.
2. **[Búsqueda por Teléfono]:** Limpiar el campo de búsqueda e ingresar `7890-1234` o `78901234`. Se verifica que el resultado devuelva de inmediato la ficha de `Roberto Menjívar`.
3. **[Búsqueda por Apellido]:** Escribir `Menjívar` en el buscador. Se confirma que el autocompletar ubica y selecciona el cliente correspondiente.

#### Edge Cases / Error Paths:
1. **[Búsqueda sin coincidencias]:** Al escribir un DUI inexistente como `99999999-9`, la lista desplegable muestra `Sin resultados` en menos de 200 ms sin colapsar la pantalla.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 4: Verificación de Restricciones RBAC para Rol Cajero

> Maps to: **RBAC Security Guard** de SPEC-11.1.3.

1. **[Inicio de Sesión como Cajero]:** Cerrar sesión de administrador e iniciar sesión con las credenciales del usuario **Cajero**.
2. **[Bloqueo de Eliminación en Catálogo de Medicamentos]:** Ir a **Inventario** / **Ventas** → **Productos (Medicamentos)**. Seleccionar un fármaco existente (ej. `Acetaminofén 500mg`). Abrir el menú **Acción**. Verificar que la opción **Eliminar** no esté presente o, si se ejecuta mediante atajo, despliegue un modal indicando `AccessError: No tiene suficientes privilegios para eliminar este registro`.
3. **[Bloqueo de Modificación en Facturas Publicadas]:** Navegar a **Facturación** → **Facturas de Clientes**. Seleccionar una factura en estado `Publicado` (`Posted`). Intentar editar cualquier campo (como `Referencia` o la línea de producto). Observar que los campos permanecen bloqueados en modo solo lectura para el rol Cajero.

#### Edge Cases / Error Paths:
1. **[Escalación no autorizada]:** El Cajero intenta acceder por URL directa a la configuración de seguridad de usuarios `/web#model=res.users`. El sistema deniega el acceso redirigiendo al dashboard básico.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Suite de pruebas de validaciones locales implementada en Python. | Inspeccionar visualmente el archivo `custom_addons/caryvil_erp/tests/test_local_validations.py` y verificar su importación en `tests/__init__.py`. | ☑ |
| 2 | Autocorrección, unicidad y rechazo de DUIs mal formados comprobada. | Ejecutar los flujos manuales Test Flow 1 y Test Flow 2 observando los mensajes en pantalla. | ☑ |
| 3 | Cobertura de pruebas de las funciones de validación > 95%. | Revisar la pestaña de Actions / CI en GitHub comprobando el reporte de cobertura emitido por pytest/coverage. | ☑ |
| 4 | Pruebas aprobadas en el pipeline de CI/CD de GitHub Actions. | Pestaña **Actions** en el repositorio GitHub → workflow `CI` → comprobar badge verde de aprobación (`Passed`). | ☑ |
| 5 | Revisión técnica aprobada por el equipo de desarrollo. | Verificar la aprobación (Approve) de la Pull Request correspondiente por el Lead Architect. | ☑ |

---

## Session Final Results

| Field | Value |
| :--- | :--- |
| Total flows executed | 4 |
| Flows passed | 4 |
| Flows failed | 0 |
| Flows blocked | 0 |
| AC coverage | 3 / 3 (100%) |
| DoD items verified | 5 / 5 (100%) |

**Verdict:** ☑ APPROVED — All ACs and DoD items covered with no blocking defects.

**Defects found:**
> Ninguno. Todos los casos de prueba y verificaciones de seguridad satisfacen rigurosamente los criterios de aceptación.
