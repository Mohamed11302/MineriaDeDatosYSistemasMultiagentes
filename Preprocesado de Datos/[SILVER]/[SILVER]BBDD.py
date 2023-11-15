import pandas as pd
from sqlalchemy import create_engine, URL
import importlib

def obtener_dataframe(nombre_tabla):
    conn = ConectarseABBDD(local=False)
    consulta = f"SELECT * FROM {nombre_tabla}"
    df = pd.read_sql_query(consulta, conn)
    return df

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

def SubirDataframeABBDD(local, nombre_tabla, df):
    conn = ConectarseABBDD(local)
    conn.connect()
    df.to_sql(nombre_tabla, conn, if_exists="replace", index=False)



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

def SubirDataframes()->dict:
    ScriptsLimpieza = {
        'data_CO2':'[SILVER]CO2_data',
        'electric_car_data_clean':'[SILVER]Electric_Car_Data',
        'electricity_all_countries':'[SILVER]electricity_in_all_countries',
        'gasoline_Diesel_prices':'[SILVER]Gasoline_Diesel',
        'level_of_studies':'[SILVER]Level_Of_Studies',
        'model_per_year':'[SILVER]model_per_year',
        'pib_per_capita':'[SILVER]PIB_per_capita',
        'puntos_de_carga':'[SILVER]Puntos_De_Carga'
    }
    return ScriptsLimpieza
def subir_dataframe_limpios():
    Dataframes = SubirDataframes()
    for nombre_bbdd, ruta in Dataframes.values():        
        Dataframe_Subir = importlib.import_module(ruta)
        df = Dataframe_Subir.limpiar_dataframe()


dataframe_resultante = obtener_dataframe('puntos_de_carga')
print(dataframe_resultante.head())
