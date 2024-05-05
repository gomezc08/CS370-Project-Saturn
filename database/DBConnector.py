import os
from datetime import datetime
import mysql.connector
import pydub


class DBConnector:
    """
    Provides a streamlined interface for connecting to the MySQL Workbench/database.

    Attributes:
        sound_dir (str): Directory of our sounds file.
        sound_list (list): A list containing sounds in our sound archive. Each element in the list represents a sound.

    Methods:
        create_database_connection: Establishes a secure connection to the MySQL Workbench.
        open_connection: Opens the connection to Saturn's SQL database.
        close_connection: Closes the connection to Saturn's SQL database.
        init_playlist: Initializes tables found in our database.
    """

    def __init__(self, sound_dir):
        self.sound_dir = sound_dir
        self.sound_list = []
        self.cnx = None
        self.cursor = None
        # self.connect_to_my_sql()

    def open_connection(self):
        print("<<Opening>> connection to MySQL")
        config = {
            "user": "AidanVB",
            "password": "2ibtxFzCi95AqWFpZb6O",
            "host": "database-test1.cb6ak8csmzrs.us-west-2.rds.amazonaws.com",
            "port": 3306,
            "database": "saturnDB",
            "raise_on_warnings": True,
        }

        try:
            self.cnx = mysql.connector.connect(**config)
            self.cursor = self.cnx.cursor()
            print("Connected to MySQL")
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print("Could not connect to MySQL:", err)

    def close_connection(self):
        print("<<Closing>> connection to MySQL\n\n\n\n")
        self.cnx.close()
        self.cursor.close()

    def init_playlist(self):
        # OPEN CONNECTION
        self.open_connection()

        # SQL query to insert data from our sounds directory into a table
        insert_query_soundlist = (
            "INSERT INTO soundlist"
            "(Title, Length, IsEdited, DateCreated) "
            "VALUES (%s, %s, %s, %s)"
        )
        insert_query_soundplaylistsinfo = (
            "INSERT INTO soundplaylistsinfo"
            "(SoundTitle, PlaylistTitle)"
            "VALUES (%s, %s)"
        )
        insert_query_playlistnames = "INSERT INTO playlistnames(Name) VALUES(%s)"
        playlist_name = "Your Library"

        try:
            self.cursor.execute(insert_query_playlistnames, (playlist_name,))
            self.cnx.commit()
            print(f"Playlist '{playlist_name}' added successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

        for filename in os.listdir(self.sound_dir):
            if filename.endswith(".mp3"):
                file_path = os.path.join(self.sound_dir, filename)
                # Get the title.
                title = os.path.splitext(filename)[0]

                # SQL query to check if the title already exists in the soundlist table
                check_query_soundlist = (
                    "SELECT COUNT(*) FROM soundlist WHERE Title = %s"
                )
                self.cursor.execute(check_query_soundlist, (title,))
                result_soundlist = self.cursor.fetchone()

                # SQL query to check if the title already exists in the soundplaylistsinfo table
                check_query_soundplaylistsinfo = (
                    "SELECT COUNT(*) FROM soundplaylistsinfo WHERE SoundTitle = %s"
                )
                self.cursor.execute(check_query_soundplaylistsinfo, (title,))
                result_soundplaylistsinfo = self.cursor.fetchone()

                if title not in self.sound_list:
                    self.sound_list.append(title)

                if result_soundlist[0] > 0:
                    print(f"{title} already exists in the soundlist database.")
                else:
                    try:
                        # Get the length of the .wav file
                        duration = pydub.AudioSegment.from_file(
                            file_path
                        ).duration_seconds
                    except Exception as e:
                        print(f"Error processing {filename}: {e}")
                        continue

                    # Get the current date and time
                    date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    soundlist_data = (title, duration, False, date_created)

                    # Execute the query
                    self.cursor.execute(insert_query_soundlist, soundlist_data)
                    self.cnx.commit()

                if result_soundplaylistsinfo[0] > 0:
                    print(f"{title} already exists in the soundplaylistsinfo database.")
                else:
                    soundplaylistsinfo_data = (title, "Your Library")

                    # Execute the query
                    self.cursor.execute(
                        insert_query_soundplaylistsinfo, soundplaylistsinfo_data
                    )
                    self.cnx.commit()

        print("Data in sounds directory inserted successfully")

        # CLOSE CONNECTION.
        self.close_connection()
