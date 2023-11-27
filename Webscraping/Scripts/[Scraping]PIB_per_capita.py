
import requests
from bs4 import BeautifulSoup
import pandas as pd
import xlrd
import os
import numpy as np
from sklearn.impute import SimpleImputer

from pandas.io import sql
import sqlalchemy as db
from datetime import datetime,date
from scipy import stats
import pymysql




'''
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.style.use("seaborn")'''

def main():
    '''NO SIRVE DE NADA AL FORMARSE DE FORMA DINÁMICA EL LINK DE DESCARGA Y NO ENCOTRARSE EN EL HTML DEL BOTÓN A PULSAR'''

    #url = 'https://www.imf.org/external/datamapper/NGDPDPC@WEO/OEMDC/ADVEC/WEOWORLD'
    #r = requests.get(url=url)

    archivo_html = "international_GDP_per_capita.html"
    with open(archivo_html, "r", encoding="utf-8") as file:
        contenido = file.read()

    soup = BeautifulSoup(contenido,"html.parser")

    botones_descarga = soup.find_all(class_ = "dm-share-button")
    boton_buscado = None

    for boton in botones_descarga:

        if boton["data-what"] == "all":
            boton_buscado = boton
            break

    print(boton)

def obtener_datos(nombre_archivo_excel, nombre_archivo_csv):

    url_archivo = "https://www.imf.org/external/datamapper//export/excel.php?indicator=NGDPDPC"
    peticion = requests.get(url_archivo)
    
    with open(nombre_archivo_excel, "wb") as o:
        o.write(peticion.content)

    workbook = xlrd.open_workbook(nombre_archivo_excel, ignore_workbook_corruption=True)
    dataframe = pd.read_excel(workbook)
    dataframe.to_csv(nombre_archivo_csv, index=False)
    os.remove(nombre_archivo_excel)
    return dataframe


def filtrar_datos(nombre_archivo_csv):
    dataframe_completo = pd.read_csv(nombre_archivo_csv)
    dataframe_desde_2000 = dataframe_completo.iloc[1:dataframe_completo.shape[0]-2,[0] + list(range(21, dataframe_completo.shape[1]))]
    return dataframe_desde_2000

'''
def obtener_media_fila_sin_nulos(dataframe,num_fila): #obtengo la media de cada fila sin valores "no data"
    
        fila = dataframe.iloc[num_fila,1:] #quito la columna del pais
        contador_no_nulos = 0
        suma = 0
        for i in range(len(fila)):
            if not pd.isna(fila[i]):
                suma += float(fila[i])
                contador_no_nulos += 1

        return suma/contador_no_nulos

def formatear_valores_nulos(dataframe, valor_cambiar):
    columnas_originales = dataframe.columns
    imp = SimpleImputer(missing_values=valor_cambiar, strategy='constant', fill_value=np.nan)
    dataframe= imp.fit_transform(dataframe)
    dataframe = pd.DataFrame(dataframe, columns= columnas_originales)
    return dataframe


def limpiar_datos(dataframe):  #cambio de valores nulos por la media de cada fila
        
    for fila in range(dataframe.shape[0]):
        media_fila = obtener_media_fila_sin_nulos(dataframe, fila)
        for columna in range(dataframe.shape[1]):
            if pd.isna(dataframe.iloc[fila,columna]):
                dataframe.iloc[fila,columna] = media_fila
                
    return dataframe
'''

def anula_valores_no_numericos(dataframe):
    return dataframe.apply(pd.to_numeric, errors='coerce')

def media_no_nulos_fila(fila):
    return pd.to_numeric(fila.dropna()).mean()

def elimina_nulos(dataframe):
    for index, fila in dataframe.iterrows():
        dataframe.iloc[index-1] = fila.fillna(media_no_nulos_fila(fila))
    return dataframe


###################################################
# PARA MYSQL
###################################################

def crea_traspuesta(dataframe):
    traspuesta = datos_raw.iloc[:,1:].T.reset_index()
    columnas_nuevas = pd.concat([pd.Series(['año']), datos_raw.iloc[:,0]])
    traspuesta.columns = columnas_nuevas.str.replace(' ', '_').str.replace('[^a-zA-Z0-9_]', '')

    traspuesta = traspuesta.iloc[:,[0]+list(range(2,traspuesta.shape[1]-2))]
    return traspuesta

def conecta_BD(dataframe, nombre_tabla):
    database_username = "root"
    database_password = "010203En"
    database_ip = 'localhost'
    database_name = "prueba"
    database_connection = db.create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.
                                           format(database_username,database_password,database_ip,database_name))
    connection = database_connection.connect()
    metadata = db.MetaData()
    dataframe.to_sql(nombre_tabla, connection,if_exists='replace', index=False)

# hacer una lambda función en la que se consiga la media de una fila (coja sólo los valores no nulos, los meta en 
# una lista y luego devuelva la media)
#hacer una lambda función que, dado un valor nulo, lo sustituya por el valor de la media de su fila calculada 
# con la función anterior

# sustituir cada nan por un 0 y con apply() hacer sum() de toda la fila con axis=1 y despues dividir esa cantidad
# entre el numero de elementos que no sean 0 (Eso puede hacerse con otra función). Después habrá que sustituir
# los 0 por cada valor correspondiente


if __name__ == '__main__':
    print("Executing [Scraping]PIB_per_capita.py")
    nombre_archivo_excel = "DataSets/[RAW]pib_per_capita.xls"
    nombre_archivo_csv = "DataSets/[RAW]pib_per_capita.csv"
    datos_raw = obtener_datos(nombre_archivo_excel, nombre_archivo_csv)
    
    '''dataframe_desde_2000 = filtrar_datos(nombre_archivo_csv)
    print(dataframe_desde_2000)
    columna_paises = dataframe_desde_2000.iloc[:,0]
    dataframe_nulos_introducidos = anula_valores_no_numericos(dataframe_desde_2000.iloc[:,1:])
    print(dataframe_nulos_introducidos)
    dataframe_limpio = elimina_nulos(dataframe_nulos_introducidos)
    print(pd.concat([columna_paises, dataframe_limpio], axis=1))'''

    #conecta_BD(datos_raw,'pib_per_capita')
    #conecta_BD(crea_traspuesta(datos_raw),'pib_per_capita_traspuesta')
    

    '''
    dataframe_nulos_formateados = formatear_valores_nulos(dataframe_desde_2000,"no data")
    dataframe_sin_nulos = limpiar_datos(dataframe_nulos_formateados)
    #print(dataframe_sin_nulos)
    dataframe_sin_paises = dataframe_nulos_formateados = dataframe_sin_nulos.iloc[:,1:]
    print(dataframe_sin_paises)
    print(dataframe_sin_paises.dtypes)
    '''


        
        
