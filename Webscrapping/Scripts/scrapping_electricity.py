import requests
import io
import zipfile
import os


def main():

    url = "https://ember-climate.org/app/uploads/2022/09/european_wholesale_electricity_price_data_hourly-2.zip"

    csv_folder = "electricity_csv"
    os.makedirs(csv_folder, exist_ok=True)

    r = requests.get(url)

    with zipfile.ZipFile(io.BytesIO(r.content), "r") as zip_zip:
        
        for file in zip_zip.infolist():
            #Just .csv files saved
            if file.filename.endswith(".csv"):
                csv_content = zip_zip.read(file.filename)
                
                #If there are folders inside another folder
                sub_dir = os.path.dirname(file.filename)
                if sub_dir:
                    os.makedirs(os.path.join(csv_folder, sub_dir), exist_ok=True)
                
                with open(os.path.join(csv_folder, file.filename), "wb") as csv_file:
                    csv_file.write(csv_content)

if __name__ == "__main__":
    main()