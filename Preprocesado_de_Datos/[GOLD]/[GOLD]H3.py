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
    return model_per_year

def prepare_charging_points(charging_points):
    charging_points = charging_points[~charging_points["year"].isin([2015, 2016])]
    charging_points = charging_points.pivot_table(index=['region', 'year'], columns='powertrain', values='value', aggfunc='sum').reset_index()

    charging_points = charging_points[['region', 'year', 'Publicly available fast', 'Publicly available slow']]
    charging_points = charging_points.rename(columns={'region': 'Country', 'Publicly available fast': 'Fast Charging Point', 'Publicly available slow': 'Slow Charging Point'})
    charging_points['Fast Charging Point'] = charging_points['Fast Charging Point'].replace([np.inf, -np.inf, np.nan], 0)
    charging_points['Slow Charging Point'] = charging_points['Slow Charging Point'].replace([np.inf, -np.inf, np.nan], 0)

    charging_points['Fast Charging Point'] = charging_points['Fast Charging Point'].astype(int)
    charging_points['Slow Charging Point'] = charging_points['Slow Charging Point'].astype(int)

    return charging_points


def TarjetaDeDatos():
    model_per_year = obtener_dataframe_sql("model_per_year", SILVER)
    charging_points = obtener_dataframe_sql("puntos_de_carga", SILVER)

    model_per_country = prepare_model_per_year(model_per_year)
    charging_region_year = prepare_charging_points(charging_points)
    merged_df = pd.merge(model_per_country,charging_region_year, how='inner', on=['Country', 'year'])
    return merged_df


