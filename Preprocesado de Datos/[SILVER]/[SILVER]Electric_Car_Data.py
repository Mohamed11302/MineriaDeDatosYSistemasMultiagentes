import importlib
import pandas as pd
import re
from unicodedata import normalize


SILVER_BBDD = importlib.import_module('[SILVER]BBDD')


def limpiar_dataframe():
    dataframe = SILVER_BBDD.obtener_dataframe('electric_car_data_clean')
    return dataframe
