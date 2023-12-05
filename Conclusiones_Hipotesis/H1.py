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

    correlation_matrix = dataframe.corr()
    sns.set(style="white")
    plt.figure(figsize=(15, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
    plt.title("Matriz de Correlación entre todas las variables iniciales")
    plt.xlabel("Variables")
    plt.ylabel("Variables")
    plt.savefig(RUTA_IMAGENES + "correlacion_variables" +f"_Segmento{segmento}"+ ".png")
    
def TrabajoHipotesis():
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
    TrabajoHipotesis()


