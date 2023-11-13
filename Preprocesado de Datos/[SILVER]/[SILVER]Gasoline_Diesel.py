import importlib
import pandas as pd

SILVER_BBDD = importlib.import_module('[SILVER]BBDD')


def limpiar_dataframe():
    dataframe = SILVER_BBDD.obtener_dataframe('gasoline_Diesel_prices')
    print(dataframe)
    return dataframe

dataframe = limpiar_dataframe()
