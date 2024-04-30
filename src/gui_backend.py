import sys
import pydub.playback as p
from pydub import AudioSegment
import random as r

sys.path.append("src")
from ml import AudioClustering
from database.PlaylistManager import PlaylistManager


class Backend:
    """
    Backend class for audio manipulation and playback.

    Attributes:
        audioSegment (AudioSegment): Original audio segment.
        changedAudioSegment (AudioSegment): Modified audio segment.
        reversed (bool): Flag indicating if the audio is reversed.
    """

    audioSegment = None
    hangedAudioSegment = None


    def __init__(self):
        """
        Initializes the Backend with the given audio file.

        Args:
            audio_file (str): Path to the audio file.
        """

        self.reversed = False

    def getInstance():
        """
        if an instance of already exists, return it
        otherwise, create a new instance
        """
        if not hasattr(Backend, "_instance"):
            Backend._instance = Backend()
        return Backend._instance

    def auto_cluster_audio_files():
        """
        Automatically clusters audio files and creates playlists based on the clusters.
        Deletes any existing playlists with 'cluster' in the name.
        """
        # TODO: uncomment this when AudioClustering is fixed
        clustering = AudioClustering()
        playlistManager = PlaylistManager()

        # Delete all playlists that have 'cluster' in the name anywhere
        for playlist in playlistManager.view_playlists():
            if "cluster" in playlist:
                playlistManager.delete_playlist(playlist)

        epsilon = clustering.get_optimal_epsilon()

        # call this with different min_samples values when we have more audio files
        clusters = clustering.cluster_audio_files(eps=epsilon)

        for cluster_name in clusters.keys():
            playlist_cluster_name = "cluster_" + str(cluster_name)
            playlistManager.create_playlist(playlist_cluster_name)
            for sound in clusters[cluster_name]:
                sound_name = sound.split(".")[0]
                playlistManager.add_sound_into_playlist(
                    sound_name, playlist_cluster_name
                )

    def load_audio(self, audio_file):
        """
        Loads the audio file into the Backend.

        Args:
            audio_file (str): Path to the audio file.
        """
        self.audioSegment = AudioSegment.from_file(audio_file)
        self.changedAudioSegment = self.audioSegment

    def modify_speed(self, change_amnt):
        """
        Modifies the playback speed of the audio.

        Args:
            change_amnt (float): Amount of speed change.
        """
        # This should work ?
        self.changedAudioSegment = self.changedAudioSegment.speedup(
            playback_speed=change_amnt
        )

    def modify_pitch(self, change_amnt):
        """
        Modifies the pitch of the audio.

        Args:
            change_amnt (float): Amount of pitch change.
        """
        # This should work ?
        self.changedAudioSegment = self.changedAudioSegment.set_frame_rate(
            self.changedAudioSegment.frame_rate * change_amnt
        )

    def reverse(self):
        """
        Toggles the reversed attribute and reverses the audio segment.
        """
        if self.reversed == False:
            self.reversed = True
            self.changedAudioSegment = self.changedAudioSegment.reverse()
        if self.reversed == True:
            self.reversed = False
            self.changedAudioSegment = self.changedAudioSegment.reverse()

    def revert(self):
        """
        Reverts the audio to its original state.
        """
        self.changedAudioSegment = self.audioSegment
        if self.reversed == True:
            self.reversed = False

    def play_modified_audio(self):
        """
        Plays the modified audio.
        """
        p.play(self.changedAudioSegment)

    def play_audio_file(audio_file):
        sound = AudioSegment.from_file(audio_file, format=audio_file.split(".")[-1])
        p.play(sound)

    def save(self, name):
        """
        Saves the modified audio to a file.

        Args:
            name (str): Name of the output file.
        """
        self.changedAudioSegment.export(name, format="wav")

    def overlap(self, audio_file):
        """
        Overlaps the modified audio with another audio file.

        Args:
            audio_file (AudioSegment): Audio segment to overlap with.
        """
        self.changedAudioSegment.overlay(audio_file)

    def concatentate(self, audio_file, crossfade_value):
        """
        Concatenates the modified audio with another audio file.

        Args:
            audio_file (AudioSegment): Audio segment to concatenate.
            crossfade_value (int): Crossfade duration in milliseconds.
        """
        # This should work, adapted straight from saturn
        self.changedAudioSegment.append(audio_file, crossfade=crossfade_value)

    def randomInsert(self, audio_file):
        """
        Inserts another audio file randomly into the modified audio.

        Args:
            audio_file (AudioSegment): Audio segment to insert.
        """
        length = len(self.changedAudioSegment)

        # Get random time to insert
        random_time = r.randint(0, length)

        # Insert the audio file at the random time
        tempAudioSegment = self.changedAudioSegment[:random_time]
        tempAudioSegment.append(audio_file)
        tempAudioSegment.append(self.changedAudioSegment[random_time:])

        self.changedAudioSegment = tempAudioSegment

    def compile_audio(self, speed_val = 1, pitch_val = 1, reverse = False, overlap = None, concate = None, randInsert = None):
        # load file.
        self.load_audio()
        
        # go through and edit em.
        if speed_val != 1:
            self.modify_speed(speed_val)
        
        if pitch_val != 1:
            self.modify_pitch()
        
        if not reverse:
            self.reverse()
        
        if overlap != None:  
            self.overlap(overlap)
        
        if concate != None:  
            self.concatentate(concate)
                
        if randInsert != None:
            self.randomInsert(randInsert)