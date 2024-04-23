import os
import librosa
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score


def extract_mfcc(audio_file, sr=22050, n_mfcc=13):
    """
    Extracts Mel-Frequency Cepstral Coefficients (MFCC) features from an audio file.

    Parameters:
    - audio_file: Path to the audio file
    - sr: Sampling rate (default: 22050 Hz)
    - n_mfcc: Number of MFCC coefficients to extract (default: 13)

    Returns:
    - mfcc_features: Extracted MFCC features
    """
    # Load audio file
    y, sr = librosa.load(audio_file, sr=sr)

    # Extract MFCC features
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)

    # Compute the mean of each MFCC coefficient over time
    mfcc_features = np.mean(mfcc, axis=1)

    return mfcc_features


# Directory containing audio files
audio_dir = "sounds/"


print(extract_mfcc("sounds/coffee.wav"))

# List all audio files in the directory
audio_files = [os.path.join(audio_dir, file) for file in os.listdir(audio_dir)]

print(audio_files)

# Extract MFCC features for all audio files
mfcc_features_list = [extract_mfcc(audio_file) for audio_file in audio_files if audio_file.endswith(".wav") or audio_file.endswith(".mp3")]

# Convert the list of features into a numpy array
X = np.array(mfcc_features_list)

# Preprocessing: Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Clustering
# Using hierarchical clustering
agg_clustering = AgglomerativeClustering(
    n_clusters=3, linkage="ward"
)  # You can adjust the number of clusters and linkage method
cluster_labels = agg_clustering.fit_predict(X_scaled)

# Evaluation
silhouette_avg = silhouette_score(X_scaled, cluster_labels)
print("Silhouette Score:", silhouette_avg)

# Group audio files based on cluster labels
clusters = {}
for i, label in enumerate(cluster_labels):
    filename = os.path.basename(audio_files[i])
    if label not in clusters:
        clusters[label] = [filename]
    else:
        clusters[label].append(filename)

# Print filenames in each cluster
for cluster_label, filenames in clusters.items():
    print(f"Cluster {cluster_label}:")
    for filename in filenames:
        print(filename)
    print()
