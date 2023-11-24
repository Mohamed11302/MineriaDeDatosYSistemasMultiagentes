from pandas_profiling import ProfileReport
import importlib
import os
import sys
ruta_actual = os.path.dirname(os.path.abspath(sys.argv[0]))
directorio_superior = os.path.dirname(ruta_actual)
abuelo_directorio = os.path.dirname(directorio_superior)
abuelo_directorio = os.path.dirname(abuelo_directorio)
sys.path.append(abuelo_directorio)
from Preprocesado_de_Datos.Acceso_BBDD.MetodosBBDD import *
GOLD_BBDD = importlib.import_module('Preprocesado_de_Datos.[GOLD].[GOLD]BBDD')

def RealizarProfiling():
    tarjetas_de_datos = GOLD_BBDD.Hipotesis()
    for nombre_bbdd, ruta_profiling in tarjetas_de_datos.items():   
        print("PROFILING: " + str(nombre_bbdd)) 
        PROFILE = importlib.import_module(ruta_profiling)
        df = PROFILE.TarjetaDeDatos()
        ruta_profiling = "Preprocesado_de_Datos/[GOLD]/Profiling/" + str(nombre_bbdd)+ "_reporte.html"
        print(ruta_profiling)
        profile = ProfileReport(df, title='Pandas Profiling Report', explorative=True)
        profile.to_file(ruta_profiling) 

if __name__ == "__main__":
    RealizarProfiling()