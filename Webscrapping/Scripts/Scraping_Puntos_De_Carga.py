import requests
from bs4 import BeautifulSoup

def main():
    with open('HTML\Puntos De Carga\Global EV Data Explorer – Data Tools - IEA.html', 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()

    soup = BeautifulSoup(contenido, "html.parser")
    buton = soup.find(class_ = 'a-button a-button--primary')
    enlace_descarga = buton.get('href')
    response = requests.get(enlace_descarga)

    if response.status_code == 200:
        ruta_destino = 'DataSets\Puntos_de_Carga.csv'
        with open(ruta_destino, 'wb') as archivo_csv:
            archivo_csv.write(response.content)

main()