
<center><h1> Proyecto Despliegue Soluciones Analíticas</h1></center>

## Problema y contexto

El desafío principal que se aborda en este proyecto está relacionado con la inconsistencia e imprevisibilidad de los retrasos en vuelos comerciales generados por una compleja interacción entre diferentes factores como las condiciones climáticas, la temporada del año, la aerolínea, el origen, el destino, entre otros. Este problema impacta directamente la experiencia de los pasajeros y la eficiencia de las aerolíneas conllevando a costos adicionales, interrupciones en la operación y una disminución en la calidad del servicio.

## Pregunta de negocio y alcance del proyecto

¿Cómo podemos predecir con precisión los retrasos de vuelos comerciales utilizando datos históricos de vuelos y condiciones climáticas durante el período de abril a octubre de 2013?

**Alcance del Proyecto:**

-	Recopilación, limpieza y transformación de datos de vuelos comerciales y registros climatológicos del periodo de interés (abril a octubre de 2013).
-	Integración de los conjuntos de datos.
-	Exploración de los conjuntos de datos.
-	Selección y entrenamiento de modelos para la predicción de retrasos.
-	Creación de tablero de visualización de datos históricos.
-	Integración del tablero con una interfaz de captura de datos para realizar predicciones de retrasos.
-	Despliegue y operación de la solución (incluye tablero e interfaz de interacción con el modelo predictivo). 
-	Todo lo anterior, realizado bajo las mejores prácticas de MLOPS para el versionamiento de modelos, código, experimentos y su reproducibilidad.
-	El objetivo final del proyecto es proporcionar información útil para la toma de decisiones operativas y estratégicas en aerolíneas y aeropuertos.


## Descripción de los datos utilizados en este proyecto

Los datos se obtienen del Buró de Estadísticas de Transporte del Departamento de Transporte de los Estados Unidos (DOT) quien realiza un seguimiento puntual de los vuelos nacionales operados por grandes transportistas aéreos.

En este proyecto vamos a trabajar con datos de vuelos y condiciones climáticas que contienen información diaria de abril a octubre de 2013. La base de vuelos contiene 14 variables y poco más de 1 millón de registros y la base de condiciones climáticas tiene 26 columnas y más de 400.000 registros.

En términos generales tenemos información de origen, destino, fechas, horas, retrasos, cancelaciones e información climática de cada vuelo en ese periodo.

La información se descarga directamente de la página del Buró https://www.bts.dot.gov/ en formato csv lo cual permite el fácil acceso, mantenimiento y divulgación.

## Archivos y estructura del repositorio

```
📦 proyecto_despliegue_soluciones
 ┣ 📄 Exploración_base_vuelos.ipynb --> Notebook con la preprocesamiento y exploración de la base de vuelos.
 ┣ 📄 Exploración_base_clima.ipynb --> Notebook con la preprocesamiento y exploración de la base de clima.
 ┣ 📄 Integración_base_final.ipynb --> Notebook con la integración de las bases de clima y vuelos.
 ┣ 📄 README.md --> Documento de orientación y explicación del proyecto y sus archivos.
 ┣ 📄 .dvcignore --> Define archivos a ignorar por el sistema de control de versiones en relación con los datos.
 ┣ 📂 .dvc --> Carpeta con la configuración de DVC.
 ┗ 📂 data --> Carpeta con los datos a trabajar.
   ┣ 📄 Weather Dataset.csv.dvc --> Archivo con los metadatos de DVC del conjunto de datos de condiciones climáticas.
   ┣ 📄 Flight Delays Data.csv.dvc --> Archivo con los metadatos de DVC del conjunto de datos de vuelos.
   ┗ 📄 .gitignore --> Archivo para ignorar archivos de datos (pues estos los maneja DVC).
 ```

## Integrantes del equipo
* Claudia Marcela Baquero Rico
* Johan Alberto Medina Cetina
* Daniel Hoyos Ospina
