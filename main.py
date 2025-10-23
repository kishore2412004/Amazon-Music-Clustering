# ==========================================
# 🎵 AMAZON MUSIC CLUSTERING - FINAL VERSION (Feature + Mood + Climate + Artist Dropdown)
# ==========================================

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# ------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------
st.set_page_config(page_title="Amazon Music Clustering", layout="wide")

st.markdown("""
    <style>
        body {
            background: linear-gradient(145deg, #121212, #1e1e1e);
            color: #FFFFFF;
            font-family: 'Poppins', sans-serif;
        }
        .main-header {
            text-align: center;
            font-size: 44px;
            font-weight: bold;
            color: #FFD369;
            text-shadow: 0px 2px 8px rgba(0,0,0,0.6);
        }
        .sub-header {
            text-align: center;
            font-size: 18px;
            color: #CCCCCC;
        }
        .cluster-card {
            background-color: #1b1b1f;
            border-radius: 16px;
            padding: 15px;
            margin-bottom: 10px;
            box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        }
        .cluster-card:hover {
            transform: scale(1.02);
            box-shadow: 0px 8px 25px rgba(255, 211, 105, 0.25);
        }
        h3 {
            color: #FFD369;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🎵 Amazon Music Clustering</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Discover how songs naturally group by their audio characteristics, moods, and climates</div>', unsafe_allow_html=True)
st.markdown("---")

# ------------------------------------------------------------
# LOAD DATA & SCALER
# ------------------------------------------------------------
csv_path = "clustered_songs_final.csv"
try:
    df = pd.read_csv(csv_path)
    st.success("✅ Dataset loaded successfully!")
except FileNotFoundError:
    st.error(f"❌ File '{csv_path}' not found!")
    st.stop()

try:
    scaler = joblib.load("scaler.pkl")
    st.success("✅ Scaler loaded successfully!")
except Exception as e:
    st.error(f"❌ Scaler not found: {e}")
    st.stop()

# ------------------------------------------------------------
# FEATURE COLUMNS
# ------------------------------------------------------------
feature_cols = [
    "danceability", "energy", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness",
    "valence", "tempo", "duration_ms"
]

if not set(feature_cols).issubset(df.columns):
    st.error("❌ Dataset missing required audio feature columns.")
    st.stop()

# ------------------------------------------------------------
# CLUSTER THEMES
# ------------------------------------------------------------
cluster_themes = {
    0: "🔥 Party & Dance Hits",
    1: "🌙 Chill Acoustic Vibes",
    2: "💥 Energetic Pop Beats",
    3: "🎸 Indie & Alternative",
    4: "🎹 Instrumental Lounge",
    5: "❤️ Romantic & Soft Songs"
}

# ------------------------------------------------------------
# COMPUTE CLUSTER CENTROIDS (Feature-based)
# ------------------------------------------------------------
if "cluster" not in df.columns:
    st.warning("Dataset missing 'cluster' column. Please ensure clusters are labeled.")
else:
    cluster_centroids = df.groupby("cluster")[feature_cols].mean()
    cluster_centroids_scaled = scaler.transform(cluster_centroids.values)
    cluster_labels = list(cluster_centroids.index)

# ------------------------------------------------------------
# MOOD & CLIMATE MAPS
# ------------------------------------------------------------
mood_map = {
    "Happy": {"valence": 0.8, "energy": 0.7},
    "Sad": {"valence": 0.2, "acousticness": 0.7},
    "Energetic": {"energy": 0.9, "tempo": 0.8},
    "Calm": {"acousticness": 0.8, "energy": 0.3},
    "Romantic": {"valence": 0.6, "speechiness": 0.3, "acousticness": 0.5},
    "Chill": {"energy": 0.4, "liveness": 0.3, "valence": 0.6}
}

climate_map = {
    "Rainy": {"acousticness": 0.7, "valence": 0.4},
    "Sunny": {"energy": 0.8, "valence": 0.9},
    "Winter": {"acousticness": 0.8, "liveness": 0.2},
    "Summer": {"energy": 0.8, "valence": 0.7}
}

# ------------------------------------------------------------
# SEARCH SECTION
# ------------------------------------------------------------
st.markdown("## 🔍 Search Options")

tab1, tab2, tab3 = st.tabs(["🎧 Search by Song", "🎤 Search by Artist", "🌤️ Search by Mood/Climate"])

# ========== SONG SEARCH ==========
with tab1:
    song_query = st.text_input("Enter a song name:", "")
    if song_query:
        matched = df[df["name_song"].str.contains(song_query, case=False, na=False)]
        if matched.empty:
            st.warning("⚠️ No matching song found.")
        else:
            song = matched.iloc[0]
            st.markdown(f"## 🎧 {song['name_song']} — *{song['name_artists']}*")

            X_features = song[feature_cols].to_numpy().reshape(1, -1)
            X_scaled = scaler.transform(X_features)

            centroid_sims = cosine_similarity(X_scaled, cluster_centroids_scaled)[0]
            best_idx = int(np.argmax(centroid_sims))
            cluster_label = cluster_labels[best_idx]
            cluster_name = cluster_themes.get(cluster_label, f"Cluster {cluster_label}")

            st.success(f"This song belongs to **{cluster_name}** cluster!")

            same_cluster = df[df["cluster"] == cluster_label].copy()
            same_cluster_scaled = scaler.transform(same_cluster[feature_cols])
            sims = cosine_similarity(X_scaled, same_cluster_scaled)[0]
            same_cluster["similarity_score"] = sims

            recommendations = (
                same_cluster[same_cluster["name_song"] != song["name_song"]]
                .sort_values("similarity_score", ascending=False)
                .head(10)
            )

            st.markdown(f"### 🎶 Songs similar to *{song['name_song']}*")
            for _, row in recommendations.iterrows():
                st.markdown(f"- **{row['name_song']}** — *{row['name_artists']}* 🎯 *(Similarity: {row['similarity_score']:.2f})*")

# ========== ARTIST SEARCH (DROPDOWN) ==========
with tab2:
    st.markdown("### 🎤 Explore Songs by Artist")

    # Prepare sorted list of unique artists
    artist_list = sorted(df["name_artists"].dropna().unique())

    selected_artist = st.selectbox("Select an Artist:", ["None"] + artist_list)

    if selected_artist != "None":
        matched_artist = df[df["name_artists"] == selected_artist]
        st.markdown(f"## 🎤 Songs by *{selected_artist}*")
        st.dataframe(matched_artist[["name_song", "name_artists", "cluster"]])

        # Determine the artist’s main cluster
        top_cluster = int(matched_artist["cluster"].mode()[0])
        cluster_name = cluster_themes.get(top_cluster, f"Cluster {top_cluster}")
        st.info(f"🎵 This artist mostly belongs to **{cluster_name}** cluster")

        # Recommend similar songs from same cluster
        same_cluster = df[df["cluster"] == top_cluster].sample(min(10, len(df[df["cluster"] == top_cluster])))
        st.markdown("### 🎶 Songs with similar vibe:")
        for _, row in same_cluster.iterrows():
            st.markdown(f"- **{row['name_song']}** — *{row['name_artists']}*")

# ========== MOOD/CLIMATE SEARCH ==========
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        mood_choice = st.selectbox("Select a Mood:", ["None"] + list(mood_map.keys()))
    with col2:
        climate_choice = st.selectbox("Select a Climate:", ["None"] + list(climate_map.keys()))

    if st.button("🎯 Find Songs by Mood/Climate"):
        pref_vector = np.zeros(len(feature_cols))
        feature_index = {f: i for i, f in enumerate(feature_cols)}

        for mapping in [mood_map.get(mood_choice, {}), climate_map.get(climate_choice, {})]:
            for f, v in mapping.items():
                if f in feature_index:
                    pref_vector[feature_index[f]] += v

        if np.sum(pref_vector) == 0:
            st.warning("⚠️ Please select at least one mood or climate.")
        else:
            pref_vector = pref_vector / np.linalg.norm(pref_vector)
            scaled_features = scaler.transform(df[feature_cols])
            sims = cosine_similarity([pref_vector], scaled_features)[0]
            df["similarity_score"] = sims
            results = df.sort_values("similarity_score", ascending=False).head(10)

            st.markdown(f"### 🎵 Top 10 Songs for {mood_choice or ''} {climate_choice or ''}")
            for _, row in results.iterrows():
                st.markdown(f"- **{row['name_song']}** — *{row['name_artists']}* 🌟 *(Similarity: {row['similarity_score']:.2f})*")

st.markdown("---")

# ------------------------------------------------------------
# CLUSTER INSIGHTS
# ------------------------------------------------------------
st.markdown("## 📈 Cluster Insights")

if st.checkbox("Show Cluster Visualizations"):
    cluster_summary = df.groupby("cluster")[feature_cols].mean().round(2)
    st.dataframe(cluster_summary)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(cluster_summary, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(df[feature_cols])
    df["pca1"], df["pca2"] = pca_result[:, 0], pca_result[:, 1]

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x="pca1", y="pca2", hue="cluster", data=df, palette="tab10", s=70)
    st.pyplot(fig)

st.markdown("---")

# ------------------------------------------------------------
# DOWNLOAD SECTION
# ------------------------------------------------------------
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("💾 Download Final Clustered Dataset", csv, "clustered_songs_final.csv", "text/csv")

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<center>🚀 Amazon Music Clustering — AI-driven Song Discovery</center>", unsafe_allow_html=True)
