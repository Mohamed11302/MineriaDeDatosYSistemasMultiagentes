import importlib
import pandas as pd

SILVER_BBDD = importlib.import_module('[SILVER]BBDD')

def limpiar_dataframe():
   dataframe = SILVER_BBDD.obtener_dataframe('electricity_all_countries')
   
   # Date column datetime
   dataframe['Date'] = pd.to_datetime(dataframe['Date'])
   dataframe['Year'] = dataframe['Date'].dt.year

   # Average per year for each country
   dataframe = dataframe.groupby(['Country', 'ISO3_Code', 'Year'])['Price_(EUR/MWhe)'].mean().reset_index()
   
   
   return dataframe

dataframe = limpiar_dataframe()