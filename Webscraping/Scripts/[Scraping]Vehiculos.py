import kaggle 
import os

def main():
    import os
    kaggle_data={"username":"jorgevdeinglaterra","key":"07ae4ac606fb20ee99e7318665c78a16"}
    os.environ['KAGGLE_USERNAME']=kaggle_data["username"]
    os.environ['KAGGLE_KEY']=kaggle_data["key"]
    # Autentica con el archivo "kaggle.json" en la ubicación correcta
    kaggle.api.authenticate()

    dataset_name = 'geoffnel/evs-one-electric-vehicle-dataset'
    kaggle.api.dataset_download_files(dataset_name, path='DataSets', unzip=True)
    
    try:
        os.remove("DataSets/[RAW]electric_car_data_clean.csv")
    except Exception as e:
        print(e)

    os.rename("DataSets/ElectricCarData_Clean.csv", "DataSets/[RAW]electric_car_data_clean.csv")
    os.remove("DataSets/ElectricCarData_Norm.csv")

if __name__ == '__main__':
    print("Executing [Scraping]Vehiculos.py")
    main()
