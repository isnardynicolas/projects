import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

# Logo et titre
logo = "https://static.vecteezy.com/ti/vecteur-libre/p3/552996-icone-de-vecteur-bbq-grill-gratuit-vectoriel.jpg"
st.sidebar.image(logo, use_column_width=True)
st.sidebar.markdown("<h1 style='text-align: center;'>Data Grill Masters</h1>", unsafe_allow_html=True)

df = pd.read_csv("/Users/isnardynicolas/Desktop/PROJETS/datathon/datathonbbq.csv")

df.drop('Unnamed: 0', axis=1, inplace=True)

st.markdown("<center><h1>DashBoard</h1></center>", unsafe_allow_html=True)
st.write("")

# Viz 1: tableau des caractéristiques pour chaque moment du barbec
df_google_sheet = pd.read_csv("/Users/isnardynicolas/Desktop/PROJETS/datathon/tableau_csv - Feuille 1.csv")

df_google_sheet.rename(columns={"Unnamed: 0": "caracteristics"}, inplace=True)

st.subheader("Tableau des caractéristiques musicales")
st.table(df_google_sheet)
st.write("")
st.write("")

# Viz 2: heatmap des corrélations entre les caractéristiques
sns.set_palette("coolwarm")
heatmap_caract = sns.heatmap(data = df.corr(), cmap="coolwarm")
heatmap_caract = heatmap_caract.set_title("heatmap des corrélations entre nos caractéristiques")

heatmap_caract, ax = plt.subplots()
sns.heatmap(data = df.corr(), cmap="coolwarm", ax=ax)
ax.set_title("Heatmap des corrélations entre nos caractéristiques")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

st.subheader("Vérification des surreprésentations")
st.pyplot(heatmap_caract)
st.write("")
st.write("")

df.reset_index(drop=True, inplace=True)


# ML création des playlists grâce aux plus proches voisins
aperitif = [0.5, 0.4, -5, 0.7, 0.2]
repas = [0.3, 0.3, -10, 0.7, 0.4]
soiree = [0.8, 0.8, 0, 0.4, 0.9]
after = [0.9, 0.9, 0, 0.2, 0.8]
list_time = [aperitif, repas, soiree, after]

X = df.select_dtypes("number").drop(["duration_ms", "tempo"], axis = 1)

scaler = StandardScaler().fit(X)
X_scaled = scaler.transform(X)

distanceKNN = NearestNeighbors(n_neighbors=40).fit(X_scaled)

df_playlist = pd.DataFrame(columns = ["Titre", "Artist"])

dfs = {}
for i in list_time:
    neighbors = distanceKNN.kneighbors([i])
    df_playlist = pd.DataFrame({"Titre": df.iloc[neighbors[1][0], 1], "Artists": df.iloc[neighbors[1][0], 4]})
    df_playlist = df_playlist.reset_index(drop = True)
    df_playlist.index = df_playlist.index + 1
    dfs[f"playlist_{i}"] = df_playlist

st.subheader("Playlists")
time = st.selectbox(label = "Choissisez votre playlist: ", options = ["Apéritif", "Repas", "Soirée", "After", "Créer une playlist à partir d'une musique"])

if time == "Créer une playlist à partir d'une musique":
    choix_perso = st.text_input("Entrez une musique (titre exact): ").lower()
    choix_perso = ' '.join(word.capitalize() for word in choix_perso.split())
    st.write(choix_perso)
    if choix_perso != "":
        neighbors = distanceKNN.kneighbors(df.loc[df.name == choix_perso, X.columns])
        playlist_perso = pd.DataFrame({"Titre": df.iloc[neighbors[1][0], 1], "Artists": df.iloc[neighbors[1][0], 4]})
        playlist_perso = playlist_perso.reset_index(drop = True)
        playlist_perso.index = playlist_perso.index + 1
        st.markdown(f"Voici une playlist qui pourrait vous plaire:")
        st.table(playlist_perso)

else:
    def choix(time):
        if time == "Apéritif":
            return aperitif
        elif time == "Repas":
            return repas
        elif time == "Soiree":
            return soiree
        elif time == "After":
            return after

    st.table(dfs[f"playlist_{choix(time)}"])