import sys
import pydub.playback as p
from pydub import AudioSegment

import random as r

sys.path.append("src")
from src.ml import AudioClustering
from database.PlaylistManager import PlaylistManager


class Backend:
    def __init__(self, audio_file):
        # TODO: uncomment this when AudioClustering is fixed
        # clustering = AudioClustering()
        playlistManager = PlaylistManager()

        # Delete all playlists that have 'cluster' in the name anywhere
        for playlist in playlistManager.view_playlists():
            if "cluster" in playlist:
                playlistManager.delete_playlist(playlist)

        """
        clusters = clustering.cluster_audio_files()

        for cluster_name in clusters.keys():
            playlistManager.create_playlist(cluster_name)
            for sound in clusters[cluster_name]:
                playlistManager.add_sound_into_playlist(self, sound, cluster_name)
        """

        self.audioSegment = None
        self.changedAudioSegment = None

        self.reversed = False

        self.load_audio(audio_file)

        self.overlain = False

    def load_audio(self, audio_file):
        self.audioSegment = AudioSegment.from_file(audio_file)
        self.changedAudioSegment = self.audioSegment

    def modify_speed(self, change_amnt):
        # TODO: This likely won't work.
        self.changedAudioSegment = self.changedAudioSegment.speedup(
            playback_speed=change_amnt
        )

    def modify_pitch(self, change_amnt):
        # TODO: This likely won't work.
        self.changedAudioSegment = self.changedAudioSegment.pitch_change(
            semitones=change_amnt
        )

    def reverse(self):
        if self.reversed == False:
            self.reversed = True
            self.changedAudioSegment = self.changedAudioSegment.reverse()
        if self.reversed == True:
            self.reversed = False
            self.changedAudioSegment = self.changedAudioSegment.reverse()

    def revert(self):
        self.changedAudioSegment = self.audioSegment

    def play(self):
        p.play(self.changedAudioSegment)

    def save(self, name):
        self.changedAudioSegment.export(name, format="wav")

    def overlap(self, audio_file):
        # This should work as well
        self.changedAudioSegment.overlay(audio_file)

    def concatentate(self, audio_file, crossfade_value):
        # This should work, adapted straight from saturn
        self.changedAudioSegment.append(audio_file, crossfade=crossfade_value)

    def randomInsert(self, audio_file):
        length = len(self.changedAudioSegment)

        # Get random time to insert
        random_time = r.randint(0, length)

        # Insert the audio file at the random time
        tempAudioSegment = self.changedAudioSegment[:random_time]
        tempAudioSegment.append(audio_file)
        tempAudioSegment.append(self.changedAudioSegment[random_time:])

        self.changedAudioSegment = tempAudioSegment
