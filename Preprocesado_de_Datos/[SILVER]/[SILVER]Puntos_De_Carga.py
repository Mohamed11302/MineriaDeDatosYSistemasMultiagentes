import pandas as pd
import random
random.seed(42)
import os
import sys
ruta_actual = os.path.dirname(os.path.abspath(sys.argv[0]))
directorio_superior = os.path.dirname(ruta_actual)
abuelo_directorio = os.path.dirname(directorio_superior)
sys.path.append(abuelo_directorio)
from Acceso_BBDD.MetodosBBDD import *

def completar_anios_con_tendencia(df):
    valor_min = df.groupby(['region', 'powertrain'])['value'].min().reset_index()

    val_faltantes = []
    for _, row in df.iterrows():
        region = row['region']
        powertrain = row['powertrain']
        v_min = valor_min[(valor_min['region'] == region) & (valor_min['powertrain'] == powertrain)]['value'].fillna(0).astype(int)
        if not v_min.empty:
            v_min = v_min.iloc[0]
            anio_min = row['year']
            if not pd.isna(anio_min):
                valor = random.randint(int(0.1 * v_min), int(0.6 * v_min))
                for anio in range(2015, int(anio_min)):
                    val_faltantes.append({'region': region, 'powertrain': powertrain, 'year': anio, 'value': valor})
                    valor = random.randint(int(valor), int(v_min))

    val_faltantes = pd.DataFrame(val_faltantes)
    result_concat = pd.concat([df, val_faltantes], axis=0)
    result_sorted = result_concat.sort_values(by=["region", "powertrain", "year"])
    return result_sorted

def limpiar_dataframe():
    dataframe = obtener_dataframe_sql('puntos_de_carga', RAW)
    dataframe = dataframe[dataframe['value'] == dataframe['value'].astype(int)]
    dataframe['value'] = dataframe['value'].astype(int)
    dataframe.drop(['category', 'parameter', 'mode', 'unit'], axis=1, inplace=True)
    dataframe = completar_anios_con_tendencia(dataframe)
    return dataframe

