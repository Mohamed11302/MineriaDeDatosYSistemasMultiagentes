from Preprocesado_de_Datos.Acceso_BBDD.MetodosBBDD import *
import os
import sys
ruta_actual = os.path.dirname(os.path.abspath(sys.argv[0]))
directorio_superior = os.path.dirname(ruta_actual)
abuelo_directorio = os.path.dirname(directorio_superior)
sys.path.append(abuelo_directorio)


def prepare_model_per_year(model_per_year):
    # Cogemos solo aquellos vehículos eléctricos
    model_per_year_ev = model_per_year[model_per_year["isEv"] == 1]

    # El dataset de los puntos de carga va desde 2015 hasta 2021
    model_per_country = model_per_year_ev.groupby(
        ['Country'])[['2017', '2018', '2019', '2020', '2021']].sum()
    for year in range(2017, 2023):
        new_name = f'CochesVendidos_{year}'
        model_per_country.rename(columns={str(year): new_name}, inplace=True)

    model_per_country = model_per_country.astype(int)
    return model_per_year


def prepare_charging_points(charging_points):
    charging_points = charging_points[~charging_points["year"].isin([
                                                                    2015, 2016])]
    grouped_region_year = charging_points.groupby(["region", "year"])[
        ["value"]].sum()
    region_year = grouped_region_year.unstack()
    region_year.columns = region_year.columns.droplevel(0)

    for year in range(2017, 2023):
        new_name = f'PuntosRecarga_{year}'
        region_year.rename(columns={year: new_name}, inplace=True)

    region_year.index = region_year.index.rename("Country")

    return region_year


def TarjetaDeDatos():
    model_per_year = obtener_dataframe_sql("model_per_year", SILVER)
    charging_points = obtener_dataframe_sql("puntos_de_carga", SILVER)

    model_per_country = prepare_model_per_year(model_per_year)
    charging_region_year = prepare_charging_points(charging_points)

    data_card = pd.merge(model_per_country, charging_region_year, on='Country')

    return data_card