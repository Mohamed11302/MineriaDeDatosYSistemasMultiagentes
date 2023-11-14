import importlib
import pandas as pd
import re
from unicodedata import normalize


SILVER_BBDD = importlib.import_module('[SILVER]BBDD')


def limpiar_dataframe():
    dataframe = SILVER_BBDD.obtener_dataframe('gasoline_Diesel_prices')
    dataframe.rename(columns={'País': 'Pais'}, inplace=True)
    for i in range(len(dataframe["Pais"])):
        dataframe["Pais"][i]= dataframe["Pais"][i].replace(' [+]','')
        dataframe["Pais"][i] = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", dataframe["Pais"][i]), 0, re.I)
        dataframe["Pais"][i] = normalize( 'NFC', dataframe["Pais"][i])
        if 'ñ' in dataframe["Pais"][i]:
            dataframe["Pais"][i]=dataframe["Pais"][i].replace('ñ','n')

    for i in dataframe:
        if i=="Pais":
            pass
        else:
            for j in range(len(dataframe[i])):
                dataframe[i][j]=dataframe[i][j].replace('\xa0€','')
                dataframe[i][j]=dataframe[i][j].replace(',','.')
            dataframe[i] = dataframe[i].str.rstrip('%').astype(float)


    return dataframe

dataframe = limpiar_dataframe()
print(dataframe)
