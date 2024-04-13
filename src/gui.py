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
        var = StringVar(value="Small")

        def update_label():
            playlist_label.config(text=var.get())

        for playlist in playlists:
            self.radio_vars[playlist[0]] = var 
            r_button = Radiobutton(self.playlist, text=playlist[0], variable=var, value=playlist[0], command=update_label, fg="Black", bg=self.bg_color)
            r_button.pack(anchor=W, padx=50, pady = 5)

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
            
        plus_button = Button(self.playlist, text="+", padx=50, pady=5, fg="Black", bg=self.bg_color, command=lambda: self.db.create_playlist(e.get()))
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
        var = StringVar(value="Small")
        
        def update_label():
            """
            This function is bound to the Radiobuttons and sound_label and is called when one of the radio buttons is clicked.
            This function then updates our sound label so the user can see/verify the sound they clicked. 
            """
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
        
        play_btn = Button(frame_buttons, text="Play", command=lambda: self.saturn_instance.play(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/sounds/" + var.get() + ".mp3"), padx=50, pady = 5)
        play_btn.grid(row=0, column=0, padx=50, pady = 5)

        play_edit = Button(frame_buttons, text="Edit", padx=50, pady = 5, command=self.edit_screen)
        play_edit.grid(row=0, column=1, padx=50, pady = 5)

        # add sound into playlist button IFF the playlist name is not My Library since this playlist by default has every sound.
        if(playlist_title != "Your Library"):
            # creating the label.
            add_l = Entry(self.sound, width=50)
            add_l.pack(padx=50, pady=20)
            
            # creating the button.
            add_b = Button(self.sound, text="Add to this Playlist", padx=50, pady = 5, bg = "Green", fg = "White", command=lambda: self.db.add_sound_into_playlist(add_l.get(), playlist_title))
            add_b.pack(padx=50, pady = 5)
            
        
        def delete_button():
            """
            This function is bound to the "Delete" button and is called when the button is clicked.
            It removes the sound selected in the playlist and updates the display accordingly.
            """
            self.db.remove_sound_from_playlist(var.get(), playlist_title)
            self.sound.update()
            
        play_delete = Button(frame_buttons, text="Delete", padx=50, pady = 5, command=delete_button)
        play_delete.grid(row=0, column=2, padx=50, pady = 5)

    
    
    def edit_screen(self):
        # initialize screen.
        self.sound.destroy()
        self.edit = Toplevel()
        self.edit.title("Edit Mode")        
        self.edit.geometry("950x500")
        self.edit.configure(bg=self.bg_color)
        
        # working in the 0th column: adding ALL edit features.
        Label(self.edit, text="Speed", fg="Black", bg=self.bg_color, font=("Courier New", 10)).grid(row=0, column=0, padx=50, pady=15, sticky=W)
        Label(self.edit, text="Pitch", fg="Black", bg=self.bg_color, font=("Courier New", 10)).grid(row=1, column=0, padx=50, pady=15, sticky=W)
        Label(self.edit, text="Reverse", fg="Black", bg=self.bg_color, font=("Courier New", 10)).grid(row=2, column=0, padx=50, pady=15, sticky=W)
        Label(self.edit, text="Overlap", fg="Black", bg=self.bg_color, font=("Courier New", 10)).grid(row=3, column=0, padx=50, pady=15, sticky=W)
        Label(self.edit, text="Sequential", fg="Black", bg=self.bg_color, font=("Courier New", 10)).grid(row=4, column=0, padx=50, pady=15, sticky=W)
        Label(self.edit, text="Random Insert", fg="Black", bg=self.bg_color, font=("Courier New", 10)).grid(row=5, column=0, padx=50, pady=15, sticky=W)
        
        # working in the 1st column: adding buttons for ALL edit features.
        buttons_data = [
            {"text": "Up", "row": 0, "column": 1, "columnspan": 2},
            {"text": "Down", "row": 0, "column": 4, "columnspan": 2},
            {"text": "Up", "row": 1, "column": 1, "columnspan": 2},
            {"text": "Down", "row": 1, "column": 4, "columnspan": 2},
            {"text": "Reverse", "row": 2, "column": 1, "columnspan": 5},
            {"text": "Overlap", "row": 3, "column": 1, "columnspan": 5},
            {"text": "Sequential", "row": 4, "column": 1, "columnspan": 5},
            {"text": "Random Insert", "row": 5, "column": 1, "columnspan": 5}
        ]
        for button_data in buttons_data:
            button = Button(self.edit, text=button_data["text"], fg="Black", bg=self.bg_color, padx=10, pady=5)
            button.grid(row=button_data["row"], column=button_data["column"], columnspan=button_data["columnspan"], sticky=W)

        # play button.
        button = Button(self.edit, text="Play", fg="White", bg="Green", padx=30, pady=5)
        button.grid(row=7, column=1, columnspan=5, sticky=W, pady=20)
        
        # save button.
        button_save = Button(self.edit, text="Save", fg="White", bg="Red", padx=30, pady=5)
        button_save.grid(row=7, column=20, columnspan=5, sticky=E, pady=20)
        
if __name__ == "__main__":
    gui = Gui()
    gui.root.mainloop()
