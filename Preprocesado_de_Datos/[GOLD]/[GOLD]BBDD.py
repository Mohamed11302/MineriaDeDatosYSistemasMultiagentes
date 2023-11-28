import os
import sys
import importlib
ruta_actual = os.path.dirname(os.path.abspath(sys.argv[0]))
directorio_superior = os.path.dirname(ruta_actual)
abuelo_directorio = os.path.dirname(directorio_superior)
sys.path.append(abuelo_directorio)
from Acceso_BBDD.MetodosBBDD import *

def Hipotesis()->dict:
    ScriptsHipotesis = {
        "Hipotesis_1":'Preprocesado_de_Datos.[GOLD].[GOLD]H1',
        'Hipotesis_2':'Preprocesado_de_Datos.[GOLD].[GOLD]H2',
        'Hipotesis_3':'Preprocesado_de_Datos.[GOLD].[GOLD]H3',
        'Hipotesis_4':'Preprocesado_de_Datos.[GOLD].[GOLD]H4'
    }
    return ScriptsHipotesis
def subir_hipotesis():
    tarjetas_de_datos = Hipotesis()
    for nombre_bbdd, ruta in tarjetas_de_datos.items():      
        print("UPLOADING DATASET: " + str(nombre_bbdd))
        hipotesis = importlib.import_module(ruta)
        df = hipotesis.TarjetaDeDatos()
        subir_dataframe_sql(df, nombre_bbdd, GOLD)

if __name__ == "__main__":
    subir_hipotesis()