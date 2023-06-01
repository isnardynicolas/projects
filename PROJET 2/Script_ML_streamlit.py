import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import streamlit as st

# Importation des bibliothèques requises

# Chargement des données à partir d'un fichier CSV
df_all = pd.read_csv('https://raw.githubusercontent.com/isnardynicolas/streamlit/main/film_oriented2.csv')


# Configuration de la barre latérale
st.sidebar.markdown("<h1 style='text-align: center;'>Système de recommandation de films des 70's - 90's 🎬</h1>", unsafe_allow_html=True)
st.sidebar.write(" ", unsafe_allow_html=True)
st.sidebar.write(" ", unsafe_allow_html=True)
st.sidebar.write(" ", unsafe_allow_html=True)
st.sidebar.write(" ", unsafe_allow_html=True)
st.sidebar.write(" ", unsafe_allow_html=True)
st.sidebar.write(" ", unsafe_allow_html=True)
st.sidebar.markdown("<h6 style='text-align: center;'>pour le compte du</h6>", unsafe_allow_html=True)
st.sidebar.write(" ", unsafe_allow_html=True)

# Affichage du logo du cinéma dans la barre latérale
image_url = "https://github.com/isnardynicolas/streamlit/blob/main/logo-cinema-noir.png?raw=true"
st.sidebar.image(image_url, use_column_width=True)

st.sidebar.write(" ", unsafe_allow_html=True)
st.sidebar.write(" ", unsafe_allow_html=True)
st.sidebar.write(" ", unsafe_allow_html=True)
st.sidebar.write(" ", unsafe_allow_html=True)
st.sidebar.write(" ", unsafe_allow_html=True)
st.sidebar.write(" ", unsafe_allow_html=True)
st.sidebar.write(" ", unsafe_allow_html=True)

st.sidebar.markdown("<h6 style='text-align: center;'>by</h6>", unsafe_allow_html=True)

# Affichage du logo du groupe dans la barre latérale
image_url2 = "https://github.com/isnardynicolas/streamlit/blob/d229c268ae6b02c40212af4c60aa07aa24cd36ef/logo_480.png?raw=true"
st.sidebar.image(image_url2, use_column_width=True)

# Suppression de la colonne inutile "Unnamed: 0"
df_all.drop("Unnamed: 0", inplace=True, axis=1)

# Conversion de la colonne "runtimeMinutes" en type numérique
df_all.runtimeMinutes = pd.to_numeric(df_all.runtimeMinutes, errors='coerce')
df_all.dropna(subset="runtimeMinutes", inplace=True)

# Suppression des lignes où le genre est manquant ("\N")
df_all = df_all.loc[df_all.genre_1 != "\\N"]
df_all.reset_index(drop=True)

# Extraction des genres uniques
genres = set(df_all['genre_1']).union(set(df_all['genre_2'])).union(set(df_all.genre_3))

# Ajout des colonnes correspondant aux genres
for genre in genres:
    df_all[genre] = df_all.apply(lambda row: 1 if genre in [row['genre_1'], row['genre_2'], row["genre_3"]] else 0, axis=1)

# Suppression de la colonne inutile
df_all.drop(df_all.columns[12], axis=1, inplace=True)

# Affichage du titre et de l'image d'introduction
st.markdown("<h3 style='text-align: center;'>Manque d'inspiration pour votre soirée cinéma ? Nous sommes là pour vous aider !</h3>", unsafe_allow_html=True)
st.write(" ", unsafe_allow_html=True)
image_url3 = "https://media.giphy.com/media/13C8uU4ZKi9CW4/giphy.gif"
st.image(image_url3, use_column_width=True)
st.write(" ", unsafe_allow_html=True)
st.write(" ", unsafe_allow_html=True)
st.write(" ", unsafe_allow_html=True)

df = df_all.loc[(df_all["startYear"] >= 1970) &
                                      (df_all["startYear"] <= 1990), :]

# Saisie du titre du film choisi par l'utilisateur
film_choisi = st.text_input("Entrez le titre du film de votre choix 😊")
film_choisi = film_choisi.lower()

df_all["title_lower"] = df_all.title.str.lower()

# Fonction pour concaténer les genres en une seule chaîne
def concat_genres(row):
    genres = []
    if pd.notnull(row["Genre 1"]):
        genres.append(str(row["Genre 1"]))
    if pd.notnull(row["Genre 2"]):
        genres.append(str(row["Genre 2"]))
    if pd.notnull(row["Genre 3"]):
        genres.append(str(row["Genre 3"]))
    return ", ".join(genres)

# Condition si le réalisateur du film a sorti un ou des films dans les années 70-90

if film_choisi in df_all.title_lower.values:

    # Recommandations de films du même réalisateur

    # Récupération du nom du réalisateur du film choisi
    director_choisi = df_all.loc[df_all["title_lower"] == film_choisi, "primaryName"].item()

    # Création d'un dataframe contenant les enregistrements avec le même réalisateur
    df_ml_director = df.loc[df["primaryName"] == director_choisi, :]

    if director_choisi in list(df_ml_director["primaryName"]):


        # Sélection des colonnes numériques pour l'apprentissage automatique
        X_director = df_ml_director.select_dtypes("number")

        # Standardisation des données
        scaler = StandardScaler()
        scaler.fit(X_director)
        X_scaled = scaler.transform(X_director)

        # Normalisation des données
        norm = MinMaxScaler()
        norm.fit(X_scaled)
        X_norm = norm.transform(X_scaled)

        # Sélection du nombre de voisins à recommander
        st.write(" ", unsafe_allow_html=True)
        st.write(" ", unsafe_allow_html=True)    
        st.write(" ", unsafe_allow_html=True)
        st.write(" ", unsafe_allow_html=True)
        n_neighbors_director = st.slider("Choisissez le nombre de recommandations que vous souhaitez :", 0, len(df_ml_director), len(df_ml_director))

        # Entraînement du modèle de voisins les plus proches
        modelKNN_directors = NearestNeighbors(n_neighbors=n_neighbors_director).fit(X_norm)

        # Recherche des voisins les plus proches du film choisi
        z_director = df_all.loc[df_all.title_lower == film_choisi, X_director.columns]
        z_scaled = scaler.transform(z_director)
        z_norm = norm.transform(z_scaled)
        neighbor = modelKNN_directors.kneighbors(z_norm)

        # Création d'un dataframe contenant les recommandations de films du même réalisateur
        df_result_director = df_ml_director.iloc[neighbor[1][0]].rename(columns={
            "title": "Titre",
            "primaryName": "Réalisateur",
            "genre_1": "Genre 1",
            "genre_2": "Genre 2",
            "genre_3": "Genre 3",
            "startYear": "Année de sortie",
            "runtimeMinutes": "Durée",
            "averageRating": "Note moyenne"
        })

     
        # Affichage des recommandations de films du même réalisateur
        st.markdown("<h5 style='text-align: center;'>Nous vous proposons ces films du/de la même réalisateur/trice :</h5>", unsafe_allow_html=True)
        df_result_director["Genres"] = df_result_director.apply(concat_genres, axis=1)
        df_result_director["Année de sortie"] = df_result_director["Année de sortie"].astype(str).str.replace(",", "")
        df_result_director["Durée"] = df_result_director["Durée"].apply(lambda x: str(round(x // 60)) + "h" + str(round(x % 60)) + "m")
        st.dataframe(df_result_director.loc[:, ["Titre", "Réalisateur", "Genres", "Année de sortie", "Durée", "Note moyenne"]].set_index("Titre"))

    # Condition si le réalisateur du film choisi n'a pas sorti de film entre 1970 et 1990

    else :
        st.markdown("<h5 style='text-align: center;'>Nous vous proposons ces films du/de la même réalisateur/trice :</h5>", unsafe_allow_html=True)
        st.write("Désolé, ce réalisateur n'a sorti aucun film entre 1970 et 1990.")


    # Recommandations de films du même genre

    # Récupération du genre du film choisi
    genre_choisi = df_all.loc[df_all["title_lower"] == film_choisi, "genre_1"].item()

    # Création d'un dataframe contenant les enregistrements avec le même genre
    df_ml_genre = df.loc[df["genre_1"] == genre_choisi, :]

    # Sélection des colonnes numériques pour l'apprentissage automatique
    X_genre = df_ml_genre.select_dtypes("number")

    # Standardisation des données
    scaler = StandardScaler()
    scaler.fit(X_genre)
    X_scaled = scaler.transform(X_genre)

    # Normalisation des données
    norm = MinMaxScaler()
    norm.fit(X_scaled)
    X_norm = norm.transform(X_scaled)

    # Sélection du nombre de voisins à recommander
    st.write(" ", unsafe_allow_html=True)
    st.write(" ", unsafe_allow_html=True)    
    st.write(" ", unsafe_allow_html=True)
    st.write(" ", unsafe_allow_html=True)
    n_neighbors_genre = st.slider("Choisissez le nombre de recommandations que vous souhaitez :", 0, 30, 30)

    # Entraînement du modèle de voisins les plus proches
    modelKNN_genre = NearestNeighbors(n_neighbors=n_neighbors_genre).fit(X_norm)

    # Recherche des voisins les plus proches du film choisi
    z_genre = df_all.loc[df_all.title_lower == film_choisi, X_genre.columns]
    z_scaled = scaler.transform(z_genre)
    z_norm = norm.transform(z_scaled)
    neighbor = modelKNN_genre.kneighbors(z_norm)

    # Création d'un dataframe contenant les recommandations de films du même genre
    df_result_genre = df_ml_genre.iloc[neighbor[1][0]].rename(columns={
        "title": "Titre",
        "primaryName": "Réalisateur",
        "genre_1": "Genre 1",
        "genre_2": "Genre 2",
        "genre_3": "Genre 3",
        "startYear": "Année de sortie",
        "runtimeMinutes": "Durée",
        "averageRating": "Note moyenne"
    })

    # Affichage des recommandations de films du même genre
    st.markdown("<h5 style='text-align: center;'>Ces films du même genre vous plairont certainement :</h5>", unsafe_allow_html=True)
    df_result_genre["Genres"] = df_result_genre.apply(concat_genres, axis=1)
    df_result_genre["Année de sortie"] = df_result_genre["Année de sortie"].astype(str).str.replace(",", "")
    df_result_genre["Durée"] = df_result_genre["Durée"].apply(lambda x: str(round(x // 60)) + "h" + str(round(x % 60)) + "m")
    st.dataframe(df_result_genre.loc[:, ["Titre", "Réalisateur", "Genres", "Année de sortie", "Durée", "Note moyenne"]].set_index("Titre"))

    # Recommandations de films de la même année

    # Récupération de l'année de sortie du film choisi
    year_choisi = df_all.loc[df_all["title_lower"] == film_choisi, "startYear"].item()

    # Création d'un dataframe contenant les enregistrements de la même année de sortie
    df_ml_year = df.loc[df["startYear"] == year_choisi, :]

    # Condition si le film choisi est sorti entre 1970 et 1990 

    if year_choisi in list(df_ml_year["startYear"]):

        # Sélection des colonnes numériques pour l'apprentissage automatique
        X_year = df_ml_year.select_dtypes("number")

        # Standardisation des données
        scaler = StandardScaler()
        scaler.fit(X_year)
        X_scaled = scaler.transform(X_year)

        # Normalisation des données
        norm = MinMaxScaler()
        norm.fit(X_scaled)
        X_norm = norm.transform(X_scaled)

        # Sélection du nombre de voisins à recommander
        st.write(" ", unsafe_allow_html=True)
        st.write(" ", unsafe_allow_html=True)    
        st.write(" ", unsafe_allow_html=True)
        st.write(" ", unsafe_allow_html=True)
        n_neighbors_year = st.slider("Choisissez le nombre de recommandations que vous souhaitez :", 0, 30,29)

        # Entraînement du modèle de voisins les plus proches
        modelKNN_year = NearestNeighbors(n_neighbors=n_neighbors_year).fit(X_norm)

        # Recherche des voisins les plus proches du film choisi
        z_year = df_all.loc[df_all.title_lower == film_choisi, X_year.columns]
        z_scaled = scaler.transform(z_year)
        z_norm = norm.transform(z_scaled)
        neighbor = modelKNN_year.kneighbors(z_norm)

        # Création d'un dataframe contenant les recommandations de films de la même année
        df_result_year = df_ml_year.iloc[neighbor[1][0]].rename(columns={
            "title": "Titre",
            "primaryName": "Réalisateur",
            "genre_1": "Genre 1",
            "genre_2": "Genre 2",
            "genre_3": "Genre 3",
            "startYear": "Année de sortie",
            "runtimeMinutes": "Durée",
            "averageRating": "Note moyenne"
        })


        # Affichage des recommandations de films de la même année
        st.markdown("<h5 style='text-align: center;'>Ces films de la même année sont également intéressants :</h5>", unsafe_allow_html=True)
        df_result_year["Genres"] = df_result_year.apply(concat_genres, axis=1)
        df_result_year["Année de sortie"] = df_result_year["Année de sortie"].astype(str).str.replace(",", "")
        df_result_year["Durée"] = df_result_year["Durée"].apply(lambda x: str(round(x // 60)) + "h" + str(round(x % 60)) + "m")
        st.dataframe(df_result_year.loc[:, ["Titre", "Réalisateur", "Genres", "Année de sortie", "Durée", "Note moyenne"]].set_index("Titre"))

    # Condition si le film choisi est sorti en dehors de la période 1970 - 1990   
    else :
        st.write(" ", unsafe_allow_html=True)
        st.write(" ", unsafe_allow_html=True)    
        st.write(" ", unsafe_allow_html=True)
        st.write(" ", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;'>Ces films de la même année sont également intéressants :</h5>", unsafe_allow_html=True)
        st.write("Désolé, le film choisi est sorti en dehors de la période 1970 - 1990.")

# Condition pour éviter un message d'erreur lors du chargement de la page (entrée vide dans l'input)
elif film_choisi == "":
    st.write("")

# Condition concernant un film choisi absent de la base de données
else:
    st.write("Désolé, le film que vous avez saisi n'est pas dans notre base de données. Veuillez réessayer avec un autre titre.")
