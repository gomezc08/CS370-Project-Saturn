import sys
import pydub.playback as p

sys.path.append("src")
from saturn_cli import Saturn
from ml import AudioClustering
from database.PlaylistManager import PlaylistManager


class Backend:
    def __init__(self, audio_file):
        clustering = AudioClustering()
        self.saturn = Saturn.getInstance(sys.argv, len(sys.argv))
        playlistManager = PlaylistManager()

        # Delete all playlists that have 'cluster' in the name anywhere
        for playlist in playlistManager.view_playlists():
            if "cluster" in playlist:
                playlistManager.delete_playlist(playlist)

        clusters = clustering.cluster_audio_files()

        for cluster_name in clusters.keys():
            playlistManager.create_playlist(cluster_name)
            for sound in clusters[cluster_name]:
                playlistManager.add_sound_into_playlist(self, sound, cluster_name)

        self.audioSegment = None
        self.changedAudioSegment = None

        self.reversed = False

        self.load_audio(audio_file)

    def load_audio(self, audio_file):
        self.audioSegment = self.saturn.getSound(audio_file)
        self.changedAudioSegment = self.audioSegment

    def modify_speed(self, change_amnt):
        # TODO: This likely won't work.
        self.changedAudioSegment = self.audioSegment.speedup(playback_speed=change_amnt)

    def modify_pitch(self, change_amnt):
        # TODO: This likely won't work.
        self.changedAudioSegment = self.audioSegment.pitch_change(semitones=change_amnt)

    def reverse(self):
        if self.reversed == False:
            self.reversed = True
            self.changedAudioSegment = self.audioSegment.reverse()
        if self.reversed == True:
            self.reversed = False
            self.changedAudioSegment = self.audioSegment.reverse()

    def revert(self):
        self.changedAudioSegment = self.audioSegment

    def play(self):
        p.play(self.changedAudioSegment)

    def save(self, name):
        self.changedAudioSegment.export(name, format="wav")

    def overlap(self):
        pass

    def concatentate(self):
        pass

    def randomInsert(self):
        # Need to have a check for the audio to be inserted is longer than select audio
        pass
