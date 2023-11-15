import importlib
import pandas as pd
import os
import random

SILVER_BBDD = importlib.import_module('[SILVER]BBDD')

def completar_anios_con_tendencia(df):
    # Generar una lista de años desde 2015 hasta el primer año con registros
    anios_faltantes = []
    valor_min = []
    for pais in df['region'].unique():
        anio_min = df[df['region'] == pais]['year'].min()
        valor_min.append((pais, df[df['region'] == pais]['value'].min()))
        anios_faltantes += [(pais, anio) for anio in range(2015, anio_min)]

    valor_min = pd.DataFrame(valor_min, columns=['region', 'min'])
    
    val_faltantes = []
    for pais in df['region'].unique():
        v_min = valor_min[valor_min['region']==pais]['min'].astype(int)
        if not v_min.empty:
            v_min =v_min.iloc[0]
            anio_min = df[df['region'] == pais]['year'].min()
            valor = random.randint(int(0.1 * v_min), int(0.6 * v_min))
            for anio in range(2015, anio_min):
                val_faltantes.append((pais, anio, valor))
                valor = random.randint(int(valor), int(v_min))
    
    val_faltantes = pd.DataFrame(val_faltantes, columns=['region', 'year', 'value'])
    result_concat = pd.concat([df, val_faltantes], axis=0)
    result_sorted = result_concat.sort_values(by=["region", "year"])
    return result_sorted

def limpiar_dataframe():
    dataframe = SILVER_BBDD.obtener_dataframe('puntos_de_carga')
    dataframe = dataframe[dataframe['value'] == dataframe['value'].astype(int)]
    dataframe['value'] = dataframe['value'].astype(int)
    dataframe = dataframe.groupby(['region', 'year'], as_index=False)['value'].sum()
    dataframe = dataframe[dataframe['year'] >= 2015]
    dataframe = completar_anios_con_tendencia(dataframe)

    return dataframe
    