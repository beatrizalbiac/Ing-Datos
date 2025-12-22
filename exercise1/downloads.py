import os
import requests
from zipfile import ZipFile

url=[
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip" # it's wrong it should be 2020
]

path = "./downloads"
if not os.path.exists(path):
    os.makedirs(path)
    print('folder created')

dfs = []
for i in url:
    response = requests.get(i)
    filename = os.path.basename(i)
    fpath = os.path.join(path, filename)
    

    if response.status_code == 200:
        with open(fpath, 'wb') as file:
            file.write(response.content)
        print('File downloaded successfully')

        try:
            with ZipFile(fpath, 'r') as zip_ref:
                zip_ref.extractall(path)
                csv_files = [name for name in zip_ref.namelist()if name.endswith(".csv") and "__MACOSX" not in name]
                dfs.extend(csv_files)
            print(f'{filename} extracted successfully')
        except Exception as e:
            print(f'Failed to extract {filename}: {e}')
    
        os.remove(fpath)
        print('.zip deleted')

    else:
        print('Failed to download file')