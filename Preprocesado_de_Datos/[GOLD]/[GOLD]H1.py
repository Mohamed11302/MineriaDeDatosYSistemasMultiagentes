import os
import sys
ruta_actual = os.path.dirname(os.path.abspath(sys.argv[0]))
directorio_superior = os.path.dirname(ruta_actual)
abuelo_directorio = os.path.dirname(directorio_superior)
sys.path.append(abuelo_directorio)
from Preprocesado_de_Datos.Acceso_BBDD.MetodosBBDD import *
import pandas as pd



def prepare_df1 (dataframe1):

    dataframe1= dataframe1.groupby(['Model'])[['2017', '2018', '2019', '2020', '2021', '2022']].sum()
    
    return dataframe1
    

def prepare_df2 (dataframe2,models):
    dataframe2= dataframe2.drop(['Brand'],axis=1)
    for i in models:
        for j in dataframe2['Model']:
            if j in i or i in j:
                dataframe2['Model']=dataframe2['Model'].replace(j,i)

    dataframe2 = dataframe2.set_index('Model')

    return dataframe2


def TarjetaDeDatos():
    
    nombre_tabla = 'model_per_year'
    dataframe1 = obtener_dataframe_sql(nombre_tabla, SILVER)

    nombre_tabla = 'electric_car_data_clean'
    dataframe2 = obtener_dataframe_sql(nombre_tabla, SILVER)
    
    dataframe1 = prepare_df1(dataframe1)
    
    dataframe2 = prepare_df2(dataframe2,dataframe1.index)

    data_card = pd.merge(dataframe1, dataframe2, on='Model')

    numeric_columns = data_card.select_dtypes(include='number').columns
    non_numeric_columns = data_card.select_dtypes(exclude='number').columns

    # Agrupar por 'Model' y aplicar funciones de agregación, como tenemos varias versiones del mismo modelo sin mucha variación.
    # se juntan en la misma fila haciendo la media de sus características.
    aggregated_data = data_card.groupby('Model').agg({
    **{col: lambda x: round(x.mean(), 2) for col in numeric_columns},
    **{col: 'first' for col in non_numeric_columns}
    })

    aggregated_data.reset_index(inplace=True)
    
    return aggregated_data
