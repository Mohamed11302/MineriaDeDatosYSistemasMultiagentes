
# 1. Imports básicos

import warnings
warnings.filterwarnings("ignore")
import os
import sys
import sklearn
import matplotlib.pyplot as plt
import numpy
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn import preprocessing
min_max_scaler = preprocessing.MinMaxScaler()
scaler = preprocessing.StandardScaler()
from sklearn import metrics
#from sklearn.neighbors import kneighbors_graph
from scipy import cluster
#from  sklearn.metrics import DistanceMetric
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn import metrics

ruta_actual = os.path.dirname(os.path.abspath(sys.argv[0]))
directorio_superior = os.path.dirname(ruta_actual)
sys.path.append(directorio_superior)
from Acceso_BBDD.MetodosBBDD import *

# DESCOMENTAR SI SE QUIEREN LAS IMÁGENES (AL IGUAL QUE LAS LÍNEAS EN LAS QUE SE GUARDAN LAS IMÁGENES EN SÍ)
ruta_carpeta_imagenes = ruta_actual + "/Imagenes_H2/"
if not os.path.exists(ruta_carpeta_imagenes):
    # Si no existe, crear la carpeta
    os.makedirs(ruta_carpeta_imagenes)


def cargar_datos():

    # 1. Carga de datos

    dataframe  = obtener_dataframe_sql('Hipotesis_2', GOLD)
    dataframe = dataframe.set_index('Country')

    return dataframe


def analizar_componentes_principales(dataframe):
    # 2. Análisis de Componentes Principales de todo el Dataframe

    states = scaler.fit_transform(dataframe)
    estimator = PCA (n_components = 2)
    X_pca = estimator.fit_transform(states)

    plt.figure(figsize=(10, 8))
    plt.title("Análisis de Componentes Principales de todo el Dataframe")
    plt.scatter(X_pca[:,0], X_pca[:,1], s=50)
    for i in range(len(X_pca)):
        plt.text(X_pca[i, 0], X_pca[i, 1], dataframe.iloc[i, :].name)
    plt.grid()
    plt.savefig(ruta_carpeta_imagenes + "componentes_principales_tarjeta_datos_H2" + ".png")
    plt.show()

def normalizacion_Gasolina_Diesel(dataframe): 
    # 3. Separación y normalización de datos sobre combustible 

    df_Gasolina_Diesel = dataframe[['Gasolina_2017','Gasolina_2018','Gasolina_2019','Gasolina_2020','Gasolina_2021','Gasolina_2022','Diesel_2017','Diesel_2018','Diesel_2019','Diesel_2020','Diesel_2021','Diesel_2022']]
    datanorm_Gasolina_Diesel = min_max_scaler.fit_transform(df_Gasolina_Diesel)

    return df_Gasolina_Diesel, datanorm_Gasolina_Diesel

def normalización_Vehiculos_Vendidos(dataframe):
    # 4. Separación y normalización de datos sobre Vehículos Vendidos

    df_Coches_Vendidos = dataframe[['CochesVendidos_2017','CochesVendidos_2018','CochesVendidos_2019','CochesVendidos_2020','CochesVendidos_2021','CochesVendidos_2022']]
    datanorm_Coches_Vendidos = min_max_scaler.fit_transform(df_Coches_Vendidos)
    
    return df_Coches_Vendidos, datanorm_Coches_Vendidos

def calcular_matriz_similitud(datanorm, nombre_grafica):
    # 5. Obtención de Componentes Principales sobre el dataframe normalizado introducido y Similarity Matrix

    states_datanorm = scaler.fit_transform(datanorm)
    estimator = PCA (n_components = 2)
    pca_dataframe = estimator.fit_transform(states_datanorm)
    #print(estimator.explained_variance_ratio_)
    
    dist = sklearn.metrics.DistanceMetric.get_metric('euclidean')
    matsim = dist.pairwise(datanorm)
    ax = sns.heatmap(matsim,vmin=0, vmax=1)
    plt.savefig(ruta_carpeta_imagenes + nombre_grafica + ".png")
    plt.show()

    return matsim, pca_dataframe

def representar_clusters(dataframe, labels, num_inicial_labels, pca_dataframe, nombre_grafica):
    # 6. Algoritmo para representar los cluster generados

    colores = []
    for label in labels:
        if label == num_inicial_labels:
            colores.append("blue")
        elif label == 2:
            colores.append("orange")
        else:
            colores.append("green")

    plt.figure(figsize=(10, 8))
    plt.title(nombre_grafica)
    plt.scatter(pca_dataframe[:,0], pca_dataframe[:,1], c=colores,s=50)

    for i in range(len(labels)):
        plt.text(pca_dataframe[i, 0], pca_dataframe[i, 1], dataframe.iloc[i, :].name)

    plt.grid()
    plt.savefig(ruta_carpeta_imagenes + nombre_grafica + ".png")
    plt.show()


def clustering_jerarquico(dataframe, datanorm, matsim, pca_dataframe, nombre_grafica):
    # 7. Clustering Jerárquico sobre el combustible o los Vehiculos Vendidos

    best_silhouette = -1
    best_cut = -1
    best_method = ""

    # Prueba diferentes valores de cut y métodos de enlace
    for cut_value in range(1,  6):  # Prueba diferentes valores de cut
        for method in ['single', 'complete', 'average', 'ward']:  # Prueba diferentes métodos de enlace
            clusters = cluster.hierarchy.linkage(matsim, method=method)
            labels = cluster.hierarchy.fcluster(clusters, cut_value, criterion='distance')
            silhouette = metrics.silhouette_score(datanorm, labels)

            if silhouette > best_silhouette:
                best_silhouette = silhouette
                best_cut = cut_value
                best_method = method

    #print('Best cut value: %d' % best_cut)
    #print('Best linkage method: %s' % best_method)
    #print('Best Silhouette Coefficient: %0.3f' % best_silhouette) 

    clusters = cluster.hierarchy.linkage(matsim, method=best_method)
    labels = cluster.hierarchy.fcluster(clusters, 1, criterion = 'distance')
    
    representar_clusters(dataframe, labels, min(labels), pca_dataframe, nombre_grafica)

    cluster.hierarchy.dendrogram(clusters, color_threshold=18, labels = dataframe.index)

    # 3.2.1 Visualization
    f = plt.figure()
    plt.show()
    
    # Aquellos países pertenecientes al segundo cluster
    df_aux = dataframe.copy()
    df_aux["group"] = labels
    #print(df_aux[df_aux["group"] != min(labels)])
  

    return df_aux


def clustering_k_means(dataframe, pca_dataframe, nombre_grafica):
    # 8. Clustering K-Means sobre el combustible o los Vehiculos Vendidos

    n_clusters_values = range(2, 7)
    init_values = ['k-means++', 'random']

    best_silhouette = -1
    best_params = {}

    for n_clusters in n_clusters_values:
        for init_method in init_values:
            km = KMeans(n_clusters=n_clusters, init=init_method, n_init=10, max_iter=300, tol=0.0001, random_state=42)
            labels = km.fit_predict(Gasolina_Diesel_pca)
            silhouette = metrics.silhouette_score(pca_dataframe, labels)

            if silhouette > best_silhouette:
                best_silhouette = silhouette
                best_params = {'n_clusters': n_clusters, 'init': init_method}

    #print('Best combination of parameters:')
    #print(best_params)
    #print('Best Silhouette Coefficient: %0.3f' % best_silhouette)

    km = KMeans(n_clusters=best_params['n_clusters'], init=best_params['init'], n_init=10, max_iter=300, tol=0.0001, random_state=42)
    y_km = km.fit_predict(pca_dataframe)
    
    #AD-HOC !!! (para que el cluster de la derecha sea el verde como en el caso del clustering jerárquico)
    lista_invertida = []
    if nombre_grafica == "clustering_k_means_Gasolina_Diesel":
        lista_invertida = [1 if valor == 0 else 0 for valor in km.labels_] 
        representar_clusters(dataframe, lista_invertida, min(lista_invertida), pca_dataframe, nombre_grafica)
    else:
        representar_clusters(dataframe, km.labels_, min(km.labels_), pca_dataframe, nombre_grafica)


def clasification_model(df_clasificacion_Vehiculos):
    # Modelo de clasificacion en paises que venden mas o menos coches
    feature_selection = ['CochesVendidos_2017','CochesVendidos_2018','CochesVendidos_2019','CochesVendidos_2020','CochesVendidos_2021','CochesVendidos_2022']
    X = df_clasificacion_Vehiculos[feature_selection]
    y = df_clasificacion_Vehiculos['group']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    gnb = GaussianNB()
    gnb.fit(X_train, y_train)

    y_pred = gnb.predict(X_test)

    # Calculate Accuracy
    accuracy = metrics.accuracy_score(y_test, y_pred)
    #print(f"Accuracy: {accuracy}")


    # Predict
    data_China = {
    'Country': ['China'],
    'CochesVendidos_2017': [14117684],
    'CochesVendidos_2018': [13919656],
    'CochesVendidos_2019': [13188211],
    'CochesVendidos_2020': [12419372],
    'CochesVendidos_2021': [12118025],
    'CochesVendidos_2022': [13105950]
    }
    

    df_China = pd.DataFrame(data_China)
    df_China.set_index('Country', inplace=True)

    group_China = gnb.predict(df_China)
    #print("China in classified as", group_China)
 
if __name__ == "__main__":
    dataframe_original = cargar_datos()
    analizar_componentes_principales(dataframe_original)
    df_Gasolina_diesel, datanorm_Gasolina_Diesel = normalizacion_Gasolina_Diesel(dataframe_original)
    df_Coches_Vendidos, datanorm_Coches_Vendidos = normalización_Vehiculos_Vendidos(dataframe_original)
    matsim_Gasolina_Diesel, Gasolina_Diesel_pca = calcular_matriz_similitud(datanorm_Gasolina_Diesel, "matriz_similitud_Gasolina_Diesel")
    matsim_coches_vendidos, Coches_Vendidos_pca  = calcular_matriz_similitud(datanorm_Coches_Vendidos, "matriz_similitud_Vehiculos_Vendidos")
    df_clasificacion_Gasolina = clustering_jerarquico(df_Gasolina_diesel, datanorm_Gasolina_Diesel, matsim_Gasolina_Diesel, Gasolina_Diesel_pca, "clustering_jerarquico_Gasolina_Diesel")
    df_clasificacion_Vehiculos = clustering_jerarquico(df_Coches_Vendidos, datanorm_Coches_Vendidos, matsim_coches_vendidos, Coches_Vendidos_pca, "clustering_jerarquico_Vehiculos_Vendidos")
    clustering_k_means(df_Gasolina_diesel, Gasolina_Diesel_pca, "clustering_k_means_Gasolina_Diesel")
    clustering_k_means(df_Coches_Vendidos, Coches_Vendidos_pca, "clustering_k_means_Vehiculos_Vendidos")
    clasification_model(df_clasificacion_Vehiculos)