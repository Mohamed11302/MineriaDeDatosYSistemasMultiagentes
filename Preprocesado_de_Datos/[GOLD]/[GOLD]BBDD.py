import os
import sys
import importlib
ruta_actual = os.path.dirname(os.path.abspath(sys.argv[0]))
directorio_superior = os.path.dirname(ruta_actual)
abuelo_directorio = os.path.dirname(directorio_superior)
sys.path.append(abuelo_directorio)
from Preprocesado_de_Datos.Acceso_BBDD.MetodosBBDD import *

'''
Importante poner lo de arriba para que podais conectaros con la base de datos
'''

def TarjetaDeDatos():
    nombre_tabla = 'Ejemplo'
    dataframe = obtener_dataframe_sql(nombre_tabla, SILVER)
    #Creais la tarjeta de datos
    return dataframe
def SubirDataframes()->dict:
    ScriptsHipotesis = {
        "Hipotesis_1":'Preprocesado_de_Datos.[GOLD].[GOLD]H1',
        'Hipotesis_2':'Preprocesado_de_Datos.[GOLD].[GOLD]H2',
        'Hipotesis_3':'Preprocesado_de_Datos.[GOLD].[GOLD]H3',
        'Hipotesis_4':'Preprocesado_de_Datos.[GOLD].[GOLD]H4'
    }
    return ScriptsHipotesis
def subir_hipotesis():
    Dataframes = SubirDataframes()
    for nombre_bbdd, ruta in Dataframes.items():      
        print("UPLOADING DATASET: " + str(nombre_bbdd))
        Dataframe_Subir = importlib.import_module(ruta)
        df = Dataframe_Subir.TarjetaDeDatos()
        subir_dataframe_sql(df, nombre_bbdd, GOLD)

subir_hipotesis()