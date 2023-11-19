import pandas as pd
import random
import os
import sys
ruta_actual = os.path.dirname(os.path.abspath(sys.argv[0]))
directorio_superior = os.path.dirname(ruta_actual)
abuelo_directorio = os.path.dirname(directorio_superior)
sys.path.append(abuelo_directorio)
from Preprocesado_de_Datos.Acceso_BBDD.MetodosBBDD import *



def quitar_paises_sin_valores(df):
    df = df[df['year'] >= 2015]
    df = df[df['year'] <= 2021]
    df_filtrado = df.groupby('region').filter(lambda x: x['year'].min() <= 2015)
    return df_filtrado

def limpiar_dataframe():
    dataframe = obtener_dataframe_sql('puntos_de_carga', RAW)
    dataframe = dataframe[dataframe['value'] == dataframe['value'].astype(int)]
    dataframe['value'] = dataframe['value'].astype(int)
    dataframe.drop(['category', 'parameter', 'mode', 'unit'], axis=1, inplace=True)
    dataframe = quitar_paises_sin_valores(dataframe)
    
    return dataframe