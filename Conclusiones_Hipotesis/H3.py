import os
import sys
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
import numpy as np
ruta_actual = os.path.dirname(os.path.abspath(sys.argv[0]))
directorio_superior = os.path.dirname(ruta_actual)
sys.path.append(directorio_superior)
from Acceso_BBDD.MetodosBBDD import *

def EntrenarModelo():
    df = obtener_dataframe_sql('Hipotesis_3', GOLD)
    print(df)
    X = df
    y = df.Sells
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    DTR = DecisionTreeRegressor()
    param_dist = {
    'criterion': ['friedman_mse', 'absolute_error','squared_error', 'poisson'],
    'splitter': ['best', 'random'],
    'max_depth': [None] + list(np.arange(1, 20)),
    'min_samples_split': np.arange(2, 20),
    'min_samples_leaf': np.arange(1, 20),
    'max_features': ['sqrt', 'log2', None] + list(np.arange(0.1, 1.1, 0.1)),
    }
    random_DTR = RandomizedSearchCV(DTR, param_distributions=param_dist, n_iter=10, cv=5, scoring='roc_auc', n_jobs=-1, verbose=1)
    random_DTR.fit(X_train, y_train)
    print(random_DTR.best_estimator_)


if __name__ == "__main__":
    #EntrenarModelo()
    df = obtener_dataframe_sql('Hipotesis_3', GOLD)
    df.to_csv('Hipotesis3.csv', sep=";")


