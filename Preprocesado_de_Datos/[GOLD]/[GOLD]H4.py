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
    dataframe1 = dataframe1.reset_index() #to use again the "Country" as a column

    dataframe1 = replace_zero_values(dataframe1)
    
    # change the name of the colums for a better undestanding
    for year in range(2017, 2023):
        new_name = f'CochesVendidos_{year}'
        dataframe1.rename(columns={str(year): new_name}, inplace=True)

    return dataframe1
    
def replace_zero_values(dataframe):

    # Detecta las filas con al menos un valor igual a 0
    rows_with_zeros = dataframe[(dataframe == 0).any(axis=1)]

    countries = rows_with_zeros["Country"]
    rows_with_zeros = rows_with_zeros.drop(["Country"], axis=1)
    
    # Calcula la media de las filas excluyendo los valores iguales a 0
    media_filas_sin_ceros = rows_with_zeros[rows_with_zeros != 0].mean(axis=1)

    for index, country in countries.items():
        dataframe.loc[dataframe["Country"] == country] = dataframe.loc[dataframe["Country"] == country].replace(0, media_filas_sin_ceros.loc[index])
    
    final_countries = dataframe["Country"]
    dataframe = dataframe.drop(["Country"], axis=1)
    dataframe = dataframe.astype(int)
    dataframe["Country"] = final_countries
 
    return dataframe


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

def find_differences(column1, column2):
    union = pd.merge(column1, column2, on='Country')
    diferencia_1 = column1.loc[~column1.isin(union['Country'])]
    #diferencia_2 = column2.loc[~column2.isin(union['Country'])]
    print(diferencia_1)
    #print(diferencia_2)

    '''
    Changes to be done in dataframe_2:

        "China, People's Republic of" -> China
        "Korea, Republic of" -> Korea
        Russian Federation -> Russia
        Slovak Republic -> Slovakia
        Taiwan Province of China -> Taiwan
        United Arab Emirates -> UAE
        United Kingdom -> UK
        United States -> USA

    '''

def change_country_names(dataframe):

    changes = {
        "China, People's Republic of": 'China',
        "Korea, Republic of": 'Korea',
        'Russian Federation': 'Russia',
        'Slovak Republic': 'Slovakia',
        'Taiwan Province of China': 'Taiwan',
        'United Arab Emirates': 'UAE',
        'United Kingdom': 'UK',
        'United States': 'USA'
    }
    dataframe['Country'] = dataframe['Country'].replace(changes)

    return dataframe


def TarjetaDeDatos():
    
    nombre_tabla = 'model_per_year'
    dataframe1 = obtener_dataframe_sql(nombre_tabla, SILVER)
    nombre_tabla = 'pib_per_capita'
    dataframe2 = obtener_dataframe_sql(nombre_tabla, SILVER)

    dataframe1 = prepare_df1(dataframe1)
    dataframe2 = prepare_df2(dataframe2)

    #find_differences(dataframe1["Country"] , dataframe2["Country"])

    dataframe2 = change_country_names(dataframe2)

    data_card = pd.merge(dataframe2, dataframe1, on='Country')
    data_card.set_index('Country')

    return data_card

TarjetaDeDatos()