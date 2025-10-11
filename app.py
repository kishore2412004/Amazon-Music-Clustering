import streamlit as st
import pandas as pd
import requests
import base64
import random
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


st.set_page_config(page_title="Amazon Music Clustering", layout="wide")

st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: #FFFFFF;
        }
        .main-header {
            text-align: center;
            font-size: 44px;
            font-weight: bold;
            color: #FFFFFF;
            text-shadow: 0px 2px 4px rgba(0,0,0,0.6);
        }
        .sub-header {
            text-align: center;
            font-size: 18px;
            color: #DDDDDD;
        }
        .album-img {
            border-radius: 18px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
        }
        .album-img:hover {
            transform: scale(1.05);
            box-shadow: 0px 6px 20px rgba(255,255,255,0.2);
        }
        .album-title {
            text-align: left;
            font-size: 20px;
            color: #FFFFFF;
            font-weight: 600;
            margin-top: 10px;
            text-shadow: 0px 2px 5px rgba(0,0,0,0.8);
        }
        .view-btn {
            display: block;
            margin: 8px auto;
            background-color: #1DB954;
            color: white !important;
            font-weight: bold;
            border-radius: 20px;
            border: none;
            padding: 8px 20px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .view-btn:hover {
            background-color: #1ed760;
        }
        h4, p {
            margin: 5px 0;
            color: #FFFFFF;
            text-align: left;
            text-shadow: 0px 1px 4px rgba(0,0,0,0.6);
        }
        audio {
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🎵 Amazon Music Clustering</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Discover music clusters powered by Spotify API</div>', unsafe_allow_html=True)
st.write("")


# LOAD DATA

csv_path = "clustered_songs_final.csv"
try:
    df = pd.read_csv(csv_path)
    st.success("✅ Cleaned dataset loaded successfully!")
except FileNotFoundError:
    st.error(f"❌ File '{csv_path}' not found!")
    st.stop()


# CLUSTER ALBUMS (NAMES + THEMES)

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
    return response.json().get("access_token")

token = get_spotify_token()
headers = {"Authorization": f"Bearer {token}"}


# FETCH SONGS FROM SPOTIFY

def fetch_random_songs(query):
    """Fetch random 10-12 songs from Spotify search."""
    offset = random.randint(0, 500)  # shuffle results
    url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=12&offset={offset}"
    response = requests.get(url, headers=headers).json()
    return response.get("tracks", {}).get("items", [])


# DISPLAY CLUSTERS

st.subheader("🎼 Browse Clusters as Albums")
album_cols = st.columns(3)

for i, cluster_id in enumerate(sorted(df['cluster'].unique())):
    cluster = cluster_themes.get(int(cluster_id), default_theme)
    with album_cols[i % 3]:
        st.image(cluster['img'], width=250)
        st.markdown(f"<div class='album-title'>{cluster['name']}</div>", unsafe_allow_html=True)
        if st.button(f"🎧 Explore {cluster['name']}", key=f"cluster_{cluster_id}"):
            # Every click gets a FRESH recommendation
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
                track_name = track['name']
                artist_name = track['artists'][0]['name']
                img_url = track['album']['images'][0]['url'] if track['album']['images'] else None
                preview = track.get('preview_url')

                st.image(img_url or "https://upload.wikimedia.org/wikipedia/commons/3/3c/No-album-art-placeholder.png", width=250)
                st.markdown(f"<h4>{track_name}</h4><p>{artist_name}</p>", unsafe_allow_html=True)
                if preview:
                    st.audio(preview)
                else:
                    st.caption("🎵 No preview available")

    # Optional: Shuffle button for fresh set of songs
    if st.button("🔁 Get New Recommendations"):
        st.session_state['recommendations'] = fetch_random_songs(st.session_state['cluster_query'])
        st.rerun()

st.markdown("---")


# INSIGHTS & VISUALIZATIONS

st.subheader("📊 Cluster Insights & Visualizations")

if st.checkbox("Show All Insights and Visualizations"):
    feature_cols = [
        'danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
        'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms'
    ]

    # PCA Visualization
    st.markdown("### 🌀 PCA 2D Cluster Visualization")
    try:
        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(df[feature_cols])
        df['pca1'], df['pca2'] = pca_result[:, 0], pca_result[:, 1]
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(x='pca1', y='pca2', hue='cluster', data=df, palette='tab10', s=60, alpha=0.8, ax=ax)
        st.pyplot(fig)
    except Exception as e:
        st.warning(f"PCA Visualization skipped: {e}")

    # Cluster summary heatmap
    st.markdown("### 🔥 Cluster Feature Averages (Heatmap)")
    cluster_summary = df.groupby('cluster')[feature_cols].mean().round(2)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(cluster_summary, cmap='coolwarm', annot=True, fmt=".2f", ax=ax)
    st.pyplot(fig)
    st.dataframe(cluster_summary)

    # Cluster size distribution
    st.markdown("### 🎧 Cluster Size Distribution")
    fig, ax = plt.subplots(figsize=(7, 5))
    df['cluster'].value_counts().sort_index().plot(kind='bar', color='skyblue', ax=ax)
    plt.xlabel("Cluster")
    plt.ylabel("Number of Songs")
    st.pyplot(fig)

    # Feature correlation heatmap
    st.markdown("### 🧠 Feature Correlation Heatmap")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(df[feature_cols].corr(), cmap='viridis', annot=True, fmt=".2f", ax=ax)
    st.pyplot(fig)

    # Boxplot feature comparison
    st.markdown("### 🎚️ Compare Feature Distribution by Cluster")
    selected_feature = st.selectbox("Select a feature:", feature_cols)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(x='cluster', y=selected_feature, data=df, palette='Set2', ax=ax)
    st.pyplot(fig)

    # Radar chart for each cluster
    st.markdown("### 🕸️ Cluster Profile (Radar Chart)")
    try:
        from math import pi
        cluster_norm = (cluster_summary - cluster_summary.min()) / (cluster_summary.max() - cluster_summary.min())
        for i in cluster_norm.index:
            values = cluster_norm.loc[i].tolist()
            labels = cluster_norm.columns.tolist()
            values += values[:1]
            angles = [n / float(len(labels)) * 2 * pi for n in range(len(labels))]
            angles += angles[:1]

            fig = plt.figure(figsize=(5, 5))
            ax = plt.subplot(111, polar=True)
            plt.xticks(angles[:-1], labels, color='white', size=8)
            ax.plot(angles, values, linewidth=2, linestyle='solid', label=f'Cluster {i}')
            ax.fill(angles, values, alpha=0.25)
            plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
            st.pyplot(fig)
    except Exception as e:
        st.warning(f"Radar Chart skipped: {e}")

st.markdown("---")


# EXPORT DATA

csv = df.to_csv(index=False).encode('utf-8')
st.download_button("💾 Download Final Clustered Dataset", csv, "clustered_songs_final.csv", "text/csv")
