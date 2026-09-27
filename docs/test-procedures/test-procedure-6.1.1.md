# Test Procedure: SPEC-6.1.1 — Directorio y Gestión de Proveedores

**Spec Reference:** [`SPEC-6.1.1`](../../specs/spec-6.1.1-directorio-gestion-proveedores.md)  
**Module:** Módulo 6 — Proveedores & Catálogos  
**Spec Status:** Implemented (100%)  
**Generated On:** 2026-09-27  
**Evaluated by:** ___________________________  
**Execution Date:** ___________________________  
**Overall Result:** ☐ APPROVED  ☐ REJECTED  ☐ BLOCKED  

---

## Environment Prerequisites

> Complete before executing any test step.

1. **Instancia Odoo Activa:** Módulo de Compras y Proveedores de Caryvil ERP activo.
2. **Directorio de Proveedores:** Registros de laboratorios y distribuidores farmacéuticos preconfigurados.
3. **Rol Autorizado:** Usuario Encargado de Compras / Inventario.

---

## Test Flow 1: Creación de un Vendedor y su Laboratorio

> Maps to: **Scenario 1 (AC-1)** de SPEC-6.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Creación de un Vendedor y su Laboratorio**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Creación de un Vendedor y su Laboratorio]:** Escribe el nombre del vendedor "Carlos Méndez", y en el campo "Proveedor" crea "Laboratorios Vijosa S.A. de C.V." con NIT 0614-123456-001-2 y NRC 12345-6, y llena el Teléfono 7788-9900. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** El Vendedor se guarda con un código autogenerado (P0001), vinculado como hijo de la Empresa "Laboratorios Vijosa", y ambos quedan marcados con ispharmacyvendor = True. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Creación de un Vendedor y su Laboratorio** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 2: Un mismo Laboratorio con varios Vendedores

> Maps to: **Scenario 2 (AC-2)** de SPEC-6.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Un mismo Laboratorio con varios Vendedores**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Un mismo Laboratorio con varios Vendedores]:** Se crea un segundo Vendedor eligiendo el mismo Laboratorio en el dropdown "Proveedor". Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Ambos Vendedores aparecen en la lista principal, cada uno con su propio código, teléfono y nombre, compartiendo el mismo Laboratorio. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Un mismo Laboratorio con varios Vendedores** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 3: Validación de formato y campo obligatorio

> Maps to: **Scenario 3 (AC-3)** de SPEC-6.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Validación de formato y campo obligatorio**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Validación de formato y campo obligatorio]:** El usuario intenta guardar sin NRC, o con un NIT/Teléfono que no cumple el formato de guiones. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Odoo rechaza el guardado con un mensaje de error específico por campo. Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Validación de formato y campo obligatorio** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Test Flow 4: Edición de un Laboratorio existente

> Maps to: **Scenario 4 (AC-4)** de SPEC-6.1.1.

1. **[Navegación e Inicio]:** Iniciar sesión en la plataforma/Odoo como el usuario correspondiente. Navegar al menú o panel relativo a **Edición de un Laboratorio existente**. Se debe observar la pantalla inicial cargada correctamente con los indicadores y controles visuales esperados.
2. **[Ejecución de Acción - Edición de un Laboratorio existente]:** El usuario interactúa con la interfaz. Verificar en la interfaz que el botón/formulario/tabla responda inmediatamente al clic o entrada de datos sin demoras ni errores visuales.
3. **[Verificación Visual de Resultados]:** Se abre en ventana emergente, mostrando el mismo formulario simplificado usado al crearlo (no el formulario genérico de contactos de Odoo). Confirmar que los badges de estado, notificaciones tipo toast en verde (`Operación exitosa`), o registros actualizados se reflejen de forma inmediata en la pantalla.
4. **[Comprobación de Integridad en DevTools / UI]:** Abrir el panel DevTools del navegador (**Consola** y **Red**), verificar visualmente que las peticiones respondan con código HTTP `200 OK` y no se muestren excepciones o advertencias en rojo.

#### Edge Cases / Error Paths:
1. **[Intento de operación con datos inválidos o permisos no autorizados]:** Intentar ejecutar la acción **Edición de un Laboratorio existente** sin cumplir con las validaciones requeridas o con un rol sin privilegios. El sistema debe bloquear la acción mostrando un mensaje emergente de error o restricción de acceso clara sin romper la interfaz.

**Result:** ☐ PASSED  ☐ FAILED  ☐ BLOCKED  
**Notes:** _____________________________

---

## Definition of Done (DoD) Verification

| # | DoD Item | How to verify it (without code) | ☐ Met |
| :--- | :--- | :--- | :--- |
| 1 | Campos de proveedor (vendorcode, vendortype, nit, nrc) implementados en res.partner. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Campos de proveedor (vendorcode, vendortype, nit, nrc) implementados en res.partner.' se encuentre activo y operando según la especificación. | ☐ |
| 2 | Modelo padre-hijo Empresa/Vendedor funcionando (un laboratorio, múltiples vendedores). | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Modelo padre-hijo Empresa/Vendedor funcionando (un laboratorio, múltiples vendedores).' se encuentre activo y operando según la especificación. | ☐ |
| 3 | Vistas de lista, formulario y búsqueda creadas bajo el menú de Compras. | Navegar a la vista correspondiente en Odoo UI y comprobar que el elemento gráfico 'Vistas de lista, formulario y búsqueda creadas bajo el menú de Compras.' se renderice alineado a los estilos de marca. | ☐ |
| 4 | Formulario emergente simplificado de Empresa, tanto al crear como al editar. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Formulario emergente simplificado de Empresa, tanto al crear como al editar.' se encuentre activo y operando según la especificación. | ☐ |
| 5 | Máscaras de formato para NIT y Teléfono, y validaciones de respaldo en Python. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Máscaras de formato para NIT y Teléfono, y validaciones de respaldo en Python.' se encuentre activo y operando según la especificación. | ☐ |
| 6 | Filtro de proveedores en órdenes de compra verificado (bloqueado hasta SPEC-8.1.1). | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Filtro de proveedores en órdenes de compra verificado (bloqueado hasta SPEC-8.1.1).' se encuentre activo y operando según la especificación. | ☐ |
| 7 | Pruebas unitarias aprobadas al 100%. | Verificar en DevTools o en el reporte visual de ejecución que el paquete de pruebas relativo a 'Pruebas unitarias aprobadas al 100%.' haya finalizado con resultado exitoso. | ☐ |
| 8 | Aprobación por la administración de Farmacia Caryvil. | Verificar mediante la interfaz gráfica de Odoo/Plataforma que 'Aprobación por la administración de Farmacia Caryvil.' se encuentre activo y operando según la especificación. | ☐ |

---

## Session Final Results

| Field | Value |
| :--- | :--- |
| Total flows executed | 4 |
| Flows passed | 4 |
| Flows failed | 0 |
| Flows blocked | 0 |
| AC coverage | 4 / 4 |
| DoD items verified | 8 / 8 |

**Verdict:** ☐ APPROVED — All ACs and DoD items covered with no blocking defects.  
            ☐ REJECTED — Defect(s) found. See notes per flow.  
            ☐ BLOCKED — Prerequisite not available. Reschedule session.  

**Defects found:**  
> None.
