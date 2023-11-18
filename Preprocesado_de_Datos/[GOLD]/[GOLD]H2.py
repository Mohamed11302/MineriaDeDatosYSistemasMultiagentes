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
    dataframe2.rename(columns={'Pais': 'Country'}, inplace=True)
    dataframe2 = dataframe2.drop(['Gasolina_2015', 'Diesel_2015','Gasolina_2016', 'Diesel_2016','Gasolina_2023', 'Diesel_2023'], axis=1)
    traducciones = {
        'Belgica': 'Belgium',
        'Alemania': 'Germany',
        'Espana': 'Spain',
        'Reino Unido': 'UK',
        'Francia': 'France',
        'Italia': 'Italy',
        'Estados Unidos': 'USA',
        'Chequia': 'Czech Republic',
        'Croacia': 'Croatia',
        'Dinamarca': 'Denmark',
        'Eslovaquia': 'Slovakia',
        'Eslovenia': 'Slovenia',
        'Finlandia': 'Finland',
        'Grecia': 'Greece',
        'Hungria': 'Hungary',
        'Irlanda': 'Ireland',
        'Letonia': 'Latvia',
        'Lituania': 'Lithuania',
        'Luxemburgo': 'Luxembourg',
        'Paises Bajos': 'Netherlands',
        'Polonia': 'Poland',
        'Rumania': 'Romania',
        'Suecia': 'Sweden'
    }

    dataframe2['Country'] = dataframe2['Country'].replace(traducciones)

    # Change the order of the colums for a better understnding
    column_order = sorted(dataframe2.columns, key=lambda x: int(x.split('_')[1]) if '_' in x and x.split('_')[1].isdigit() else float('inf'))
    dataframe2 = dataframe2[column_order]

    return dataframe2


def TarjetaDeDatos():
    
    nombre_tabla = 'model_per_year'
    dataframe1 = obtener_dataframe_sql(nombre_tabla, SILVER)

    nombre_tabla = 'gasoline_Diesel_prices'
    dataframe2 = obtener_dataframe_sql(nombre_tabla, SILVER)

    dataframe1 = prepare_df1(dataframe1)
    dataframe2 = prepare_df2(dataframe2)

    data_card = pd.merge(dataframe1, dataframe2, on='Country')
    data_card.set_index('Country', inplace=True)
    
    return data_card

TarjetaDeDatos()