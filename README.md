<p align="center"><img src="src\henry_logo.png" height=100></p>

# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>

# <h1 align=center>**`Machine Learning Operations (MLOps)`**</h1>

<p align="center">
<img src="src\machine.png"  height=200>
</p>
<hr>

# <h1 align=center> **Introducción** </h1>

En este emocionante proyecto, nos sumergiremos en el mundo de las Operaciones de Machine Learning, abordando tres etapas fundamentales que son esenciales para el éxito en este campo. Comienza con la Preparación, la Exploración y Transformación de Datos, luego avanza hacia el Análisis exploratorio de datos (EDA) y finalmente hacia la Aplicación de Técnicas de Machine Learning, donde se lleva a cabo la exploración y entrenamiento del modelo.

Nuestra misión se centra en un conjunto de datos relacionado con los juegos de la plataforma Steam, un entorno que entusiasma a millones de usuarios en todo el mundo.

# <h1 align=center> **Descripción** </h1>

En la primera etapa, asumimos el rol de Data Engineer y comenzamos el proceso de Extracción, Transformación y Carga (ETL). El proceso detallado se encuentra en  el notebook [ETL](ETL.ipynb). Durante esta fase, nos enfocamos en la limpieza de datos de los tres conjuntos de datos, eliminando valores nulos, creando una nueva columna llamada "sentiment_analysis" basada en la columna "recommend", y descartando columnas irrelevantes. Esto nos permitió preparar los datos para la siguiente fase.

A continuación, aplicamos nuestras habilidades en la preparación de datos al crear funciones específicas para construir una API utilizando FastAPI. Esta API facilitará la interacción eficiente con nuestros datos y se alojará en un servidor web de Render para simplificar el acceso y la consulta de información valiosa. Hemos diseñado consultas especializadas para obtener datos como: la cantidad de ítems y el porcentaje de contenido gratuito por año según la empresa desarrolladora, el gasto por usuario y el porcentaje de recomendación basado en revisiones, también exploraremos los tres desarrolladores con juegos más recomendados por los usuarios para un año específico. lo cual se encuentra detallado en el archivo[funciones.py](funciones.py).

Nuestra próxima etapa se centra en explorar y transformar los datos. Durante esta fase, nos enfocamos en la limpieza y exploración de los datos, preparándolos para futuras predicciones. Utilizamos el Análisis Exploratorio de Datos (EDA) como nuestra herramienta clave para comprender las relaciones entre variables y detectar posibles patrones e irregularidades. El proceso se encuentra detallado en el cuaderno [EDA](EDA.ipynb).

Finalmente, llegaremos al núcleo de nuestro proyecto: la creación de un modelo predictivo. Entrenamos un algoritmo de aprendizaje automático que se dedica a recomendar juegos, ya sea por elemento o usuario, utilizando técnicas de recomendación con la biblioteca "surprise", diseñada específicamente para sistemas de recomendación y filtrado colaborativo. El proceso se detalla en el cuaderno [machine](machine.ipynb).

No obstante, no nos limitamos a la parte técnica. Reconocemos la importancia de comunicar nuestros resultados de manera efectiva. Por lo tanto, hemos preparado un video que demuestra cómo funcionan las funciones contenidas en el endpoint de la API, lo que facilitará la comprensión y el acceso a nuestros avances.

Este proyecto nos desafía a adquirir habilidades y conocimientos esenciales para abordar situaciones del mundo real en el campo de las Operaciones de Aprendizaje Automático. Desde la preparación y análisis de datos hasta la implementación de un modelo predictivo para recomendaciones de juegos en la plataforma Steam, estamos preparados para proporcionar un acceso sencillo y eficaz a información valiosa.

# <h1 align=center> **Diccionario de Datos** </h1>

<p align="center">
<img src="src\diccionario.png"  height=500>
</p>
<hr>

# <h1 align=center> **Links de utilidad** </h1>


➮ [ETL Jupyter Notebook](ETL.ipynb)<br>
➮ [EDA Jupyter Notebook](EDA.ipynb)<br>
➮ [Modelo Machine Learning](machine.ipynb)<br>
➮ [Diccionario de Datos](Diccionario%20de%20Datos%20STEAM.xlsx)<br>
➮ [Fuente de Datos](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj) <br>
➮ [Link a Render](https://proyecto-1-ml-ops.onrender.com/docs) <br>
➮ [Link al Video]() <br>

# <h1 align=center> **Desarrollo Fast API** </h1>

**`Desarrollo API`**: Se disponibilizan las siguientes funciones de consulta a traves de FastAPI:


+ def **developer( desarrollador : str )**: 
    Cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora. 

+ def **userdata( User_id : str )**:
    Debe devolver cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a reviews.recommend y cantidad de items.

+ def **best_developer_year( año : int )**:
    Devuelve el top 3 de desarrolladores con juegos más recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos)

+ def **developer_reviews_analysis( desarrolladora : str )**:
    Según el desarrollador, se devuelve un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.


<br/>

**`Deployment`**: Se desplegó la API con Render para poder ser consumida desde la web.

<br/>

**`Análisis exploratorio de los datos`**: _(Exploratory Data Analysis-EDA)_

En esta fase del proyecto, después de haber limpiado los datos, se llevaron a cabo investigaciones para comprender las relaciones entre las variables del conjunto de datos. Se buscó identificar outliers o anomalías, que no necesariamente son errores, y se detectaron patrones interesantes que podrían ser explorados en análisis posteriores. En esta ocasión, se realizó un EDA de manera manual, sin el uso de bibliotecas automatizadas, con el objetivo de aplicar los conceptos y tareas involucradas en este proceso. Finalmente, se realizó un análisis univariable y multivariable para estudiar la distribución de los datos en cada columna y la relación entre ellas a través de gráficos.


**`Modelo de predicción`**: 

La data es consumible por la API, está lista para ser utilizada por los departamentos de Analytics y Machine Learning, y nuestro EDA nos permite entender bien los datos a los que tenemos acceso. Se entrenó un modelo surprise de recomendación para predecir recomendaciones de juegos a usuarios. Se exportó el modelo como archivo pkl para ser importado en el script que contiene las funciones utilizadas en el main.Ingresando el id de un usuario (ejemplo: user_id:Gamer0009), deberíamos recibir una lista con 5 juegos recomendados para dicho usuario.
En este enfoque, el modelo se basa en el filtro usuario-ítem. Toma un usuario como entrada, busca usuarios similares y recomienda juegos que a esos usuarios similares les han gustado. 

+ def **recomendacion_usuario( id de usuario )**:<br/>
    Ingresando el id de un usuario, deberíamos recibir una lista con 5 juegos recomendados para dicho usuario.
 

<h1>Autor:</h1>

Kathiuska del Carmen Mangones Ramos <br>
Email: [kathiuska06@hotmail.com](kathiuska06@hotmail.com)<br>
[GitHub](https://github.com/KATHIUSKA06/PI_ML_OPS/blob/master/README.md) <br>
[LinkedIn](https://www.linkedin.com/in/kathiuska-mangones-ramos-1b494913b/)
_________________________________________________________________________________________________________________