import pandas as pd
import requests
import io

# ITS THE SAME EXACT CODE AS WHAT'S IN THE EDA NOTEBOOK (but I save the csvs to use them later)

urls = ["https://raw.githubusercontent.com/beatrizalbiac/Ing-Datos-datasets/refs/heads/main/global-project/pokemon-data.csv",
       "https://raw.githubusercontent.com/beatrizalbiac/Ing-Datos-datasets/refs/heads/main/global-project/move-data.csv"]

# this is so they're each saved in their corresponding dataframe, and not just overwrite one df
df_pokemon = None
df_moves = None

for i in urls:
    try:
        print(f"Fetching data from: {i}")
        response = requests.get(i, timeout=10)
    
        print("Data fetched from web source, loading into DataFrame...")

        if "pokemon-data.csv" in i:
            sep = ';'
        elif "move-data.csv" in i:
            sep = ','
        
        df = pd.read_csv(io.StringIO(response.text), sep=sep, on_bad_lines='warn')

        if "pokemon-data.csv" in i:
            df_pokemon = df
        elif "move-data.csv" in i:
            df_moves = df
    
        print(f"retrieval succesfull")
        print(f"status code:{response.status_code}\n")
   
    except Exception as e:
        print(f"error: {e}")
        raise e
    
df_pokemon.to_csv('db/data/raw/pokemon_data.csv', index=False, sep=';')
df_moves.to_csv('db/data/raw/move_data.csv', index=False)