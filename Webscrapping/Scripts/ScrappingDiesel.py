import requests
import csv
from bs4 import BeautifulSoup as bs

def main():
    url = "https://datosmacro.expansion.com/energia/precios-gasolina-diesel-calefaccion"

    userAgent = {'User-agent': 'Mozilla/5.0'}
    r = requests.get(url=url,headers=userAgent)
    soup = bs(r.content, "html.parser")

    table = soup.find_all(class_='table')
    
    data = []

    for row in table:
        # Procesa cada fila y extrae los datos que necesitas
        columns = row.find_all('td')
        if len(columns) >= 3:  # Asegúrate de que haya suficientes columnas
            country = columns[0].text.strip()
            last = columns[1].text.strip()
            
            previous = columns[3].text.strip()
            # Agrega los datos a la lista
            data.append(str(country)+";"+str(last)+";" +str(previous))

    
    # Escribe los datos en un archivo CSV
    with open('../DataSets/gasDie_prices.csv', 'w', newline='') as csvfile:
        print(data)
        csv_writer = csv.writer(csvfile)
        # Escribe el encabezado
        csv_writer.writerow(["Country ; Gas 95 ; Diesel"])
        # Escribe los datos
        csv_writer.writerows(data)
    


if __name__ == '__main__':
    main()