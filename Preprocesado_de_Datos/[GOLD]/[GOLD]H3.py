import os
import sys
import numpy as np
ruta_actual = os.path.dirname(os.path.abspath(sys.argv[0]))
directorio_superior = os.path.dirname(ruta_actual)
abuelo_directorio = os.path.dirname(directorio_superior)
sys.path.append(abuelo_directorio)
from Acceso_BBDD.MetodosBBDD import *

def prepare_model_per_year(model_per_year):
    model_per_year = model_per_year.groupby(['Country', 'PowerTrain'])[['2017', '2018', '2019', '2020', '2021', '2022']].sum()
    model_per_year = model_per_year.reset_index()
    hibridos = [
        "PHV",        # Vehículo eléctrico enchufable
        "Mild HV",    # Semi-híbrido
        "HV",         # Híbrido
        "48V Mild HV",# Híbrido
        "HV/PHV",
        "HV/MHV",
        "HV/EV/PHV",
        "HV/EV"
    ]
    electricos = [
        "EV"
    ]
    ev_powertrain = hibridos + electricos
    model_per_year = model_per_year[model_per_year['PowerTrain'].isin(ev_powertrain)]
    model_per_year['Type_Vehicle'] = model_per_year['PowerTrain'].apply(lambda x: 'Hybrid' if x in hibridos else 'Electric' if x in electricos else 'Otro')
    model_per_year = model_per_year.groupby(['Country', 'Type_Vehicle'])[['2017', '2018', '2019', '2020', '2021', '2022']].sum()
    
    
    for year in range(2017, 2023):
        model_per_year[str(year)] = model_per_year[str(year)].astype(int)

    model_per_year = model_per_year.reset_index()
    model_per_year = pd.melt(model_per_year, id_vars=['Country', 'Type_Vehicle'], var_name='year', value_name='Sells')
    model_per_year['year'] = model_per_year['year'].astype(int)
    model_per_year = model_per_year.rename(columns={'year':'Year'})


    ### AÑADIR LAS VENTAS DEL AÑO ANTERIOR
    df_last_year = model_per_year[['Country', 'Type_Vehicle', 'Year', 'Sells']].copy()
    df_last_year['Year'] = df_last_year['Year'] + 1
    df_last_year.rename(columns={'Sells': 'Sells_last_year'}, inplace=True)
    df = pd.merge(model_per_year, df_last_year, on=['Country', 'Type_Vehicle', 'Year'], how='left')

    ### QUITAMOS LAS COLUMNAS DEL AÑO 2017
    df = df[df.Year != 2017]
    
    return df

def prepare_charging_points(charging_points):
    charging_points = charging_points[~charging_points["year"].isin([2015, 2016])]
    charging_points = charging_points.pivot_table(index=['region', 'year'], columns='powertrain', values='value', aggfunc='sum').reset_index()

    charging_points = charging_points[['region', 'year', 'Publicly available fast', 'Publicly available slow']]
    charging_points = charging_points.rename(columns={'region': 'Country', 'Publicly available fast': 'Fast Charging Point', 'Publicly available slow': 'Slow Charging Point', 'year':'Year'})
    charging_points['Fast Charging Point'] = charging_points['Fast Charging Point'].replace([np.inf, -np.inf, np.nan], 0)
    charging_points['Slow Charging Point'] = charging_points['Slow Charging Point'].replace([np.inf, -np.inf, np.nan], 0)

    charging_points['Fast Charging Point'] = charging_points['Fast Charging Point'].astype(int)
    charging_points['Slow Charging Point'] = charging_points['Slow Charging Point'].astype(int)

    return charging_points

def prepare_electricity(electricity):
    return electricity


def TarjetaDeDatos():
    model_per_year = obtener_dataframe_sql("model_per_year", SILVER)
    charging_points = obtener_dataframe_sql("puntos_de_carga", SILVER)
    electricity = obtener_dataframe_sql('electricity_all_countries', SILVER)

    model_per_country = prepare_model_per_year(model_per_year)
    charging_region_year = prepare_charging_points(charging_points)
    electricity = prepare_electricity(electricity)
    dataframe = pd.merge(model_per_country,charging_region_year, how='inner', on=['Country', 'Year']).merge(electricity, on=['Country', 'Year'], how='inner')
    dataframe.rename(columns={'Price_(EUR/MWhe)': 'Price_Electricity'}, inplace=True)
    dataframe.drop(columns=['ISO3_Code'], inplace=True)
    order = ['Country', 'Year', 'Type_Vehicle', 'Fast Charging Point', 'Slow Charging Point', 'Price_Electricity', 'Sells_last_year', 'Sells']
    dataframe = dataframe[order]

    return dataframe