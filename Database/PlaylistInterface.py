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
        sort_type (dict): A dictionary containing different ways to sort a playlist. Keys represent sort options, and values provide descriptions or implementations of the sorting method.
        playlist_list(list): A list containing playlists. Each element in the list represents a playlist.

    Methods:
        sort_playlist: Sorts the playlist by sound title, length, or date added to playlist.
        create_playlist: Creates a new playlist name. The new playlist name is added to playlist_list.
        play_sound_in_playlist: Plays a sound from one of the playlists. Plays using the play method in our CommandLineParser class
        add_sound_into_playlist: Adds a sound into a defined playlist.
        remove_sound_from_playlist: Removes a sound from a defined playlist.
        view_playlist: Displays all the songs from a requested playlist.
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
    
    def play_sound_in_playlist(self, sound_title, sound_playlist):
        # verify sound_title and sound_playlist valid.
        if sound_title not in self.playlist_manager.sound_list or sound_playlist not in self.playlist_list:
            raise Exception(f'Invalid sound name: {sound_title} or playlist name: {sound_playlist}')
        
        # play the sound.
        parser = CommandLineParser(sys.argv)
        parser.play(parent_dir + "/sounds/" + sound_title + ".wav")
        
    def add_sound_into_playlist(self, sound_title, sound_playlist):
        # verify sound_title, sound_playlist exits.
        if sound_title not in self.playlist_manager.sound_list or sound_playlist not in self.playlist_list:
            raise Exception(f'Invalid sound name: {sound_title} or playlist name: {sound_playlist}')
        
        # TODO: verify sound_title not already in sound_playlist; database lookup.
        
        # insert it.
        self.playlist_manager.open_connection()
        query = "INSERT INTO soundplaylistsinfo (SoundTitle, PlaylistTitle) VALUES (%s, %s)"
        values = (sound_title, sound_playlist)
        try:
            self.playlist_manager.open_connection()
            self.playlist_manager.cursor.execute(query, values)
            self.playlist_manager.cnx.commit()
        except Exception as e:
            print(f"Error adding sound to playlist: {e}")
        finally:
            self.playlist_manager.close_connection()
            
    def remove_sound_from_playlist(self, sound_title, sound_playlist):
        # verify sound_title and sound_playlist valid.
        if sound_title not in self.playlist_manager.sound_list or sound_playlist not in self.playlist_list:
            raise Exception(f'Invalid sound name: {sound_title} or playlist name: {sound_playlist}')
        
    def view_playlist(self, playlist_title):
        # verify playlist is valid.
        if playlist_title not in self.playlist_list:
            raise Exception(f'Invalid playlist: {playlist_title}')
        
        # display all sounds in playlist_title.
        query = ("SELECT SoundTitle FROM soundplaylistsinfo WHERE PlaylistTitle = %s")
        try:
            self.playlist_manager.open_connection()
            self.playlist_manager.cursor.execute(query, (playlist_title,))
            result = self.playlist_manager.cursor.fetchone()
            print(result)
            self.playlist_manager.cnx.commit()
        
        except Exception as e:
            print(f"Error showing playlist: {e}")
        
        finally:
            self.playlist_manager.close_connection()
        
if __name__ == "__main__":
    # create a command line parser and parse the command line arguments
    playlist = PlaylistInterface(["Liked"])
    playlist_manager = PlaylistEditor("../sounds")
    
    
    
    # commands to run.
    #playlist_manager.init_playlist()
    #print(playlist.playlist_list)
    #playlist.view_playlist("Liked")
    #playlist.play_sound_in_playlist("toaster", "N/A")
    
    # playlist.add_sound_into_playlist("coffee-slurp-2", "Liked")
    
    # we can sort based on Title, Length, and DateCreated.
    #playlist.sort_playlist("Title")