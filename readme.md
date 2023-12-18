# Minería de datos y Sistemas Multiagentes 2023

Repositorio con toda la información de prácticas para las asignaturas Minería de Datos y Sistemas Multiagentes 

## Participantes

| Nombre    | Correo|
|-----------|-------|
| Diego Cordero Contreras      | diego.cordero@alu.uclm.es
| Enrique Albalate Prieto     | enrique.albalate@alu.uclm.es
| Lucía De Ancos Villa    | lucia.ancos@alu.uclm.es
| Pablo Del Hoyo Abad      | pablo.hoyo@alu.uclm.es
| Mohamed Essalhi Ahamyan     | mohamed.essalhi.ahamyan@alu.uclm.es

## Ejecutar programas

Primero, se deberá **agregar al directorio raíz el archivo .env** que ha sido enviado a través de las tareas pertinentes a los profesores con el cuál podremos acceder a la base de datos

A continuación deberán instalarse los requisitos del proyecto

```
pip install -r requirements.txt
```

### WebScraping
Accedemos a la API de Kaggle, por lo que es recomendable que cada usuario descargue sus credenciales. Sin embargo, para evitar más carga, se proporciona el dataset ya descargado de la página web de Kaggle.
Los archivos se descargan en /DataSets
Para ejecutar los programas que ejecutan el WebScraping
```
python3 .\Webscraping\Scripts\[Scraping]Main.py
```

### Limpieza y Transformación
#### RAW
Primero subimos los archivos descargados en WebScraping a la BBDD 
```
python3 .\Preprocesado_de_Datos\[RAW]\[RAW]BBDD.py
```
#### SILVER
A continuación traemos los datos de la base de datos, los limpiamos y los devolvemos a la BBDD 
```
python3 .\Preprocesado_de_Datos\[SILVER]\[SILVER]BBDD.py
```
#### GOLD
Por último, creamos las 4 tarjetas de datos 
```
python3 .\Preprocesado_de_Datos\[GOLD]\[GOLD]BBDD.py 
```

### Conclusiones
Podemos comprobar los resultados de nuestras líneas de trabajo en /Conclusiones_Hipótesis, en este caso no es necesario ejecutar ningún script ya que están almacenados los programas en notebooks ya cargados. 


