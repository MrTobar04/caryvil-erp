# [ADR-0010] Historial de Compras y Trazabilidad Transaccional de Clientes

## Status
Accepted

## Context
En la operación cotidiana de Farmacia Caryvil, los clientes y pacientes recurrentes solicitan apoyo frecuente para recordar tratamientos previamente adquiridos, consultar montos invertidos o solicitar reimpresión de tickets pasados. 

El modelo estándar de contactos de Odoo no consolida directamente una vista transaccional orientada al mostrador con indicadores instantáneos de compras acumuladas y acceso directo a comprobantes validados, obligando a búsquedas manuales dispersas en el módulo de facturación.

Este registro se relaciona directamente con [spec-5.2.2](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-5.2.2-historial-compras-clientes.md), [spec-5.1.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-5.1.1-gestion-perfil-clientes.md), [spec-5.2.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-5.2.1-busqueda-rapida-clientes-caja.md) y [spec-9.1.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-9.1.1-interfaz-atencion-mostrador.md).

## Decision
Hemos decidido implementar una arquitectura de trazabilidad transaccional integrada en la ficha de cliente de Odoo (`res.partner`):

1. **Campos Computados de Desempeño:** Definir los campos `caryvil_invoice_count` (Integer) y `caryvil_total_spent` (Monetary) computados mediante `_compute_caryvil_purchase_stats`, filtrando exclusivamente comprobantes en estado publicado (`state = 'posted'`) de tipo cliente (`move_type = 'out_invoice'`).
2. **Acción de Filtro Directo (`action_view_caryvil_invoices`):** Proporcionar una acción de ventana dedicada que redirige a la vista filtrada de comprobantes del cliente actual.
3. **Smart Button en Ficha de Cliente:** Incluir un botón inteligente (*Smart Button*) en la cabecera del formulario de cliente con icono `fa-shopping-bag` que exhibe el conteo de compras y el valor monetario acumulado.
4. **Pestaña de Historial de Compras y Comprobantes:** Extender el formulario de cliente con la relación One2many `caryvil_invoice_ids` para listar cronológicamente los comprobantes emitidos, fecha, total y estado de pago.

## Consequences
### Positivas:
- **Respuesta Inmediata al Paciente:** Permite identificar en segundos los medicamentos adquiridos previamente y reimprimir comprobantes.
- **Transparencia Transaccional:** Visibilidad limpia del gasto acumulado del cliente sin alterar los registros contables.
- **Filtrado Estricto de Datos:** Excluye borrador o ventas anuladas, mostrando solo información contable y fiscal confirmada.

### Negativas / Trade-offs:
- **Cómputo en Apertura:** El cálculo de montos acumulados realiza consultas de agregación sobre `account.move` para cada cliente visualizado, mitigado mediante paginación en sub-vistas One2many.
