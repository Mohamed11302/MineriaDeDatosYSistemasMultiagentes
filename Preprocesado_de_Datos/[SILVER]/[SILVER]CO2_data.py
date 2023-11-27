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
   dataframe = obtener_dataframe_sql('data_CO2', RAW)
   
   # Drop useless lines
   dataframe = dataframe.drop(210)
   dataframe = dataframe.drop(211)
   dataframe = dataframe.drop(212)

   # Drop years we will not consider
   dataframe = dataframe.drop(dataframe.iloc[:,3:48].columns, axis=1)
   
   return dataframe
