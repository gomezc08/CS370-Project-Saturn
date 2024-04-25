import os
import librosa
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering

class AudioClustering:
    def __init__(self, audio_dir="sounds/", sr=22050, n_mfcc=13):
        self.audio_dir = audio_dir
        self.sr = sr
        self.n_mfcc = n_mfcc
        # TODO: find the audio formats that librosa can read
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

    def cluster_audio_files(self, n_clusters=3, linkage="ward"):
        # List all audio files in the directory
        audio_files = [
            os.path.join(self.audio_dir, file) for file in os.listdir(self.audio_dir)
        ]

        # Extract MFCC features for all audio files
        # There is no reason for this to fail (since audioread depends on ffmpeg),
        # but it does on ogg files.
        mfcc_features_list = [
            self.extract_mfcc(audio_file)
            for audio_file in audio_files
            if not audio_file.endswith(tuple(self.audioFormats))
        ]

        # Convert the list of features into a numpy array
        X = np.array(mfcc_features_list)

        # Preprocessing: Scale the features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Clustering
        # Using hierarchical clustering
        agg_clustering = AgglomerativeClustering(
            n_clusters=n_clusters, linkage=linkage
        )  # You can adjust the number of clusters and linkage method
        cluster_labels = agg_clustering.fit_predict(X_scaled)

        # Group audio files based on cluster labels
        clusters = {}
        for i, label in enumerate(cluster_labels):
            filename = os.path.basename(audio_files[i])
            if label not in clusters:
                clusters[label] = [filename]
            else:
                clusters[label].append(filename)

        # Get audio files that did not get clustered
        unclustered_files = [
            audio_files[i] for i, label in enumerate(cluster_labels) if label == -1
        ]

        # Create a new cluster for unclustered files
        if unclustered_files:
            clusters["unclustered"] = [
                os.path.basename(file) for file in unclustered_files
            ]

        return clusters
