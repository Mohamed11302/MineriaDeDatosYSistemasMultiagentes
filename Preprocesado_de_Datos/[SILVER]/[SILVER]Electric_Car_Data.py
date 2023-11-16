import importlib
import pandas as pd
import re
from unicodedata import normalize
import os
import sys
ruta_actual = os.path.dirname(os.path.abspath(sys.argv[0]))
directorio_superior = os.path.dirname(ruta_actual)
abuelo_directorio = os.path.dirname(directorio_superior)
sys.path.append(abuelo_directorio)
from Preprocesado_de_Datos.Acceso_BBDD.MetodosBBDD import *



def limpiar_dataframe():
    dataframe = obtener_dataframe_sql('electric_car_data_clean', RAW)
    return dataframe