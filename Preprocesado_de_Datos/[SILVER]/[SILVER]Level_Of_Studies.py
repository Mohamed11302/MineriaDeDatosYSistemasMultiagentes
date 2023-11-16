import importlib
import pandas as pd
import os
import sys
ruta_actual = os.path.dirname(os.path.abspath(sys.argv[0]))
directorio_superior = os.path.dirname(ruta_actual)
abuelo_directorio = os.path.dirname(directorio_superior)
sys.path.append(abuelo_directorio)
from Preprocesado_de_Datos.Acceso_BBDD.MetodosBBDD import *



def limpiar_dataframe():
    dataframe = obtener_dataframe_sql('level_of_studies', RAW)
    dataframe.drop('Tertiary_Total_Men__', axis=1, inplace=True)
    dataframe.drop('Tertiary_Total_Women__', axis=1, inplace=True)
    dataframe.drop('Below_Upper_Secondary_Men__', axis=1, inplace=True)
    dataframe.drop('Below_Upper_Secondary_Women__', axis=1, inplace=True)
    dataframe.drop('Upper_Secondary_Men__', axis=1, inplace=True)
    dataframe.drop('Upper_Secondary_Women__', axis=1, inplace=True)

    dataframe['Tertiary_Total__'] = dataframe['Tertiary_Total__'].str.rstrip('%').astype(int)
    dataframe['Below_Upper_Secondary_Total__'] = dataframe['Below_Upper_Secondary_Total__'].str.rstrip('%').astype(int)
    dataframe['Upper_Secondary_Total__'] = dataframe['Upper_Secondary_Total__'].str.rstrip('%').astype(int)

    dataframe.rename(columns={'Country__': 'Country'}, inplace=True)
    dataframe.rename(columns={'Tertiary_Total__': 'Tertiary_Total'}, inplace=True)
    dataframe.rename(columns={'Below_Upper_Secondary_Total__': 'Below_Upper_Secondary_Total'}, inplace=True)
    dataframe.rename(columns={'Upper_Secondary_Total__': 'Upper_Secondary_Total'}, inplace=True)

    return dataframe

