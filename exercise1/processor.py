import os
import pandas as pd

inpath = "./downloads"

dataframes = {}

dfs = [f for f in os.listdir(inpath) if f.endswith(".csv")] #erase when not testing
for i in dfs:
    csv_path = os.path.join(inpath, i)
    df = pd.read_csv(csv_path, encoding="latin1")
    # print(f"{i}:\n{df.isnull().sum()}\n")
    
    # store in dictionary with filename as key
    dataframes[i] = df

# the name of the colums varies from quarter to quarter, that needs to be standarized
print("Dataframes with different column names:\n")
for i in dataframes:
    if not dataframes[i].columns.equals(dataframes['Divvy_Trips_2018_Q4.csv'].columns): # I chose the csv 2018-Q4 as while checking the nulls it was identified as one of the csvs that have the same column names (the majority)
        print(i)
        print(dataframes[i].columns)
        print("\n")

# # STANDARIZING THE COLUMNS:
# print(f"The target columns:\n{dataframes['Divvy_Trips_2018_Q4.csv'].columns}")

target = ['trip_id', 'start_time', 'end_time', 'bikeid', 'tripduration',
       'from_station_id', 'from_station_name', 'to_station_id',
       'to_station_name', 'usertype', 'gender', 'birthyear']

map_2019_Q2 = {
    '01 - Rental Details Rental ID': 'trip_id',
    '01 - Rental Details Local Start Time': 'start_time',
    '01 - Rental Details Local End Time': 'end_time',
    '01 - Rental Details Bike ID': 'bikeid',
    '01 - Rental Details Duration In Seconds Uncapped': 'tripduration',
    '03 - Rental Start Station ID': 'from_station_id',
    '03 - Rental Start Station Name': 'from_station_name',
    '02 - Rental End Station ID': 'to_station_id',
    '02 - Rental End Station Name': 'to_station_name',
    'User Type': 'usertype',
    'Member Gender': 'gender',
    '05 - Member Details Member Birthday Year': 'birthyear'
}

dataframes['Divvy_Trips_2019_Q2.csv'] = dataframes['Divvy_Trips_2019_Q2.csv'].rename(columns=map_2019_Q2)
print(f"Divvy_Trips_2019_Q2.csv: \n{dataframes['Divvy_Trips_2019_Q2.csv'].head()}\n")

map_2020_Q1 = {
    'ride_id': 'trip_id',
    'started_at': 'start_time',
    'ended_at': 'end_time',
    'start_station_id': 'from_station_id',
    'start_station_name': 'from_station_name',
    'end_station_id': 'to_station_id',
    'end_station_name': 'to_station_name',
    'member_casual': 'usertype'
}

df = dataframes['Divvy_Trips_2020_Q1.csv'] # so it's easier to call it, just for this bit

df = df.rename(columns=map_2020_Q1)

for i in target:
    if i not in df.columns:
        df[i] = pd.NA

df = df[target]

print(f"\nDivvy_Trips_2019_Q2.csv:\n{df.head()}\n")

# calculate tripduration
df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce")
df["end_time"]   = pd.to_datetime(df["end_time"], errors="coerce")
df["tripduration"] = (df["end_time"] - df["start_time"]).dt.total_seconds()

# HAY QUE DETERMINAR MEJOR QUE SE ESTÁ IMPRIMIENDO Y CUANDO X PANTALLA :)
print(df.head())
print("\n")

dataframes['Divvy_Trips_2020_Q1.csv'] = df

# reasign usertype
print(dataframes['Divvy_Trips_2018_Q4.csv'].groupby(['usertype'])['usertype'].count())
print("\n")
print(dataframes['Divvy_Trips_2020_Q1.csv'].groupby(['usertype'])['usertype'].count())

dataframes['Divvy_Trips_2020_Q1.csv']["usertype"] = dataframes['Divvy_Trips_2020_Q1.csv']["usertype"].replace({
    "casual": "Customer",
    "member": "Subscriber"
})

print("\n")
print(dataframes['Divvy_Trips_2020_Q1.csv'].groupby(['usertype'])['usertype'].count())
print("\n")
print(dataframes['Divvy_Trips_2020_Q1.csv'].head())





# 2020-Q1 -> has different columns
# 2019-Q2 -> has different columns
# Divvy_Trips_2018_Q4.csv 
# Divvy_Trips_2019_Q1.csv 
# Divvy_Trips_2019_Q2.csv 
# Divvy_Trips_2019_Q3.csv 
# Divvy_Trips_2019_Q4.csv 
# Divvy_Trips_2020_Q1.csv