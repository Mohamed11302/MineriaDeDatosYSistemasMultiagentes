import requests
import csv
from bs4 import BeautifulSoup as bs
import pandas as pd
import os

def main():
    url="https://edgar.jrc.ec.europa.eu/booklet/EDGARv7.0_FT2021_fossil_CO2_booklet_2022.xlsx"
    r = requests.get(url)
    imprimirxlsx(r.content)


def imprimirxlsx(data):
    with open('DataSets/[RAW]CO2_data.xlsx', 'wb') as xlsx:
        xlsx.write(data)
    df = pd.read_excel('DataSets/[RAW]CO2_data.xlsx', sheet_name="fossil_CO2_totals_by_country")
    df.to_csv("DataSets/[RAW]CO2_data.csv", index=False) 
    os.remove('DataSets/[RAW]CO2_data.xlsx')
    

if __name__ == '__main__':
    print("Executing Scrapping_CO2.py")
    main()