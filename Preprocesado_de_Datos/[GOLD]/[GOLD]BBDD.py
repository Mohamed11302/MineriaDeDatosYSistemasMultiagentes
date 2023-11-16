import os
import sys
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
