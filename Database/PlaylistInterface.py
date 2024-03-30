from PlaylistEditor import PlaylistEditor
import sys
import os

parent_dir = os.path.dirname(os.getcwd())
print(parent_dir)
sys.path.insert(0, parent_dir + "/src")
from saturn_cli import CommandLineParser

class PlaylistInterface():
    """
    Represents the interaction between the user and the playlists.
    
    Attributes:
        playlist_manager (PlaylistManager): An instance of the PlaylistManager class.

    Methods:
        __init__(self):
            Initializes the PlaylistInterface with a PlaylistManager instance.
        
        sort_playlist():
            Sorts the playlist by sound title, length, or date added to playlist.
    """
    
    def __init__(self, playlist_list):
        # composition relationship.
        self.playlist_manager = PlaylistEditor("../sounds")
        self.sort_type = {"Title", "Length", "DateCreated"}
        self.playlist_list = playlist_list
    
    def sort_playlist(self, sort_name):
        # verify sort_name is valid.
        if sort_name not in self.sort_type:
            raise Exception(f'Invalid sorting name: {sort_name}')
        
        # OPEN CONNECTION.
        self.playlist_manager.open_connection()
        
        # sort playlist (database here).
        self.playlist_manager.cursor.execute(f"SELECT * FROM soundlist ORDER BY {sort_name}")
        results = self.playlist_manager.cursor.fetchall()
        for result in results:
            print(result)
        #self.playlist_manager.cnx.commit()
        
        # CLOSE CONNECTION.
        self.playlist_manager.close_connection()
    
    def create_playlist(self, playlist_name):
        if playlist_name not in self.playlist_list:
            self.playlist_list.append(playlist_name)
    
    def get_playlist_list(self):
        return self.playlist_list
    
    def play_sound_in_playlist(self, sound_title, sound_playlist):
        # verify sound_title and sound_playlist valid.
        #if sound_playlist not in self.playlist_list:
         #   raise Exception("Invalid title or playlist was entered.")
        
        # play the sound.
        parser = CommandLineParser(sys.argv)
        parser.play(parent_dir + "/sounds/" + sound_title + ".wav")
        
        
if __name__ == "__main__":
    # create a command line parser and parse the command line arguments
    playlist = PlaylistInterface([])
    playlist_manager = PlaylistEditor("../sounds")
    
    
    # commands to run.
    #playlist_manager.init_playlist()
    #playlist.play_sound_in_playlist("toaster", "N/A")
    
    
    # we can sort based on Title, Length, and DateCreated.
    #playlist.sort_playlist("Title")