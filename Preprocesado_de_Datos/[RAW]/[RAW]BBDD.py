import pandas as pd
import warnings
import os
import sys

ruta_actual = os.path.dirname(os.path.abspath(sys.argv[0]))
directorio_superior = os.path.dirname(ruta_actual)
abuelo_directorio = os.path.dirname(directorio_superior)
sys.path.append(abuelo_directorio)

from Preprocesado_de_Datos.Acceso_BBDD.MetodosBBDD import *
warnings.filterwarnings('ignore')
def DatosDataSets():
    db_dict = {
           "data_CO2":"DataSets/[RAW]CO2_data.csv",
           "electric_car_data_clean":"DataSets/[RAW]electric_car_data_clean.csv",
           "electricity_all_countries":"DataSets/[RAW]electricity_in_all_countries.csv",
           "gasoline_Diesel_prices":"DataSets/[RAW]gasoline_Diesel_prices.csv",
           "level_of_studies":"DataSets/[RAW]level_of_studies.csv",
           "model_per_year":"DataSets/[RAW]model_per_year.csv",
           "pib_per_capita":"DataSets/[RAW]pib_per_capita.csv",
           "puntos_de_carga":"DataSets/[RAW]puntos_de_carga.csv"
           }
    db_dict = {
         'prueba': "DataSets/[RAW]CO2_data.csv"
    }
    return db_dict


def SubirArchivosABBDD():
    datasets = DatosDataSets()
    for nombre_dataset, path in datasets.items():
        print("UPLOADING DATASET: " + str(nombre_dataset))
        if nombre_dataset == 'gasoline_Diesel_prices':
            df = pd.read_csv(path,encoding='utf-16')
        elif nombre_dataset == 'level_of_studies':
                df = pd.read_csv(path, on_bad_lines='skip')
        elif nombre_dataset == 'model_per_year':
               df= pd.read_csv(path, sep=';')
        else:
            df = pd.read_csv(path)            
        df.columns = df.columns.str.replace(' ', '_').str.replace('[^a-zA-Z0-9_]', '')
        subir_dataframe_sql(df, nombre_dataset, RAW)



SubirArchivosABBDD()