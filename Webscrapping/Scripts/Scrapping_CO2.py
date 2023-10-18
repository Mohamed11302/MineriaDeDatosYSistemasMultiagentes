import requests
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs

def main():
    url="https://edgar.jrc.ec.europa.eu/booklet/EDGARv7.0_FT2021_fossil_CO2_booklet_2022.xlsx"
    r = requests.get(url)
    imprimirxlsx(r.content)


def imprimirxlsx(data):
    with open('../DataSets/[RAW]data_CO2.xlsx', 'wb') as xlsx:
        xlsx.write(data)

if __name__ == '__main__':
    main()