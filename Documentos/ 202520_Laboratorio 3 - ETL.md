# Laboratorio 3 - Desarrollo de ETL en Google Cloud Platform

## Objetivos
- Entender con un ejercicio práctico los fundamentos y componentes básicos de un proceso ETL.
- Extender y desplegar un proceso ETL encargado de extraer información transaccional para ser cargada en un modelo multidimensional en una bodega de datos.
- Familiarizarse con algunas herramientas del proveedor de nube GCP para el desarrollo y despliegue de ETLs como son Google Storage, Google Cloud Data Fusion y BigQuery.

## Herramientas
- [GCP Storage](https://cloud.google.com/storage?hl=es): Servicio nativo de data lake proporcionado por GCP para almacenar datos no estructurados.
- [GCP Data Fusion](https://docs.cloud.google.com/data-fusion/docs/concepts/overview?hl=es-419): Servicio de datos que permite extraer, limpiar y preparar datos de forma gráfica.
- [GCP BigQuery](https://cloud.google.com/bigquery?hl=es): Plataforma de analítica de datos provista por GCP que va a desempeñar el rol de bodega de datos Data warehouse.

## Importante: Antes de la sesión de laboratorio
Redimir los créditos de forma individual a partir de la información en la sección Unificada - software requerido. En esta modalidad no se deben generar gastos de tarjeta de crédito.

Tenga en cuenta que el presente laboratorio se debe desarrollar y entregar en grupos. Sin embargo, el acceso a GCP es individual y cada estudiante contará con USD$100 para propósitos de experimentación. Estos créditos son más que suficientes para la realización del laboratorio. Además, deben reservar créditos para desarrollar el proyecto 2. La recomendación es que hagan el laboratorio utilizando los créditos de uno solo de los miembros del grupo y estén atentos al consumo de los créditos.

## Caso de estudio
**WWI (Wide World Importers)** es una empresa distribuidora que ofrece productos variados a clientes retail y naturales al mayor y al detal en diferentes ciudades de Estados Unidos.

Actualmente, la empresa se encuentra contratando un servicio de consultoría de BI con el propósito de construir herramientas analíticas para la toma decisiones basadas en datos.
Como proyecto piloto, con el objetivo de tener mayor visibilidad de sus procesos de inventario y ventas, WWI desea construir una bodega de datos en donde se incluya información histórica de las órdenes, con el detalle de los productos y tipos de empaque, agregadas por día. Adicionalmente, para WWI también es importante conocer cuanto generan las órdenes por dia en Valor Bruto de la Mercancía (GMV) .

Dado lo anterior, WWI contrata a su equipo de trabajo para que realice la implementación y despliegue de una bodega de datos y un proceso ETL que cumpla con el requerimiento planteado.

Más detalles del caso de estudio se pueden encontrar [aquí](https://learn.microsoft.com/en-us/sql/samples/wide-world-importers-what-is?view=sql-server-ver16).

## Arquitectura de la solución
Como requerimiento por parte de WWI, la solución debe ser desplegada en GCP ya que es su proveedor principal de infraestructura en la nube.
El área de datos de la empresa le ha proporcionado un conjunto de archivos en formato CSV los cuales contienen la información a ser utilizada durante este proyecto piloto.
Su equipo deberá seguir el proceso que se muestra en la figura 1 para cargar estos archivos al data lake (Storage), usando el servicio para realizar procesos de ETL (Data Fusion), en este proceso debe leer los archivos para posteriormente transformarlos y cargarlos, a la bodega de datos (BigQuery) usando un esquema estrella (modelo multidimensional).

![Arquitectura](Images/FlujoFinal.png)


## Actividades
**Etapa 1. Carga de datos a Google Cloud Storage e inicialización de un conjunto de datos en BigQuery**

1.1 Descargar los datos utilizados en el laboratorio, los cuales encuentra disponibles en este [enlace](https://gitlab.virtual.uniandes.edu.co/ISIS3301/laboratorios/-/tree/ETL/202520/Laboratorio%203%20-%20ETL/Data). 

1.2 Seguir las instrucciones básicas dadas en este [video](https://youtu.be/zmZxqjpo5UY) para subir los archivos a Google Cloud Storage. En caso de necesitarlo consultar la documentación de GCS.

1.3 Seguir las instrucciones básicas dadas en este [video](https://youtu.be/5veRi0fu8Wo) para inicializar un conjunto de datos en BigQuery. En caso de necesitarlo consultar la documentación de Big Query.

1.4 Seguir las instrucciones básicas dadas en este [video](https://youtu.be/cZzr3CsqktA) para crear una instancia en Data Fusion, para la elaboración de los flujos de datos y transformaciones.


**Etapa 2. Configurar el flujo de datos**

Ver el siguiente [video](https://youtu.be/RM6BZkybzt4) sobre como configurar y usar Data Fusion para la realización del ETL.

- El esquema base del ETL en formato JSON lo puede encontrar en este [enlace](https://gitlab.virtual.uniandes.edu.co/ISIS3301/laboratorios/-/blob/ETL/202520/Laboratorio%203%20-%20ETL/Docs/ETLPRUEBA-cdap-data-pipeline__1_.json)

- Si desea investigar sobre las directivas de línea de comandos de Wrangler para la creación de transformaciones en el flujo de datos, puede consultar la documentación disponible en este [enlace](https://docs.cloud.google.com/data-fusion/docs/concepts/wrangler-cli-directives?hl=es-419)

**Etapa 3. Proceso ETL**

Revisar este [Laboratorio](https://docs.cloud.google.com/data-fusion/docs/create-data-pipeline?hl=es) sobre el uso de Google Cloud Data Fusion para la creación y ejecución de un flujo de procesamiento de datos base. En este laboratorio encontrara los diferentes procesos que se realizan para el correcto funcionamiento de un proceso ETL.  

Como podrá observar en la interfaz de Data Fusion, el ETL proporcionado corresponde al siguiente:

![ETL](Images/ETL.png)

3.1 Analizar los diferentes subprocesos del ETL proporcionado, revise el laboratorio referenciado anteriormente para entender generalmente los procesos ETL. Identifique los nodos o bloques para la extracción de datos desde Storage, los diferentes filtros, *joins*, agregaciones y generadores de *PKs* que se encuentran implementados, así como los requeridos para la carga de datos a Data Fusion. Describa en sus propias palabras el proceso general implementado.

3.2 Extender el ETL para incluir una nueva dimensión denominada **PackageTypes** utilizando el archivo CSV con el mismo nombre (que debió descargar previamente), más una nueva medida denominada TotalPrice la cual debe ser calculada multiplicando las columnas Quantity y UnitPrice del archivo OrderLines. Además, la nueva dimensión PackageTypes debe manejarse con historia de tipo 2, de manera que se conserven los cambios históricos de sus atributos. Igualmente, se debe realizar una propuesta para manejar el identificador de la orden (OrderID) como una dimensión degenerada. Adjunte el diagrama de bloques final generado en Data Fusion, así como el archivo JSON que se exporta desde la misma interfaz de administración. Documente el diseño de estos procesos ETL, utilizando la plantilla que está disponible en este [enlace](Docs/PlantillaDiseñoETL.xlsx).

3.3 Haga un perfilamiento de los datos para cada una de las 'Recipes' del ETL.

***Importante:** Para evitar errores durante la ejecución consecutiva del ETL, se recomienda que elimine manualmente las tablas creatdas utilizando Data Fusion antes de realizar una nueva ejecución. 
Recuerde que actividades de cambios en el esquema, no son comunes en la práctica normal y, que en este laboratorio se hizo de esta manera por razones pedagógicas.*


**Etapa 4. Modelo multidimensional y análisis**

4.1 Reconstruir el modelo multidimensional que se genera en Data Fusion tras la correcta ejecución del ETL con un ejercicio de ingeniería inversa. 

4.2 Diseñar y documente el resultado de tres consultas SQL que tengan sentido para WWI (*Business questions*) y que involucren las medidas implementadas filtrando por algunas de las diferente dimensiones disponibles.

4.3 Finalmente, responder las siguientes preguntas:
- ¿Qué diferencia existe entre una arquitectura *Data warehouse* y un *Data lakehouse*? ¿Qué tipo de arquitectura le recomendaría a WWI para complementar lo desarrollado en este laboratorio incluyendo fuentes de datos no estructuradas, análisis en tiempo real que incluyan simultáneamente tanto datos estructurados como no estructurados?
- ¿Qué ventajas y desventajas observa al momento de implementar un ETL utilizando este tipo de herramientas respecto a desarrollarlo utilizando Python, Pandas y demás herramientas vistas durante la primera parte del curso?
- Investigue cómo se puede conectar a través de Tableau o Power BI a su Big Query, donde están las tablas finales creadas y con datos. Documente los hallazgos e intente conectar los datos creados del laboratorio con una de estas herramientas para crear tableros de control.
- ¿Qué tipo de tablas de hechos y de medidas se identifican en el modelo multidimensional dado? justifique la respuests. Para la tabla de hechos indique si es factless, transaccional, periódica o snapshot acumulativo. Para las medidas indique su tipo (No aditiva, Semi-aditiva o Aditiva).
- Suponga que a la dimensión Package Types del modelo creado llega información nueva y se continua con el manejo de historia de sus atributos. ¿Qué ajustes a la dimensión Package Types y al proceso ETL se deben realizar para que, al cargar la información, se incluya un manejo de historia de atributos de dimensión tipo 4? Describa cómo queda la dimensión, los atributos afectados y el proceso a seguir.
- Explore Google Cloud Data Fusion y documente sus principales características, componentes y funcionalidades. Describa cómo se pueden crear, configurar y ejecutar flujos de datos dentro de la herramienta, y en qué escenarios resulta especialmente útil su uso.
- ¿Qué errores se le presentaron en el desarrollo del laboratorio y qué solución plantearon? Haga énfasis en los que fueron más difíciles de solucionar.

## Instrucciones de Entrega

- La entrega se debe realizar en grupos de mínimo 2 estudiantes y máximo 3.
- Recuerde hacer la entrega por la sección unificada en Bloque Neón, antes del sábado 22 de noviembre a las 20:00. Este será el único medio por el cual se recibirán entregas.

## Entregables

- Diseño del proceso ETL, utilizando esta [plantilla](Docs/PlantillaDiseñoETL.xlsx), de todo lo realizado en este laboratorio.
- Descripción con sus propias palabras del paso a paso del proceso ETL final. 
- Implementación del proceso ETL generado en Data Fusion, así como el archivo JSON que se exporta desde la misma interfaz de Data Fusion.
- Modelo multidimensional que representa lo que se carga en el ETL trabajado en este laboratorio. 
- Consultas SQL utilizadas para obtener la información solicitada en la actividad 3.2 y evidencia de su correcta ejecución desde la interfaz gráfica de BigQuery.
- Respuestas a las preguntas planteadas.
- Video descriptivo de la ejecución del proceso ETL.

## Rúbrica de Calificación

| Concepto | Porcentaje |
|:---:|:---:|
| **Estudiante 1:** Diseño del ETL final (el proceso original + la extensión) y Perfilamiento de las 'Recipes'| 20% |
| **Estudiante 2:** Implementación del proceso de ETL final en Data Fusion y los archivos asociados - Diagrama y JSON del ETL final | 20% |
| **Estudiante 3:** Descripción del paso a paso del ETL final y diagrama y descripción del Modelo multidimensional| 20% |
| Video de máximo 3 minutos mostrando la correcta ejecución de los trabajos (*job*) creados en Data Fusion para el proceso del ETL final| 10% |
| Consultas SQL y evidencia de su correcta ejecución | 15% |
| Respuestas a las preguntas | 15% |


## Comentarios y recomendaciones
- **Tenga en cuenta que GCP puede presentar actualizaciones o cambios en sus herramientas. Por lo tanto, se sugiere consultar la documentación oficial en caso de que alguna funcionalidad difiera de lo mostrado durante la explicación.**
- Buckets y Bigquery se cobra por mes y por almacenamiento
- Data Fusion se cobra al ejecutar las tareas. Dado que el proceso ETL se ejecuta de forma manual y no está automatizado para que se ejecute frecuentemente, no debe existir problemas con la cantidad de créditos compartidos para el desarrollo de este laboratorio y del proyecto.
- El Json debe ser editado desde la herramienta Data Fusion. No puede ser ajustado de forma manual.
- Opciones para ver un pipeline compartido por otro usuario- Revisar la opción "Lists" abriendo el panel arriba a al izquierda ≡. Dentro estará el apartado "Drafts", ahí estará.
