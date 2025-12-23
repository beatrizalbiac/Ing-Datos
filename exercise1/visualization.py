import pandas as pd
import matplotlib.pyplot as plt
import os

# THIS IS A FILE JUST FOR SOME SIMPLE VISUALIZATIONS. I CREATED A NEW ONE JUST SO I DON'T CLUTTER THE PROCESSED.PY
# for the graphs I found that until u close one the other doesn't open, so take that into acount. If it still doesn't work u might have to dowload it to a directory by coping the next line b4 each plt.show():
# plt.savefig(os.path.join(path, "NAME.png"), dpi=200)
# u have to change the "NAME" to the name u want the pic to have

path = "./processed"

files = [f for f in os.listdir(path) if f.startswith("Divvy_Trips_") and f.endswith(".csv")]
dfs = []
for f in files:
    df = pd.read_csv(os.path.join(path, f), encoding="latin1")

    quarter = f.split("Divvy_Trips_")[1].split(".csv")[0]  # one string
    df["quarter"] = quarter

    dfs.append(df)

df = pd.concat(dfs, ignore_index=True)
# print(df.head())

# mean duration per quarter but in a line graph
means = df.groupby("quarter")["tripduration"].mean().sort_index()

plt.figure()
plt.plot(means.index, means.values, marker="*", ms=10,color="lightskyblue")
plt.ylabel("mean trip duration(s)")
plt.xlabel("quarter")
plt.title("mean trip duration by quarter")
plt.tight_layout()
plt.show()

# top 10 starting stations
top10s = df["from_station_name"].dropna().value_counts().head(10)

plt.figure()
top10s.sort_values().plot(kind="barh", color="lightskyblue")
plt.xlabel("nº of trips")
plt.ylabel("station")
plt.title("top 10 start stations")
plt.tight_layout()
plt.show()

# top 10 ending stations
top10e = df["to_station_name"].dropna().value_counts().head(10)

plt.figure()
top10e.sort_values().plot(kind="barh", color="lightskyblue")
plt.xlabel("nº of trips")
plt.ylabel("station")
plt.title("top 10 ending stations")
plt.tight_layout()
plt.show()

# gender distribution
gender = df["gender"].dropna().value_counts() # i wished to also show smth like "unknown" but the last quarter directly doesn't have any value in the genders, and there's just way to many nulls.

plt.figure()
plt.pie(gender.values, labels=gender.index, autopct="%1.1f%%", startangle=90, colors=["lightskyblue","lightpink"])
plt.title("trips by gender")
plt.tight_layout()
plt.show()
