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
   dataframe = obtener_dataframe_sql('electricity_all_countries', RAW)
   
   # Date column datetime
   dataframe['Date'] = pd.to_datetime(dataframe['Date'])
   dataframe['Year'] = dataframe['Date'].dt.year

   # Average per year for each country
   dataframe = dataframe.groupby(['Country', 'ISO3_Code', 'Year'])['Price_(EUR/MWhe)'].mean().reset_index()
   
   
   return dataframe
