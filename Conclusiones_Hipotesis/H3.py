import os
import sys
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
import joblib  # Para guardar el modelo entrenado
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import optuna

ruta_actual = os.path.dirname(os.path.abspath(sys.argv[0]))
directorio_superior = os.path.dirname(ruta_actual)
sys.path.append(directorio_superior)
from Acceso_BBDD.MetodosBBDD import *

def codificar_variables_categoricas(df):
    """
    Electric: 0
    Hybrid: 1
    Austria: 0
    Denmark: 1
    Finland: 2
    France: 3
    Germany: 4
    Greece: 5
    Italy: 6
    Netherlands: 7
    Poland: 8
    Portugal: 9
    Spain: 10
    Sweden: 11 
    """
    label_encoder = LabelEncoder()
    df['Country'] = label_encoder.fit_transform(df['Country'])
    df['Type_Vehicle'] = label_encoder.fit_transform(df['Type_Vehicle'])
    return df

def analizar_correlacion(dataframe):

    # 3. Análisis de Correlación entre variables

    correlation_matrix = dataframe.corr()
    sns.set(style="white")
    plt.figure(figsize=(15, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
    plt.title("Matriz de Correlación entre todas las variables iniciales")
    plt.xlabel("Variables")
    plt.ylabel("Variables")
    #plt.savefig(ruta_carpeta_imagenes + "correlacion_variables" + ".png")
    plt.show()


def RandomizedSearch(X_train, y_train):
    param_dist = {
    'n_estimators': [100,200,300,400,500,1000,2000,3000],
    'max_depth': [20,30,50],
    'min_samples_split': [6,8,10],
    'min_samples_leaf': [5,7,9,10],
    'max_features': ['sqrt', 'log2']
    }
    regressor = RandomForestRegressor()
    random_search = RandomizedSearchCV(
        regressor, 
        verbose=1,
        param_distributions=param_dist, 
        n_iter=100,  # Número de combinaciones aleatorias a probar
        scoring='neg_mean_squared_error',  # Puedes cambiar la métrica de evaluación según tus necesidades
        cv=10  # Número de divisiones para la validación cruzada
    )
    random_search.fit(X_train, y_train)
    print("Mejores hiperparámetros:", random_search.best_params_)
    return random_search.best_estimator_




def objective(trial, x_train, x_test, y_train, y_test):
    params = {
        # Define los hiperparámetros a optimizar
        'n_estimators': trial.suggest_int("n_estimators", 1, 3000),
        'max_depth': trial.suggest_int("max_depth", 1, 50),
        'min_samples_split': trial.suggest_float("min_samples_split", 0.1, 1.0),
        'min_samples_leaf': trial.suggest_float("min_samples_leaf", 0.1, 1.0),
        'max_features': trial.suggest_categorical("max_features", ["sqrt", "log2"])
    }

    regressor = RandomForestRegressor(**params)
    regressor.fit(x_train, y_train)
    y_pred = regressor.predict(x_test)
    mse = mean_squared_error(y_test, y_pred)

    return mse

def optuna_search(x_train, x_test, y_train, y_test): #125
    study = optuna.create_study(direction='minimize')
    objective_partial = lambda trial: objective(trial, x_train, x_test, y_train, y_test)
    study.optimize(objective_partial, n_trials=15000, timeout=1200)
    print("Mejores hiperparámetros:", study.best_params)
    best_regressor = RandomForestRegressor(**study.best_params)
    best_regressor.fit(x_train, y_train)
    return best_regressor



def entrenar_modelo(df, selected_columns):
    X = df[selected_columns]
    y = df['Sells']
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
    #regressor = RandomizedSearch(x_train, y_train)  # Asegúrate de utilizar RandomForestRegressor y no la función incorrecta RandomizedSearch
    regressor = optuna_search(x_train, x_test, y_train, y_test)
    y_pred = regressor.predict(x_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f'Mean Squared Error: {mse}')
    
    
    return regressor



def crear_modelo(df):
    df = codificar_variables_categoricas(df)
    #analizar_correlacion(df)
    selected_columns = ["Country","Type_Vehicle", "Fast Charging Point", "Slow Charging Point", "Price_Electricity", "Sells_last_year"]
    regressor = entrenar_modelo(df, selected_columns)
    #joblib.dump(regressor, 'random_forest_regressor_model')
    return regressor

def prediccion_prueba_spain(modelo):
    prueba = {
        "Country":             [10],    
        "Type_Vehicle":        [0], 
        "Fast Charging Point": [3400],  
        "Slow Charging Point": [13600], 
        #"Pib_per_capita":      [33090], 
        #"Price_Gasoline":      [1.647], 
        #"Price_Diesel":        [1.641], 
        "Price_Electricity":   [91],    
        "Sells_last_year":     [205980]
    }
    d = pd.DataFrame(prueba)
    a = modelo.predict(d)
    print("Valor españa: " + str(a))
    #Valor esperado 250k - 290k

if __name__ == "__main__":
    #EntrenarModelo()
    df = obtener_dataframe_sql('Hipotesis_3', GOLD)
    #print(df)
    modelo = crear_modelo(df)
    prediccion_prueba_spain(modelo)
    #df.to_csv('Hipotesis3.csv', sep=";")


