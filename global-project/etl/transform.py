import pandas as pd
import ast

df_pokemon = pd.read_csv('db/data/raw/pokemon_data.csv', sep=';')
df_moves = pd.read_csv('db/data/raw/move_data.csv')

# I'll parse the columns that are saved as lists
df_pokemon['Types_parsed'] = df_pokemon['Types'].apply(lambda x: ast.literal_eval(x))
df_pokemon['Abilities_parsed'] = df_pokemon['Abilities'].apply(lambda x: ast.literal_eval(x))
df_pokemon['Moves_parsed'] = df_pokemon['Moves'].apply(lambda x: ast.literal_eval(x))

# to fix the - vs ' thing so it's the same accross all data
fixes = {"Forest-s Curse": "Forest's Curse", "King-s Shield": "King's Shield", 
             "Land-s Wrath": "Land's Wrath", "Nature-s Madness": "Nature's Madness"}
df_pokemon['Moves_parsed'] = df_pokemon['Moves_parsed'].apply(lambda moves: [fixes.get(m, m) for m in moves])

df_pokemon['total_stats'] = df_pokemon[['HP', 'Attack', 'Defense', 'Special Attack', 'Special Defense', 'Speed']].sum(axis=1)

df_pokemon.to_csv('db/data/processed/pokemon.csv', index=False)
df_moves.to_csv('db/data/processed/moves.csv', index=False)

print("transformed")