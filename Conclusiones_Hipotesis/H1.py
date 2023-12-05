import os
import sys
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

ruta_actual = os.path.dirname(os.path.abspath(sys.argv[0]))
directorio_superior = os.path.dirname(ruta_actual)
sys.path.append(directorio_superior)
from Acceso_BBDD.MetodosBBDD import *

RUTA_IMAGENES = ruta_actual + '/Imagenes_H1/'
def  comprobarDatos(columna):
    a=''
    for i in columna:
        if a=='':
            a=i
        elif a!=i:
            return False
    return True

def analizar_correlacion(dataframe,segmento):

    # 3. Análisis de Correlación entre variables

    correlation_matrix = dataframe.corr()
    sns.set(style="white")
    plt.figure(figsize=(15, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
    plt.title("Matriz de Correlación entre todas las variables iniciales")
    plt.xlabel("Variables")
    plt.ylabel("Variables")
    plt.savefig(RUTA_IMAGENES + "correlacion_variables" +f"_Segmento{segmento}"+ ".png")
    #plt.show()
def analizar_componentes_principales(dataframe):
    # 4. Análisis de Componentes Principales de todo el Dataframe

    states = scaler.fit_transform(dataframe)
    estimator = PCA (n_components = 2)
    X_pca = estimator.fit_transform(states)

    plt.figure(figsize=(10, 8))
    plt.title("Análisis de Componentes Principales de todo el Dataframe")
    plt.scatter(X_pca[:,0], X_pca[:,1], s=50)
    for i in range(len(X_pca)):
        plt.text(X_pca[i, 0], X_pca[i, 1], dataframe.iloc[i, :].name)
    plt.grid()
    #plt.savefig(ruta_carpeta_imagenes + "componentes_principales_tarjeta_datos_H4" + ".png")
    plt.show()

def ComprobarRelacion():
    #Separamos en un dataset por segmento y comprobamos la relación de cada una de sus variables
    
    df = obtener_dataframe_sql('Hipotesis_1', GOLD)
    columnas_ventas = df.iloc[:, 1:7]  # Columnas de años

    # Multiplica las columnas de años para obtener un total de ventas por año
    df['RapidCharge'] = df['RapidCharge'].replace({'Yes': 1, 'No': 0}) #Adaptamos el boolean a numerico
    total_ventas_por_año = columnas_ventas.sum(axis=1)

    df_mod=df.select_dtypes(include='number')
    df_mod['Ventas_Totales']=total_ventas_por_año
    df_mod['Model']=df['Model']
    df_mod['Segment']=df['Segment']
    df_mod.set_index(df_mod['Model'], inplace=True)

    for i in range(2017,2023):
        df_mod = df_mod.drop(columns=str(i))

    df_mod = df_mod.drop(columns='Model')
    segment=df_mod.groupby('Segment')
    data_segment = {nombre: grupo for nombre, grupo in segment}
    
    for valor, dataset in data_segment.items():
        dataset['RapidCharge']=dataset['RapidCharge'].astype(float)
        if comprobarDatos(dataset['RapidCharge']): dataset=dataset.drop(columns='RapidCharge')
        analizar_correlacion(dataset.drop(columns='Segment'),valor)

if __name__ == "__main__":
    ComprobarRelacion()
    #df.to_csv('Hipotesis1.csv', sep=";")


