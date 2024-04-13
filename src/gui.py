from tkinter import *
from PIL import Image, ImageTk
import sys, os

parent_dir = os.path.dirname(os.getcwd())
sys.path.insert(0, parent_dir + "/Database")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Database.PlaylistManager import PlaylistManager
from src.saturn_cli import Saturn

class Gui():
    def __init__(self):
        # defining root.
        self.root = Tk()
        self.bg_color = "#ead6b8"
        self.root.geometry("950x500")
        self.root.configure(bg=self.bg_color)
        self.root.title("Saturn Sound Archive")
        Label(self.root, text="Saturn Sound Archive", font=("Arial", 25), padx=50, pady=5, fg="Black", bg=self.bg_color).pack(padx=50, pady=5)
        self.root_img = Image.open('./saturn.png')
        self.root_img_tk = ImageTk.PhotoImage(self.root_img)
        self.root_label = Label(self.root, image=self.root_img_tk)
        self.root_label.pack(pady=20)  
        self.root_btn = Button(self.root, text="Continue", command=self.playlists_screen, padx=50, pady=5, fg="Black", bg=self.bg_color)
        self.root_btn.pack(pady=20)
        
        self.saturn_instance = Saturn(sys.argv, len(sys.argv))
        self.db = PlaylistManager()

    def playlists_screen(self):
        # Initialize screen.
        self.root.destroy()
        self.playlist = Toplevel()
        self.playlist.title("Playlists")
        self.playlist.geometry("950x500")
        self.playlist.configure(bg=self.bg_color)
        
        # initialize title/label for radio buttons.
        Label(self.playlist, text="Select Playlist", font=("Arial", 15), padx=50, pady=5, fg="Black", bg=self.bg_color).pack(anchor=W)
        
        # Display playlists using radio buttons.
        playlists = self.db.view_playlists()
        self.radio_vars = {}
        var = StringVar()

        def update_label():
            playlist_label.config(text=var.get())

        for playlist in playlists:
            self.radio_vars[playlist[0]] = var 
            Radiobutton(self.playlist, text=playlist[0], variable=var, value=playlist[0], command=update_label, fg="Black", bg=self.bg_color).pack(anchor=W, padx=50, pady = 5)

        # click on radio button label.
        playlist_label = Label(self.playlist, text="", fg="Black", bg=self.bg_color)
        playlist_label.pack(anchor=W, padx=50, pady = 5)

        # button that looks into playlist.
        def continue_with_selection():
            self.sounds_screen(var.get())

        # "+" button
        Label(self.playlist, text="Create new Playlist", font=("Arial", 15), padx=50, pady=5, fg="Black", bg=self.bg_color).pack(anchor=E)
        e = Entry(self.playlist, width=50)
        e.pack(anchor=E, padx=50, pady=5)

        def plus_click():
            entry_value = e.get()
            print(f"here is the tentry: {entry_value}")
            
        plus_button = Button(self.playlist, text="+", padx=50, pady=5, fg="Black", bg=self.bg_color, command=plus_click)
        plus_button.pack(anchor=E, padx=50, pady=5)

        # "Continue" button
        b = Button(self.playlist, text="Continue", command=continue_with_selection, padx=50, pady = 5, fg="Black", bg=self.bg_color)
        b.pack(anchor=W, padx=50, pady = 5)

    def sounds_screen(self, playlist_title):
        # intialize screen.
        self.playlist.destroy()  
        self.sound = Toplevel()
        self.sound.title("Playlists Screen")
        self.sound.geometry("950x500")
        self.sound.configure(bg=self.bg_color)
        
        # initialize title/label for sound buttons.
        Label(self.sound, text="Select Sound", font=("Arial", 15), padx=50, pady=5, fg="Black", bg=self.bg_color).pack(anchor=W)
        
        # creating radio buttons for each song in the playlist.
        playlist = self.db.view_sort_playlist(playlist_title)
        self.radio_vars = {}  
        var = StringVar()
        
        def update_label():
            sound_label.config(text=var.get())

        for sound in playlist:
            self.radio_vars[sound[0]] = var 
            Radiobutton(self.sound, text=sound[0], variable=var, value=sound[0], command=update_label, fg="Black", bg=self.bg_color).pack(anchor=W, padx=50, pady=5)

        # click on radio button label.
        sound_label = Label(self.sound, text="", fg="Black", bg=self.bg_color)
        sound_label.pack(anchor=W, padx=50, pady=5)

        # play, edit, delete buttons.
        frame_buttons = Frame(self.sound, bg=self.bg_color)
        frame_buttons.pack()

        play_btn = Button(frame_buttons, text="Play", command=self.third_screen, padx=50, pady = 5)
        play_btn.grid(row=0, column=0, padx=50, pady = 5)

        play_edit = Button(frame_buttons, text="Edit", padx=50, pady = 5)
        play_edit.grid(row=0, column=1, padx=50, pady = 5)

        play_delete = Button(frame_buttons, text="Delete", padx=50, pady = 5)
        play_delete.grid(row=0, column=2, padx=50, pady = 5)

    
    
    def third_screen(self):
        self.sound.destroy()
        self.third = Toplevel()
        self.third.title("Third screen test")
        self.btn = Button(self.third, text="Click me to close all windows", command=self.close_all)
        self.btn.pack()

    def close_all(self):
        self.third.destroy()  # Close the third window
        self.sound.destroy()    # Close the second window

if __name__ == "__main__":
    gui = Gui()
    gui.root.mainloop()
