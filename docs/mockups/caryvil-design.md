# Caryvil ERP - UI/UX Design System & Brand Guide

> **Guía de Estilo y Sistema de Diseño UI/UX para Farmacia Caryvil ERP**  
> *Fuente de verdad visual derivada de los mockups oficiales (`docs/mockups/`)*.  
> *Esta guía es de cumplimiento obligatorio para todo agente de desarrollo, diseñador y desarrollador frontend al implementar o modificar vistas, componentes, temas SCSS, plantillas QWeb y reportes.*

---

## 1. Fundamentos e Identidad de Marca

* **Nombre de la Aplicación en Shell:** `ERP FARMACIA`
* **Nombre Institucional:** `Farmacia Caryvil` (Sucursal Soyapango)
* **Propósito del Diseño:** Interfaz clínica, moderna, minimalista y de alto contraste, optimizada para operaciones rápidas de mostrador, control de inventario de medicamentos y gestión de compras farmacéuticas sin fricción visual.
* **Paradigma Estético:**
  * Barra lateral oscura de alta densidad (*Dark Navy Blue*).
  * Barra superior de contexto en tono pizarra/acero (*Slate Grey-Blue*).
  * Lienzo de trabajo claro (*Clean Light Grey/White*) con tarjetas blancas delimitadas.
  * Botones de acción y éxito en verde salud (*Vibrant Medical Green*).
  * Acentos interactivos y selección activa en cian eléctrico (*Electric Cyan*).

---

## 2. Tokens de Color y Paleta Cromática

### 2.1. Colores Principales del Sistema

| Token de Diseño | HEX | RGB | Uso y Aplicación en Interfaz |
| :--- | :--- | :--- | :--- |
| `--caryvil-sidebar-bg` | `#002B49` | `rgb(0, 43, 73)` | Fondo de la barra de navegación lateral izquierda (*Sidebar*). |
| `--caryvil-sidebar-hover` | `#003861` | `rgb(0, 56, 97)` | Estado *hover* de los elementos del menú lateral. |
| `--caryvil-sidebar-active` | `#38B6FF` | `rgb(56, 182, 255)` | Color de texto, icono y barra indicadora del menú lateral activo. |
| `--caryvil-topbar-bg` | `#5C6F84` | `rgb(92, 111, 132)` | Fondo de la barra superior (*Topbar* / Cabecera de contexto). |
| `--caryvil-topbar-text` | `#FFFFFF` | `rgb(255, 255, 255)` | Texto de títulos y migas de pan (*breadcrumbs*) en la barra superior. |
| `--caryvil-primary-green` | `#28A745` | `rgb(40, 167, 69)` | Botones de acción primaria (`Guardar`, `Crear`, `Cliente Nuevo`, etc.). |
| `--caryvil-primary-green-hover` | `#218838` | `rgb(33, 136, 56)` | Estado *hover* de botones primarios. |
| `--caryvil-accent-blue` | `#0088CC` | `rgb(0, 136, 204)` | Enlaces de acción secundaria (`Agregar un Producto`, `Añadir Lote`, líneas de total). |
| `--caryvil-surface-bg` | `#F8F9FA` | `rgb(248, 249, 250)` | Fondo del lienzo principal de la aplicación. |
| `--caryvil-card-bg` | `#FFFFFF` | `rgb(255, 255, 255)` | Fondo de tarjetas, formularios y tablas. |
| `--caryvil-card-border` | `#E5E7EB` | `rgb(229, 231, 235)` | Bordes sutiles de contenedores y separadores de tabla. |
| `--caryvil-input-bg` | `#E9ECEF` | `rgb(233, 236, 239)` | Fondo de barra de búsqueda tipo píldora y campos secundarios. |

---

### 2.2. Badges y Estados Semánticos

Los badges de estado siguen una estética tipo píldora (*pill badge*) con fondo pastel y texto de alto contraste:

| Estado | Fondo (BG) | Texto (Color) | Borde Sugerido | Contexto de Uso |
| :--- | :--- | :--- | :--- | :--- |
| **Bajo stock** | `#FEF3C7` / `#FFF3CD` | `#B45309` / `#856404` | `#FDE68A` | Medicamentos con existencia igual o inferior al stock mínimo. |
| **Por vencer** | `#FEE2E2` / `#F8D7DA` | `#DC3545` / `#721C24` | `#FECACA` | Lotes próximos a expirar en los siguientes 60–90 días. |
| **OK / Pagado / Recibida** | `#DCFCE7` / `#D1E7DD` | `#15803D` / `#0F5132` | `#BBF7D0` | Lotes vigentes, compras recibidas o facturas pagadas. |
| **Dañado / Descartado** | `#E2E3E5` / `#E5E7EB` | `#383D41` / `#4B5563` | `#D6D8DB` | Medicamentos con mermas físicas, averías o baja. |

```scss
/* Definición de clases SCSS para Badges */
.badge-caryvil {
    display: inline-block;
    padding: 4px 14px;
    font-size: 0.8125rem;
    font-weight: 600;
    border-radius: 50rem;
    text-align: center;
    line-height: 1.2;

    &.badge-low-stock {
        background-color: #FEF3C7;
        color: #B45309;
    }
    &.badge-expiring {
        background-color: #FEE2E2;
        color: #DC3545;
    }
    &.badge-ok, &.badge-paid {
        background-color: #DCFCE7;
        color: #15803D;
    }
    &.badge-damaged {
        background-color: #E2E3E5;
        color: #383D41;
    }
}
```

---

## 3. Tipografía y Jerarquía Visual

* **Familia Tipográfica:** `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif`
* **Escala y Pesos:**

| Nivel | Tamaño | Peso | Color | Ejemplo en Mockups |
| :--- | :--- | :--- | :--- | :--- |
| **Marca Sidebar** | `18px / 1.15rem` | `700` (Bold) | `#FFFFFF` | `ERP FARMACIA` (Mayúsculas con tracking ligero) |
| **Cabecera Topbar** | `20px / 1.25rem` | `600` (Semi-Bold) | `#FFFFFF` | `Clientes > Nuevo`, `Compras > Orden de Compra` |
| **Título de Formulario** | `26px / 1.65rem` | `500` / `600` | `#6B7280` / `#111827` | `Nombre del medicamento`, `PE001`, `Nombre del Cliente` |
| **Subtítulo / Código** | `16px / 1.0rem` | `400` (Regular) | `#9CA3AF` | `[Código interno]` |
| **Títulos de Sección** | `18px / 1.15rem` | `600` (Semi-Bold) | `#111827` | `Alertas importantes`, `Ventas últimos 7 días` |
| **Encabezados Tabla** | `13px / 0.8125rem`| `600` (Semi-Bold) | `#374151` | `CÓDIGO`, `NOMBRE`, `STOCK`, `VENCIMIENTO`, `ESTADO` |
| **Cuerpo de Tabla** | `14px / 0.875rem` | `400` (Regular) | `#1F2937` | Filas de clientes, compras, medicamentos |
| **KPI Contadores** | `28px / 1.75rem` | `700` (Bold) | `#1F2937` | `$ 000.00`, `# #` |

---

## 4. Estructura del Shell de la Aplicación

El diseño se compone de un esquema fijo de 3 áreas principales:

```
+-----------------------------------------------------------------------------------------------+
| ERP FARMACIA |  Topbar: Clientes > Nuevo                          🔔  Administrador (Avatar)  |
|--------------+--------------------------------------------------------------------------------|
| ⊞ Inicio     |  [ Guardar ]  [ Cancelar ]                                                     |
| ⊞ Inventario |  +---------------------------------------------------------------------------+ |
| ⊞ Ventas     |  | Tarjeta de Contenido / Formulario / Tabla                                 | |
| ⊞ Compras    |  |                                                                           | |
| ⊞ Clientes   |  |                                                                           | |
| ⊞ Proveedores|  +---------------------------------------------------------------------------+ |
+-----------------------------------------------------------------------------------------------+
```

### 4.1. Barra Lateral de Navegación (Sidebar)
* **Ancho:** `240px` (fijo en desktop).
* **Fondo:** `#002B49`
* **Logotipo/Marca:** Texto `ERP FARMACIA` en blanco negrita, centrado o alineado a la izquierda con padding superior e inferior generoso.
* **Ítems del Menú (6 secciones exactas en este orden):**
  1. `Inicio`
  2. `Inventario`
  3. `Ventas`
  4. `Compras`
  5. `Clientes`
  6. `Proveedores`
* **Iconografía:** Icono modular unificado de 4 cuadrados en cuadrícula (`⊞`).
* **Estado Activo:**
  * Color de texto e icono: `#38B6FF`.
  * Barra indicadora: Pestaña vertical de `4px` de grosor en el extremo derecho del ítem con color `#38B6FF`.

### 4.2. Barra Superior de Contexto (Topbar)
* **Altura:** `60px`
* **Fondo:** `#5C6F84`
* **Contenido Izquierdo:** Título de sección o miga de pan jerárquica en blanco (`#FFFFFF`) separada por chevrons `>` (e.g. `Compras > Nueva Orden de Compra`).
* **Contenido Derecho:**
  * Icono de notificaciones tipo campana (`🔔`) en color blanco.
  * Etiqueta de usuario/rol: `Administrador` en texto blanco.
  * Avatar circular de usuario con borde blanco sutil.

---

## 5. Especificaciones de Componentes

### 5.1. Botones de Acción

```scss
/* Botón Primario de Éxito / Guardar / Crear */
.btn-caryvil-primary {
    background-color: #28A745;
    border: 1px solid #28A745;
    color: #FFFFFF;
    font-weight: 600;
    font-size: 0.9375rem;
    padding: 8px 24px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease-in-out;

    &:hover {
        background-color: #218838;
        border-color: #1E7E34;
    }
}

/* Botón Secundario / Cancelar */
.btn-caryvil-secondary {
    background-color: #FFFFFF;
    border: 1px solid #CED4DA;
    color: #495057;
    font-weight: 500;
    font-size: 0.9375rem;
    padding: 8px 24px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease-in-out;

    &:hover {
        background-color: #F8F9FA;
        border-color: #ADB5BD;
    }
}

/* Enlaces de Acción Interactiva */
.btn-caryvil-link {
    color: #0088CC;
    font-weight: 500;
    font-size: 0.875rem;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    cursor: pointer;

    &:hover {
        text-decoration: underline;
        color: #006699;
    }
}
```

---

### 5.2. Barra de Búsqueda y Filtros de Listados

* **Caja de Búsqueda:** Forma de píldora completamente redondeada (`border-radius: 50rem`), fondo gris claro (`#E9ECEF` / `#F1F3F5`), texto descriptivo con placeholder (e.g. `Búsqueda...`, `Buscar medicamento...`) e icono de lupa en el extremo derecho.
* **Botón de Filtros:** Icono de embudo (`Y`) en contorno gris junto a la barra de búsqueda.
* **Alternador de Vistas (Inventario):** Botones en la esquina superior derecha con icono de cuadrícula/Kanban (`[🗋]`) y lista (`[☰]`).

---

### 5.3. Tarjetas KPI (Dashboard / Inicio)

* Contenedores con fondo `#FFFFFF`, bordes redondeados de `12px`, borde gris `#E5E7EB` y sombra sutil `0 4px 12px rgba(0, 0, 0, 0.03)`.
* **Estructura Interna:**
  * Izquierda: Icono/imagen enmarcado en recuadro suave.
  * Derecha: Título superior en gris (e.g., `Ventas hoy`, `Productos`, `Por vencer`), valor numérico en tipografía grande negrita (`$ 000.00`, `# #`), y subtítulo inferior (e.g. `+00.0% que ayer`, `Total de productos`, `Próximo a vencer`).

---

### 5.4. Formularios y Tarjetas de Detalle

* **Contenedor:** Tarjeta rectangular blanca de gran amplitud con borde fino `#DEE2E6` y padding generoso (`32px`).
* **Cabecera del Formulario:**
  * Recuadro de carga de imagen (cuadrado con icono de cámara y texto "Cargar imagen") para medicamentos.
  * Título de entidad en tipografía grande (`26px`).
  * Subtítulo con código entre corchetes (e.g., `[Código interno]`).
* **Pestañas de Navegación Interna (*Tabs*):**
  * Pestaña activa: Fondo blanco, borde superior y laterales cerrados, texto oscuro.
  * Pestaña inactiva: Texto gris, sin borde contenedor.
  * Ejemplos: `[ Información general | Lotes ]`, `[ Historial de Compras ]`.
* **Campos de Entrada (*Inputs*):**
  * Línea de base minimalista (*Underline input*) o inputs enmarcados limpios.
  * Labels en texto oscuro y placeholders descriptivos en gris.

---

### 5.5. Bloque de Totales y Liquidación Financiera

Ubicado en la parte inferior derecha de formularios de Ventas y Compras:
* Alineación tabular limpia de montos a la derecha.
* `SubTotal`: Valor en dólares ($).
* `Descuento`: Valor o porcentaje ($ / %).
* `IVA (13%)`: Desglose fiscal exacto.
* `Total` / `Total Pagado`: Destacado con línea horizontal azul inferior (`#38B6FF` o `#0088CC`) y tipografía negrita en color `#0088CC` o `#002B49`.
* `Monto Recibido`, `Cambio`, `Saldo Pendiente` (específico de mostrador / caja).

---

### 5.6. Tablas y Paginación

* **Cabecera:** Fondo gris claro suave (`#EEEEEE` / `#F3F4F6`), texto en mayúsculas pequeñas y negrita (`#374151`).
* **Filas:** Fondo blanco, división con línea horizontal `#E5E7EB`, padding vertical de `12px` por celda.
* **Paginación Centrada:** `<  [1]  2  3  4  ...  10  >` en el pie de página, donde la página activa se resalta con un círculo o recuadro redondeado en azul marino (`#002B49`) con número blanco.

---

## 6. Reglas de Implementación para el Agente (Do's & Don'ts)

### ✅ Lo que DEBES hacer:
1. **Respetar la paleta corporativa:** Sidebar en `#002B49`, Topbar en `#5C6F84`, botones primarios en `#28A745`, selección activa en `#38B6FF`.
2. **Mantener los 6 módulos y su orden exacto:** `Inicio` -> `Inventario` -> `Ventas` -> `Compras` -> `Clientes` -> `Proveedores`.
3. **Aplicar los Badges correctos:** Utilizar los estilos semánticos exactos para `Bajo stock`, `Por vencer`, `OK` y `Dañado`.
4. **Incluir campos financieros completos:** Todo formulario o reporte de venta/compra debe incluir `SubTotal`, `Descuento`, `IVA (13%)`, `Total`, y en caja `Monto Recibido`, `Cambio` y `Saldo Pendiente`.
5. **Garantizar contraste WCAG AA:** Verificar que todos los textos mantengan un ratio mínimo de contraste de 4.5:1 sobre sus respectivos fondos.

### ❌ Lo que NUNCA debes hacer:
1. **No usar colores genéricos desalineados:** No utilices azules estándar de Odoo (púrpura o azul genérico `#714B67`), usa siempre `#002B49` y `#5C6F84`.
2. **No alterar el orden de los menús:** No coloques Configuración como menú de primer nivel en el sidebar; debe quedar accesible bajo el flujo operativo o roles administrativos.
3. **No omitir estados ni badges:** No uses texto plano sin estilizar para advertencias de inventario o estados de factura; utiliza siempre los pill badges definidos.
4. **No usar botones rojos destructivos para acciones normales:** El botón secundario de cancelar debe ser blanco con contorno gris (`#CED4DA`), no rojo.
