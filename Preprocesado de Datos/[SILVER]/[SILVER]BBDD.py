import pandas as pd
from sqlalchemy import create_engine

def obtener_dataframe(nombre_tabla):
    db_host, db_port, db_user, db_password, db_name, ssl_ca = DatosBBDD()
    url = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?ssl_ca={ssl_ca}"
    engine = create_engine(url)
    consulta = f"SELECT * FROM {nombre_tabla}"
    df = pd.read_sql_query(consulta, engine)
    engine.dispose()
    return df

def DatosBBDD():
    db_host = "db.programadormanchego.es"
    db_port = 3306
    db_user = "minero"
    with open("Preprocesado de Datos/Acceso BBDD/password.txt", 'r') as archivo_password:
        db_password = archivo_password.read()
    db_name = "raw"
    ssl_ca = "Preprocesado de Datos/Acceso BBDD/ca.pem"
    return db_host, db_port, db_user, db_password, db_name, ssl_ca

#dataframe_resultante = obtener_dataframe('puntos_de_carga')
#print(dataframe_resultante.head())
