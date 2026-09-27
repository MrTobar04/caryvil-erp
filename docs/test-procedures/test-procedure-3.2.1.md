# Test Procedure: SPEC-3.2.1 — Personalización del Diseño y Navegación

**Spec Reference:** [`SPEC-3.2.1`](../../specs/spec-3.2.1-personalizacion-diseno-navegacion.md)  
**Module:** Módulo 3 — Branding UI/UX & Plantillas de Reportes  
**Spec Status:** Implemented (100%)  
**Generated On:** 2026-09-27  
**Evaluated by:** ___________________________  
**Execution Date:** ___________________________  
**Overall Result:** ☐ APPROVED  ☐ REJECTED  ☐ BLOCKED  

---

## Environment Prerequisites

> Complete before executing any test step.

1. **Instancia Odoo Activa:** Odoo 17 con tema visual y branding de Farmacia Caryvil aplicado.
2. **Plantillas e Impresora/PDF:** Generador de reportes PDF habilitado y visor PDF integrado en navegador.
3. **Usuarios de Prueba:** Usuario Administrador y Usuario Cajero/Vendedor.

---

## Test Flow 1: Despliegue de la barra lateral con 6 opciones principales

> Maps to: **Scenario 1 (AC-1)** de SPEC-3.2.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Despliegue de la barra lateral con 6 opciones principales**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Despliegue de la barra lateral con 6 opciones principales]:** Observa la barra de navegación lateral izquierda. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Debe visualizar los 6 ítems en el orden exacto: Inicio, Inventario, Ventas, Compras, Clientes y Proveedores. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Despliegue de la barra lateral con 6 opciones principales** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Indicador de menú activo y miga de pan en cabecera

> Maps to: **Scenario 2 (AC-2)** de SPEC-3.2.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Indicador de menú activo y miga de pan en cabecera**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Indicador de menú activo y miga de pan en cabecera]:** Carga la vista. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El ítem Ventas en el sidebar se ilumina en cian con su indicador lateral, y la barra superior muestra la miga de pan Ventas > Nueva Venta. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Indicador de menú activo y miga de pan en cabecera** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Controles de barra de acciones y botones

> Maps to: **Scenario 3 (AC-3)** de SPEC-3.2.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Controles de barra de acciones y botones**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Controles de barra de acciones y botones]:** Se visualiza la cabecera del contenido. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Se muestra el botón primario verde (Cliente Nuevo o Crear), la barra de búsqueda tipo píldora con placeholder descriptivo, el icono de filtro y, en Inventario, el alternador de vista Cuadrícula/Lista. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Controles de barra de acciones y botones** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 4: Restricción de visibilidad por rol de usuario

> Maps to: **Scenario 4 (AC-4)** de SPEC-3.2.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Restricción de visibilidad por rol de usuario**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Restricción de visibilidad por rol de usuario]:** Ingresa al ERP. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Visualiza únicamente Inicio, Ventas y Clientes, manteniéndose ocultos los módulos operativos de Compras e Inventario reservando la seguridad del sistema. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Restricción de visibilidad por rol de usuario** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Estructura de 6 módulos (Inicio, Inventario, Ventas, Compras, Clientes, Proveedores) implementada en caryvilmenus.xml. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Estructura de 6 módulos (Inicio, Inventario, Ventas, Compras, Clientes, Proveedores) implementada en caryvilmenus.xml.' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Breadcrumbs jerárquicos y estados activos en cian validados visualmente. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Breadcrumbs jerárquicos y estados activos en cian validados visualmente.' se encuentre activo y operando según la especificación. | ☐ |
| 3 | Botones de acción verdes y controles de búsqueda alineados con los mockups. | Iniciar sesión con un usuario no privilegiado y verificar visualmente en la interfaz que el acceso a 'Botones de acción verdes y controles de búsqueda alineados con los mockups.' quede restringido o invisible. | ☐ |
| 4 | Permisos de grupo verificados para cada rol de usuario. | Iniciar sesión con un usuario no privilegiado y verificar visualmente en la interfaz que el acceso a 'Permisos de grupo verificados para cada rol de usuario.' quede restringido o invisible. | ☐ |

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

**Verdict:** ☐ APPROVED — All ACs and DoD items covered with no blocking defects.  
            ☐ REJECTED — Defect(s) found. See notes per flow.  
            ☐ BLOCKED — Prerequisite not available. Reschedule session.  

**Defects found:**  
> None.
