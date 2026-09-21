# [ADR-0009] Búsqueda Rápida Multicampo e Indexación de Clientes en Caja

## Status
Accepted

## Context
Durante las horas de mayor afluencia en mostrador de Farmacia Caryvil, la selección del cliente dentro del formulario de venta o caja representa un cuello de botella operacional. Los clientes suelen identificarse proporcionando su número de DUI (con o sin guion), número telefónico, celular o sus apellidos.

El comportamiento por defecto del motor de búsqueda de Odoo en campos Many2one realiza consultas limitadas al campo `name` o `ref`, dificultando la localización inmediata si el usuario busca por DUI o número de contacto. Asimismo, la ficha completa de cliente contiene pestañas y campos no requeridos durante una venta rápida en caja.

Este registro se relaciona directamente con [spec-5.2.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-5.2.1-busqueda-rapida-clientes-caja.md), [spec-5.1.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-5.1.1-gestion-perfil-clientes.md) y [spec-9.1.1](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-9.1.1-interfaz-atencion-mostrador.md).

## Decision
Hemos decidido implementar una estrategia integral de optimización de búsqueda e interfaz para la selección de clientes en mostrador:

1. **Índices de Base de Datos B-Tree:** Habilitar índices explícitos (`index=True`) en PostgreSQL sobre los campos `dui`, `phone`, `mobile`, `name`, `first_name` y `last_name` en la tabla `res_partner` garantizando respuestas de búsqueda en menos de 200ms.
2. **Sobreescritura Multicriterio de `_name_search`:** Extender `_name_search` en `ResPartnerCustomer` para evaluar dominios combinados OR (`|`) sobre DUI (admitiendo búsquedas continuas sin guion), teléfonos, celulares y nombres/apellidos.
3. **Formato Desambiguado de `display_name`:** Redefinir `_compute_display_name` para que los clientes de farmacia con DUI muestren la etiqueta `[DUI] Nombre Completo - Tel: XXXXXXXX` en las listas desplegables.
4. **Vista de Alta Exprés Modal (`view_partner_simple_form_caryvil`):** Proveer una vista simplificada de creación rápida reducida a los datos mínimos de identificación y contacto para completar el registro de un cliente nuevo en menos de 15 segundos sin salir de la transacción.

## Consequences
### Positivas:
- **Alta Eficiencia Operativa:** Localización del cliente en caja en menos de 2 segundos desde el teclado.
- **Desambiguación Inmediata:** La presencia del DUI en el `display_name` previene seleccionar por error a homónimos.
- **Flexibilidad en Entrada de Datos:** Permite buscar digitando el DUI sin necesidad de teclear el guion manual.

### Negativas / Trade-offs:
- **Carga Mínima de Mantenimiento de Índices:** Creación de 6 índices B-Tree en la tabla `res_partner`, lo que añade un sobrecosto imperceptible en operaciones de escritura.
