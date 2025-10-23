# import streamlit as st
# import pandas as pd
# import requests
# import base64
# import random
# from sklearn.preprocessing import StandardScaler
# from sklearn.metrics.pairwise import cosine_similarity
# from difflib import get_close_matches
# import seaborn as sns
# import matplotlib.pyplot as plt
# from sklearn.decomposition import PCA
# from math import pi
# from difflib import get_close_matches
# import numpy as np


# # ------------------------------------------------------------
# # PAGE CONFIGURATION
# # ------------------------------------------------------------
# st.set_page_config(page_title="Amazon Music Clustering", layout="wide")

# st.markdown("""
#     <style>
#         body {
#             background-color: #121212;
#             color: #FFFFFF;
#         }
#         .main-header {
#             text-align: center;
#             font-size: 44px;
#             font-weight: bold;
#             color: #FFFFFF;
#             text-shadow: 0px 2px 4px rgba(0,0,0,0.6);
#         }
#         .sub-header {
#             text-align: center;
#             font-size: 18px;
#             color: #DDDDDD;
#         }
#         .album-title {
#             text-align: left;
#             font-size: 20px;
#             color: #FFFFFF;
#             font-weight: 600;
#             margin-top: 10px;
#             text-shadow: 0px 2px 5px rgba(0,0,0,0.8);
#         }
#         h4, p {
#             margin: 5px 0;
#             color: #FFFFFF;
#             text-align: left;
#         }
#         .song-row {
#             background-color: #1e1e1e;
#             padding: 10px;
#             border-radius: 8px;
#             margin: 10px 0;
#         }
#         .more-info {
#             margin-top: 5px;
#         }
#     </style>
# """, unsafe_allow_html=True)

# st.markdown('<div class="main-header">🎵 Amazon Music Clustering</div>', unsafe_allow_html=True)
# st.markdown('<div class="sub-header">Search and Explore Songs by Similarity & Clusters</div>', unsafe_allow_html=True)

# # ------------------------------------------------------------
# # LOAD DATA
# # ------------------------------------------------------------
# csv_path = "clustered_songs_final.csv"
# try:
#     df = pd.read_csv(csv_path)
#     st.success("✅ Dataset loaded successfully!")
# except FileNotFoundError:
#     st.error(f"❌ File '{csv_path}' not found!")
#     st.stop()
# # Feature columns used for clustering and similarity
# feature_cols = [
#     "danceability", "energy", "loudness", "speechiness", "acousticness",
#     "instrumentalness", "liveness", "valence", "tempo", "duration_ms"
# ]

# import joblib
# import numpy as np

# # Load your trained model & scaler
# try:
#     model = joblib.load("cluster_model.pkl")
#     scaler = joblib.load("scaler.pkl")
#     st.success("✅ Trained clustering model loaded successfully!")
# except Exception as e:
#     st.warning(f"⚠️ Model not found or failed to load: {e}")

# # CLUSTER ALBUMS (NAMES + THEMES)

# cluster_themes = {
#     0: {"name": "🔥 Party & Dance Hits", "img": "https://imgs.search.brave.com/_taxu7GmF6QRbtawOTCPaFEKwop_jukWIM1QTIApGKA/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tLm1l/ZGlhLWFtYXpvbi5j/b20vaW1hZ2VzL0kv/ODFMeG12RUN1ZUwu/anBn"},
#     1: {"name": "🌙 Chill Acoustic Vibes", "img": "https://imgs.search.brave.com/q1kqJEUy9Tq8xMVuAzV1G_Ig0_WNHvfjohuqNTeUfuE/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tLm1l/ZGlhLWFtYXpvbi5j/b20vaW1hZ2VzL0kv/ODFPbDduUTJDY0wu/anBn"},
#     2: {"name": "💥 Energetic Pop Beats", "img": "https://imgs.search.brave.com/RKN6lvtgPAAIiXkdFF25SwHiPNmXJ9BGMr5zl9mJ0Z0/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tLm1l/ZGlhLWFtYXpvbi5j/b20vaW1hZ2VzL0kv/ODFHN05HMDlyT0wu/anBn"},
#     3: {"name": "🎸 Indie & Alternative", "img": "https://imgs.search.brave.com/jG2C8uribNb9Fbpq1QF1o5j1c41JvvF3zG2a1KqpMzQ/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tLm1l/ZGlhLWFtYXpvbi5j/b20vaW1hZ2VzL0kv/ODF4c2xOQzFncUwu/anBn"},
#     4: {"name": "🎹 Instrumental Lounge", "img": "https://imgs.search.brave.com/tDKE7uogb68s43TGVNsin0iGsLB6AXg1cFwjUcf1IiE/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tLm1l/ZGlhLWFtYXpvbi5j/b20vaW1hZ2VzL0kv/NzFVZkl1ZmxXQUwu/anBn"},
#     5: {"name": "❤️ Romantic & Soft Songs", "img": "https://imgs.search.brave.com/woS0G6KNkCJ5IV6ugC2Mz6j78CcRia9kzyv8c5zYLv4/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tLm1l/ZGlhLWFtYXpvbi5j/b20vaW1hZ2VzL0kv/NTFqalRGRERUT0wu/anBn"},
# }

# default_theme = {
#     "name": "🎶 Mixed Trending Tracks",
#     "img": "https://upload.wikimedia.org/wikipedia/commons/3/3c/No-album-art-placeholder.png",
#     "query": "top hits trending pop songs"
# }


# # SPOTIFY AUTHENTICATION

# def get_spotify_token():
#     client_id = st.secrets["spotify"]["client_id"]
#     client_secret = st.secrets["spotify"]["client_secret"]
#     auth_str = f"{client_id}:{client_secret}"
#     b64_auth_str = base64.b64encode(auth_str.encode()).decode()
#     response = requests.post(
#         "https://accounts.spotify.com/api/token",
#         headers={"Authorization": f"Basic {b64_auth_str}"},
#         data={"grant_type": "client_credentials"},
#     )
#     # return response.json().get("access_token")
#     data = response.json()
#     if "access_token" not in data:
#         st.error("❌ Failed to authenticate with Spotify API. Check your credentials.")
#         return None
#     return data["access_token"]

# token = get_spotify_token()
# headers = {"Authorization": f"Bearer {token}"}


# # FETCH SONGS FROM SPOTIFY

# def fetch_random_songs(query):
#     """Fetch random 10-12 songs from Spotify search."""
#     offset = random.randint(0, 500)  # shuffle results
#     url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=12&offset={offset}"
#     response = requests.get(url, headers=headers).json()
#     return response.get("tracks", {}).get("items", [])

# # def fetch_random_songs(query, limit=10):
# #     """
# #     Fetch random songs from Spotify based on a query keyword (like a cluster theme).
# #     Returns a list of dicts with song name, artist, preview_url, and image.
# #     """
# #     try:
# #         # Randomize offset to get varied results each time
# #         offset = random.randint(0, 100)
# #         url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit={limit}&offset={offset}"
# #         response = requests.get(url, headers=headers).json()

# #         if "tracks" not in response or not response["tracks"]["items"]:
# #             return []

# #         results = []
# #         for item in response["tracks"]["items"]:
# #             results.append({
# #                 "name": item["name"],
# #                 "artist": item["artists"][0]["name"],
# #                 "preview": item.get("preview_url"),
# #                 "image": item["album"]["images"][0]["url"] if item["album"]["images"] else None
# #             })
# #         return results
# #     except Exception as e:
# #         print(f"Error fetching songs: {e}")
# #         return []


# # FETCH SONG PREVIEW FROM SPOTIFY

# def fetch_spotify_preview(song_name, artist_name):
#     """
#     Fetch the preview audio URL from Spotify for a given song and artist.
#     Returns the preview URL if available, else None.
#     """
#     try:
#         query = f"{song_name} {artist_name}"
#         url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1"
#         response = requests.get(url, headers=headers).json()
#         tracks = response.get("tracks", {}).get("items", [])
#         if not tracks:
#             return None
#         return tracks[0].get("preview_url")
#     except Exception as e:
#         print(f"Error fetching preview for {song_name}: {e}")
#         return None


# # SEARCH + CLUSTER PREDICTION USING TRAINED MODEL

# from sklearn.metrics.pairwise import cosine_similarity

# st.markdown("### 🔍 Search Songs by Name")
# user_query = st.text_input("Enter a song name:", "")

# def fetch_spotify_features(song_name):
#     """
#     Fetch audio features + metadata from Spotify for a given song.
#     Handles missing features gracefully and returns a DataFrame of features
#     compatible with your trained scaler and model.
#     """
#     try:
#         query = song_name.strip().replace(" ", "%20")
#         search_url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1"
#         resp = requests.get(search_url, headers=headers).json()

#         tracks = resp.get("tracks", {}).get("items", [])
#         if not tracks:
#             return None

#         # Pick the first valid track
#         track = next((t for t in tracks if t.get("id")), None)
#         if not track:
#             return None

#         track = tracks[0]
#         track_id = track["id"]
#         # features_url = f"https://api.spotify.com/v1/audio-features/{track_id}"
#         features_url = f"https://api.spotify.com/v1/audio-features?ids={track_id}"

#         features_resp = requests.get(features_url, headers=headers).json()

#         if "audio_features" in features_resp and isinstance(features_resp["audio_features"], list):
#             features_data = features_resp["audio_features"][0] or {}
#         else:
#             features_data = features_resp or {}

#         if not isinstance(features_data, dict) or "danceability" not in features_data:
#             print("⚠️ Unexpected Spotify feature format:", features_resp)
#             return {
#                 "name": track["name"],
#                 "artist": track["artists"][0]["name"],
#                 "image": track["album"]["images"][0]["url"] if track["album"]["images"] else None,
#                 "features": pd.DataFrame([{f: 0.0 for f in feature_cols}])
#             }

#         if "error" in features_resp or "audio_features" not in features_resp:
#             alt_url = f"https://api.spotify.com/v1/audio-features?ids={track_id}"
#             alt_resp = requests.get(alt_url, headers=headers).json()
#             if "audio_features" in alt_resp and alt_resp["audio_features"]:
#                 features_resp = alt_resp["audio_features"][0]
#             else:
#                 print("⚠️ Both Spotify feature endpoints failed:", alt_resp)
#                 return None
#         # Define features consistently
#         # feature_cols = [
#         #     "danceability", "energy", "loudness", "speechiness",
#         #     "acousticness", "instrumentalness", "liveness",
#         #     "valence", "tempo", "duration_ms"
#         # ]

#         # Safely extract all features (default to 0 if missing)
#         # features_dict = {f: float(features_resp.get(f, 0)) for f in feature_cols}
#         features_dict = {}
#         for f in feature_cols:
#             val = features_resp.get(f, 0)
#             try:
#                 features_dict[f] = float(val) if val is not None else 0.0
#             except:
#                 features_dict[f] = 0.0

#         features_df = pd.DataFrame([features_dict])

#         features_df = pd.DataFrame([features_dict])

#         return {
#             "name": track["name"],
#             "artist": track["artists"][0]["name"],
#             "preview_url": track.get("preview_url"),
#             "image": track["album"]["images"][0]["url"] if track["album"]["images"] else None,
#             "features": features_df
#         }

#     except Exception as e:
#         print(f"⚠️ Error fetching features for {song_name}: {e}")
#         return None


# # if user_query:
# #     spotify_song = fetch_spotify_features(user_query)
# #     if spotify_song is None:
# #         st.error("❌ Song not found or no audio features available.")
# #     else:
# #         st.markdown(f"## 🎵 {spotify_song['name']} — {spotify_song['artist']}")
# #         if spotify_song["image"]:
# #             st.image(spotify_song["image"], width=300)
# #         if spotify_song["preview_url"]:
# #             st.audio(spotify_song["preview_url"])

# #         # Scale and predict cluster
# #         # X_scaled = scaler.transform([spotify_song["features"]])
# #         # X_df = pd.DataFrame([spotify_song["features"]], columns=feature_cols)

# #         # Scale and predict
# #         # X_scaled = scaler.transform(X_df)
# #         # cluster_label = int(model.predict(X_scaled)[0])
# #         # Ensure input has same feature names for scaler
# #         X_scaled = scaler.transform(spotify_song["features"][feature_cols])



# #         if hasattr(model, "predict"):  # e.g. KMeans
# #             cluster_label = int(model.predict(X_scaled)[0])
# #         else:  # For DBSCAN
# #             # Find nearest cluster center (manual)
# #             cluster_centers = df.groupby("cluster")[feature_cols].mean().values
# #             sims = cosine_similarity(X_scaled, scaler.transform(cluster_centers))[0]
# #             cluster_label = int(np.argmax(sims))

# #         cluster_info = cluster_themes.get(cluster_label, default_theme)
# #         st.success(f"🎧 This song best matches **{cluster_info['name']}** cluster!")

# #         # Show reasoning
# #         st.markdown("### 📊 Audio Profile:")
# #         feature_names = [
# #             "Danceability", "Energy", "Loudness", "Speechiness",
# #             "Acousticness", "Instrumentalness", "Liveness", "Valence", "Tempo", "Duration"
# #         ]
# #         for name, val in zip(feature_names, spotify_song["features"].iloc[0].values):
# #             try:
# #                 val_float = float(val)
# #                 st.markdown(f"- **{name}:** {val_float:.2f}")
# #             except (ValueError, TypeError):
# #                 st.markdown(f"- **{name}:** N/A")

# #         # Show top similar songs
# #         df_scaled = scaler.transform(df[feature_cols])
# #         sims = cosine_similarity(X_scaled, df_scaled)[0]
# #         df["similarity"] = sims
# #         top_similar = df.sort_values("similarity", ascending=False).head(5)

# #         st.markdown("### 🎶 Similar Songs from Dataset:")
# #         for _, row in top_similar.iterrows():
# #             st.markdown(f"- {row['name_song']} — *{row['name_artists']}* ({row['similarity']*100:.2f}% similar)")

# # if user_query:
# #     spotify_song = fetch_spotify_features(user_query)
# #     if spotify_song is None:
# #         st.error("❌ Song not found or no audio features available.")
# #     else:
# #         # 🎵 Show Spotify song details
# #         st.markdown(f"## 🎵 {spotify_song['name']} — {spotify_song['artist']}")
# #         if spotify_song["image"]:
# #             st.image(spotify_song["image"], width=280)

# #         X_scaled = scaler.transform(spotify_song["features"])
# #         cluster_label = int(model.predict(pd.DataFrame(X_scaled, columns=feature_cols))[0])
# #         cluster_info = cluster_themes.get(cluster_label, default_theme)

# #         st.success(f"🎧 This song is classified under **{cluster_info['name']}** cluster!")


# #         # ✅ Show final classification result
# #         # st.success(f"🎧 This song is classified under **{cluster_info['name']}** cluster!")

# #         # 📊 Display measured values
# #         # 🔁 Similar songs from dataset
# #         df_scaled = scaler.transform(df[feature_cols])
# #         sims = cosine_similarity(X_scaled, df_scaled)[0]
# #         df["similarity"] = sims
# #         top_similar = df.sort_values("similarity", ascending=False).head(5)

# #         st.markdown("### 🎶 Most Similar Songs from Your Dataset:")
# #         for _, row in top_similar.iterrows():
# #             st.markdown(f"- {row['name_song']} — *{row['name_artists']}* ({row['similarity']*100:.2f}% similar)")

# if user_query:
    
#     query = user_query.strip().replace(" ", "%20")
#     search_url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1"
#     response = requests.get(search_url, headers=headers).json()

#     tracks = response.get("tracks", {}).get("items", [])
#     if not tracks:
#         st.error("❌ Song not found on Spotify.")
#     else:
#         # Extract metadata
#         track = tracks[0]
#         spotify_name = track["name"]
#         spotify_artist = track["artists"][0]["name"]
#         spotify_img = track["album"]["images"][0]["url"] if track["album"]["images"] else None

#         st.markdown(f"## 🎵 {spotify_name} — {spotify_artist}")
#         if spotify_img:
#             st.image(spotify_img, width=280)

        
#         from difflib import get_close_matches

#         close_match = get_close_matches(spotify_name, df["name_song"].tolist(), n=1, cutoff=0.4)
#         if not close_match:
#             st.warning("⚠️ No close match found in dataset for cluster prediction.")
#         else:
#             matched_song = df[df["name_song"] == close_match[0]].iloc[0]

            
#             # feature_cols = [
#             #     "danceability", "energy", "loudness", "speechiness",
#             #     "acousticness", "instrumentalness", "liveness",
#             #     "valence", "tempo", "duration_ms"
#             # ]
#             # X_features = matched_song[feature_cols].to_numpy().reshape(1, -1)
#             # X_scaled = scaler.transform(X_features)

           
#             # cluster_label = int(model.predict(X_scaled)[0])
#             # cluster_info = cluster_themes.get(cluster_label, default_theme)
            
#             feature_cols = [
#                 "danceability", "energy", "loudness", "speechiness",
#                 "acousticness", "instrumentalness", "liveness",
#                 "valence", "tempo", "duration_ms"
#             ]

#             # Convert to DataFrame to preserve feature names and order
#             X_features_df = pd.DataFrame([matched_song[feature_cols].values], columns=feature_cols)

#             # Debug: show features before scaling
#             st.markdown("#### 🧩 Feature Vector Used for Prediction:")
#             st.dataframe(X_features_df)

#             # Use the exact scaler that was saved with the model
#             try:
#                 X_scaled = scaler.transform(X_features_df)
#             except Exception as e:
#                 st.error(f"⚠️ Scaling failed: {e}")
#                 st.stop()

            
#             # Predict cluster using similarity to cluster centroids (better accuracy)
            
#             try:
#                 # Compute average feature vector for each cluster in your dataset
#                 cluster_means = df.groupby("cluster")[feature_cols].mean()

#                 # Scale both song and cluster means
#                 cluster_means_scaled = scaler.transform(cluster_means)
#                 song_scaled = scaler.transform(X_features_df)

#                 # Calculate cosine similarity
#                 similarities = cosine_similarity(song_scaled, cluster_means_scaled)[0]

#                 # Find the most similar cluster
#                 cluster_label = int(np.argmax(similarities))
#                 cluster_info = cluster_themes.get(cluster_label, default_theme)

#                 st.success(f"🎧 This song best matches **{cluster_info['name']}** cluster!")

#                 # (Optional) Show top 3 similarity scores
#                 top_sim_indices = np.argsort(similarities)[::-1][:3]
#                 st.markdown("#### 🔍 Cluster Similarity Breakdown:")
#                 for i in top_sim_indices:
#                     name = cluster_themes.get(i, default_theme)["name"]
#                     st.markdown(f"- **{name}:** {similarities[i]*100:.2f}% match")

#             except Exception as e:
#                 st.error(f"⚠️ Cluster similarity computation failed: {e}")


            
#             # st.success(f"🎧 This song best matches **{cluster_info['name']}** cluster!")

            
#             # st.markdown("### 📊 Audio Feature Measures (based on dataset match):")
#             # for name, val in zip(feature_cols, matched_song[feature_cols]):
#             #     st.markdown(f"- **{name.capitalize()}:** {float(val):.2f}")

            
#             df_scaled = scaler.transform(df[feature_cols])
#             sims = cosine_similarity(X_scaled, df_scaled)[0]
#             df["similarity"] = sims
#             top_similar = df.sort_values("similarity", ascending=False).head(5)

#             st.markdown("### 🎶 Similar Songs from Dataset:")
#             for _, row in top_similar.iterrows():
#                 st.markdown(f"- {row['name_song']} — *{row['name_artists']}* ({row['similarity']*100:.2f}% similar)")


# # DISPLAY CLUSTERS

# st.subheader("🎼 Browse Clusters as Albums")
# album_cols = st.columns(3)

# for i, cluster_id in enumerate(sorted(df['cluster'].unique())):
#     cluster = cluster_themes.get(int(cluster_id), default_theme)
#     with album_cols[i % 3]:
#         st.image(cluster['img'], width=250)
#         st.markdown(f"<div class='album-title'>{cluster['name']}</div>", unsafe_allow_html=True)
#         if st.button(f"🎧 Explore {cluster['name']}", key=f"cluster_{cluster_id}"):
#             # Every click gets a FRESH recommendation
#             st.session_state['selected_cluster'] = int(cluster_id)
#             st.session_state['cluster_query'] = cluster.get('query', default_theme['query'])
#             st.session_state['recommendations'] = fetch_random_songs(st.session_state['cluster_query'])
#             st.rerun()

# st.markdown("---")


# # SHOW SONG RECOMMENDATIONS

# if 'selected_cluster' in st.session_state and 'recommendations' in st.session_state:
#     cluster_id = st.session_state['selected_cluster']
#     cluster = cluster_themes.get(cluster_id, default_theme)
#     st.markdown(f"## {cluster['name']} 🎶")

#     songs = st.session_state['recommendations']
#     if not songs:
#         st.warning("No songs found. Try again!")
#     else:
#         cols = st.columns(3)
#         for i, track in enumerate(songs[:9]):
#             col = cols[i % 3]
#             with col:
#                 track_name = track['name']
#                 artist_name = track['artists'][0]['name']
#                 img_url = track['album']['images'][0]['url'] if track['album']['images'] else None
#                 preview = track.get('preview_url')

#                 st.image(img_url or "https://upload.wikimedia.org/wikipedia/commons/3/3c/No-album-art-placeholder.png", width=250)
#                 st.markdown(f"<h4>{track_name}</h4><p>{artist_name}</p>", unsafe_allow_html=True)
#                 if preview:
#                     st.audio(preview)
#                 else:
#                     st.caption("🎵 No preview available")

#     # Optional: Shuffle button for fresh set of songs
#     if st.button("🔁 Get New Recommendations"):
#         st.session_state['recommendations'] = fetch_random_songs(st.session_state['cluster_query'])
#         st.rerun()

# st.markdown("---")


# # INSIGHTS & VISUALIZATIONS

# st.subheader("📊 Cluster Insights & Visualizations")

# if st.checkbox("Show All Insights and Visualizations"):
#     feature_cols = [
#         'danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
#         'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms'
#     ]

#     # PCA Visualization
#     st.markdown("### 🌀 PCA 2D Cluster Visualization")
#     try:
#         pca = PCA(n_components=2)
#         pca_result = pca.fit_transform(df[feature_cols])
#         df['pca1'], df['pca2'] = pca_result[:, 0], pca_result[:, 1]
#         fig, ax = plt.subplots(figsize=(8, 6))
#         sns.scatterplot(x='pca1', y='pca2', hue='cluster', data=df, palette='tab10', s=60, alpha=0.8, ax=ax)
#         st.pyplot(fig)
#     except Exception as e:
#         st.warning(f"PCA Visualization skipped: {e}")

#     # Cluster summary heatmap
#     st.markdown("### 🔥 Cluster Feature Averages (Heatmap)")
#     cluster_summary = df.groupby('cluster')[feature_cols].mean().round(2)
#     fig, ax = plt.subplots(figsize=(10, 6))
#     sns.heatmap(cluster_summary, cmap='coolwarm', annot=True, fmt=".2f", ax=ax)
#     st.pyplot(fig)
#     st.dataframe(cluster_summary)

#     # Cluster size distribution
#     st.markdown("### 🎧 Cluster Size Distribution")
#     fig, ax = plt.subplots(figsize=(7, 5))
#     df['cluster'].value_counts().sort_index().plot(kind='bar', color='skyblue', ax=ax)
#     plt.xlabel("Cluster")
#     plt.ylabel("Number of Songs")
#     st.pyplot(fig)

#     # Feature correlation heatmap
#     st.markdown("### 🧠 Feature Correlation Heatmap")
#     fig, ax = plt.subplots(figsize=(10, 6))
#     sns.heatmap(df[feature_cols].corr(), cmap='viridis', annot=True, fmt=".2f", ax=ax)
#     st.pyplot(fig)

#     # Boxplot feature comparison
#     st.markdown("### 🎚️ Compare Feature Distribution by Cluster")
#     selected_feature = st.selectbox("Select a feature:", feature_cols)
#     fig, ax = plt.subplots(figsize=(8, 5))
#     sns.boxplot(x='cluster', y=selected_feature, data=df, palette='Set2', ax=ax)
#     st.pyplot(fig)

#     # Radar chart for each cluster
#     st.markdown("### 🕸️ Cluster Profile (Radar Chart)")
#     try:
#         from math import pi
#         cluster_norm = (cluster_summary - cluster_summary.min()) / (cluster_summary.max() - cluster_summary.min())
#         for i in cluster_norm.index:
#             values = cluster_norm.loc[i].tolist()
#             labels = cluster_norm.columns.tolist()
#             values += values[:1]
#             angles = [n / float(len(labels)) * 2 * pi for n in range(len(labels))]
#             angles += angles[:1]

#             fig = plt.figure(figsize=(5, 5))
#             ax = plt.subplot(111, polar=True)
#             plt.xticks(angles[:-1], labels, color='white', size=8)
#             ax.plot(angles, values, linewidth=2, linestyle='solid', label=f'Cluster {i}')
#             ax.fill(angles, values, alpha=0.25)
#             plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
#             st.pyplot(fig)
#     except Exception as e:
#         st.warning(f"Radar Chart skipped: {e}")

# st.markdown("---")


# # EXPORT DATA

# csv = df.to_csv(index=False).encode('utf-8')
# st.download_button("💾 Download Final Clustered Dataset", csv, "clustered_songs_final.csv", "text/csv")


import requests, base64, streamlit as st

# --- SPOTIFY CLIENT INFO ---
client_id = st.secrets["spotify"]["client_id"]
client_secret = st.secrets["spotify"]["client_secret"]

auth_str = f"{client_id}:{client_secret}"
b64_auth_str = base64.b64encode(auth_str.encode()).decode()
token_resp = requests.post(
    "https://accounts.spotify.com/api/token",
    headers={"Authorization": f"Basic {b64_auth_str}"},
    data={"grant_type": "client_credentials"}
).json()

token = token_resp.get("access_token")
headers = {"Authorization": f"Bearer {token}"}

# --- SONG SEARCH ---
song_name = "Lover Taylor Swift"
search_url = f"https://api.spotify.com/v1/search?q={song_name.replace(' ', '%20')}&type=track&limit=1"
track_resp = requests.get(search_url, headers=headers).json()
st.write("🎯 TRACK SEARCH RESPONSE:", track_resp)

try:
    track_id = track_resp["tracks"]["items"][0]["id"]
    st.write("✅ Found Track ID:", track_id)
except Exception as e:
    st.write("❌ Could not extract track ID:", e)

# --- AUDIO FEATURE TEST ---
features_url = f"https://api.spotify.com/v1/audio-features?ids={track_id}"
feat_resp = requests.get(features_url, headers=headers).json()
st.write("🎧 RAW AUDIO FEATURES RESPONSE:", feat_resp)