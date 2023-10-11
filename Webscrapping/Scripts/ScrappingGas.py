import requests
import csv
from bs4 import BeautifulSoup as bs

def main():
    url = "https://tradingeconomics.com/country-list/gasoline-prices?continent=world"

    userAgent = {'User-agent': 'Mozilla/5.0'}
    r = requests.get(url=url,headers=userAgent)
    soup = bs(r.content, "html.parser")

    table = soup.find_all(class_='datatable-row-alternating') + soup.find_all(class_='datatable-row')
    
    data = []

    for row in table:
        # Procesa cada fila y extrae los datos que necesitas
        columns = row.find_all('td')
        if len(columns) >= 3:  # Asegúrate de que haya suficientes columnas
            country = columns[0].text.strip()
            last = columns[1].text.strip()
            previous = columns[2].text.strip()
            date = columns[3].text.strip()

            # Agrega los datos a la lista
            data.append([str(country)+";"+str(last)+";" +str(previous)+";"+str(date)])

    # Escribe los datos en un archivo CSV
    with open('../DataSets/gasoline_prices.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter= ',')
        # Escribe el encabezado
        csv_writer.writerow(["Country ; last ; previous ; Date"])
        # Escribe los datos
        csv_writer.writerows(data)
    


if __name__ == '__main__':
    main()