
# 1. Imports básicos

import os
import sys
import sklearn
import warnings
import numpy as np
import seaborn as sns
from sklearn import metrics
import matplotlib.pyplot as plt
from scipy import cluster, stats
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture

warnings.filterwarnings("ignore")
min_max_scaler = preprocessing.MinMaxScaler()
scaler = preprocessing.StandardScaler()

ruta_actual = os.path.dirname(os.path.abspath(sys.argv[0]))
directorio_superior = os.path.dirname(ruta_actual)
sys.path.append(directorio_superior)
from Acceso_BBDD.MetodosBBDD import *

# DESCOMENTAR SI SE QUIEREN LAS IMÁGENES (AL IGUAL QUE LAS LÍNEAS EN LAS QUE SE GUARDAN LAS IMÁGENES EN SÍ)
ruta_carpeta_imagenes = ruta_actual + "/Imagenes_H4/"
if not os.path.exists(ruta_carpeta_imagenes):
    # Si no existe, crear la carpeta
    os.makedirs(ruta_carpeta_imagenes)


def cargar_datos():

    # 2. Carga de datos

    dataframe  = obtener_dataframe_sql('Hipotesis_4', GOLD)
    dataframe = dataframe.set_index('Country')

    return dataframe

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

def analizar_componentes_principales(dataframe):
    # 4. Análisis de Componentes Principales de todo el Dataframe

    states = scaler.fit_transform(dataframe)
    estimator = PCA (n_components = 2)
    X_pca = estimator.fit_transform(states)

    plt.figure(figsize=(10, 8))
    plt.title("Análisis de Componentes Principales de todo el Dataframe")
    plt.scatter(X_pca[:,0], X_pca[:,1], s=50)
    for i in range(len(X_pca)):
        plt.text(X_pca[i, 0], X_pca[i, 1], dataframe.iloc[i, :].name)
    plt.grid()
    #plt.savefig(ruta_carpeta_imagenes + "componentes_principales_tarjeta_datos_H4" + ".png")
    plt.show()

def normalizacion_PIB(dataframe): 
    # 5. Separación y normalización de datos sobre PIB

    df_PIB = dataframe[['PIB_2017','PIB_2018','PIB_2019','PIB_2020','PIB_2021','PIB_2022']]
    datanorm_PIB = min_max_scaler.fit_transform(df_PIB)

    return df_PIB, datanorm_PIB

def normalización_Vehiculos_Vendidos(dataframe):
    # 6. Separación y normalización de datos sobre Vehículos Vendidos

    df_Coches_Vendidos = dataframe[['CochesVendidos_2017','CochesVendidos_2018','CochesVendidos_2019','CochesVendidos_2020','CochesVendidos_2021','CochesVendidos_2022']]
    datanorm_Coches_Vendidos = min_max_scaler.fit_transform(df_Coches_Vendidos)
    
    return df_Coches_Vendidos, datanorm_Coches_Vendidos

def calcular_matriz_similitud(datanorm, nombre_grafica):
    # 7. Obtención de Componentes Principales sobre el dataframe normalizado introducido y Similarity Matrix

    states_datanorm = scaler.fit_transform(datanorm)
    estimator = PCA (n_components = 2)
    pca_dataframe = estimator.fit_transform(states_datanorm)
    #print(estimator.explained_variance_ratio_)
    
    dist = sklearn.metrics.DistanceMetric.get_metric('euclidean')
    matsim = dist.pairwise(datanorm)
    ax = sns.heatmap(matsim,vmin=0, vmax=1)
    #plt.savefig(ruta_carpeta_imagenes + nombre_grafica + ".png")
    plt.show()

    return matsim, pca_dataframe

def representar_clusters(dataframe, labels, num_inicial_labels, pca_dataframe, nombre_grafica):
    # 8. Algoritmo para representar los cluster generados

    colores = []
    for label in labels:
        if label == num_inicial_labels:
            colores.append("blue")
        else:
            colores.append("green")

    plt.figure(figsize=(10, 8))
    plt.title(nombre_grafica)
    plt.scatter(pca_dataframe[:,0], pca_dataframe[:,1], c=colores,s=50)

    for i in range(len(labels)):
        if labels[i] != num_inicial_labels:
            plt.text(pca_dataframe[i, 0], pca_dataframe[i, 1], dataframe.iloc[i, :].name)

    plt.grid()
    #plt.savefig(ruta_carpeta_imagenes + nombre_grafica + ".png")
    plt.show()

def clustering_jerarquico(dataframe, datanorm, matsim, pca_dataframe, nombre_grafica):
    # 9. Clustering Jerárquico sobre el PIB o los Vehiculos Vendidos

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
    labels = cluster.hierarchy.fcluster(clusters, best_cut , criterion = 'distance')
    
    representar_clusters(dataframe, labels, min(labels), pca_dataframe, nombre_grafica)

    '''
    # Aquellos países pertenecientes al segundo cluster
    df_aux = dataframe.copy()
    df_aux["group"] = labels
    print(df_aux[df_aux["group"] != min(labels)])
    '''

def clustering_k_means(dataframe, pca_dataframe, nombre_grafica):
    # 10. Clustering K-Means sobre el PIB o los Vehiculos Vendidos

    n_clusters_values = range(2, 7)
    init_values = ['k-means++', 'random']

    best_silhouette = -1
    best_params = {}

    for n_clusters in n_clusters_values:
        for init_method in init_values:
            km = KMeans(n_clusters=n_clusters, init=init_method, n_init=10, max_iter=300, tol=0.0001, random_state=42)
            labels = km.fit_predict(PIB_pca)
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
    if nombre_grafica == "clustering_k_means_PIB":
        lista_invertida = [1 if valor == 0 else 0 for valor in km.labels_] 
        representar_clusters(dataframe, lista_invertida, min(lista_invertida), pca_dataframe, nombre_grafica)
    else:
        representar_clusters(dataframe, km.labels_, min(km.labels_), pca_dataframe, nombre_grafica)

    '''
    # Aquellos países pertenecientes al segundo cluster
    df_aux = dataframe.copy()
    #AD-HOC !!!
    if nombre_grafica == "clustering_k_means_PIB":
        df_aux["group"] = lista_invertida
    else:
        df_aux["group"] = km.labels_

    print(df_aux[df_aux["group"] != min(km.labels_)])
    '''

def clustering_probabilistico(dataframe, pca_dataframe, nombre_grafica):
    # 11. Clustering Probabilístico sobre el PIB o los Vehiculos Vendidos

    lowest_bic = np.infty
    bic = []
    best_cv = ''
    best_k = -1

    cv_types = ['spherical', 'tied', 'diag', 'full']

    for cv_type in cv_types:
        for k in range(1, 3):
            gmm = GaussianMixture(n_components=k, covariance_type=cv_type, init_params='kmeans')
            gmm.fit(pca_dataframe)
            bic.append(gmm.bic(pca_dataframe))
            if bic[-1] < lowest_bic:
                lowest_bic = bic[-1]
                best_cv = cv_type
                best_k = k  

    #print ("Mejor valor K", best_k, "Mejor tipo de Covarianza", best_cv)

    gmm = GaussianMixture(n_components=best_k, covariance_type=best_cv, init_params='random')
    gmm.fit(pca_dataframe)
    labels =  gmm.predict(pca_dataframe)
    #n_clusters = best_k - (1 if -1 in labels else 0)
    
    #AD-HOC !!! (para que el cluster de la derecha sea el verde como en el caso del clustering jerárquico)
    df_aux = dataframe.copy()
    df_aux = df_aux.reset_index()
    df_aux["group"] = labels
    indice = df_aux.index[df_aux['Country'] == 'Argentina']
    grupo = labels[indice]

    lista_invertida = []
    if nombre_grafica == "clustering_probabilistico_PIB" and grupo != 0 or nombre_grafica == "clustering_probabilistico_Vehiculos_Vendidos" and grupo != 1:
        lista_invertida = [1 if valor == 0 else 0 for valor in labels] 
        representar_clusters(dataframe, lista_invertida, min(lista_invertida), pca_dataframe, nombre_grafica)
    else:
        representar_clusters(dataframe, labels, min(labels), pca_dataframe, nombre_grafica)

    '''
    # Aquellos países pertenecientes al segundo cluster
    df_aux = dataframe.copy()
    #AD-HOC !!!
    if nombre_grafica == "clustering_probabilistico_PIB" and grupo != 0 or nombre_grafica == "clustering_probabilistico_Vehiculos_Vendidos" and grupo != 1:
        df_aux["group"] = lista_invertida
    else:
        df_aux["group"] = labels

    print(df_aux[df_aux["group"] != min(labels)])
    '''
 
def intervalos_confianza_columna_completa(dataframe, columna_1, columna_2):
    # 12. Contraste de hipótesis adicional
    #     Hipótesis : "Se vendieron más vehículos eléctricos en 2019 que en 2022"
    #     H0: Las ventas de 2019 superan a las de 2022 por mera casualidad
    #     H1: LAs ventas de 2019 superan a las de 2022 realmente.

    datos_1 = dataframe[columna_1]
    datos_2 = dataframe[columna_2]
    print("\n--- CONTRASTE DE HIPÓTESIS SIN BOOTSTRAP ---\n")
    print (f"Media de {columna_1}: {datos_1.mean():6.2f}")
    print(f"Desviación típica de {columna_1}: {datos_1.std():.2f}\n")
    print (f"Media de {columna_2}: {datos_2.mean():6.2f}")
    print(f"Desviación típica de {columna_2}: {datos_2.std():.2f}\n")

    print (f"Intervalo de confianza para {columna_1}: ",[datos_1.mean() - datos_1.std()*1.96/ np.sqrt(len(datos_1)), 
                            datos_1.mean() + datos_1.std()*1.96/ np.sqrt(len(datos_1))])
    print (f"Intervalo de confianza para {columna_2}: ",[datos_2.mean() - datos_2.std()*1.96/ np.sqrt(len(datos_2)), 
                            datos_2.mean() + datos_2.std()*1.96/ np.sqrt(len(datos_2))],"\n")
                            
    print(stats.ttest_ind(datos_1, datos_2, equal_var = False), "\n\n") 
    #Conclusión: Se rechaza H1 y se acepta H0, las ventas de 2019 superan a las de 2022 por mera casualidad.

def meanBootstrap(dataframe, num_datos):
  muestra = [0] * num_datos
  for i in range(num_datos):
    sample = [dataframe[j] for j in np.random.randint(len(dataframe), size=len(dataframe))]
    muestra[i] = np.mean(sample)
  return muestra

def intervalo_confianza_bootstrap(dataframe, columna_1, columna_2):
    
    sample_1 = meanBootstrap(dataframe[columna_1], 200)
    mean_1 = np.mean(sample_1)
    se_1 = np.std(sample_1)

    sample_2 = meanBootstrap(dataframe[columna_2], 200)
    mean_2 = np.mean(sample_2)
    se_2 = np.std(sample_2)

    print("--- INTERVALOS DE CONFIANZA CON BOOTSTRAP ---\n")
    print (f"Media de {columna_1}: {mean_1:6.2f}")
    print(f"Desviación típica de {columna_1}: {se_1:.2f}\n")
    print (f"Media de {columna_2}: {mean_2:6.2f}")
    print(f"Desviación típica de {columna_2}: {se_2:.2f}\n")

    print (f"Intervalo de confianza para {columna_1}: ",[mean_1 - se_1*1.96/ np.sqrt(len(sample_1)), 
                            mean_1 + se_1*1.96/ np.sqrt(len(sample_1))])
    print (f"Intervalo de confianza para {columna_2}: ",[mean_2 - se_1*1.96/ np.sqrt(len(sample_1)), 
                            mean_2 + se_2*1.96/ np.sqrt(len(sample_2))],"\n")
     

if __name__ == "__main__":
    dataframe_original = cargar_datos()
    '''analizar_correlacion(dataframe_original)
    analizar_componentes_principales(dataframe_original)
    df_PIB, datanorm_PIB = normalizacion_PIB(dataframe_original)
    df_Coches_Vendidos, datanorm_Coches_Vendidos = normalización_Vehiculos_Vendidos(dataframe_original)
    matsim_pib, PIB_pca = calcular_matriz_similitud(datanorm_PIB, "matriz_similitud_PIB")
    matsim_coches_vendidos, Coches_Vendidos_pca  = calcular_matriz_similitud(datanorm_Coches_Vendidos, "matriz_similitud_Vehiculos_Vendidos")
    clustering_jerarquico(df_PIB, datanorm_PIB, matsim_pib, PIB_pca, "clustering_jerarquico_PIB")
    clustering_jerarquico(df_Coches_Vendidos, datanorm_Coches_Vendidos, matsim_coches_vendidos, Coches_Vendidos_pca, "clustering_jerarquico_Vehiculos_Vendidos")
    clustering_k_means(df_PIB, PIB_pca, "clustering_k_means_PIB")
    clustering_k_means(df_Coches_Vendidos, Coches_Vendidos_pca, "clustering_k_means_Vehiculos_Vendidos")
    clustering_probabilistico(df_PIB, PIB_pca, "clustering_probabilistico_PIB") 
    clustering_probabilistico(df_Coches_Vendidos, Coches_Vendidos_pca, "clustering_probabilistico_Vehiculos_Vendidos")
    '''
    intervalos_confianza_columna_completa(dataframe_original, "CochesVendidos_2019", "CochesVendidos_2022")
    #intervalo_confianza_bootstrap(dataframe_original, "CochesVendidos_2019", "CochesVendidos_2022")
    