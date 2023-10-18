from bs4 import BeautifulSoup
import csv

def main():
    with open('../HTML/Nivel de Estudios/Most Educated Countries 2023.html', 'rb') as archivo:
        contenido = archivo.read()
    data_matrix = []
    data_labels = []
    soup = BeautifulSoup(contenido, "html.parser")
    classes = "has-tooltip-bottom flex flex-nowrap items-center whitespace-nowrap font-semibold text-black first-of-type:self-start"
    elements = soup.find_all(class_=classes)
    for element in elements:
        data_labels.append(element.get_text())
    data_matrix.append(data_labels)


    class_name = "odd:bg-white even:bg-gray-100 null"
    rows = soup.find_all('tr', class_=class_name)
    for row in rows:
        a_tag = row.find('a')
        td_tags = row.find_all('td')
        row_data = []
        
        if a_tag:
            row_data.append(a_tag.get_text())
        
        for td in td_tags:
            row_data.append(td.get_text())
        data_matrix.append(row_data)

    
    ruta_destino = '../DataSets/[RAW]level_of_studies.csv'
    with open(ruta_destino, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in data_matrix:
            writer.writerow(row)

if __name__ == '__main__':
    print("Executing Scraping_Estudios.py")
    main()