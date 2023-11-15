import pandas as pd
from sqlalchemy import create_engine, URL


RAW = 'raw'
SILVER = 'silver'
GOLD = 'gold'
def obtener_dataframe(nombre_tabla, db_name):
    conn = ConectarseABBDD(local=False, db_name=db_name)
    consulta = f"SELECT * FROM {nombre_tabla}"
    df = pd.read_sql_query(consulta, conn)
    return df

def subir_dataframe(dataframe:pd.core.frame.DataFrame, db_name:str, nombre_tabla:str):
    conn = ConectarseABBDD(local=False,db_name=db_name)
    dataframe.to_sql(nombre_tabla, conn, if_exists="replace", index=False)


def ConectarseABBDD(local, db_name):
    db_url = DatosBBDD(db_name)
    if local:
        connect_args = {"ssl": {"fake_flag_to_enable_tls": True}}
        conn = create_engine(db_url, connect_args=connect_args)
    else:
        ssl_args = {"ssl_ca": "Preprocesado de Datos/Acceso BBDD/ca.pem", "ssl_verify_identity": False, "ssl_verify_cert": True}
        conn = create_engine(db_url, connect_args=ssl_args)
    conn.connect()
    return conn


def DatosBBDD(db_name:str):
    db_url = URL.create(
        "mysql+pymysql",
        username="minero",
        password="MineriaMultiagentes2324*",
        host="db.programadormanchego.es",
        port=3306,
        database=db_name,
    )
    return db_url


dataframe_resultante = obtener_dataframe('puntos_de_carga', RAW)
subir_dataframe(dataframe_resultante, RAW, 'prueba_subida')
print(dataframe_resultante.head())

