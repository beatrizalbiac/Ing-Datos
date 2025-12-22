import os
import pandas as pd

inpath = "./downloads"
outpath = "./processed"

if not os.path.exists(outpath):
    os.makedirs(outpath)
    print("folder created")

dataframes = {}

dfs = [f for f in os.listdir(inpath) if f.endswith(".csv")] 
for i in dfs:
    csv_path = os.path.join(inpath, i)
    df = pd.read_csv(csv_path, encoding="latin1")
    print(f"{i}:\n{df.isnull().sum()}\n")
    
    # store in dictionary with filename as key
    dataframes[i] = df

# FOR STANDARIZING THE COLUMNS:
target = ["trip_id", "start_time", "end_time", "bikeid", "tripduration",
       "from_station_id", "from_station_name", "to_station_id",
       "to_station_name", "usertype", "gender", "birthyear"]

map_2019_Q2 = {
    "01 - Rental Details Rental ID": "trip_id",
    "01 - Rental Details Local Start Time": "start_time",
    "01 - Rental Details Local End Time": "end_time",
    "01 - Rental Details Bike ID": "bikeid",
    "01 - Rental Details Duration In Seconds Uncapped": "tripduration",
    "03 - Rental Start Station ID": "from_station_id",
    "03 - Rental Start Station Name": "from_station_name",
    "02 - Rental End Station ID": "to_station_id",
    "02 - Rental End Station Name": "to_station_name",
    "User Type": "usertype",
    "Member Gender": "gender",
    "05 - Member Details Member Birthday Year": "birthyear"
}

dataframes["Divvy_Trips_2019_Q2.csv"] = dataframes["Divvy_Trips_2019_Q2.csv"].rename(columns=map_2019_Q2)
print(f"Divvy_Trips_2019_Q2.csv: \n{dataframes["Divvy_Trips_2019_Q2.csv"].head()}\n")

map_2020_Q1 = {
    "ride_id": "trip_id",
    "started_at": "start_time",
    "ended_at": "end_time",
    "start_station_id": "from_station_id",
    "start_station_name": "from_station_name",
    "end_station_id": "to_station_id",
    "end_station_name": "to_station_name",
    "member_casual": "usertype"
}

df = dataframes["Divvy_Trips_2020_Q1.csv"] # so it's easier to call it, just for this bit
df = df.rename(columns=map_2020_Q1)

for i in target:
    if i not in df.columns:
        df[i] = pd.NA

df = df[target]

print(f"\nDivvy_Trips_2020_Q1.csv:\n{df.head()}\n")

# calculate tripduration
df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce")
df["end_time"]   = pd.to_datetime(df["end_time"], errors="coerce")
df["tripduration"] = (df["end_time"] - df["start_time"]).dt.total_seconds()

dataframes["Divvy_Trips_2020_Q1.csv"] = df

# reasign usertype
print(dataframes["Divvy_Trips_2018_Q4.csv"].groupby(["usertype"])["usertype"].count())
print("\n")
print(dataframes["Divvy_Trips_2020_Q1.csv"].groupby(["usertype"])["usertype"].count())

dataframes["Divvy_Trips_2020_Q1.csv"]["usertype"] = dataframes["Divvy_Trips_2020_Q1.csv"]["usertype"].replace({
    "casual": "Customer",
    "member": "Subscriber"
})

print("\n")
print(dataframes["Divvy_Trips_2020_Q1.csv"].head())

print("\nFinal processed dfs:\n")
for i in dataframes:
    # to erase the "," that appear in some tripdurations
    if "tripduration" in dataframes[i].columns:
        dataframes[i]["tripduration"] = (
            dataframes[i]["tripduration"]
            .astype(str)
            .str.replace(",", "", regex=False)
        )
        dataframes[i]["tripduration"] = pd.to_numeric(dataframes[i]["tripduration"], errors="coerce").astype("Int64") # they're always .0 so I can make them ints

        # to fix some floats that shouldn't be floats
        dataframes[i]["birthyear"] = pd.to_numeric(dataframes[i]["birthyear"], errors="coerce").astype("Int64")
        dataframes[i]["to_station_id"] = pd.to_numeric(dataframes[i]["to_station_id"], errors="coerce").astype("Int64")

        dataframes[i].to_csv(os.path.join(outpath, i), index=False) # saves the "clean" dataframes to the new folder

        print(f"{i}:\n{dataframes[i].head()}\n")

# CALCULATE THE MEANS:
print("\nMean per quarter:")
means = []

for i in dataframes:
    df = dataframes[i]
    quarter = i.split("Divvy_Trips_")[1].split(".csv")[0] # so I can take just the "quarter" part (like 2020-Q1 etc)

    mean = df["tripduration"].mean() # there's no nulls so it's fine like this
    means.append({"quarter": quarter, "mean(s)": mean})

summary = pd.DataFrame(means)
summary.to_csv(os.path.join(outpath, "mean-per-quarter.csv"), index=False) # it's kinda ambiguous as what to do w this, so I just saved it to a csv just in case

print(summary)

    