import kaggle as kg

def main():
    kg.api.authenticate()

    dataset_name = 'geoffnel/evs-one-electric-vehicle-dataset'
    kg.api.dataset_download_files(dataset_name, path='../DataSets', unzip=True)

if __name__ == '__main__':
    main()