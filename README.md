# 🎵 Amazon Music Clustering — Streamlit App

## 📘 Overview
**Amazon Music Clustering** is a data-driven music recommendation project that groups songs into **meaningful clusters** based on their **audio features** such as energy, tempo, danceability, and valence.  

The goal is to **analyze music characteristics** and create a system that:
- Groups songs that sound similar.  
- Helps users explore songs like in **Amazon Music / Spotify playlists**.  
- Recommends fresh tracks dynamically from **Spotify API** based on cluster mood and theme.  
- Visualizes musical trends using advanced data insights.  

This project integrates **Machine Learning (Clustering)**, **Spotify API**, and an interactive **Streamlit Web App** for a rich exploration experience.

---

## 🌟 Key Features
✅ **Automatic Song Clustering:** Groups songs based on their acoustic and rhythmic properties.  
✅ **Spotify-Powered Recommendations:** Fetches real songs & previews dynamically.  
✅ **Interactive Streamlit UI:** Explore clusters like “Party Hits” or “Chill Vibes” with audio previews.  
✅ **Visual Insights:** PCA plots, heatmaps, feature analysis, and radar charts for deep understanding.  
✅ **Ready-to-Run:** Uses your cleaned dataset (`clustered_songs_final.csv`) directly without file upload.  

---

## 🧠 Project Workflow

### 1️⃣ Data Preprocessing
- Started with a cleaned dataset of songs containing features like:
  - `danceability`, `energy`, `loudness`, `speechiness`, `acousticness`, `valence`, `tempo`, etc.  
- Standardized and scaled these values for better clustering performance.  

### 2️⃣ Clustering
- Applied **K-Means Clustering** to group songs based on audio similarity.  
- Each cluster reflects a distinct **mood or genre** pattern (like Spotify’s playlist logic).  

| Cluster | Theme | Description |
|----------|--------|-------------|
| 0 | 🔥 Party & Dance Hits | High energy, loud, rhythmic — perfect for parties. |
| 1 | 🌙 Chill Acoustic Vibes | Calm, soothing acoustic music for relaxation. |
| 2 | 💥 Energetic Pop Beats | Upbeat pop songs with vibrant tempos. |
| 3 | 🎸 Indie & Alternative | Raw, emotional indie and alternative tracks. |
| 4 | 🎹 Instrumental Lounge | Lofi, background, and instrumental beats. |
| 5 | ❤️ Romantic & Soft Songs | Emotional, soft ballads for relaxation or romance. |

---

## 📊 Insights & Visualizations

The app includes a rich **Insights Dashboard**:
- 🌀 **PCA Scatter Plot:** Shows how clusters separate in 2D space.  
- 🔥 **Cluster Feature Heatmap:** Average feature intensity per cluster.  
- 🎧 **Cluster Size Distribution:** Visual breakdown of songs per cluster.  
- 🧠 **Feature Correlation Heatmap:** Finds relationships among features.  
- 🎚️ **Boxplots:** Compare feature distributions across clusters.  
- 🕸️ **Radar Charts:** Visualize each cluster’s personality (e.g., energy vs. acousticness).  

---

## 🧩 How the Spotify Integration Works

Each cluster is assigned a **Spotify search query keyword**, like “party pop hits” or “romantic love songs.”  
When a cluster is selected:
1. The app queries **Spotify’s Track Search API**.  
2. Randomized results (top trending tracks) are fetched dynamically.  
3. Each song’s **cover image, title, artist name, and preview** is displayed.  

---

## 💻 Technologies Used

| Category | Tools |
|-----------|-------|
| Programming Language | Python |
| Frontend Framework | Streamlit |
| APIs | Spotify Web API |
| Machine Learning | K-Means, PCA |
| Visualization | Matplotlib, Seaborn |
| Data Handling | Pandas, NumPy |

---

## ⚙️ Installation & Setup Guide

Follow these steps to run the project on your system:

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Amazon-Music-Clustering.git
cd Amazon-Music-Clustering
```
### 2. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate       # For Linux/Mac
# OR
.venv\Scripts\activate          # For Windows
```
### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```
### 4. Setup Spotify API Credentials

- 1.Go to the Spotify Developer Dashboard
- 2. Click “Create an App” → Give it any name
- 3. Copy your Client ID and Client Secret
- 4. Create a folder named .streamlit in your project directory and add a file called secrets.toml:
```bash
[spotify]
client_id = "your_spotify_client_id_here"
client_secret = "your_spotify_client_secret_here"
```
### 6. Run the Streamlit App
```bash
streamlit run app.py
```
