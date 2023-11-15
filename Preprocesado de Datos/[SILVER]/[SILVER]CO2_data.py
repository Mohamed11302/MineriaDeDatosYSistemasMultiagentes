import importlib
import pandas as pd

SILVER_BBDD = importlib.import_module('[SILVER]BBDD')

def limpiar_dataframe():
   dataframe = SILVER_BBDD.obtener_dataframe('data_CO2')
   
   # Drop useless lines
   dataframe = dataframe.drop(210)
   dataframe = dataframe.drop(211)
   dataframe = dataframe.drop(212)

   # Drop years we will not consider
   dataframe = dataframe.drop(dataframe.iloc[:,3:48].columns, axis=1)
   
   return dataframe
