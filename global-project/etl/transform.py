import pandas as pd
import ast

df_pokemon = pd.read_csv('db/data/raw/pokemon_raw.csv', sep=';')
df_moves = pd.read_csv('db/data/raw/move_raw.csv')

# I'll parse the columns that are saved as lists
df_pokemon["Types"] = df_pokemon["Types"].apply(ast.literal_eval)
df_pokemon["Abilities"] = df_pokemon["Abilities"].apply(ast.literal_eval)
df_pokemon["Moves"] = df_pokemon["Moves"].apply(ast.literal_eval)
df_pokemon["Next Evolution(s)"] = df_pokemon["Next Evolution(s)"].apply(ast.literal_eval)

# to fix the - vs ' thing so it's the same accross all data 
df_pokemon["Moves"] = df_pokemon["Moves"].apply(
    lambda moves: [m.replace("'", "-") for m in moves]
)

df_pokemon['total_stats'] = df_pokemon[['HP', 'Attack', 'Defense', 'Special Attack', 'Special Defense', 'Speed']].sum(axis=1)

df_moves["Contest"] = df_moves["Contest"].replace("???", "") # so the values are more intuitive

df_moves["Power"] = pd.to_numeric(df_moves["Power"], errors="coerce").astype("Int64")
df_moves["Accuracy"] = pd.to_numeric(df_moves["Accuracy"], errors="coerce").astype("Int64")

df_pokemon.to_csv('db/data/processed/pokemon_clean.csv', index=False)
df_moves.to_csv('db/data/processed/moves_clean.csv', index=False)

print("transformed")