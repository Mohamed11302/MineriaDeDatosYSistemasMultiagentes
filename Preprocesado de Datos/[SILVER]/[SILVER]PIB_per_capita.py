
import importlib
import pandas as pd

SILVER_BBDD = importlib.import_module('[SILVER]BBDD')

def filtrar_datos(dataframe_completo):
    dataframe_desde_2000 = dataframe_completo.iloc[1:dataframe_completo.shape[0]-2,[0] + list(range(31, dataframe_completo.shape[1]))]
    return dataframe_desde_2000

def anula_valores_no_numericos(dataframe):
    return dataframe.apply(pd.to_numeric, errors='coerce')

def media_no_nulos_fila(fila):
    return pd.to_numeric(fila.dropna()).mean()

def elimina_nulos(dataframe):
    for index, fila in dataframe.iterrows():
        dataframe.iloc[index-1] = fila.fillna(media_no_nulos_fila(fila))
    return dataframe

def limpiar_dataframe():

    dataframe = SILVER_BBDD.obtener_dataframe('pib_per_capita')
    dataframe_desde_2000 = filtrar_datos(dataframe)
    columna_paises = dataframe_desde_2000.iloc[:,0]
    dataframe_nulos_introducidos = anula_valores_no_numericos(dataframe_desde_2000.iloc[:,1:])
    dataframe_limpio = elimina_nulos(dataframe_nulos_introducidos)
    return pd.concat([columna_paises, dataframe_limpio.iloc[:,list(range(5, dataframe_limpio.shape[1]-5))]], axis=1)

