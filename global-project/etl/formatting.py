# this is an "extra" code so the etl main functionality doesn't get cluttered with all the transformations I need to make to be able to load my datasets into the dwh designed
# the "issues" between the datasets have been handled in the transform.py, here I'll just format and/or calculate que columns needed
import pandas as pd

df_pokemon = pd.read_csv('db/data/raw/pokemon.csv')
df_moves = pd.read_csv('db/data/raw/move.csv')

