import pandas as pd
import importlib
import os
import sys
ruta_actual = os.path.dirname(os.path.abspath(sys.argv[0]))
directorio_superior = os.path.dirname(ruta_actual)
abuelo_directorio = os.path.dirname(directorio_superior)
sys.path.append(abuelo_directorio)
from Preprocesado_de_Datos.Acceso_BBDD.MetodosBBDD import *
def SubirDataframes()->dict:
    ScriptsLimpieza = {
        "data_CO2":'Preprocesado_de_Datos.[SILVER].[SILVER]CO2_data',
        'electric_car_data_clean':'Preprocesado_de_Datos.[SILVER].[SILVER]Electric_Car_Data',
        'electricity_all_countries':'Preprocesado_de_Datos.[SILVER].[SILVER]electricity_in_all_countries',
        'gasoline_Diesel_prices':'Preprocesado_de_Datos.[SILVER].[SILVER]Gasoline_Diesel',
        'level_of_studies':'Preprocesado_de_Datos.[SILVER].[SILVER]Level_Of_Studies',
        'model_per_year':'Preprocesado_de_Datos.[SILVER].[SILVER]model_per_year',
        'pib_per_capita':'Preprocesado_de_Datos.[SILVER].[SILVER]PIB_per_capita',
        'puntos_de_carga':'Preprocesado_de_Datos.[SILVER].[SILVER]Puntos_De_Carga'
    }
    return ScriptsLimpieza
def subir_dataframe_limpios():
    Dataframes = SubirDataframes()
    for nombre_bbdd, ruta in Dataframes.items():      
        print("UPLOADING DATASET: " + str(nombre_bbdd))
        Dataframe_Subir = importlib.import_module(ruta)
        df = Dataframe_Subir.limpiar_dataframe()
        subir_dataframe_sql(df, nombre_bbdd, SILVER)

subir_dataframe_limpios()