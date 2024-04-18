from tkinter import *
from PIL import Image, ImageTk
import sys, os

parent_dir = os.path.dirname(os.getcwd())
sys.path.insert(0, parent_dir + "/Database")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.PlaylistManager import PlaylistManager
from src.saturn_cli import Saturn

class Gui():
    def __init__(self):
        # defining root.
        self.root = Tk()
        self.bg_color = "#ead6b8"
        self.continue_button_color = "#102C57"
        self.font_title ="Courier New"
        self.root.geometry("950x500")
        self.root.configure(bg=self.bg_color)
        self.root.title("Saturn Sound Archive")
        Label(self.root, text="Saturn Sound Archive", font=(self.font_title, 25), padx=50, pady=5, fg="Black", bg=self.bg_color).pack(padx=50, pady=5)
        self.root_img = Image.open('./saturn.png')
        self.root_img_tk = ImageTk.PhotoImage(self.root_img)
        self.root_label = Label(self.root, image=self.root_img_tk)
        self.root_label.pack(pady=20)  
        self.root_btn = Button(self.root, text="Continue", command=self.playlists_screen, padx=50, pady=5, fg="White", bg=self.continue_button_color)
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
        
        # Playlist Manager title.
        Label(self.playlist, text="Playlist", font=(self.font_title, 20), padx=50, pady=5, fg="Black", bg=self.bg_color).grid(pady=10, row=0, column=2)
        
        # Select Playlist.
        Label(self.playlist, text="Select Playlist", font=(self.font_title, 15), padx=50, pady=5, fg="Black", bg=self.bg_color).grid(sticky=W, pady=10, padx=30, row=1, column=1)
        
        # Radio buttons (for each playlist).
        playlists = self.db.view_playlists()
        self.radio_vars = {}
        var = StringVar(value="Small")

        def update_label():
            playlist_label.config(text=var.get())

        r = 2
        for playlist in playlists:
            self.radio_vars[playlist[0]] = var 
            r_button = Radiobutton(self.playlist, text=playlist[0], variable=var, value=playlist[0], padx=50, pady=5, command=update_label, fg="Black", bg=self.bg_color)
            r_button.grid(sticky=W, pady=2, padx=30, column=1, row=r)
            r += 1

        # Radio button label.
        playlist_label = Label(self.playlist, text="", fg="Black", bg=self.bg_color, padx=50, pady=5)
        playlist_label.grid(sticky=W, padx=30, pady = 5, column=1, row=r)
        r += 1

        def continue_with_selection():
            self.sounds_screen(var.get())
        
        # continue button.
        b = Button(self.playlist, text="Continue", command=continue_with_selection, padx=20, pady = 5, fg="White", bg=self.continue_button_color)
        b.grid(padx=20, pady = 5, row=r, column=1, sticky=W) 
        
        # delete button.
        def delete_btn_command():
            """
            This function is bound to the delete_btn and is called when we click delete button.
            This function deletes a playlist that isn't our library.
            """
            if var.get() != "Your Library":
                print("this is NOT ur library")
                self.db.delete_playlist(var.get())
        
        delete_btn = Button(self.playlist, text="Delete Playlist", bg = "Red", fg = "White", padx=20, pady=5, command=delete_btn_command)
        delete_btn.grid(pady = 5, row=r, column=1, sticky=E)

        # Create new Playlist label.
        Label(self.playlist, text="Create new Playlist", font=(self.font_title, 15), padx=50, pady=5, fg="Black", bg=self.bg_color).grid(row=1, column=3, sticky=W)
        
        # white entry box.
        e = Entry(self.playlist, width=50)
        e.grid(padx=50, pady=5, row=2, column=3, sticky=E)
            
        # Create Playlist button.
        plus_button = Button(self.playlist, text="Create Playlist", padx=50, pady=5, fg="White", bg=self.continue_button_color, command=lambda: self.db.create_playlist(e.get()))
        plus_button.grid(padx=50, pady=5, column=3, row=3, sticky=W) 

    def sounds_screen(self, playlist_title):
        # intialize screen.
        self.playlist.destroy() 
        self.sound = Toplevel()
        self.sound.title("Playlists Screen")
        self.sound.geometry("950x500")
        self.sound.configure(bg=self.bg_color)
        
        # [Playlist title].
        Label(self.sound, text=playlist_title, font=(self.font_title, 20), pady=5, fg="Black", bg=self.bg_color).grid(padx=20, pady=10, row=0, column=2, sticky=W)
        
        # initialize title/label for sound buttons.
        Label(self.sound, text="Select Sound", font=(self.font_title, 15), pady=5, fg="Black", bg=self.bg_color).grid(padx=20, pady=10, row=1, column=2, sticky=W)
        
        # setting-up for radio buttons.
        playlist = self.db.view_sort_playlist(playlist_title)
        var = StringVar(value="Small")
        
        def update_label():
            """
            This function is bound to the Radiobuttons and sound_label and is called when one of the radio buttons is clicked.
            This function then updates our sound label so the user can see/verify the sound they clicked. 
            """
            sound_label.config(text=var.get())

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
            sound_button = Radiobutton(self.sound, text=sound[0], variable=var, value=sound[0], command=update_label, fg="Black", bg=self.bg_color, width=20)
            sound_button.grid(row=r, column=c, pady=5, padx=5, sticky=EW)
            c += 1
        r += 1
        
        # radio button label.
        sound_label = Label(self.sound, text="", fg="Black", bg="white")
        sound_label.grid(row=r, column=2, sticky=EW, padx=10, pady=10)
        r += 1
        def next_screen():
            self.edit_screen(var.get())  
            
        play_btn = Button(self.sound, text="Play", command=lambda: self.saturn_instance.play(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/sounds/" + var.get() + ".mp3"), padx=50, pady = 5, bg=self.continue_button_color, fg="white")
        play_btn.grid(row=r, column=1, pady=20, padx=10)

        play_edit = Button(self.sound, text="Edit", padx=50, pady = 5, command=next_screen, bg=self.continue_button_color, fg="white")
        play_edit.grid(row=r, column=2, pady=20, padx=10)

        
        # add sound button (only shows up in non your library playlists).
        if(playlist_title != "Your Library"):
            # creating the label.
            add_l = Entry(self.sound, width=50)
            add_l.grid(row=r+1, column=0, padx=20, pady=10)
            
            # creating the button.
            add_b = Button(self.sound, text="Add to this Playlist", padx=50, pady = 5, bg = self.continue_button_color, fg = "White", command=lambda: self.db.add_sound_into_playlist(add_l.get(), playlist_title))
            add_b.grid(padx=20, pady = 5, row=r+2, column=0)
            
        
        def delete_button():
            """
            This function is bound to the "Delete" button and is called when the button is clicked.
            It removes the sound selected in the playlist and updates the display accordingly.
            """
            self.db.remove_sound_from_playlist(var.get(), playlist_title)
            self.sound.update()
            
        play_delete = Button(self.sound, text="Delete", padx=50, pady=5, command=delete_button, bg="Red", fg="White")
        play_delete.grid(row=r, column=3, pady=20, padx=10)    
    
    def edit_screen(self, sound_name):
        active_color = "#FFD700"
        inactive_color = "#FFFACD"
        
        # initialize screen.
        self.sound.destroy()
        self.edit = Toplevel()
        self.edit.title("Edit Mode")        
        self.edit.geometry("950x500")
        self.edit.configure(bg=self.bg_color)
        
        # [Sound] title
        Label(self.edit, text=sound_name, font=(self.font_title, 20), padx=50, pady=5, fg="Black", bg=self.bg_color).grid(pady=10, row=0, column=2, sticky=EW)
        
        # working in the 0th column: adding ALL edit features.
        Label(self.edit, text="Speed", fg="Black", bg=self.bg_color, font=("Courier New", 10)).grid(row=1, column=0, padx=50, pady=15, sticky=W)
        Label(self.edit, text="Pitch", fg="Black", bg=self.bg_color, font=("Courier New", 10)).grid(row=2, column=0, padx=50, pady=15, sticky=W)
        Label(self.edit, text="Reverse", fg="Black", bg=self.bg_color, font=("Courier New", 10)).grid(row=3, column=0, padx=50, pady=15, sticky=W)
        Label(self.edit, text="Overlap", fg="Black", bg=self.bg_color, font=("Courier New", 10)).grid(row=4, column=0, padx=50, pady=15, sticky=W)
        Label(self.edit, text="Sequential", fg="Black", bg=self.bg_color, font=("Courier New", 10)).grid(row=5, column=0, padx=50, pady=15, sticky=W)
        Label(self.edit, text="Random Insert", fg="Black", bg=self.bg_color, font=("Courier New", 10)).grid(row=6, column=0, padx=50, pady=15, sticky=W)
        
        self.speed_val = 1.00
        pitch_val = 1.00
        def adjust_speed_label(is_up):
            if is_up and self.speed_val < 2.00:
                self.speed_val += 0.25
            elif not is_up and self.speed_val > 0.00:
                self.speed_val -= 0.25
            speed_label.config(text="{:.2f}".format(self.speed_val))
            
        # speed up/down buttons.
        speed_up_button = Button(self.edit, text="Up", fg="Black", bg=inactive_color, padx=10, pady=5, command=lambda: adjust_speed_label(True))
        speed_up_button.grid(row=1, column=1, sticky=W)
        speed_down_button = Button(self.edit, text="Down", fg="Black", bg=inactive_color, padx=10, pady=5, command=lambda: adjust_speed_label(False))
        speed_down_button.grid(row=1, column=2, sticky=W)
        # speed Label.
        speed_label = Label(self.edit, text=self.speed_val)
        speed_label.grid(row=1, column=3)
        
        # pitch up/down buttons.
        pitch_up_button = Button(self.edit, text="Up", fg="Black", bg=inactive_color, padx=10, pady=5)
        pitch_up_button.grid(row=2, column=1, sticky=W)
        pitch_down_button = Button(self.edit, text="Down", fg="Black", bg=inactive_color, padx=10, pady=5)
        pitch_down_button.grid(row=2, column=2, sticky=W)
        # pitch Label.
        pitch_label = Label(self.edit, text=pitch_val).grid(row=2, column=3)
        
        # reverse button.
        def toggle_btn_click(button):
            if button["bg"] == inactive_color:
                button["bg"] = active_color
            else:
                button["bg"] = inactive_color
            
        reverse_button = Button(self.edit, text="Reverse", fg="black", bg=inactive_color, padx=10, pady=5, command=lambda: toggle_btn_click(reverse_button))
        reverse_button.grid(row=3, column=1, columnspan=5, sticky=W)
        
        # overlap.
        overlap_button = Button(self.edit, text="Overlap", fg="Black", bg=inactive_color, padx=10, pady=5, command=lambda: toggle_btn_click(overlap_button))
        overlap_button.grid(row=4, column=1, sticky=W) 
        overlap_entry = Entry(self.edit, width=30)
        overlap_entry.grid(row=4, column=2)
        
        # sequential.
        seq_button = Button(self.edit, text="Sequential", fg="Black", bg=inactive_color, padx=10, pady=5, command=lambda: toggle_btn_click(seq_button))
        seq_button.grid(row=5, column=1, sticky=W) 
        seq_entry = Entry(self.edit, width=30)
        seq_entry.grid(row=5, column=2)
        
        # rand insert.
        rand_button = Button(self.edit, text="Random Insert", fg="Black", bg=inactive_color, padx=10, pady=5, command=lambda: toggle_btn_click(rand_button))
        rand_button.grid(row=6, column=1, sticky=W) 
        rand_entry = Entry(self.edit, width=30)
        rand_entry.grid(row=6, column=2)
        
        # play button.
        button = Button(self.edit, text="Play", fg="White", bg=self.continue_button_color, padx=30, pady=5)
        button.grid(row=7, column=1, sticky=W, pady=20)
        
        # save button.
        button_save = Button(self.edit, text="Save", fg="White", bg=self.continue_button_color, padx=30, pady=5)
        button_save.grid(row=7, column=2, sticky=E, pady=20)
        
if __name__ == "__main__":
    gui = Gui()
    gui.root.mainloop()
