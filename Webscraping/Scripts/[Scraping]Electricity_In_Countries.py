import requests
import pandas
from io import BytesIO

def main():

    url = "https://ember-climate.org/app/uploads/2022/09/european_wholesale_electricity_price_data_monthly-5.csv"

    r = requests.get(url)

    df = pandas.read_csv(BytesIO(r.content))

    print(df)

    df.to_csv("DataSets/[RAW]electricity_in_all_countries.csv", index=False)


if __name__ == '__main__':
    main()