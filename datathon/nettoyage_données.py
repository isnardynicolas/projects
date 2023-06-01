# -*- coding: utf-8 -*-
"""nettoyage_données.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YQH9-OKnAs3eS4Duco8Z6a8VVmpus8j3
"""

import pandas as pd
import numpy as np

df = pd.read_csv("https://gitlab.com/isnardynicolas/wcs_import/-/raw/main/tracks_features.csv")

# On récupère les types des valeurs des colonnes du data frame
def get_unique_column_types(df, col_name):
    """
    Returns a list of the unique types of values in the specified column of the DataFrame.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing the column.
    col_name (str): The name of the column to check.

    Returns:
    list: A list of the unique types of values in the column.
    """
    unique_types = df[col_name].apply(type).unique()
    return unique_types

# List of column names in the DataFrame
column_names = df.columns.tolist()

# Iterate over each column name and print the unique types of values in that column
for col_name in column_names:
    types = get_unique_column_types(df, col_name)
    print(f"{col_name}' = {types}")

df.nunique()

# On change une valeur abérante de la colonne release_date
df.loc[df.release_date == "0000", "release_date"] = "2018-09-04"

# On change une valeur abérante de la colonne year
df.loc[df.year == 0, "year"] = 2018

# Vérification 
print((df.release_date == "0000").sum())
print((df.year == 0).sum())

# Conversion de la colonne year en date_time
df.year = pd.to_datetime(df.year, format=  "%Y")

## Creation d'une copie pour éviter les bétises
df_copy = df.copy()

# On sélectionne les colonnes pertinantes
df_copy = df_copy[['id', 'name', 'album', 'album_id', 'artists', 'artist_ids',
       'explicit', 'danceability', 'energy',
       'loudness', 'speechiness',
       'valence', 'tempo', 'duration_ms',
       'year']]

# Création d'un masque des durées de musique supérieure à 10 min 
mask = df_copy.duration_ms > 600000
# On ne garde que les lignes qui ne sont pas dans le masque
df_copy = df_copy[~mask]

def nettoyage(artist):
    return artist.replace("[", "").replace("]", "")

df_copy.artists = df_copy.artists.apply(nettoyage)

df_copy

# On exporte au format csv
df_copy.to_csv("/content/sample_data/datathonbbq.csv")

df_copy.loc[(df.name.str.contains("Thunder"))]