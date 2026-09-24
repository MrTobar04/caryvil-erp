# ADR-0017: Acceso a Reglas de Reabastecimiento para Compras e Inventario

## Estado
Aceptado

## Contexto

La SPEC-7.2.2 requiere implementar reglas de reabastecimiento y stock mínimo
para los medicamentos de Caryvil ERP.

El sistema cuenta con los siguientes roles:

- Cajero / Dependiente de Mostrador
- Encargado de Compras e Inventario
- Administrador / Propietario

El grupo `group_caryvil_inventory_purchases` hereda:

- `stock.group_stock_user`
- `purchase.group_purchase_user`

Mientras que el grupo de Administrador hereda adicionalmente:

- `stock.group_stock_manager`
- `purchase.group_purchase_manager`

Durante la validación de la SPEC se comprobó que el usuario de
Compras e Inventario puede acceder al módulo de Inventario, pero no visualiza
el menú específico de Reglas de Reabastecimiento.

## Decisión

Se mantiene el grupo `Encargado de Compras e Inventario` con
`stock.group_stock_user` y no se le asignará `stock.group_stock_manager`
únicamente para habilitar el menú de Reglas de Reabastecimiento.

El grupo Administrador conservará los permisos de `stock.group_stock_manager`.

La implementación de SPEC-7.2.2 continuará utilizando las reglas de
reabastecimiento de Odoo y los permisos existentes, evitando ampliar
innecesariamente los privilegios del rol de Compras e Inventario.

## Justificación

Asignar `stock.group_stock_manager` al encargado ampliaría sus permisos
sobre Inventario más allá de las necesidades específicas de la
SPEC-7.2.2.

Mantener la separación entre `stock.group_stock_user` y
`stock.group_stock_manager` permite conservar el principio de mínimo
privilegio.

## Consecuencias

### Positivas

- Se evita otorgar permisos administrativos de Inventario al encargado.
- Se conserva la separación de responsabilidades entre roles.
- Se mantiene la configuración actual de seguridad de Caryvil ERP.
- El Administrador conserva acceso completo a la configuración de Inventario.

### Negativas

- El usuario de Compras e Inventario no visualiza actualmente el menú
  específico de Reglas de Reabastecimiento.
- Si posteriormente se requiere que dicho usuario gestione las reglas desde
  la interfaz, será necesario implementar un mecanismo de acceso específico
  sin otorgarle permisos administrativos generales.

## Relación

- SPEC-7.2.2: Reglas de Reabastecimiento y Stock Mínimo
- ADR-0016: Reglas de acceso y seguridad a nivel de modelo y registro