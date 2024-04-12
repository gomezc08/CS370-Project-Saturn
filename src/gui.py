import tkinter as tk
import sys, os

parent_dir = os.path.dirname(os.getcwd())
sys.path.insert(0, parent_dir + "/Database")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Database.PlaylistManager import PlaylistManager

class AudioEditorApp(PlaylistManager):
    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        self.root.title("Sound Archive App")
        self.root.geometry("800x600")
        self.root.configure(bg="lightblue")
        self.p_name = None

        # Create frames for all our pages we drew on the whiteboard.
        self.home_frame = tk.Frame(self.root)
        self.playlist_frame = tk.Frame(self.root)
        self.add_playlist_frame = tk.Frame(self.root)
        self.edit_frame = tk.Frame(self.root)

        self.f_names = [self.home_frame, self.playlist_frame, self.edit_frame]

        # Initialize the start screen
        self.home_screen()
        self.root.mainloop()

    def home_screen(self):
        self.clear_frames()

        # Pack the home frame into the root window
        self.home_frame.pack()

        # Add a button to open the next page.
        button = tk.Button(self.home_frame, text="Open", command=self.playlist_screen)
        button.pack()

    def playlist_screen(self):
        self.clear_frames()

        # Pack the playlist frame into the root window
        self.playlist_frame.pack()

        # Add a button to open the new page
        # TODO: create a button for every playlist we have. For now, I left kinda a default hard coded value.

        button = tk.Button(
            self.playlist_frame,
            text="My Library",
            command=self.songs_in_playlist_screen,
        )
        button.pack()

        # Define our back button back to the home
        back_button = tk.Button(
            self.playlist_frame, text="Go Back", command=self.home_screen
        )
        back_button.pack()

        # Define input button (this is for creating a new playlist, this is to get playlist name)
        plus_button = tk.Button(
            self.playlist_frame,
            text="New Playlist",
            command=self.new_playlist,
        )
        plus_button.pack()

    def new_playlist(self):
        self.add_playlist_frame.pack()
        print(self.p_name)
        new_playlist_window = tk.Toplevel()
        new_playlist_window.config(width=500, height=500)

        self.entry = tk.Entry(
            new_playlist_window, fg="yellow", bg="lightblue", width=50
        )
        self.entry.pack()

        label = tk.Label(new_playlist_window, text="Playlist Name")
        label.pack()

        accept_name_button = tk.Button(
            new_playlist_window, text="Ok", command=self.get_name
        )
        accept_name_button.pack()

    def get_name(self):
        name = self.entry.get()
        print(name)
        # TODO: TEST to see if it gets added to db

    def songs_in_playlist_screen(self):
        self.clear_frames()
        # TODO: Placeholder action for now
        print("Displaying songs in the playlist...")
        self.view_sort_playlist("Your Library")

    def clear_frames(self):
        # Destroy widgets in all frames
        for frame in self.f_names:
            for widget in frame.winfo_children():
                widget.destroy()


if __name__ == "__main__":
    app = AudioEditorApp()
