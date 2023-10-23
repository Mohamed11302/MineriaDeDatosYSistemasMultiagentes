import requests
import csv
from bs4 import BeautifulSoup as bs

def main():
    url = "https://datosmacro.expansion.com/energia/precios-gasolina-diesel-calefaccion"

    dataTotal =[]
    userAgent = {'User-agent': 'Mozilla/5.0'}
    r = requests.get(url=url,headers=userAgent)
    soup = bs(r.content, "html.parser")

    table = soup.find_all(class_='table')

    for row in table:
        # Procesa cada fila y extrae los datos que necesitas
        columns = row.find_all('td')
        for column in columns:
            country= column.text.strip()
            if '[+]' in country:
                href=column.find("a")["href"]
                url1=url+href[44:]
                dataTotal.append(anterior(url1,[country]))
                imprimirCSV(dataTotal)

def anterior(url,dataTotal):
    for i in range(9):
        r1 = requests.get(url)
        soup = bs(r1.content, "html.parser")
        ano=soup.find(class_ = "table tabledat table-striped table-condensed table-hover")
        #Busqueda tabla
        table = (soup.find_all(class_ = "table"))
        column = (table[0].find_all('td')) #Lo usaremos como precio medio
        dataTotal.append(column[1].text.strip())
        dataTotal.append(column[3].text.strip())
        url=ano.find("a")["href"]
    return dataTotal

def imprimirCSV(data):
    with open('../DataSets/[RAW]gasoline_Diesel_prices.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile,delimiter=';')
        anos=[""]
        gasDie=["País"]
        for i in range(9):
            anos.append(2023-i)
            anos.append("")
            gasDie.append("Gasolina")
            gasDie.append("Diesel")
        csv_writer.writerow(anos)
        csv_writer.writerow(gasDie)
        for i in data:
            csv_writer.writerows([i])

if __name__ == '__main__':
    print("Executing Scrapping_Diesel_Gasoline.py")
    main()