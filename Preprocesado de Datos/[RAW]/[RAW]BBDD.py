import pandas as pd
from sqlalchemy import create_engine, URL
import warnings
import importlib
'''
import sys
sys.path.append("Preprocesado de Datos/Acceso BBDD")
print(sys.path)
MetodosBBDD = importlib.import_module('Preprocesado de Datos/Acceso BBDD/MetodosBBDD')
'''

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
    return db_dict

def DatosBBDD():
    db_url = URL.create(
        "mysql+pymysql",
        username="minero",
        password="MineriaMultiagentes2324*",
        host="db.programadormanchego.es",
        port=3306,
        database="raw",
    )
    return db_url

def ConectarseABBDD(local):
    db_url = DatosBBDD()
    if local:
        connect_args = {"ssl": {"fake_flag_to_enable_tls": True}}
        conn = create_engine(db_url, connect_args=connect_args)
    else:
        ssl_args = {"ssl_ca": "Preprocesado de Datos/Acceso BBDD/ca.pem", "ssl_verify_identity": False, "ssl_verify_cert": True}
        conn = create_engine(db_url, connect_args=ssl_args)
    conn.connect()
    return conn

def SubirArchivosABBDD(local):
    conn = ConectarseABBDD(local)
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
        df.to_sql(nombre_dataset, conn, if_exists="replace", index=False)



SubirArchivosABBDD(local = False)