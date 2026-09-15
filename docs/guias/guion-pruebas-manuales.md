# Guión de Pruebas Manuales - Farmacia Caryvil ERP

Guía operativa para la ejecución, validación y verificación funcional manual del sistema **Farmacia Caryvil ERP**, desarrollado sobre **Odoo 17.0 Community Edition** y **PostgreSQL 16**.

---

### Índice
- [1. Propósito](#1-propósito)
- [2. Configuración Inicial](#2-configuración-inicial)
- [3. Problemas Comunes](#3-problemas-comunes)
- [4. Flujos de Verificación](#4-flujos-de-verificación)

---

## 1. Propósito

Establecer una metodología estructurada paso a paso para la verificación manual y validación funcional del sistema **Farmacia Caryvil ERP**. Este documento permite a desarrolladores, evaluadores de calidad (QA) y usuarios clave (*stakeholders*) validar de forma exhaustiva los flujos críticos de negocio:

- **Compras y Abastecimiento:** Emisión de órdenes de compra a laboratorios y recepción física con registro obligatorio de número de lote y fecha de caducidad.
- **Gestión Farmacéutica e Inventario:** Fraccionamiento de unidades (cajas, blísteres, unidades) y control de trazabilidad de lotes.
- **Venta y Despacho FEFO:** Salida prioritaria de medicamentos por fecha de vencimiento más próxima (*First Expired, First Out*).
- **Facturación y Cumplimiento Tributario:** Emisión de tickets térmicos de 80mm con validación de identificadores salvadoreños (DUI/NIT) y cálculo exacto de IVA (13%).
- **Tablero de Control:** Visualización de KPIs de venta, alertas de stock mínimo y monitor preventivo de caducidades (30, 60 y 90 días).

Este guión complementa la suite de pruebas unitarias automatizadas (`specs/spec-11.1.*`) asegurando que la experiencia de usuario y la integridad operativa se ajusten a las especificaciones formales (SDD).

---

## 2. Configuración Inicial

### 2.1. Prerrequisitos del Sistema
Para ejecutar las pruebas manuales localmente, asegúrate de contar con:
- **Docker Engine** v24.0+ y **Docker Compose** v2.20+
- **Git** v2.30+
- **Navegador Web Moderno** (Google Chrome, Mozilla Firefox, Microsoft Edge o Safari)
- **Herramienta de terminal / Shell** (Bash, Zsh o PowerShell)

### 2.2. Puesta en Marcha del Entorno
1. **Navegar a la raíz del repositorio:**
   ```bash
   cd caryvil-erp
   ```

2. **Compilar y levantar los contenedores en segundo plano:**
   ```bash
   docker compose -f infra/compose/docker-compose.yml up -d --build
   ```

3. **Verificar el estado de los servicios:**
   ```bash
   docker compose -f infra/compose/docker-compose.yml ps
   ```
   *Ambos contenedores (`caryvil-web` y `caryvil-db`) deben encontrarse en estado `Up` / `healthy`.*

4. **Inspeccionar logs de inicialización (opcional):**
   ```bash
   docker compose -f infra/compose/docker-compose.yml logs -f web
   ```

### 2.3. Parámetros de Acceso y Credenciales

| Parámetro | Valor por Defecto |
|---|---|
| **URL del Servicio Web** | [http://localhost:8069](http://localhost:8069) |
| **Base de Datos** | `caryvil_dev` |
| **Puerto PostgreSQL** | `5432` |
| **Contraseña Maestra de Odoo** | `admin_caryvil_secret_2026` |

#### Matriz de Usuarios y Roles de Prueba:

| Rol de Usuario | Login / Correo | Contraseña | Alcance Operativo |
|---|---|---|---|
| **Administrador General** | `admin` | `admin` | Control total, instalación de addons y ajustes globales |
| **Cajero / Mostrador** | `cajero@caryvil.com` | `cajero123` | Búsqueda rápida de clientes, venta en mostrador y facturación |
| **Farmacéutico / Dispensador** | `farmaceutico@caryvil.com` | `farma123` | Consulta de existencias, dispensación FEFO y mermas |
| **Encargado de Compras/Bodega** | `compras@caryvil.com` | `compras123` | Solicitudes de cotización, órdenes de compra y recepción de lotes |

### 2.4. Instalación y Verificación del Módulo `caryvil_erp`
1. Ingresar a [http://localhost:8069](http://localhost:8069) con el usuario `admin`.
2. Activar el **Modo Desarrollador** navegando a **Ajustes** -> **Activar modo de desarrollador** (o agregando `?debug=1` en la URL del navegador).
3. Acceder al menú **Aplicaciones**.
4. Hacer clic en el botón **Actualizar lista de aplicaciones** en la barra superior.
5. En la barra de búsqueda, escribir `Farmacia Caryvil ERP` (módulo técnico: `caryvil_erp`).
6. Hacer clic en **Instalar** (o **Actualizar** si ya está presente).
7. Verificar que el menú principal **Farmacia Caryvil** aparezca disponible en la barra de navegación superior.

---

## 3. Problemas Comunes

<!-- Sección reservada: se incorporarán soluciones rápidas a incidentes típicos de despliegue, caché o conectividad -->

---

## 4. Flujos de Verificación

<!-- Sección reservada: se detallarán los casos de prueba con pasos, datos de entrada y resultados esperados -->
