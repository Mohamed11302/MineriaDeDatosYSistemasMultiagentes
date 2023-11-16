
import importlib
import pandas as pd
import numpy as np
import os
import sys
ruta_actual = os.path.dirname(os.path.abspath(sys.argv[0]))
directorio_superior = os.path.dirname(ruta_actual)
abuelo_directorio = os.path.dirname(directorio_superior)
sys.path.append(abuelo_directorio)
from Preprocesado_de_Datos.Acceso_BBDD.MetodosBBDD import *


def limpiar_dataframe():
     df = obtener_dataframe_sql('model_per_year', RAW)

     # Reemplaza los guiones por un valor nulo
     df[df == "-"] = np.nan

     # Elimina las comas y convierte los números a float
     df.replace(",", "", regex=True, inplace=True)
     df.iloc[:, -6:] = df.iloc[:, -6:].astype(float)

     ev_powertrain = [
          "EV", # Vehículo eléctrico
          "PHV", # Vehículo eléctrico enchufable
          "Mild HV", # Semi-híbrido
          "HV", # Híbrido
          "48V Mild HV", # Híbrido
          "HV/PHV",
          "HV/MHV",
          "HV/EV/PHV",
          "HV/EV"
     ]

     # Añade una columna que indica si el vehículo es eléctrico o no
     # y elimina el tipo de motor
     is_ev = df["PowerTrain"].isin(ev_powertrain)
     df.insert(4, "isEv", is_ev)

     # Elimina las filas que tengan al menos un número negativo
     years = df.iloc[:, -6:]
     valid_rows = years[((years < 0).sum(axis=1) == 0)]
     df.iloc[:, -6:] = valid_rows

     # Sustituye los valores nulos por 0
     df.fillna(0, inplace=True)
     return df