




from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import faiss
import requests
from sklearn.preprocessing import normalize

app = Flask(__name__)
CORS(app)

df = pd.read_csv("Top_movies2_features1_plus_index.csv")
index = faiss.read_index("faiss_hybrid_fast.index")
embeddings = np.load("faiss_hybrid_fast_embeddings.npy")

TMDB_API = "756829d00f537c980ee54bc17d2e2038"


# ==========================
# 🧠 NEW: TEXT → MOOD
# ==========================
def detect_mood_from_text(text):
    text = text.lower()

    mood_keywords = {
        "happy": ["happy", "fun", "good", "great"],
        "sad": ["sad", "bad", "not great", "depressed"],
        "action": ["action", "thrill", "exciting"],
        "romantic": ["love", "romantic"],
        "dark": ["dark", "horror", "mystery"]
    }

    for mood, words in mood_keywords.items():
        for w in words:
            if w in text:
                return mood

    return None


# ==========================
# TMDB INFO (WITHOUT POSTER)
# ==========================
def get_movie_info(title):
    try:
        url = "https://api.themoviedb.org/3/search/movie"
        params = {"api_key": TMDB_API, "query": title}

        response = requests.get(url, params=params).json()

        if response.get("results"):
            movie = response["results"][0]

            movie_id = movie.get("id")

            return {
                "id": movie_id,
                "link": f"https://www.themoviedb.org/movie/{movie_id}"
            }
    except:
        pass

    return {"id": None, "link": ""}


# ==========================
# OTT
# ==========================
def get_ott(movie_id):
    if not movie_id:
        return []

    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"
        res = requests.get(url, params={"api_key": TMDB_API}).json()

        for country in res.get("results", {}).values():
            for key in ["flatrate", "rent", "buy"]:
                if country.get(key):
                    return [p["provider_name"] for p in country[key]]
    except:
        pass

    return []


# ==========================
# FAISS
# ==========================
def faiss_recommend(title):

    row = df[df["title"].str.contains(title, case=False, na=False)]

    if row.empty:
        return []

    idx = row.index[0]

    q = normalize(embeddings[idx].reshape(1, -1))
    _, indices = index.search(q, 8)

    results = []

    for i in indices[0][1:]:

        movie = df.iloc[i]

        info = get_movie_info(movie["title"])
        ott = get_ott(info["id"])

        results.append({
            "title": movie["title"],
            "rating": float(movie.get("vote_average", 0)),
            "genres": movie.get("genres", ""),
            "ott": ott,

            # 🔥 NEW
            "link": info["link"],
            "reason": f"Recommended based on your input: {title}"
        })

    return results


# ==========================
# MAIN API
# ==========================
@app.route("/recommend", methods=["POST"])
def recommend():

    data = request.json

    movie = data.get("movie", "").lower()
    mood = data.get("mood", "")

    # 🧠 NEW: detect mood automatically
    if movie and not mood:
        detected = detect_mood_from_text(movie)
        if detected:
            mood = detected

    mood_map = {
        "happy": "Comedy",
        "sad": "Drama",
        "action": "Action",
        "romantic": "Romance",
        "dark": "Thriller"
    }

    if mood in mood_map:
        genre = mood_map[mood]

        filtered = df[df["genres"].str.contains(genre, case=False, na=False)].head(8)

        results = []

        for _, m in filtered.iterrows():
            info = get_movie_info(m["title"])
            ott = get_ott(info["id"])

            results.append({
                "title": m["title"],
                "rating": float(m.get("vote_average", 0)),
                "genres": m.get("genres", ""),
                "ott": ott,

                # 🔥 NEW
                "link": info["link"],
                "reason": f"Because you feel {mood}"
            })

        return jsonify(results)

    if movie:
        return jsonify(faiss_recommend(movie))

    return jsonify([])


if __name__ == "__main__":
    app.run(debug=True)
