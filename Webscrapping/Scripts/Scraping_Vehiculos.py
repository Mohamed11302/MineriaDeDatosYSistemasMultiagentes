import kaggle as kg
import os

def main():
    kg.api.authenticate()

    dataset_name = 'geoffnel/evs-one-electric-vehicle-dataset'
    kg.api.dataset_download_files(dataset_name, path='../DataSets', unzip=True)
    os.rename("../DataSets/ElectricCarData_Clean.csv", "../DataSets/[RAW]electric_car_data_clean.csv")
    os.rename("../DataSets/ElectricCarData_Norm.csv", "../DataSets/[RAW]electric_car_data_norm.csv")

if __name__ == '__main__':
    print("Executing Scraping_Vehiculos.py")
    main()