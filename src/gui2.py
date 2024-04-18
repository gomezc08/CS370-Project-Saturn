from tkinter import *
from PIL import Image, ImageTk
import sys, os

parent_dir = os.path.dirname(os.getcwd())
sys.path.insert(0, parent_dir + "/Database")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.PlaylistManager import PlaylistManager
from src.saturn_cli import Saturn

class Application(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry("950x500")
        self.title("Saturn Sound Archive")
        self.frames = [HomeFrame(self), PlaylistFrame(self), SoundFrame(self)]
        self.current_frame = 0
        self.show_frame()

    def switch_frame(self):
        print(self.frames[self.current_frame])
        self.frames[self.current_frame].pack_forget()
        self.current_frame += 1
        self.frames[self.current_frame].pack()
    
    def show_frame(self):
        # Hide all frames
        for frame in self.frames:
            frame.pack_forget()
        # Show the current frame
        self.frames[self.current_frame].pack()

class BaseFrame(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.font_title = "Courier New"
        self.bg_color = "#ead6b8"
        self.default_button_color = "#102C57"
        self.config(bg=self.bg_color)
        self.saturn_instance = Saturn(sys.argv, len(sys.argv))
        self.db = PlaylistManager()
        self.var = StringVar(value="Small")
        self.pack()

class HomeFrame(BaseFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.create_widgets()
        
    def create_widgets(self):
        Label(self, text="Saturn Sound Archive", font=(self.font_title, 25), padx=50, pady=5, fg="Black", bg=self.bg_color).pack(padx=50, pady=5)
        self.saturn_img = ImageTk.PhotoImage(Image.open('./saturn.png'))
        self.root_label = Label(self, image=self.saturn_img)
        self.root_label.pack(pady=20)  
        self.root_btn = Button(self, text="Continue", command=self.master.switch_frame, padx=50, pady=5, fg="White", bg=self.default_button_color)
        self.root_btn.pack(pady=20)

class PlaylistFrame(BaseFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        # Playlist Manager title.
        Label(self, text="Playlist", font=(self.font_title, 20), padx=50, pady=5, fg="Black", bg=self.bg_color).grid(pady=10, row=0, column=2)
        
        # Select Playlist.
        Label(self, text="Select Playlist", font=(self.font_title, 15), padx=50, pady=5, fg="Black", bg=self.bg_color).grid(sticky=W, pady=10, padx=30, row=1, column=1)
        
        # Radio buttons (for each playlist).
        playlists_list = self.db.view_playlists()

        for idx, playlist in enumerate(playlists_list, start=2):
            r_button = Radiobutton(self, text=playlist[0], variable=self.var, value=playlist[0], padx=50, pady=5, command=lambda: playlist_label.config(text=self.var.get()), fg="Black", bg=self.bg_color)
            r_button.grid(sticky=W, pady=2, padx=30, column=1, row=idx)
        
        idx += 1
        # playlist label.
        playlist_label = Label(self, text="", fg="Black", bg=self.bg_color, padx=50, pady=5)
        playlist_label.grid(sticky=W, padx=30, pady = 5, column=1, row=idx)
        
        # continue button.
        continue_button = Button(self, text="Continue", padx=20, pady=5, fg="White", bg=self.default_button_color, command=self.master.switch_frame)
        continue_button.grid(padx=20, pady=5, row=idx + 1, column=1, sticky=W) 

        # delete button.
        delete_btn = Button(self, text="Delete Playlist", bg="Red", fg="White", padx=20, pady=5, command=self.db.delete_playlist)
        delete_btn.grid(pady=5, row=idx + 1, column=1, sticky=E)

        # Create new Playlist label.
        Label(self, text="Create new Playlist", font=(self.font_title, 15), padx=50, pady=5, fg="Black", bg=self.bg_color).grid(row=1, column=3, sticky=W)
        
        # white entry box.
        entry = Entry(self, width=50)
        entry.grid(padx=50, pady=5, row=2, column=3, sticky=E)
            
        # Create Playlist button.
        plus_button = Button(self, text="Create Playlist", padx=50, pady=5, fg="White", bg=self.default_button_color, command=self.db.create_playlist)
        plus_button.grid(padx=50, pady=5, column=3, row=3, sticky=W) 

class SoundFrame(BaseFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.playlist_title = self.var.get()
        print(self.playlist_title)
        self.create_widgets()
    
    def create_widgets(self):
        # [Playlist title].
        Label(self, text=self.playlist_title, font=(self.font_title, 20), pady=5, fg="Black", bg=self.bg_color).grid(padx=20, pady=10, row=0, column=2, sticky=W)
        
        # initialize title/label for sound buttons.
        Label(self, text="Select Sound", font=(self.font_title, 15), pady=5, fg="Black", bg=self.bg_color).grid(padx=20, pady=10, row=1, column=2, sticky=W)
        
        # setting-up for radio buttons.
        playlist = self.db.view_sort_playlist(self.playlist_title)

        # playlist radio buttons.
        # add sounds in rows of 7.
        #self.sound.grid_rowconfigure(0, weight=1)  

        # Inside the loop
        r = 2
        c = 0
        for sound in playlist:
            if c == 5: 
                r += 1
                c = 0
            sound_button = Radiobutton(self, text=sound[0], variable=self.var, value=sound[0], command=lambda: sound_label.config(text=self.var.get()), fg="Black", bg=self.bg_color, width=20)
            sound_button.grid(row=r, column=c, pady=5, padx=5, sticky=EW)
            c += 1
        r += 1
        
        # radio button label.
        sound_label = Label(self, text="", fg="Black", bg="white")
        sound_label.grid(row=r, column=2, sticky=EW, padx=10, pady=10)
        r += 1
        
        # play button.    
        play_btn = Button(self, text="Play", command=lambda: self.saturn_instance.play(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/sounds/" + self.var.get() + ".mp3"), padx=50, pady = 5, bg=self.default_button_color, fg="white")
        play_btn.grid(row=r, column=1, pady=20, padx=10)

        # edit button.
        play_edit = Button(self, text="Edit", padx=50, pady = 5, command=self.master.switch_frame, bg=self.default_button_color, fg="white")
        play_edit.grid(row=r, column=2, pady=20, padx=10)
        
        # add sound button (only shows up in non your library playlists).
        if(self.playlist_title != "Your Library"):
            # creating the label.
            add_l = Entry(self, width=50)
            add_l.grid(row=r+1, column=0, padx=20, pady=10)
            
            # creating the button.
            add_b = Button(self, text="Add to this Playlist", padx=50, pady = 5, bg = self.default_button_color, fg = "White", command=lambda: self.db.add_sound_into_playlist(add_l.get(), self.playlist_title))
            add_b.grid(padx=20, pady = 5, row=r+2, column=0)
            
        def delete_button():
            """
            This function is bound to the "Delete" button and is called when the button is clicked.
            It removes the sound selected in the playlist and updates the display accordingly.
            """
            self.db.remove_sound_from_playlist(self.var.get(), self.playlist_title)
            self.update()
            
        play_delete = Button(self, text="Delete", padx=50, pady=5, command=delete_button, bg="Red", fg="White")
        play_delete.grid(row=r, column=3, pady=20, padx=10)  


class Frame2(BaseFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        Button(self, text="click toen", command=self.master.switch_frame).pack()

class Frame3(BaseFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        print("yo")
        Button(self, text=" to go to next screen", command=self.master.switch_frame).pack()


# Create frames
app = Application()
app.mainloop()