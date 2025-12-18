"""
DATA CLEANING EXERCISE
=====================
Retrieve, explore, and clean an e-commerce customer orders dataset
"""
from datetime import datetime
import pandas as pd
import numpy as np
import requests
import io

print("=" * 70)
print("DATA CLEANING EXERCISE - E-COMMERCE CUSTOMER ORDERS")
print("=" * 70)
print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# ============================================================================
# STEP 1: RETRIEVE DATA FROM WEB SOURCE
# ============================================================================

print("STEP 1: RETRIEVING DATA FROM WEB SOURCE")
print("-" * 70)
 
url = "https://raw.githubusercontent.com/victorbrub/data-engineering-class/refs/heads/main/pre-post_processing/exercise.csv"
 
try:
    print(f"Fetching data from: {url}")
    response = requests.get(url, timeout=10)
 
    # print("Response:", response.text)
   
    print("✓ Data fetched from web source, loading into DataFrame...")
    # print("Response:", response.text)  
    df = pd.read_csv(io .StringIO(response.text),sep=',',on_bad_lines='warn') # the line 1005 is a "bad line" so it doesn't import it
   
    print(f"✓ Data retrieved successfully!")
    print(f"✓ Status Code: {response.status_code}")
    print(f"✓ Rows: {len(df)}, Columns: {len(df.columns)}\n")
    print(df.head())
   
except Exception as e:
    print(f"✗ Error: {e}")
    raise e

df_raw = df.copy()

# ============================================================================
# STEP 2: INITIAL EXPLORATION
# ============================================================================

print("\nSTEP 2: INITIAL DATA EXPLORATION")
print("-" * 70)
print(f"\nDataset Shape: {df.shape}")
print(f"\nColumn Names & Types:\n{df.dtypes}")
print(f"\nFirst 5 Rows:\n{df.head()}")
print(f"\nMissing Values:\n{df.isnull().sum()}")
print(f"\nTotal Missing: {df.isnull().sum().sum()}\n")

# ============================================================================
# STEP 3: IDENTIFY QUALITY ISSUES
# ============================================================================

print("STEP 3: DATA QUALITY ISSUES")
print("-" * 70)
 
print(f"Duplicates: {df.duplicated().sum()}")
print(f"Duplicate OrderIDs: {df['OrderID'].duplicated().sum()}")
 
if df[df.duplicated(subset=['OrderID'], keep=False)].shape[0] > 0:
    print(f"\nDuplicate Records:\n{df[df.duplicated(subset=['OrderID'], keep=False)].sort_values('OrderID')}\n")

# ============================================================================
# STEP 4: DATA CLEANING
# ============================================================================

print("\nSTEP 4: DATA CLEANING")
print("-" * 70)

print("RULES:\n")
print("- CustomerName: Standarize the font (capitals and lowercase letters) -> So the first letter of the name and lastname is capitalized, and the rest is in lowercase\n" \
"- Email: Standarize the font -> so everything's on lowecase\n" \
"- Phone: Erase everything that isn't a number\n" \
"- Country: Standarize it so the same country is refered to with the same format and wording\n" \
"- OrderDate: Standarize it to DD/MM/YYYY so every date has the same format\n" \
"- Quantity: Has to be greater than 0\n" \
"- Price: Has to be greater than 0\n" \
"- CustomerAge: Has to be a number between 1 and 100\n" \
"- OrderStatus: It's already clean and standarized\n")

print("NULLS:\n")
print("- Drop rows with null Quantity or Price\n" \
"- Drop rows with BOTH null Email and Phone\n")

df["CustomerName"] = df["CustomerName"].str.title() # so every name and lastname has the same format. Idrk what to do w antonio tho (he doens't have a lastname)

df["Email"] = df["Email"].str.lower()

df["Phone"] = df["Phone"].str.replace(r"\D", "", regex=True) # it looks at the data and removes anything that isn't a number (-, " ",invalid...), that's what /D does
df["Phone"] = pd.to_numeric(df["Phone"], errors="coerce") # so there's not spaces and NaNs mixed
df["Phone"] = df["Phone"].astype("Int64") # bc it's returned in float, and we want phone numbers (It returns as <NA> instead of NaN bc of smth of pandas)

df["Country"] = df["Country"].str.lower()
print(df["Country"].value_counts())
print("\n")

countries = { # manual mapping bc it's a small sample. It'd be better to limit the users to they can only choose from base options
    "usa": "USA",
    "us": "USA",
    "canada": "Canada",
    "united kingdom": "UK",
    "united states": "USA",
    "uk": "UK",
    "gb": "UK" # bc the name of the country is the UK
}

df["Country"] = df["Country"].map(countries) # to standarize it

df["OrderDate"] = df["OrderDate"].astype("string").str.strip().str.replace("-", "/", regex=False) # bc there is - and / mixed
mask = df["OrderDate"].str.match(r"^\d{4}/\d{2}/\d{2}$") # to standarize YYYY/MM/DD dates
df["OrderDate"] = (
    pd.to_datetime(df["OrderDate"].where(mask), format="%Y/%m/%d", errors="coerce")
    .fillna(pd.to_datetime(df["OrderDate"].where(~mask), dayfirst=False, errors="coerce")) # it implies that every date that isn't YYYY first is MM first (even smth like 04/01) for simplicity
    .dt.strftime("%Y/%m/%d") # the format should be left as YYYY/MM/DD. I'd prefer DD/MM/YYYY but that creates problems later on
)

df.loc[df["Quantity"] <= 0, "Quantity"] = np.nan
df["Quantity"] = df["Quantity"].astype("Int64")

# price ¿drop nulls?

# i'm filtering the "unknown" and "troll" ages.
df["CustomerAge"] = pd.to_numeric(df["CustomerAge"], errors="coerce")
conditions = (df["CustomerAge"] <= 0) | (df["CustomerAge"] > 100)
df.loc[conditions, "CustomerAge"] = np.nan
df["CustomerAge"] = df["CustomerAge"].astype("Int64") # it's so they don't look like floats


# order status is already standardized and clean (it has no nulls)

print(f"\nCleaned dataset snippet:\n{df.head(10)}\n")

print(f"After format cleaning:\n{df.isna().sum()}")

# handle nulls:

df = df.dropna(subset=["Quantity", "Price"])

df = df.dropna(subset=["Email", "Phone"], how="all") # if there were any where both the phone and email where missing it'd drop them

print(f"\nAfter null cleaning:\n{df.isna().sum()}")
print(f"\nFinal shape:{df.shape}")

# ============================================================================
# STEP 5: FINAL VALIDATION
# ============================================================================

print("\nSTEP 5: FINAL VALIDATION")
print("-" * 70)

def validation(df):
    total = len(df)

    # to avoid errors and warnings bc of conflicting types
    email = df["Email"].astype("string")
    country = df["Country"].astype("string")
    age = pd.to_numeric(df["CustomerAge"], errors="coerce")
    order_date = pd.to_datetime(df["OrderDate"], format="%Y/%m/%d", errors="coerce")

    accuracy_mask = age.between(1, 100) # bc ages should be realistic

    completeness_mask = email.notna() & (email.str.strip() != "") # based on the ppt, but not so aplicable bc of the rules i set in place (like that u can have a missing email if u have a valid phone number)

    consistency_mask = country.isin([ # so USA/UK/etc aren't written in multiple ways
        "USA", "Canada", "UK",
        "usa", "us", "united states",
        "united kingdom", "uk", "gb"
    ])

    validity_mask = email.notna() & email.str.contains("@", na=False) # to check format

    uniqueness_mask = ~df["OrderID"].duplicated(keep=False) # unique id. the ~ is to get everithing but the variable after the symbol

    timeliness_mask = order_date.dt.year == 2023 # kinda picked by hand (just following the csv data kinda)

    results = { # % rows that pass each dimension test
        "Accuracy": accuracy_mask.sum() / total,
        "Completeness": completeness_mask.sum() / total,
        "Consistency": consistency_mask.sum() / total,
        "Validity": validity_mask.sum() / total,
        "Uniqueness": uniqueness_mask.sum() / total,
        "Timeliness": timeliness_mask.sum() / total,
    }

    for k, v in results.items(): # prints the percentages
        print(f"{k:12s}: {v:.2%}")

    print("\n")
    return results


raw_results = validation(df_raw)
clean_results = validation(df)

print("\nComparison:") # raw vs cleaned side by side
print(f"{'':12s}  {'RAW':>8s}  {'CLEAN':>8s}")
for dim in raw_results:
    print(f"{dim:12s}: {raw_results[dim]:>8.2%}  {clean_results[dim]:>8.2%}")

# ============================================================================
# STEP 6: SAVE CLEANED DATA
# ============================================================================

print("\nSTEP 6: SAVE DATASET")
print("-" * 70)

df.to_csv('dfcleaned.csv', index=False)
print("dataset saved")

