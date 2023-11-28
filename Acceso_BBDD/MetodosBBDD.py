import pandas as pd
from sqlalchemy import create_engine, URL
from Acceso_BBDD.password import *
RAW = 'raw'
SILVER = 'silver'
GOLD = 'gold'


def obtener_dataframe_sql(nombre_tabla, schema_name):
    conn = ConectarseABBDD(local=False, schema_name=schema_name)
    consulta = f"SELECT * FROM {nombre_tabla}"
    df = pd.read_sql_query(consulta, conn)
    return df

def subir_dataframe_sql(dataframe:pd.core.frame.DataFrame, nombre_tabla:str, schema_name:str):
    conn = ConectarseABBDD(local=False,schema_name=schema_name)
    dataframe.to_sql(nombre_tabla, conn, if_exists="replace", index=False)


def ConectarseABBDD(local, schema_name):
    db_url = DatosBBDD(schema_name)
    if local:
        connect_args = {"ssl": {"fake_flag_to_enable_tls": True}}
        conn = create_engine(db_url, connect_args=connect_args)
    else:
        ssl_args = {"ssl_ca": "Acceso_BBDD/ca.pem", "ssl_verify_identity": False, "ssl_verify_cert": True}
        conn = create_engine(db_url, connect_args=ssl_args)
    conn.connect()
    return conn


def DatosBBDD(schema_name:str):
    db_url = URL.create(
        "mysql+pymysql",
        username="minero",
        password=PasswordBBDD(),
        host="db.programadormanchego.es",
        port=3306,
        database=schema_name,
    )
    return db_url
