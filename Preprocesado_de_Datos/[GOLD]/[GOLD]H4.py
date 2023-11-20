import os
import sys
ruta_actual = os.path.dirname(os.path.abspath(sys.argv[0]))
directorio_superior = os.path.dirname(ruta_actual)
abuelo_directorio = os.path.dirname(directorio_superior)
sys.path.append(abuelo_directorio)
from Preprocesado_de_Datos.Acceso_BBDD.MetodosBBDD import *
import pandas as pd



def prepare_df1 (dataframe1):

    # number of cars sold by country and year 
    dataframe1= dataframe1.groupby(['Country'])[['2017', '2018', '2019', '2020', '2021', '2022']].sum()

    # change the name of the colums for a better undestanding
    for year in range(2017, 2023):
        new_name = f'CochesVendidos_{year}'
        dataframe1.rename(columns={str(year): new_name}, inplace=True)
    
    return dataframe1
    

def prepare_df2 (dataframe2):

    # Change language name to merge both tables in a data card
    dataframe2.rename(columns={'GDP_per_capita,_current_prices\r\n_(U.S._dollars_per_capita)': 'Country'}, inplace=True)

    #Drop several columns related to years that won't be finally used
    dataframe2 = dataframe2.drop(['2015', '2016', '2023'], axis=1)

    # change the name of the colums for a better undestanding
    for year in range(2017, 2023):
        new_name = f'PIB_{year}'
        dataframe2.rename(columns={str(year): new_name}, inplace=True)

    return dataframe2


def TarjetaDeDatos():
    
    nombre_tabla = 'model_per_year'
    dataframe1 = obtener_dataframe_sql(nombre_tabla, SILVER)

    nombre_tabla = 'pib_per_capita'
    dataframe2 = obtener_dataframe_sql(nombre_tabla, SILVER)

    dataframe1 = prepare_df1(dataframe1)
    dataframe2 = prepare_df2(dataframe2)

    data_card = pd.merge(dataframe1, dataframe2, on='Country')
    data_card.set_index('Country', inplace=True)
    
    return data_card
