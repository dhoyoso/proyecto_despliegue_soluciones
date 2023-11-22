
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
- Registro de modelos y experimentos en mlflow.
-	Creación de tablero de visualización de datos históricos.
- Creación del paquete con el modelo entrenado.
- Creación del API que albergará el modelo entrenado para predecir.
-	Integración del tablero con una interfaz de captura de datos para realizar predicciones de retrasos.
- Integración del tablero con el API.
-	Despliegue y operación de la solución (incluye tablero y API).
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
 ┣ 📄 Modelado final.ipynb --> Notebook con el entrenamiento del modelo final definitivo usado en el API.
 ┣ 📄 Merge_nombres.py --> Script de Python con unificación valores de referencia con nombres de aerolineas y aeropuertos.
 ┣ 📄 mlflow-flight-delay.py --> Script de python para registrar los experimentos de entrenamiento y evaluación en mlflow.
 ┣ 📄 mlflow_flight_delay_VF.py --> Script de python para registrar experimentos en mlflow. Versión final.
 ┣ 📄 README.md --> Documento de orientación y explicación del proyecto y sus archivos.
 ┣ 📄 .dvcignore --> Define archivos a ignorar por el sistema de control de versiones en relación con los datos.
 ┣ 📂 .dvc --> Carpeta con la configuración de DVC.
 ┣ 📂 api --> Carpeta con el codigo fuente del api (servidor que expone la predicción).
 ┃ ┣ 📄 Dockerfile --> Archivo Dockerfile para el despliegue del api como contenedor.
 ┃ ┣ 📂 flights-delay-api --> Carpeta con el codigo fuente del api.
 ┃ ┃ ┣ 📂 app --> Carpeta que contiene el código fuente del api.
 ┃ ┃ ┃ ┣ 📂 schemas --> Carpeta con los schemas del api.
 ┃ ┃ ┃ ┃ ┣ 📄 __init__.py --> Archivo de inicialización e import de schemas.
 ┃ ┃ ┃ ┃ ┣ 📄 health.py --> Esquema del método health.
 ┃ ┃ ┃ ┃ ┗ 📄 predict.py --> Esquema del método predict.
 ┃ ┃ ┃ ┣ 📂 test --> Pruebas unitarias del api.
 ┃ ┃ ┃ ┃ ┣ 📄 __init__.py --> Archivo init.
 ┃ ┃ ┃ ┃ ┣ 📄 conftest.py --> Archivo de configuración de las pruebas unitarias.
 ┃ ┃ ┃ ┃ ┗ 📄 test_api.py --> Pruebas unitarias.
 ┃ ┃ ┃ ┣ 📄 __init__.py --> Codigo del archivo init que contien la versión del api.
 ┃ ┃ ┃ ┣ 📄 api.py --> Codigo fuente api.
 ┃ ┃ ┃ ┣ 📄 config.py --> Codigo fuente de la configuración del api.
 ┃ ┃ ┃ ┗ 📄 main.py --> Codigo fuente principal (main) del api.
 ┃ ┃ ┣ 📂 model-pkg --> Carpeta con el modelo empaquetado.
 ┃ ┃ ┃ ┗ 📄 model_flights_delays-0.0.1-py3-none-any.whl --> Modelo empaquetado.
 ┃ ┃ ┣ 📄 tox..ini --> Archivo de configuración del tox.
 ┃ ┃ ┣ 📄 .python-version --> Archivo que especifica la versión de python requerida.
 ┃ ┃ ┣ 📄 mypy.ini --> Archivo de configuración.
 ┃ ┃ ┣ 📄 Procfile --> Archivo de configuración.
 ┃ ┃ ┣ 📄 requirements.txt --> Archivo de requerimientos.
 ┃ ┃ ┣ 📄 test_requirements.txt --> Archivo de requerimientos de prueba.
 ┃ ┃ ┣ 📄 typing_requirements.txt --> Archivo de requerimientos de escritura de código.
 ┃ ┗ ┗ 📄 run.sh --> Shell script que ejecuta el api.
 ┣ 📂 client --> Carpeta con el codigo fuente del cliente (tablero).
 ┃ ┣ 📄 Dockerfile --> Archivo Dockerfile para el despliegue del tablero como contenedor.
 ┃ ┣ 📂 app --> Carpeta con el codigo fuente del tablero.
 ┃ ┃ ┣ 📄 app.py --> Codigo fuente tablero en dash.
 ┃ ┃ ┣ 📄 .python-version --> Archivo que especifica la versión de python requerida.
 ┃ ┃ ┣ 📄 mypy.ini --> Archivo de configuración.
 ┃ ┃ ┣ 📄 Procfile --> Archivo de configuración.
 ┃ ┃ ┣ 📄 requirements.txt --> Archivo de requerimientos.
 ┃ ┃ ┣ 📄 test_requirements.txt --> Archivo de requerimientos de prueba.
 ┃ ┃ ┣ 📄 run.sh --> Shell script que ejecuta el tablero.
 ┃ ┃ ┣ 📂 assets --> Carpeta con estilos css del tablero y data histórica.
 ┃ ┃ ┃ ┣ 📄 base.css --> Archivo con estilos css base.
 ┃ ┃ ┃ ┣ 📄 clinical-analytics.css --> Archivo con estilos css.
 ┃ ┗ ┗ ┗ 📄 resultado_merge.csv --> Archivo csv con data histórica.
 ┣ 📂 data --> Carpeta con los datos a trabajar.
 ┃ ┣ 📄 Weather Dataset.csv.dvc --> Archivo con los metadatos de DVC del conjunto de datos de condiciones climáticas.
 ┃ ┣ 📄 Flight Delays Data.csv.dvc --> Archivo con los metadatos de DVC del conjunto de datos de vuelos.
 ┃ ┗ 📄 .gitignore --> Archivo para ignorar archivos de datos (pues estos los maneja DVC).
 ┣ 📂 model-package --> Carpeta con el codigo fuente del api (servidor que expone la predicción).
 ┃ ┣ 📂 dist --> Builds del paquete.
 ┃ ┃ ┣ 📄 model_flights_delays-0.0.1-py3-none-any.whl --> .whl del modelo empaquetado.
 ┃ ┃ ┗ 📄 model-flights-delays-0.0.1.tar.gz --> .tar.gz del modelo empaquetado.
 ┃ ┣ 📂 model --> Carpeta con el código fuente del paquete.
 ┃ ┃ ┣ 📂 config --> Carpeta con los archivos de manejo de configuración.
 ┃ ┃ ┃ ┣ 📄 __init__.py --> Archivo __init__.
 ┃ ┃ ┃ ┗ 📄 core.py --> Script con los métodos para procesar la configuración.
 ┃ ┃ ┣ 📂 datasets --> Carpeta con los datasets del modelo.
 ┃ ┃ ┃ ┣ 📄 __init__.py --> Archivo __init__.
 ┃ ┃ ┃ ┣ 📄 train.csv --> Datos de entrenamiento del modelo.
 ┃ ┃ ┃ ┗ 📄 test.csv --> Datos de prueba del modelo.
 ┃ ┃ ┣ 📂 processing --> Carpeta con los scripts de utilidad para manejar datos, features y validaciones.
 ┃ ┃ ┃ ┣ 📄 __init__.py --> Archivo __init__.
 ┃ ┃ ┃ ┣ 📄 data_manager.py --> Script para manejo de datos. 
 ┃ ┃ ┃ ┣ 📄 features.py --> Script para manejo de features. 
 ┃ ┃ ┃ ┗ 📄 validation.py --> Script para validación de schemas. 
 ┃ ┃ ┣ 📂 trained --> Carpeta con los .pkl de los modelos entrenados.
 ┃ ┃ ┃ ┣ 📄 __init__.py --> Archivo __init__.
 ┃ ┃ ┃ ┗ 📄 model-flights-delays-output0.0.1.pkl --> .pkl del modelo entrenado
 ┃ ┃ ┣ 📄 __init__.py --> Archivo __init__ del paquete.
 ┃ ┃ ┣ 📄 config.yml --> Archivo de configuración con el diccionario de valores.
 ┃ ┃ ┣ 📄 pipeline.py --> Script de python con el pipeline de predicción.
 ┃ ┃ ┣ 📄 predict.py --> Script con la lógica de predicción.
 ┃ ┃ ┣ 📄 train_pipeline.py --> Script con la lógica o pipeline de entrenamiento.
 ┃ ┃ ┗ 📄 VERSION --> Archivo que especifica la versión del paquete.
 ┃ ┣ 📂 requirements --> Archivo con los requerimientos del paquete.
 ┃ ┃ ┣ 📄 requirements.txt --> Archivo de requerimientos.
 ┃ ┃ ┣ 📄 test_requirements.txt --> Archivo de requerimientos de prueba.
 ┃ ┃ ┣ 📄 typing_requirements.txt --> Archivo de requerimientos de escritura de código.
 ┃ ┣ 📂 tests --> Carpeta con el codigo fuente del api.
 ┃ ┃ ┃ ┣ 📄 __init__.py --> Archivo init.
 ┃ ┃ ┃ ┣ 📄 conftest.py --> Archivo de configuración de las pruebas unitarias.
 ┃ ┃ ┃ ┗ 📄 test_prediction.py --> Pruebas unitarias de la predicción del paquete.
 ┃ ┃ ┣ 📄 MANIFEST.in --> Archivo que define las rutas a incluir en el paquete.
 ┃ ┃ ┣ 📄 mypy.ini --> Archivo de configuración.
 ┃ ┃ ┣ 📄 pyproject.toml --> Archivo de configuración del build.
 ┃ ┃ ┣ 📄 setup.py --> Script de configuración del paquete.
 ┃ ┗ ┗ 📄 tox.ini --> Archivo de configuración de tox para el paquete.
 ┣ 📂 manuales --> Carpeta con los manuales de usuario e instalación del tablero.
 ┃ ┣ 📄 manual de usuario tablero.docx --> Manual de usuario del tablero en word.
 ┃ ┣ 📄 manual de usuario tablero.pdf --> Manual de usuario del tablero en pdf.
 ┃ ┣ 📄 manual de instalación tablero.docx --> Manual de instalación del tablero en word.
 ┗ ┗ 📄 manual de instalación tablero.pdf --> Manual de instalación del tablero en pdf.
 ```

# MLFlow
Con el mejor modelo validado en instancias locales, se procedio realizar en una maquina virtual la corrida con diferentes hiperparametros para encontrar el modelo con el mejor desempeño de posible e implementarlo en el tablero final.

## Integrantes del equipo
* Claudia Marcela Baquero Rico
* Johan Alberto Medina Cetina
* Daniel Hoyos Ospina
