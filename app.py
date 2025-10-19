import streamlit as st
import pandas as pd
import requests
import base64
import random
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from math import pi
import numpy as np
from pytube import Search



# PAGE CONFIGURATION

st.set_page_config(page_title="Amazon Music Clustering", layout="wide")


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

body {
    background: linear-gradient(145deg, #0e0e10, #1b1b1f);
    color: #FFFFFF;
}

.main-header {
    text-align: center;
    font-size: 52px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.5em;
    text-shadow: 0px 2px 8px rgba(0,0,0,0.7);
    letter-spacing: 1.5px;
}

.sub-header {
    text-align: center;
    font-size: 20px;
    color: #bfbfbf;
    margin-bottom: 2em;
}

.stTextInput>div>div>input {
    background-color: #1e1e26 !important;
    color: #ffffff !important;
    border: 1px solid #2a2a33 !important;
    border-radius: 10px;
    padding: 10px;
}

.stButton>button {
    background: linear-gradient(90deg, #ff6a00, #ee0979);
    color: white;
    font-weight: 600;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    box-shadow: 0px 3px 10px rgba(255, 0, 100, 0.4);
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #ee0979, #ff6a00);
    transform: scale(1.05);
}

.song-card {
    background: linear-gradient(135deg, #1a1a22, #23232d);
    border-radius: 16px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
    transition: all 0.3s ease;
}
.song-card:hover {
    transform: scale(1.03);
    box-shadow: 0px 6px 30px rgba(255, 165, 0, 0.25);
}

.cluster-box {
    border-radius: 18px;
    padding: 20px;
    margin: 10px;
    background: linear-gradient(120deg, #18181f, #1f1f2e);
    box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
    transition: all 0.3s ease-in-out;
}
.cluster-box:hover {
    transform: scale(1.05);
    box-shadow: 0px 8px 25px rgba(255, 200, 0, 0.25);
}

.dataframe {
    background-color: #202030 !important;
    color: #ffffff !important;
    border-radius: 10px !important;
}

hr {
    border-top: 1px solid #444;
    margin: 2em 0;
}

.audio-container {
    background-color: #141414;
    border-radius: 12px;
    padding: 10px;
    box-shadow: 0px 3px 10px rgba(255,255,255,0.05);
}

</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🎵 Amazon Music Clustering</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Discover Clusters, Explore Genres, and Feel the Vibe</div>', unsafe_allow_html=True)



# LOAD DATA

csv_path = "clustered_songs_final.csv"
try:
    df = pd.read_csv(csv_path)
    st.success("✅ Dataset loaded successfully!")
except FileNotFoundError:
    st.error(f"❌ File '{csv_path}' not found!")
    st.stop()

feature_cols = [
    "danceability", "energy", "loudness", "speechiness", "acousticness",
    "instrumentalness", "liveness", "valence", "tempo", "duration_ms"
]

import joblib

# Load model & scaler
try:
    model = joblib.load("cluster_model.pkl")
    scaler = joblib.load("scaler.pkl")
    st.success("✅ Trained clustering model loaded successfully!")
except Exception as e:
    st.warning(f"⚠️ Model not found or failed to load: {e}")



# CLUSTER THEMES

cluster_themes = {
    0: {"name": "🔥 Party & Dance Hits", "img": "https://imgs.search.brave.com/_taxu7GmF6QRbtawOTCPaFEKwop_jukWIM1QTIApGKA/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tLm1l/ZGlhLWFtYXpvbi5j/b20vaW1hZ2VzL0kv/ODFMeG12RUN1ZUwu/anBn"},
    1: {"name": "🌙 Chill Acoustic Vibes", "img": "https://imgs.search.brave.com/q1kqJEUy9Tq8xMVuAzV1G_Ig0_WNHvfjohuqNTeUfuE/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tLm1l/ZGlhLWFtYXpvbi5j/b20vaW1hZ2VzL0kv/ODFPbDduUTJDY0wu/anBn"},
    2: {"name": "💥 Energetic Pop Beats", "img": "https://imgs.search.brave.com/RKN6lvtgPAAIiXkdFF25SwHiPNmXJ9BGMr5zl9mJ0Z0/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tLm1l/ZGlhLWFtYXpvbi5j/b20vaW1hZ2VzL0kv/ODFHN05HMDlyT0wu/anBn"},
    3: {"name": "🎸 Indie & Alternative", "img": "https://imgs.search.brave.com/jG2C8uribNb9Fbpq1QF1o5j1c41JvvF3zG2a1KqpMzQ/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tLm1l/ZGlhLWFtYXpvbi5j/b20vaW1hZ2VzL0kv/ODF4c2xOQzFncUwu/anBn"},
    4: {"name": "🎹 Instrumental Lounge", "img": "https://imgs.search.brave.com/tDKE7uogb68s43TGVNsin0iGsLB6AXg1cFwjUcf1IiE/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tLm1l/ZGlhLWFtYXpvbi5j/b20vaW1hZ2VzL0kv/NzFVZkl1ZmxXQUwu/anBn"},
    5: {"name": "❤️ Romantic & Soft Songs", "img": "https://imgs.search.brave.com/woS0G6KNkCJ5IV6ugC2Mz6j78CcRia9kzyv8c5zYLv4/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tLm1l/ZGlhLWFtYXpvbi5j/b20vaW1hZ2VzL0kv/NTFqalRGRERUT0wu/anBn"},
}
default_theme = {
    "name": "🎶 Mixed Trending Tracks",
    "img": "https://upload.wikimedia.org/wikipedia/commons/3/3c/No-album-art-placeholder.png",
    "query": "top hits trending pop songs"
}



# SPOTIFY AUTHENTICATION

def get_spotify_token():
    client_id = st.secrets["spotify"]["client_id"]
    client_secret = st.secrets["spotify"]["client_secret"]
    auth_str = f"{client_id}:{client_secret}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={"Authorization": f"Basic {b64_auth_str}"},
        data={"grant_type": "client_credentials"},
    )
    data = response.json()
    if "access_token" not in data:
        st.error("❌ Failed to authenticate with Spotify API. Check credentials.")
        return None
    return data["access_token"]

token = get_spotify_token()
headers = {"Authorization": f"Bearer {token}"}


# FETCH RANDOM SONGS FROM SPOTIFY

def fetch_random_songs(query):
    offset = random.randint(0, 500)
    url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=12&offset={offset}"
    response = requests.get(url, headers=headers).json()
    return response.get("tracks", {}).get("items", [])



# SEARCH + CLUSTER PREDICTION USING TRAINED MODEL

st.markdown("### 🔍 Search Songs by Name")
user_query = st.text_input("Enter a song name:", "")

if user_query:
    query = user_query.strip().replace(" ", "%20")
    search_url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1"
    response = requests.get(search_url, headers=headers).json()

    tracks = response.get("tracks", {}).get("items", [])
    

    
    if not tracks:
        st.error("❌ Song not found on Spotify.")
    else:
        track = tracks[0]
        spotify_name = track["name"]
        spotify_artist = track["artists"][0]["name"]
        spotify_img = track["album"]["images"][0]["url"] if track["album"]["images"] else None

        st.markdown(f"## 🎵 {spotify_name} — {spotify_artist}")
        if spotify_img:
            st.image(spotify_img, width=280)

        close_match = get_close_matches(spotify_name, df["name_song"].tolist(), n=1, cutoff=0.4)

        def fetch_youtube_embed(song_name):
            try:
                results = Search(f"{song_name} official audio").results
                if results:
                    video_id = results[0].video_id
                    return f"https://www.youtube.com/embed/{video_id}"
                return None
            except Exception as e:
                st.warning(f"⚠️ YouTube fetch failed: {e}")
                return None


        # Show YouTube preview right below search bar
        if user_query.strip():
            embed_url = fetch_youtube_embed(user_query)
            if embed_url:
                # st.markdown("### ")
                st.markdown(
                    f'<iframe width="100%" height="320" src="{embed_url}" frameborder="0" '
                    f'allow="autoplay; encrypted-media" allowfullscreen></iframe>',
                    unsafe_allow_html=True,
                )
            else:
                st.caption("🎵 No YouTube preview available for this song.")

        if not close_match:
            st.warning("⚠️ No close match found in dataset for cluster prediction.")
        else:
            matched_song = df[df["name_song"] == close_match[0]].iloc[0]
            X_features_df = pd.DataFrame([matched_song[feature_cols].values], columns=feature_cols)
            st.markdown("#### Feature Vector Used for Prediction:")
            st.dataframe(X_features_df)

            try:
                X_scaled = scaler.transform(X_features_df)
                cluster_means = df.groupby("cluster")[feature_cols].mean()
                cluster_means_scaled = scaler.transform(cluster_means)
                similarities = cosine_similarity(X_scaled, cluster_means_scaled)[0]
                cluster_label = int(np.argmax(similarities))
                cluster_info = cluster_themes.get(cluster_label, default_theme)

                st.success(f"This song best matches **{cluster_info['name']}** cluster!")
                st.image(cluster_info['img'], width=400)

                top_sim_indices = np.argsort(similarities)[::-1][:3]
                st.markdown("#### 🔍 Cluster Similarity Breakdown:")
                for i in top_sim_indices:
                    name = cluster_themes.get(i, default_theme)["name"]
                    st.markdown(f"- **{name}:** {similarities[i]*100:.2f}% match")

            except Exception as e:
                st.error(f"⚠️ Cluster similarity computation failed: {e}")

            df_scaled = scaler.transform(df[feature_cols])
            sims = cosine_similarity(X_scaled, df_scaled)[0]
            df["similarity"] = sims
            top_similar = df.sort_values("similarity", ascending=False).head(5)

            st.markdown("### 🎶 Similar Songs from Dataset:")
            for _, row in top_similar.iterrows():
                st.markdown(f"- {row['name_song']} — *{row['name_artists']}* ({row['similarity']*100:.2f}% similar)")

# user_query = st.text_input("Enter a song name:", "")


# from pytube import Search

# def fetch_youtube_embed(song_name):
#     try:
#         results = Search(f"{song_name} official audio").results
#         if results:
#             video_id = results[0].video_id
#             return f"https://www.youtube.com/embed/{video_id}"
#         return None
#     except Exception as e:
#         st.warning(f"⚠️ YouTube fetch failed: {e}")
#         return None


# # 🎧 Show YouTube preview right below search bar
# if user_query.strip():
#     embed_url = fetch_youtube_embed(user_query)
#     if embed_url:
#         # st.markdown("### ")
#         st.markdown(
#             f'<iframe width="100%" height="320" src="{embed_url}" frameborder="0" '
#             f'allow="autoplay; encrypted-media" allowfullscreen></iframe>',
#             unsafe_allow_html=True,
#         )
#     else:
#         st.caption("🎵 No YouTube preview available for this song.")

# ------------------------------------------------------------
# DISPLAY CLUSTERS AS ALBUMS
# ------------------------------------------------------------
st.subheader("🎼 Browse Clusters as Albums")
album_cols = st.columns(3)
for i, cluster_id in enumerate(sorted(df['cluster'].unique())):
    cluster = cluster_themes.get(int(cluster_id), default_theme)
    with album_cols[i % 3]:
        st.markdown(f"""
        <div class='cluster-box'>
            <img src="{cluster['img']}" style="border-radius:12px;width:100%;height:230px;object-fit:cover;">
            <h4 style="text-align:center;margin-top:10px;color:#FFD369;">{cluster['name']}</h4>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"🎧 Explore {cluster['name']}", key=f"cluster_{cluster_id}"):
            st.session_state['selected_cluster'] = int(cluster_id)
            st.session_state['cluster_query'] = cluster.get('query', default_theme['query'])
            st.session_state['recommendations'] = fetch_random_songs(st.session_state['cluster_query'])
            st.rerun()

st.markdown("---")



# SHOW SONG RECOMMENDATIONS

if 'selected_cluster' in st.session_state and 'recommendations' in st.session_state:
    cluster_id = st.session_state['selected_cluster']
    cluster = cluster_themes.get(cluster_id, default_theme)
    st.markdown(f"## {cluster['name']} 🎶")

    songs = st.session_state['recommendations']
    if not songs:
        st.warning("No songs found. Try again!")
    else:
        cols = st.columns(3)
        for i, track in enumerate(songs[:9]):
            col = cols[i % 3]
            with col:
                img_url = track['album']['images'][0]['url'] if track['album']['images'] else None
                track_name = track['name']
                artist_name = track['artists'][0]['name']
                preview = track.get('preview_url')

                st.markdown(f"""
                <div class='song-card'>
                    <img src="{img_url or 'https://upload.wikimedia.org/wikipedia/commons/3/3c/No-album-art-placeholder.png'}"
                        style="border-radius:12px;width:100%;height:230px;object-fit:cover;">
                    <h4 style="margin-top:10px;">{track_name}</h4>
                    <p style="color:#BBBBBB;margin:0;">{artist_name}</p>
                </div>
                """, unsafe_allow_html=True)
                if preview:
                    st.audio(preview)
                else:
                    st.caption("🎵 No preview available")

    if st.button("🔁 Get New Recommendations"):
        st.session_state['recommendations'] = fetch_random_songs(st.session_state['cluster_query'])
        st.rerun()

st.markdown("---")



# FLOATING FOOTER

st.markdown("""
    <div style='
        position:fixed;
        bottom:15px;
        right:15px;
        background:linear-gradient(90deg,#ee0979,#ff6a00);
        padding:10px 20px;
        border-radius:50px;
        color:white;
        font-weight:600;
        box-shadow:0px 3px 15px rgba(255,100,50,0.4);
        z-index:999;
    '>
        🎶 Now Playing Dashboard • Amazon Music Clustering
    </div>
""", unsafe_allow_html=True)
