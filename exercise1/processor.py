import os
import pandas

inpath = "./downloads"

dataframes = {}

dfs = [f for f in os.listdir(inpath) if f.endswith(".csv")] #erase when not testing
for i in dfs:
    csv_path = os.path.join(inpath, i)
    df = pd.read_csv(csv_path, encoding="latin1")
    print(f"{i}:\n{df.isnull().sum()}\n")
    
    # store in dictionary with filename as key
    dataframes[i] = df

print(dataframes.keys())
print('\n')
print(dataframes['Divvy_Trips_2018_Q4.csv'].columns)
print('\n')
print(dataframes['Divvy_Trips_2020_Q1.csv'].columns)
print('\n')
print(dataframes['Divvy_Trips_2019_Q2.csv'].columns)

# for i in dataframes:
#     if dataframes[i].columns != dataframes['Divvy_Trips_2018_Q4.csv'].columns:
#         pass



# 2020-Q1 -> has different columns
# 2019-Q2 -> has different columns
# Divvy_Trips_2018_Q4.csv 
# Divvy_Trips_2019_Q1.csv 
# Divvy_Trips_2019_Q2.csv 
# Divvy_Trips_2019_Q3.csv 
# Divvy_Trips_2019_Q4.csv 
# Divvy_Trips_2020_Q1.csv