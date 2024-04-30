from database.DBConnector import DBConnector
import sys
import os

parent_dir = os.path.dirname(os.getcwd())
sys.path.insert(0, parent_dir + "/src")
from saturn_cli import CommandLineParser


class PlaylistManager:
    """
    Focuses on handling playlist-related operations within the sound archive system, such as creating, modifying, and deleting playlists.

    Attributes:
        connector (PlaylistManager): An instance of the PlaylistManager class.
        sort_type (dict): A dictionary conPtaining different ways to sort a playlist. Keys represent sort options, and values provide descriptions or implementations of the sorting method.
        playlist_list(list): A list containing playlists. Each element in the list represents a playlist.

    Methods:
        view_sort_playlist: Sorts and displays the playlist by sound title, length, or date added to playlist.
        view_playlists: Displays each playlist title.
        create_playlist: Creates a new playlist name. The new playlist name is added to playlist_list.
        delete_playlist: Deletes a playlist.
        play_sound_in_playlist: Plays a sound from one of the playlists. Plays using the play method in our CommandLineParser class
        add_sound_into_playlist: Adds a sound into a defined playlist.
        remove_sound_from_playlist: Removes a sound from a defined playlist.
    """

    def __init__(self):
        # composition relationship.
        self.connector = DBConnector("sounds")
        self.sort_type = {"Title", "Length", "DateCreated"}

    def view_sort_playlist(self, playlist_title, sort_name=None):
        # Verify playlist is valid.
        # if playlist_title not in self.playlist_list:
        #   raise Exception(f"Invalid playlist: {playlist_title}")

        playlist_list = []
        # OPEN CONNECTION
        self.connector.open_connection()

        try:
            # Sort playlist.
            if sort_name:
                # Verify sort_name is valid.
                if sort_name not in self.sort_type:
                    raise Exception(f"Invalid sorting name: {sort_name}")

                query = (
                    "SELECT spi.soundtitle "
                    "FROM soundplaylistsinfo spi "
                    "JOIN soundlist sl ON spi.soundtitle = sl.title "
                    f"WHERE spi.playlisttitle = '{playlist_title}' "
                    f"ORDER BY sl.{sort_name}"
                )

                self.connector.cursor.execute(query)
                print("test2")
            else:
                # Display all sounds in playlist_title.
                query = (
                    "SELECT SoundTitle FROM soundplaylistsinfo WHERE PlaylistTitle = %s"
                )
                self.connector.cursor.execute(query, (playlist_title,))

            results = self.connector.cursor.fetchall()
            for result in results:
                playlist_list.append(result)
                print(result)
            # self.connector.cnx.commit()  # Uncomment if needed.
        except Exception as e:
            print(f"Error showing playlist: {e}")

        finally:
            # CLOSE CONNECTION.
            self.connector.close_connection()

        return playlist_list

    def view_playlists(self):
        playlists = []
        self.connector.open_connection()
        try:
            query = "SELECT * FROM playlistnames"
            self.connector.cursor.execute(query)
            # self.connector.cnx.commit()
            results = self.connector.cursor.fetchall()
            for result in results:
                playlists.append(result)

        except Exception:
            print(f"Error loading playlists")

        finally:
            self.connector.close_connection()

        return playlists

    def create_playlist(self, playlist_name):
        # if playlist_name not in self.playlist_list:
        #   self.playlist_list.append(playlist_name)

        self.connector.open_connection()

        try:
            query = "INSERT INTO playlistnames (Name) VALUES (%s)"
            self.connector.cursor.execute(query, (playlist_name,))
            self.connector.cnx.commit()

        except Exception as e:
            print(f"Error adding playlist: {e}")

        finally:
            self.connector.close_connection()

    def delete_playlist(self, playlist_name):
        # delete from playlistsname.
        self.connector.open_connection()

        try:
            query = "DELETE FROM playlistnames WHERE (Name) = %s"
            self.connector.cursor.execute(query, (playlist_name,))
            self.connector.cnx.commit()

        except Exception as e:
            print(f"Error deleting playlist: {e}")

        finally:
            self.connector.close_connection()

        # delete from soundplaylistsinfo.
        self.connector.open_connection()

        try:
            query = "DELETE FROM soundplaylistsinfo WHERE (PlaylistTitle) = %s"
            self.connector.cursor.execute(query, (playlist_name,))
            self.connector.cnx.commit()

        except Exception as e:
            print(f"Error deleting playlist: {e}")

        finally:
            self.connector.close_connection()

    def play_sound_in_playlist(self, sound_title, sound_playlist):
        # verify sound_title and sound_playlist valid.
        """
        if sound_title not in self.connector.sound_list:
            raise Exception(f"Invalid sound name: {sound_title}")

        if sound_playlist not in self.playlist_list:
            raise Exception(f"Invalid playlist name: {sound_playlist}")
        """
        # play the sound.
        parser = CommandLineParser(sys.argv)
        parser.play(parent_dir + "/sounds/" + sound_title + ".wav")

    def add_sound_into_playlist(self, sound_title, sound_playlist):
        # insert it.
        self.connector.open_connection()
        query = (
            "INSERT INTO soundplaylistsinfo (SoundTitle, PlaylistTitle) VALUES (%s, %s)"
        )
        values = (sound_title, sound_playlist)
        try:
            self.connector.open_connection()
            self.connector.cursor.execute(query, values)
            result = self.connector.cursor.fetchone()
            print(f"this is the result! {result}")
            self.connector.cnx.commit()
        except Exception as e:
            print(f"Error adding sound to playlist: {e}")
        finally:
            self.connector.close_connection()

    def remove_sound_from_playlist(self, sound_title, sound_playlist):
        self.connector.open_connection()

        try:
            query = "DELETE FROM soundplaylistsinfo WHERE (SoundTitle) = %s AND (PlaylistTitle) = %s"
            self.connector.cursor.execute(query, (sound_title, sound_playlist))
            self.connector.cnx.commit()
            print(
                f"Row with SoundTitle '{sound_title}' and PlaylistTitle '{sound_playlist}' deleted successfully!"
            )

        except Exception as e:
            print(f"Error deleting playlist: {e}")

        finally:
            self.connector.close_connection()


if __name__ == "__main__":
    manager = PlaylistManager()
    manager.view_playlists()
    """
    manager.connector.init_playlist()

    # viewing sounds initially.
    print("\n\n\nView all sounds in our library: ")
    manager.view_sort_playlist("Your Library")
    print("\n\n\n")

    # sorting by length (example).
    print("\n\n\nView all sounds in our library (in sorted order by length): ")
    manager.view_sort_playlist("Your Library", "Length")
    print("\n\n\n")

    # Example: create Liked playlist + add sounds into Liked.
    manager.create_playlist("Liked")
    manager.add_sound_into_playlist("coffee-slurp-2", "Liked")
    manager.add_sound_into_playlist("toaster-2", "Liked")
    manager.add_sound_into_playlist("coffee", "Liked")

    # view liked sorted.
    print("\n\n\nView all sounds in our liked playlist: ")
    manager.view_sort_playlist("Liked")
    print("\n\n\n")

    # let's remove coffee from liked.
    manager.remove_sound_from_playlist("Coffee", "Liked")

    # lets delete a playlist.
    manager.delete_playlist("Liked")

    # playing a sound.
    manager.play_sound_in_playlist("toaster", "Your Library")    
    """
