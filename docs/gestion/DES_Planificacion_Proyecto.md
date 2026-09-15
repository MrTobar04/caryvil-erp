# UNIVERSIDAD DON BOSCO
## FACULTAD DE INGENIERÍA
### ESCUELA DE COMPUTACIÓN
**DESARROLLO DE SOFTWARE EMPRESARIAL**

**PLANIFICACIÓN DE PROYECTO**

**Docente:** DELMY MAJANO  
**GITHUB:** [Odoo_ERP_Farmacia](https://github.com/MelissaFloresA/Odoo_ERP_Farmacia.git)

**Integrantes:**
* GABRIEL ERNESTO TOBAR ABREGO - TA220649
* ALEJANDRO JAVIER HERNANDEZ ORELLANA - HO221200
* MELISSA ABIGAIL FLORES ALFARO - FA220709
* WENDY MARCELA AGUILAR VASQUEZ - AV220801
* CÉSAR DANIEL GUZMÁN RAMIREZ - GR220295

**Fecha:** LUNES 17 DE AGOSTO DEL 2026

---

## Introducción

El presente proyecto tiene como propósito mejorar la forma en que Farmacia Caryvil gestiona sus principales actividades. La empresa, ubicada en Soyapango, San Salvador, actualmente utiliza algunas herramientas digitales, como una app para recibir pedidos y Excel para llevar parte de la información de sus operaciones. Sin embargo, estas herramientas funcionan de manera independiente y gran parte de los procesos todavía requiere revisiones y registros manuales. A partir del diagnóstico realizado y de la información obtenida de la empresa, se identificó que las principales dificultades se encuentran en el control de inventario, las ventas, las compras y la gestión de clientes. Por ello, el equipo propone personalizar Odoo para reunir estos procesos en un mismo sistema, facilitar el manejo de la información y reducir parte del trabajo manual que se realiza actualmente.

### 1.1 Objetivos

**Objetivo general**
Desarrollar una solución de gestión para Farmacia Caryvil mediante la personalización de Odoo, que permita organizar en un mismo sistema los procesos de inventario, ventas, compras y gestión de clientes, reduciendo el trabajo manual y facilitando el manejo de la información.

**Objetivos específicos**
* Organizar la información de los medicamentos y productos mediante un módulo de inventario que permita conocer las existencias, los lotes, las fechas de vencimiento y los niveles mínimos de stock.
* Mejorar el registro de las ventas mediante un módulo que permita llevar un control de las transacciones y relacionarlas con los productos y clientes correspondientes.
* Hacer que las ventas actualicen automáticamente las cantidades disponibles en el inventario.
* Facilitar el proceso de compras mediante el registro de proveedores y la creación de órdenes de compra, permitiendo actualizar las existencias cuando se reciba la mercadería.
* Mantener la información básica de los clientes en un mismo lugar y llevar un registro de sus compras para facilitar su consulta y seguimiento.
* Crear un dashboard que permita consultar de forma sencilla información importante sobre las ventas y el estado del inventario.

### 1.2 Alcance del proyecto

**Incluido dentro del proyecto**
* Configuración y personalización de Odoo como sistema principal.
* Creación de un dashboard de inicio con información sobre ventas y estado del inventario.
* Implementación del módulo de Inventario para registrar productos, existencias, lotes, fechas de vencimiento y niveles mínimos de stock.
* Implementación del módulo de Ventas para registrar las transacciones y generar facturas simples para consumidor final.
* Actualización automática del inventario cuando se registre una venta.
* Implementación del módulo de Compras para registrar órdenes a proveedores y la recepción de productos.
* Actualización del inventario cuando se reciba mercadería de los proveedores.
* Implementación del módulo de Clientes para guardar su información básica y consultar sus compras.
* Registro y manejo básico de Proveedores para apoyar el proceso de compras.
* Personalización de la apariencia de Odoo.
* Puesta en funcionamiento del sistema en la nube junto con la base de datos PostgreSQL.

**Excluido del proyecto**
* Integración de la aplicación actual con Odoo.
* Implementación completa del área de contabilidad y finanzas.
* Integración completa con la plataforma del Ministerio de Hacienda.
* Emisión de otros tipos de documentos fiscales además de la facturación simple para consumidor final.
* Funciones avanzadas para clientes, como campañas automáticas, segmentación o análisis detallado de sus compras.
* Implementación de una herramienta independiente de BI para análisis avanzados o predicción de la demanda.
* Integración con plataformas externas de pago, entrega u otros servicios de terceros.
* Desarrollo de una nueva aplicación, ya que el proyecto estará enfocado en la personalización del sistema de gestión en Odoo.

---

## Análisis del problema

**Entrevistada:** Ana Vilma Rivas – Propietaria de Farmacia Caryvil

**¿Cómo llevan actualmente el control de los productos que tienen en existencia?**
> *R//* Principalmente llevamos el control en Excel. También tenemos la aplicación donde aparecen los productos, pero tenemos que revisar que las cantidades coincidan porque cuando se vende algo en la farmacia no siempre se refleja ahí automáticamente. Entonces se hacen revisiones para mantenerlo actualizado.

**Cuando notan que hace falta algún medicamento, ¿cómo realizan el proceso para volver a comprarlo?**
> *R//* Primero nos damos cuenta de qué hace falta o qué ya está bajo y luego se revisa con el propietario para hacer el pedido al proveedor. Dependiendo del producto, también hay que revisar bien las cantidades que se necesitan.

**¿Cómo manejan las compras cuando llega la mercadería?**
> *R//* Cuando llega el pedido se revisa que venga lo que se solicitó y que las cantidades estén correctas. Después se actualiza el inventario.

**¿La aplicación que utilizan para los pedidos está conectada con el inventario de la farmacia?**
> *R//* No completamente. La aplicación nos sirve para recibir los pedidos y para que el cliente pueda ver los productos, pero nosotros tenemos que estar pendientes de revisar si realmente hay existencias.

**¿Cómo llevan la información de los clientes que realizan pedidos?**
> *R//* La aplicación guarda la información que el cliente coloca cuando hace el pedido. Tenemos esos datos, pero no hacemos algo más avanzado con ellos; principalmente se utilizan para poder comunicarnos y entregar el pedido.

**¿Cómo llevan la parte de las ventas y la información contable?**
> *R//* La información la vamos registrando y después se trabaja en Excel. Para la parte de facturación electrónica utilizamos la plataforma correspondiente, pero está aparte de lo demás.

**¿Qué es lo que más trabajo les genera de la forma en que llevan actualmente estos procesos?**
> *R//* Estar revisando varias veces que la información esté bien, especialmente cuando se venden productos y hay que actualizar las cantidades. También hay que estar pendientes de las compras y de que todo coincida.

**¿Qué les gustaría mejorar en la forma en que llevan actualmente la farmacia?**
> *R//* Sería bueno tener todo más organizado y poder consultar las cosas en un mismo lugar. Sobre todo, el inventario, las ventas y las compras, porque son cosas que se están revisando constantemente.

Gracias a la entrevista con la propietaria, pudimos conocer con mayor detalle cómo se llevan a cabo actualmente las principales actividades de la farmacia. La empresa cuenta con algunas herramientas digitales, como una aplicación para recibir pedidos y Excel para llevar parte de la información del negocio. Sin embargo, estas herramientas se utilizan por separado y no existe un sistema que permita manejar la información de las diferentes áreas desde un mismo lugar.

Uno de los principales problemas se encuentra en el control del inventario. La aplicación permite mostrar los productos que ofrece la farmacia, pero las cantidades no se actualizan automáticamente cuando se realiza una venta. Por esta razón, el personal debe revisar las existencias y actualizar la información de forma manual para tratar de mantenerla al día. Esto significa que una venta realizada en la farmacia y la información que aparece en la aplicación no necesariamente se actualizan al mismo tiempo. Esta situación también afecta el proceso de compras. Cuando se nota que un producto está por agotarse, primero es necesario revisar las existencias y luego comunicar la necesidad de realizar una compra. Después de hacer el pedido al proveedor y recibir la mercadería, nuevamente se deben revisar las cantidades y actualizar los registros. De esta manera, varias partes del proceso dependen de revisiones y actualizaciones hechas por el personal.

La gestión de los clientes presenta una situación un poco diferente. La aplicación permite guardar información básica de las personas que realizan pedidos, como sus datos de contacto, pero actualmente esta información se utiliza principalmente para atender y entregar los pedidos. No existe un proceso adicional que permita aprovechar esos datos para conocer mejor a los clientes o llevar un seguimiento más completo de sus compras. En cuanto a la información financiera, esta se lleva principalmente mediante Excel, mientras que la facturación electrónica se realiza de forma independiente a través de la plataforma correspondiente del Ministerio de Hacienda. Por lo tanto, estas actividades tampoco están conectadas directamente con el resto de los procesos de la farmacia.

Es así como podemos identificar un mismo problema en varias áreas de la empresa: la información se encuentra repartida y muchas tareas requieren que una persona revise, pase o actualice los datos manualmente. Por ejemplo, una venta puede cambiar la cantidad disponible de un medicamento, esa cantidad puede indicar que es necesario realizar una compra y, posteriormente, la llegada de nuevos productos debe volver a reflejarse en los registros. Actualmente, cada uno de estos pasos se maneja por separado. Esto genera trabajo adicional para el personal y hace más difícil saber cuál es la situación real de las existencias, las ventas o las compras. También aumenta la posibilidad de que se presenten diferencias entre lo que está registrado y lo que realmente tiene la farmacia. Además, cuando la propietaria necesita revisar cómo está funcionando el negocio, debe consultar información que se encuentra en diferentes lugares en lugar de tenerla disponible de una forma más sencilla.

---

## Diagrama BPMN (Diagrama de procesos de negocio)

*(Figura 1. Diagrama BPMN incluido en el documento original)*

La orquestación de estos procesos mediante este modelo asegura que cualquier evento (como una venta o el ingreso de mercadería) actualice de manera automática el resto de los componentes. Esto elimina el doble trabajo, reduce los errores de registro y proporciona visibilidad completa del estado de la farmacia en tiempo real.

---

## Diseño Técnico

### 1. Arquitectura del sistema

El sistema ERP para la farmacia Caryvil estará basado en una arquitectura cliente-servidor. A continuación, se presentan los componentes tecnológicos que se utilizarán para implementar el proyecto:

* **Servidor de aplicaciones:** Odoo ERP será utilizado como plataforma principal del sistema, aprovechando sus módulos existentes y desarrollando personalizaciones y módulos adicionales de acuerdo con las necesidades de la farmacia.
* **Módulos de Odoo:** Se utilizarán módulos estándar de Odoo y módulos personalizados para adaptar el ERP a los procesos específicos de la farmacia.
* **Plantillas y vistas:** Se utilizarán herramientas de Odoo, como XML/QWeb, para personalizar formularios, vistas, menús e informes del sistema.
* **Interfaz de usuario:** Los empleados accederán al sistema mediante la interfaz web proporcionada por Odoo, desde la cual podrán utilizar las funcionalidades correspondientes a inventario, compras, ventas, clientes y proveedores.
* **Base de datos:** La información generada por el sistema será almacenada y gestionada mediante PostgreSQL, donde se conservarán los datos relacionados con los diferentes procesos de la farmacia.
* **Despliegue:** El sistema será publicado en Render utilizando el plan gratuito, con el propósito de facilitar el acceso durante las etapas de desarrollo, pruebas y demostración.
* **Lenguaje de programación:** Python será utilizado para el desarrollo de las personalizaciones y módulos necesarios para adaptar Odoo a los procesos de la farmacia.
* **Contenedorización:** Docker será utilizado para proporcionar un entorno de ejecución aislado y reproducible para los servicios del sistema, facilitando su configuración y ejecución durante el desarrollo y, según la configuración de despliegue definida, durante la implementación.

*(Figura 2. Arquitectura técnica del sistema ERP para la farmacia Caryvil incluida en el documento original)*

La arquitectura representa la interacción entre los usuarios y los principales componentes del sistema. Los empleados accederán al ERP mediante un navegador web y la interfaz de Odoo, donde se procesará la lógica de negocio desarrollada en Python. PostgreSQL gestionará la información del sistema, mientras que Docker y Render facilitarán su ejecución y despliegue.

### 2. Herramientas de diseño y desarrollo

Para implementar el software se utilizarán diversas herramientas destinadas al diseño, desarrollo y gestión del proyecto:

* **IDE:** Visual Studio Code será utilizado como entorno de desarrollo para la creación y modificación de los módulos y componentes personalizados del sistema.
* **Control de versiones:** Git y GitHub serán utilizados para gestionar las versiones del código fuente y facilitar el trabajo colaborativo entre los integrantes del equipo.
* **Herramienta de diseño:** Figma será utilizado para la elaboración de mockups y prototipos de las interfaces del sistema, con el objetivo de definir la estructura visual de las diferentes vistas antes de su implementación.

### 3. Hardware

Para el desarrollo, despliegue y utilización del sistema ERP se consideran los siguientes requerimientos de hardware:

**Hardware para desarrollo:**
* **Computadora o laptop:** Un equipo por cada integrante encargado del desarrollo.
* **Procesador:** Intel Core i5, AMD Ryzen 5 o equivalente.
* **Memoria RAM:** 8 GB como mínimo; 16 GB recomendados.
* **Almacenamiento:** 20 GB de espacio disponible como mínimo.
* **Sistema operativo:** Windows 10/11, Linux o equivalente compatible.
* **Conexión a Internet:** Conexión estable para acceder a repositorios, servicios de despliegue y herramientas de desarrollo.

**Hardware para usuarios finales:**
* **Computadora o laptop:** Equipo capaz de ejecutar un navegador web moderno.
* **Procesador:** Intel Core i3, AMD Ryzen 3 o equivalente.
* **Memoria RAM:** 4 GB como mínimo.
* **Almacenamiento:** No se requiere un espacio específico para la instalación del ERP, debido a que este estará alojado en un servidor remoto.
* **Conexión a Internet:** Conexión estable para acceder al sistema.

### 4. Supuestos técnicos

* Se asume que las versiones seleccionadas de Odoo, Python y PostgreSQL serán compatibles entre sí durante el desarrollo e implementación del sistema.
* Se asume que los equipos de los integrantes contarán con los recursos necesarios para ejecutar las herramientas de desarrollo y los contenedores Docker requeridos por el proyecto.
* Se asume que los usuarios dispondrán de una conexión estable a Internet y de un navegador web actualizado para acceder al sistema ERP.
* Se asume que Docker permitirá configurar y ejecutar de manera consistente los servicios necesarios para el funcionamiento del sistema.
* Se asume que los recursos proporcionados por Render en su plan gratuito serán suficientes para las etapas de desarrollo, pruebas y demostración del proyecto.
* Se asume que la farmacia proporcionará la información necesaria para configurar y realizar la carga inicial del sistema, incluyendo datos de productos, clientes y proveedores.
* Se asume que cada empleado contará con credenciales de acceso y permisos definidos de acuerdo con las funciones que desempeñe dentro del sistema.
* Se asume que la información proporcionada para la carga inicial del sistema será correcta, completa y estará disponible en un formato que permita su incorporación a la base de datos.

---

## Mockups

Los mockups diseñados representan una propuesta inicial y sirven como base de referencia para visualizar la estructura, distribución y funcionamiento esperado. Sin embargo, estos diseños están sujetos a cambios y ajustes durante las etapas posteriores de desarrollo de acuerdo con las necesidades del proyecto, los requerimientos funcionales y las consideraciones técnicas que puedan surgir. Por lo tanto, la versión final de las interfaces puede presentar modificaciones respecto a lo mostrado.

Se han considerado vistas de inicio, inventario, compras, ventas, clientes y proveedores. Estos no contemplan elementos como animaciones, ventanas modales, mensajes o etiquetas dinámicas (por ejemplo, notificaciones de "medicamento editado"), entre otros componentes que se incorporarán durante el desarrollo.

**Visualización en Figma:** [Ver Mockups en Figma](https://www.figma.com/design/2acNnqCHjQkNWvyGqhVHtA/ERP_Odoo?node-id=70-1494&t=QafASzV1PzK9UZNN-1)

*(Interfaces visuales referenciadas en el documento original)*

---

## Matriz de Procesos y Valor para el negocio

| Proceso | Valor para el Negocio | Solución Propuesta (Odoo / Arquitectura) |
| :--- | :--- | :--- |
| **Gestión de Ventas y Facturación** | Trazabilidad de clientes y transacciones. Permite emitir facturas de forma automática al generar una venta (restringido a consumidor final para simplificar operaciones). | Módulo de Ventas y Facturación integrado. |
| **Control de Inventario** | Mantener un control centralizado y real sobre las existencias de medicamentos y productos de la farmacia. | Módulo de Inventario. |
| **Gestión de Compras a Proveedores** | Facilita el abastecimiento del negocio mediante la emisión de órdenes de compra formales y permite contrastarlas con las facturas recibidas. | Módulo de Compras. |
| **Gestión y Registro de Clientes** | Centralizar la base de datos de los compradores (recolectando Nombre, Apellido, DUI, correo, teléfono y dirección) para mejorar el seguimiento. | Módulo de Clientes (Contactos). |
| **Monitoreo y Reportes** | Proveer visibilidad en tiempo real del estado de la farmacia a través de métricas y reportes al abrir el sistema. | Pantalla de inicio configurada como Dashboard (Reportes). |
| **Despliegue e Infraestructura** | Garantizar la accesibilidad, estabilidad y seguridad del sistema en un entorno en la nube. | Despliegue en la nube mediante Render, utilizando una imagen de Docker y una base de datos PostgreSQL. |

---

## Cronograma (Plan de implementación)

El plan de implementación del ERP Odoo, utiliza una metodología ágil fundamentada en el desarrollo iterativo e incremental. Este enfoque permite mantener un ritmo de trabajo dinámico, garantizando la entrega continua de valor funcional y facilitando la adaptación progresiva a los requerimientos del proyecto. El plan de ejecución se ha estructurado en un total de 6 sprints, con una duración exacta de una semana cada uno.

A través de estos ciclos cortos, el equipo abordará de manera organizada todas las fases críticas, desde la configuración del entorno y el diseño inicial, hasta la personalización de los módulos, las pruebas de integración y el despliegue final. A continuación, se detalla la planificación y los objetivos específicos de cada iteración:

| Sprint (Semana) | Descripción | Tareas (Objetivos del Sprint) |
| :--- | :--- | :--- |
| **Sprint 1 (Semana 1)** | **Preparación, Entorno y Diseño Inicial**<br>Configuración de la infraestructura base de Odoo y diseño visual (mockups). | • Despliegue de la imagen Docker de Odoo junto con la base de datos PostgreSQL.<br>• Diseño de mockups en Figma para los 5 módulos (colores institucionales azul/verde).<br>• Configuración del entorno de desarrollo y pruebas.<br>• Levantamiento del documento de análisis del problema e introducción. |
| **Sprint 2 (Semana 2)** | **Personalización y Módulo de Clientes**<br>Ajustes generales del ERP y gestión de la base de datos de los clientes de la farmacia. | • Personalización de interfaz de Odoo (menú a la derecha, adaptación de colores).<br>• Implementación del módulo "Clientes".<br>• Configuración de campos obligatorios (Nombre, Apellido, DUI, Correo, Teléfono, Dirección).<br>• Pruebas de registro de clientes. |
| **Sprint 3 (Semana 3)** | **Módulos de Inventario y Compras**<br>Gestión del catálogo de medicamentos y procesos de abastecimiento con proveedores. | • Configuración del módulo "Inventario" (categorización de medicamentos).<br>• Implementación del módulo "Compras" para órdenes a proveedores.<br>• Integración de Compras con Inventario (actualización automática de stock al recibir pedidos).<br>• Mapeo y diagrama de procesos (BPMN) de compras e inventario. |
| **Sprint 4 (Semana 4)** | **Módulo de Ventas y Facturación**<br>Digitalización del ciclo de ingresos y registro de transacciones al consumidor final. | • Configuración del módulo "Ventas".<br>• Generación de facturas simples (enfocado a consumidor final, omitiendo crédito fiscal de momento).<br>• Integración de Ventas con Inventario (descuento automático de existencias al facturar).<br>• Vinculación de ventas con clientes registrados en el sistema. |
| **Sprint 5 (Semana 5)** | **Dashboard e Integración del Sistema**<br>Implementación del panel de control principal y pruebas funcionales de todo el flujo. | • Configuración del "Dashboard" (Inicio) para reportes de ventas diarias y estado del inventario.<br>• Pruebas integrales del flujo completo (Compra a proveedor → Ingreso a inventario → Venta a cliente).<br>• Resolución de bugs y ajustes de interfaz.<br>• Redacción del diseño técnico (arquitectura) en el documento entregable. |
| **Sprint 6 (Semana 6)** | **Despliegue y Documentación Final**<br>Puesta en producción del ERP y finalización de los entregables académicos. | • Despliegue de la solución final (evaluar plataforma como Render u otra según requerimientos técnicos).<br>• Cierre de la documentación: tabla de costos, cronograma, y supuestos técnicos.<br>• Elaboración de la presentación final del proyecto para la clase. |

---

## Presupuesto

**Costo de servicio**
* Por hora: $10 USD + IVA

**Costo de implementación**
Nuestros servicios están contemplados bajo un modelo de costo de implementación basado en el modelo mixto de horas/hombre con relación al producto a entregar. Cabe mencionar que estos precios son ficticios, la empresa en cuestión no incurrirá en ningún gasto al tratarse de un proyecto académico, pero son una base representativa (a la baja) de un caso real.

| Producto | Horas facturadas | Precio |
| :--- | :--- | :--- |
| Módulo de Monitorización (Dashboard) | 200 horas | $2,000 + IVA |
| Módulo de Inventario | 200 horas | $2,000 + IVA |
| Módulo de Ventas | 400 horas | $4,000 + IVA |
| Módulo de Compras | 300 horas | $3,000 + IVA |
| Módulo de Clientes (CRM) | 300 horas | $3,000 + IVA |
| **Total** | **1,200 horas** | **$12,000 + IVA** |

*\*Los precios son en dólares estadounidenses (USD), antes de IVA*  
*\*Los precios son facturados al momento de completarse los hitos*

**Costo de licenciamiento (Costos del equipo)**
Nos enfocamos en un modelo ‘low-cost’, priorizando alternativas con ‘free-tier’ generosas, que nos permitan hacer despliegues e integraciones en la nube a un costo reducido, sin que esto genere overhead técnico.

| Producto | Licencia | Costo |
| :--- | :--- | :--- |
| Odoo | Community Licence | $0 |
| Render | Free-Tier | $0 |
| Extras Base de Datos | A demanda/Por consumo | $0.25 adicional por GB mensual |
| **Total** | | **$0.25 + IVA** |

*\*Los precios son en dólares estadounidenses (USD), antes de IVA*  
*\*Los precios son facturados mensualmente*

---

## Evidencias

*(Capturas de pantalla de Odoo y Render incluidas en el documento original)*
* Odoo. (s.f.). Precios de Odoo. Recuperado el 16 de agosto de 2026, de https://www.odoo.com/es/pricing
* Render. (s.f.). Pricing. Recuperado el 16 de agosto de 2026, de https://render.com/pricing

---

## Declaración de Uso de IA
En el desarrollo de este trabajo se emplearon herramientas de inteligencia artificial (tales como ChatGPT, Gemini, Claude, Copilot y SWE-1.7) como apoyo en la comprensión conceptual y exploración técnica. Todo el contenido resultante fue revisado, adaptado y validado de forma crítica por los autores mediante un esquema propio de pruebas, asumiendo la responsabilidad total del producto final.
