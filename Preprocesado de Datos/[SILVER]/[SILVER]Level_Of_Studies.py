import importlib
import pandas as pd

SILVER_BBDD = importlib.import_module('[SILVER]BBDD')


def limpiar_dataframe():
    dataframe = SILVER_BBDD.obtener_dataframe('level_of_studies')
    print(dataframe)
    dataframe.drop('Tertiary_Total_Men__', axis=1, inplace=True)
    dataframe.drop('Tertiary_Total_Women__', axis=1, inplace=True)
    dataframe.drop('Below_Upper_Secondary_Men__', axis=1, inplace=True)
    dataframe.drop('Below_Upper_Secondary_Women__', axis=1, inplace=True)
    dataframe.drop('Upper_Secondary_Men__', axis=1, inplace=True)
    dataframe.drop('Upper_Secondary_Women__', axis=1, inplace=True)

    dataframe['Tertiary_Total__'] = dataframe['Tertiary_Total__'].str.rstrip('%').astype(int)
    dataframe['Below_Upper_Secondary_Total__'] = dataframe['Below_Upper_Secondary_Total__'].str.rstrip('%').astype(int)
    dataframe['Upper_Secondary_Total__'] = dataframe['Upper_Secondary_Total__'].str.rstrip('%').astype(int)

    dataframe.rename(columns={'Country__': 'Country'}, inplace=True)
    dataframe.rename(columns={'Tertiary_Total__': 'Tertiary_Total'}, inplace=True)
    dataframe.rename(columns={'Below_Upper_Secondary_Total__': 'Below_Upper_Secondary_Total'}, inplace=True)
    dataframe.rename(columns={'Upper_Secondary_Total__': 'Upper_Secondary_Total'}, inplace=True)

    return dataframe

dataframe = limpiar_dataframe()
