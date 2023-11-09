
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker
import pandas as pd
import pymysql
from pandas.io import sql
import mysql.connector



def conecta_BD(db_dict, url):
    database_connection = sqlalchemy.create_engine(url)
    connection = database_connection.connect()

    for clave in db_dict.keys():
        print(clave)
        dataframe_aux = pd.read_csv(db_dict[clave])
        dataframe_aux.columns = dataframe_aux.columns.str.replace(' ', '_').str.replace('[^a-zA-Z0-9_]', '')
        dataframe_aux.to_sql(clave, connection,if_exists='replace', index=False)
        


# Datos de conexión a la base
db_host = "db.programadormanchego.es"
db_port = 3306
db_user = "minero"
with open("password.txt", 'r') as archivo_password:
        db_password = archivo_password.read()
db_name = "raw"
ssl_ca = "ca.pem"
db_dict = {
           "pib_per_capita":"../DataSets/[RAW]pib_per_capita.csv",
           "data_CO2":"../DataSets/[RAW]data_CO2.csv",
           "electric_car_data_clean":"../DataSets/[RAW]electric_car_data_clean.csv",
           "electricity_all_countries":"../DataSets/[RAW]electricity_all_countries.csv",
           #"gasoline_Diesel_prices":"../DataSets/[RAW]gasoline_Diesel_prices.csv",
           "level_of_studies":"../DataSets/[RAW]level_of_studies.csv",
           #"model_per_year":"../DataSets/[RAW]model_per_year.csv",
           "puntos_de_carga":"../DataSets/[RAW]puntos_de_carga.csv"
           }

# Crear una conexión a la base de datos usando SQLAlchemy
db_url = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?ssl_ca={ssl_ca}"

conecta_BD(db_dict, db_url)



