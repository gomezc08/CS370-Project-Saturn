import os
import librosa
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from kneed import KneeLocator


class AudioClustering:
    def __init__(self, audio_dir="sounds/", sr=22050, n_mfcc=13):
        self.audio_dir = audio_dir
        self.sr = sr
        self.n_mfcc = n_mfcc
        # Supported audio formats by librosa
        self.audioFormats = [
            ".wav",
            ".mp3",
            ".ogg",
            ".flac",
            ".m4a",
            ".wma",
            ".aiff",
            ".alac",
            ".aac",
            ".amr",
            ".au",
            ".awb",
            ".dct",
            ".dss",
            ".dvf",
            ".gsm",
            ".iklax",
            ".ivs",
            ".m4p",
            ".mmf",
            ".mpc",
            ".msv",
            ".nmf",
            ".nsf",
            ".oga",
            ".mogg",
            ".opus",
            ".ra",
            ".rm",
            ".raw",
            ".sln",
            ".tta",
            ".vox",
            ".wv",
            ".webm",
            ".8svx",
        ]

    def extract_mfcc(self, audio_file):
        """
        Extracts Mel-Frequency Cepstral Coefficients (MFCC) features from an audio file.

        Parameters:
        - audio_file: Path to the audio file

        Returns:
        - mfcc_features: Extracted MFCC features
        """
        # Load audio file
        y, sr = librosa.load(audio_file, sr=self.sr)

        # Extract MFCC features
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=self.n_mfcc)

        # Compute the mean of each MFCC coefficient over time
        mfcc_features = np.mean(mfcc, axis=1)

        return mfcc_features

    def get_optimal_epsilon(self, min_pts=5):
        # List all audio files in the directory
        audio_files = [
            os.path.join(self.audio_dir, file)
            for file in os.listdir(self.audio_dir)
            if file.endswith(tuple(self.audioFormats))
        ]

        # Extract MFCC features for all audio files
        mfcc_features_list = [
            self.extract_mfcc(audio_file) for audio_file in audio_files
        ]

        # Convert the list of features into a numpy array
        X = np.array(mfcc_features_list)

        # Preprocessing: Scale the features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Compute the k-distance graph
        nbrs = NearestNeighbors(n_neighbors=min_pts).fit(X_scaled)
        distances, indices = nbrs.kneighbors(X_scaled)

        # Sort distances and plot the graph
        distances = np.sort(distances, axis=0)
        distances = distances[
            :, 1
        ]  # consider only the distances to the second nearest neighbor

        # Plot the graph to find the knee point
        kneedle = KneeLocator(
            np.arange(len(distances)), distances, curve="convex", direction="increasing"
        )
        optimal_epsilon_index = kneedle.elbow
        optimal_epsilon = distances[optimal_epsilon_index]

        return optimal_epsilon

    def cluster_audio_files(
        self, eps=0.5, min_samples=2
    ):  # we can up min_samples when we have more audio files
        # List all audio files in the directory              but its better to keep it low for now
        audio_files = [
            os.path.join(self.audio_dir, file)
            for file in os.listdir(self.audio_dir)
            if file.endswith(tuple(self.audioFormats))
        ]

        # Extract MFCC features for all audio files
        mfcc_features_list = [
            self.extract_mfcc(audio_file) for audio_file in audio_files
        ]

        # Convert the list of features into a numpy array
        X = np.array(mfcc_features_list)

        # Preprocessing: Scale the features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Clustering
        # Using DBSCAN
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        cluster_labels = dbscan.fit_predict(X_scaled)

        # Group audio files based on cluster labels
        clusters = {}
        for i, label in enumerate(cluster_labels):
            filename = os.path.basename(audio_files[i])
            if label not in clusters:
                clusters[label] = [filename]
            else:
                clusters[label].append(filename)

        return clusters


if __name__ == "__main__":
    clustering = AudioClustering()
    epsilon = clustering.get_optimal_epsilon()
    clusters = clustering.cluster_audio_files(eps=epsilon)
    print(clusters)
