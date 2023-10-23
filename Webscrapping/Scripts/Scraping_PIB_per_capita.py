
import requests
from bs4 import BeautifulSoup
import pandas as pd
import xlrd
import os
import numpy as np
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


def filtrar_datos(nombre_archivo_csv):
    dataframe_completo = pd.read_csv(nombre_archivo_csv)
    dataframe_desde_2000 = dataframe_completo.iloc[1:dataframe_completo.shape[0]-2,[0] + list(range(21, dataframe_completo.shape[1]))]
    return dataframe_desde_2000


def obtener_media_fila_sin_nulos(dataframe,num_fila): #obtengo la media de cada fila sin valores "no data"
    
        fila = dataframe.iloc[num_fila,1:] #quito la columna del pais
        contador_no_nulos = 0
        suma = 0
        for i in range(len(fila)):
            if not fila[i] == 'no data':
                suma += float(fila[i])
                contador_no_nulos += 1

        return suma/contador_no_nulos

def limpiar_datos(dataframe):  #cambio de valores nulos por la media de cada fila
        
    for fila in range(dataframe.shape[0]):
        media_fila = obtener_media_fila_sin_nulos(dataframe, fila)
        for columna in range(dataframe.shape[1]):
            if dataframe.iloc[fila,columna] == 'no data':
                a =1
                #dataframe[fila,columna] = media_fila
                
    return dataframe



if __name__ == '__main__':
    print("Executing Scraping_PIB_per_capita.py")
    nombre_archivo_excel = "../DataSets/pib_per_capita.xls"
    nombre_archivo_csv = "../DataSets/[RAW]pib_per_capita.csv"
    obtener_datos(nombre_archivo_excel, nombre_archivo_csv)
    dataframe_desde_2000 = filtrar_datos(nombre_archivo_csv)

    dataframe_sin_nulos = limpiar_datos(dataframe_desde_2000)
    
    

        
        
