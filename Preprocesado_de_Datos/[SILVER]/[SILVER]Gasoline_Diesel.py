import os
import sys
import warnings
import Aux_Traductor_Paises


warnings.filterwarnings('ignore')
ruta_actual = os.path.dirname(os.path.abspath(sys.argv[0]))
directorio_superior = os.path.dirname(ruta_actual)
abuelo_directorio = os.path.dirname(directorio_superior)
sys.path.append(abuelo_directorio)
from Acceso_BBDD.MetodosBBDD import *


def limpiar_dataframe():
    dataframe = obtener_dataframe_sql('gasoline_Diesel_prices', RAW)
    dataframe.rename(columns={'País': 'Pais'}, inplace=True)
    for i in range(len(dataframe["Pais"])):
        dataframe["Pais"][i]= dataframe["Pais"][i].replace(' [+]','')
        dataframe["Pais"][i]=Aux_Traductor_Paises.traducir_al_ingles(dataframe["Pais"][i])
    for i in dataframe:
        if i=="Pais":
            pass
        else:
            for j in range(len(dataframe[i])):
                dataframe[i][j]=dataframe[i][j].replace('\xa0€','')
                dataframe[i][j]=dataframe[i][j].replace(',','.')
            dataframe[i] = dataframe[i].str.rstrip('%').astype(float)

 
    return dataframe
