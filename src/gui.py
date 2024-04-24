import os, sys

parent_dir = os.path.dirname(os.getcwd())
sys.path.insert(0, parent_dir + "/Database")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.PlaylistManager import PlaylistManager
from src.saturn_cli import Saturn
from src.gui_backend import Backend

from tkinter import *
from PIL import Image, ImageTk
import sys, os


class BaseClass(Tk):
    """
    Creates a base frame for all other frames

    Attributes:
        font_title (str): The font for all titles in each frame.
        bg_color (str): Background color for frame (represents saturn's main color).
        radio_item (str): Represents option user clicks on the radio buttons.
        sound_item (str): Shared variable of the actual button user clicked on for the playlist and sound name.

    Methods:
        change_frame: Destroys the current frame and switches to the another frame.
        reload_frame: Destroys and reloads the current frame (same idea as refreshing a page).
    """

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Set up common attributes
        self.font_title = "Courier New"
        self.geometry("950x600")
        self.title("Saturn Sound Archive")
        self.default_button_color = "#102C57"
        self.bg_color = "#ead6b8"
        self.radio_item = StringVar(value="Small")
        self.sound_item = None

        self.db = PlaylistManager()
        self.saturn = Saturn(sys.argv, len(sys.argv))

    def change_frame(self, change_frame, sound_argument=None):
        self.destroy()
        if sound_argument is not None:
            app = change_frame(sound_argument)
        else:
            app = change_frame()
        app.mainloop()

    def reload_frame(self, change_frame, sound_argument=None, sort=None):
        self.destroy()
        if sound_argument is not None:
            app = change_frame(sound_argument, sort)
        else:
            app = change_frame()
        app.mainloop()


class HomeFrame(BaseClass):
    """
    Frame for the main home screen of our sound archive app.

    Attributes:
        None

    Methods:
        None
    """

    def __init__(self, *args, **kwargs):
        # intialize screen.
        BaseClass.__init__(self, *args, **kwargs)
        self.config(bg=self.bg_color)

        # layout screen.
        Label(
            self,
            text="Saturn Sound Archive",
            font=(self.font_title, 25),
            padx=50,
            pady=5,
            fg="Black",
            bg=self.bg_color,
        ).pack(padx=50, pady=5)
        self.saturn_img = ImageTk.PhotoImage(Image.open("./saturn.png"))
        self.root_label = Label(self, image=self.saturn_img)
        self.root_label.pack(pady=20)
        self.root_btn = Button(
            self,
            text="Continue",
            command=lambda: self.change_frame(PlaylistFrame),
            padx=50,
            pady=5,
            fg="White",
            bg=self.default_button_color,
        )
        self.root_btn.pack(pady=20)


class PlaylistFrame(BaseClass):
    """
    Frame for playlist screen of our sound archive app.

    Attributes:
        entry (Entry): White prompt box which allows user to type name of playlist they want to create.

    Methods:
        continue_with_selection: handles setting up next frame.
        create_new_playlist: handles setting up a new playlist in database.
        delete_playlist: handles deleting playlist from database.
    """

    def __init__(self, *args, **kwargs):
        # initialize screen.
        BaseClass.__init__(self, *args, **kwargs)
        self.config(bg=self.bg_color)
        self.entry = Entry(self, width=50)

        # layout screen.
        # Playlist Manager title.
        Label(
            self,
            text="Playlist",
            font=(self.font_title, 20),
            padx=50,
            pady=5,
            fg="Black",
            bg=self.bg_color,
        ).grid(pady=10, row=0, column=2, padx=5)

        # Select Playlist.
        Label(
            self,
            text="Select Playlist",
            font=(self.font_title, 15),
            padx=50,
            pady=5,
            fg="Black",
            bg=self.bg_color,
        ).grid(sticky=W, pady=10, padx=30, row=1, column=1)

        # Radio buttons (for each playlist in rows of 5).
        playlists_list = self.db.view_playlists()

        for idx, playlist in enumerate(playlists_list, start=2):
            r_button = Radiobutton(
                self,
                text=playlist[0],
                variable=self.radio_item,
                value=playlist[0],
                padx=50,
                pady=5,
                command=lambda: playlist_label.config(text=self.radio_item.get()),
                fg="Black",
                bg=self.bg_color,
            )
            r_button.grid(sticky=W, pady=2, padx=30, column=1, row=idx)

        idx += 1

        # playlist label.
        playlist_label = Label(
            self, text="", fg="Black", bg=self.bg_color, padx=50, pady=5
        )
        playlist_label.grid(sticky=W, padx=30, pady=5, column=1, row=idx)

        # continue button.
        continue_button = Button(
            self,
            text="Continue",
            padx=20,
            pady=5,
            fg="White",
            bg=self.default_button_color,
            command=self.continue_with_selection,
        )
        continue_button.grid(padx=20, pady=5, row=idx + 1, column=1, sticky=W)

        # delete button.
        delete_btn = Button(
            self,
            text="Delete Playlist",
            bg="Red",
            fg="White",
            padx=20,
            pady=5,
            command=self.delete_playlist,
        )
        delete_btn.grid(pady=5, row=idx + 1, column=1, sticky=E)

        # Create new Playlist label.
        Label(
            self,
            text="Create new Playlist",
            font=(self.font_title, 15),
            padx=50,
            pady=5,
            fg="Black",
            bg=self.bg_color,
        ).grid(row=1, column=3, sticky=W)

        # white entry box.
        self.entry.grid(padx=50, pady=5, row=2, column=3, sticky=E)

        # Create Playlist button.
        plus_button = Button(
            self,
            text="Create Playlist",
            bg=self.default_button_color,
            fg="White",
            padx=50,
            pady=5,
            command=self.create_new_playlist,
        )
        plus_button.grid(padx=50, pady=5, column=3, row=3, sticky=W)

        # back button.
        back_button = Button(
            self, text="Back", padx=20, command=lambda: self.change_frame(HomeFrame)
        )
        back_button.grid(pady=90, padx=30, row=idx + 2, column=1, sticky=W)

    def continue_with_selection(self):
        # self.playlist_name = self.radio_item.get()
        # self.playlist_name
        self.playlist_name = self.radio_item.get()
        self.sound_item = self.playlist_name
        self.change_frame(SoundFrame, sound_argument=self.radio_item.get())

    def create_new_playlist(self):
        self.db.create_playlist(self.entry.get())
        self.reload_frame(PlaylistFrame)

    def delete_playlist(self):
        self.db.delete_playlist(self.radio_item.get())
        self.reload_frame(PlaylistFrame)


class SoundFrame(BaseClass):
    """
    Frame for sound screen of our sound archive app.

    Attributes:
        playlist_title (str): User chosen playlist title from previous frame specifiec using radio buttons.
        dropdown_item (StringVar): handles drop down entry options that user clicks on.
        sort_name (str): user chosen drop down item that they want to sort the sounds in the playlist by.

    Methods:
        continue_with_selection: handles setting up next frame.
        remove_button: removes the sound selected in the playlist and updates the display accordingly.
    """

    def __init__(self, playlist_title, sort_name=None, **kwargs):
        # initialize screen.
        BaseClass.__init__(self, **kwargs)
        self.playlist_title = playlist_title
        self.config(bg=self.bg_color)
        self.dropdown_item = StringVar(value="Sort by")
        self.sort_name = sort_name

        # layout screen.
        # [Playlist title].
        Label(
            self,
            text=self.playlist_title,
            font=(self.font_title, 20),
            pady=5,
            fg="Black",
            bg=self.bg_color,
        ).grid(padx=20, pady=10, row=0, column=2, sticky=W)

        # initialize title/label for sound buttons.
        Label(
            self,
            text="Select Sound",
            font=(self.font_title, 15),
            pady=5,
            fg="Black",
            bg=self.bg_color,
        ).grid(padx=20, pady=10, row=1, column=2, sticky=W)

        # setting-up for radio buttons.
        playlist = self.db.view_sort_playlist(self.playlist_title, self.sort_name)

        # playlist radio buttons.
        # add sounds in rows of 7.
        r = 2
        c = 0
        for sound in playlist:
            if c == 5:
                r += 1
                c = 0
            sound_button = Radiobutton(
                self,
                text=sound[0],
                variable=self.radio_item,
                value=sound[0],
                command=lambda: sound_label.config(text=self.radio_item.get()),
                fg="Black",
                bg=self.bg_color,
                width=20,
            )
            sound_button.grid(row=r, column=c, pady=5, padx=5, sticky=EW)
            c += 1
        r += 1

        # radio button label.
        sound_label = Label(self, text="", fg="Black", bg="white")
        sound_label.grid(row=r, column=2, sticky=EW, padx=10, pady=10)
        r += 1

        # play button.
        play_btn = Button(
            self,
            text="Play",
            command=lambda: self.saturn.play(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                + "/sounds/"
                + self.radio_item.get()
                + ".mp3"
            ),
            padx=50,
            pady=5,
            bg=self.default_button_color,
            fg="white",
        )
        play_btn.grid(row=r, column=1, pady=20, padx=10)

        # edit button.
        play_edit = Button(
            self,
            text="Edit",
            padx=50,
            pady=5,
            command=self.continue_with_selection,
            bg=self.default_button_color,
            fg="white",
        )
        play_edit.grid(row=r, column=2, pady=20, padx=10)

        # add sound button (only shows up in non your library playlists).
        if self.playlist_title != "Your Library":
            # creating the label.
            add_l = Entry(self, width=50)
            add_l.grid(row=r + 1, column=0, padx=20, pady=10)

            # creating the button.
            add_b = Button(
                self,
                text="Add to this Playlist",
                padx=50,
                pady=5,
                bg=self.default_button_color,
                fg="White",
                command=lambda: self.db.add_sound_into_playlist(
                    add_l.get(), self.playlist_title
                ),
            )
            add_b.grid(padx=20, pady=5, row=r + 2, column=0)

        # remove sound from playlist button.
        remove_button = Button(
            self,
            text="Remove",
            padx=50,
            pady=5,
            command=self.remove_button,
            bg="Red",
            fg="White",
        )
        remove_button.grid(row=r, column=3, pady=20, padx=10)

        # Sort by dropdown.
        sort_options = ["Title", "Length", "DateCreated"]
        sort_dropdown = OptionMenu(self, self.dropdown_item, *sort_options)
        sort_dropdown.grid(row=r + 3, column=2)
        sort_dropdown.config(bg=self.default_button_color, fg="White")
        sort_dropdown["menu"].config(bg="GREEN")

        # Go button for dropdown.
        ok_button = Button(
            self,
            text="Go",
            padx=30,
            pady=5,
            command=lambda: self.reload_frame(
                SoundFrame, playlist_title, self.dropdown_item.get()
            ),
            bg="green",
            fg="White",
        )
        ok_button.grid(row=r + 4, column=2, pady=20, padx=10)

        # back button.
        back_button = Button(
            self, text="Back", padx=20, command=lambda: self.change_frame(PlaylistFrame)
        )
        back_button.grid(pady=90, padx=30, row=r + 5, column=0, sticky=W)

    def continue_with_selection(self):
        self.sound_item = self.radio_item.get()
        self.change_frame(EditFrame, sound_argument=self.radio_item.get())

    def remove_button(self):
        self.db.remove_sound_from_playlist(self.radio_item.get(), self.playlist_title)
        self.reload_frame(SoundFrame, self.playlist_title)


class EditFrame(BaseClass):
    """
    Frame for edit screen of our sound archive app.

    Attributes:
        sound_title (str): User chosen sound title from previous frame specifiec using radio buttons.
        active_color: color on button if the button is active.
        inactive_color: color on button if the button is inactive.

    Methods:
        toggle_btn_click: handles activating and deactivating a button when pressed.
    """

    def __init__(self, sound_title, **kwargs):
        BaseClass.__init__(self, **kwargs)
        self.config(bg=self.bg_color)
        self.sound_title = sound_title
        self.active_color = "#FFD700"
        self.inactive_color = "#FFFACD"
        
        self.sound_features = Backend(self.sound_title)

        # [Sound] title
        Label(
            self,
            text=self.sound_title,
            font=(self.font_title, 20),
            padx=50,
            pady=5,
            fg="Black",
            bg=self.bg_color,
        ).grid(pady=10, row=0, column=2, sticky=EW)

        # working in the 0th column: adding ALL edit features.
        Label(
            self, text="Speed", fg="Black", bg=self.bg_color, font=("Courier New", 10)
        ).grid(row=1, column=0, padx=50, pady=15, sticky=W)
        Label(
            self, text="Pitch", fg="Black", bg=self.bg_color, font=("Courier New", 10)
        ).grid(row=2, column=0, padx=50, pady=15, sticky=W)
        Label(
            self, text="Reverse", fg="Black", bg=self.bg_color, font=("Courier New", 10)
        ).grid(row=3, column=0, padx=50, pady=15, sticky=W)
        Label(
            self, text="Overlap", fg="Black", bg=self.bg_color, font=("Courier New", 10)
        ).grid(row=4, column=0, padx=50, pady=15, sticky=W)
        Label(
            self,
            text="Sequential",
            fg="Black",
            bg=self.bg_color,
            font=("Courier New", 10),
        ).grid(row=5, column=0, padx=50, pady=15, sticky=W)
        Label(
            self,
            text="Random Insert",
            fg="Black",
            bg=self.bg_color,
            font=("Courier New", 10),
        ).grid(row=6, column=0, padx=50, pady=15, sticky=W)

        self.speed_val = 1.00
        pitch_val = 1.00

        def adjust_speed_label(is_up):
            if is_up and self.speed_val < 2.00:
                self.speed_val += 0.25
            elif not is_up and self.speed_val > 0.00:
                self.speed_val -= 0.25
            speed_label.config(text="{:.2f}".format(self.speed_val))

        # speed up/down buttons.
        speed_up_button = Button(
            self,
            text="Up",
            fg="Black",
            bg=self.inactive_color,
            padx=10,
            pady=5,
            command=lambda: adjust_speed_label(True),
        )
        speed_up_button.grid(row=1, column=1, sticky=W)
        speed_down_button = Button(
            self,
            text="Down",
            fg="Black",
            bg=self.inactive_color,
            padx=10,
            pady=5,
            command=lambda: adjust_speed_label(False),
        )
        speed_down_button.grid(row=1, column=2, sticky=W)
        # speed Label.
        speed_label = Label(self, text=self.speed_val)
        speed_label.grid(row=1, column=3)

        # pitch up/down buttons.
        pitch_up_button = Button(
            self, text="Up", fg="Black", bg=self.inactive_color, padx=10, pady=5
        )
        pitch_up_button.grid(row=2, column=1, sticky=W)
        pitch_down_button = Button(
            self, text="Down", fg="Black", bg=self.inactive_color, padx=10, pady=5
        )
        pitch_down_button.grid(row=2, column=2, sticky=W)
        # pitch Label.
        Label(self, text=pitch_val).grid(row=2, column=3)

        # reverse button.
        reverse_button = Button(
            self,
            text="Reverse",
            fg="black",
            bg=self.inactive_color,
            padx=10,
            pady=5,
            command=lambda: self.toggle_btn_click(reverse_button),
        )
        reverse_button.grid(row=3, column=1, columnspan=5, sticky=W)

        # overlap.
        overlap_button = Button(
            self,
            text="Overlap",
            fg="Black",
            bg=self.inactive_color,
            padx=10,
            pady=5,
            command=lambda: self.toggle_btn_click(overlap_button),
        )
        overlap_button.grid(row=4, column=1, sticky=W)
        overlap_entry = Entry(self, width=30)
        overlap_entry.grid(row=4, column=2)

        # sequential.
        seq_button = Button(
            self,
            text="Sequential",
            fg="Black",
            bg=self.inactive_color,
            padx=10,
            pady=5,
            command=lambda: self.toggle_btn_click(seq_button),
        )
        seq_button.grid(row=5, column=1, sticky=W)
        seq_entry = Entry(self, width=30)
        seq_entry.grid(row=5, column=2)

        # rand insert.
        rand_button = Button(
            self,
            text="Random Insert",
            fg="Black",
            bg=self.inactive_color,
            padx=10,
            pady=5,
            command=lambda: self.toggle_btn_click(rand_button),
        )
        rand_button.grid(row=6, column=1, sticky=W)
        rand_entry = Entry(self, width=30)
        rand_entry.grid(row=6, column=2)

        # play button.
        button = Button(
            self, text="Play", fg="White", bg=self.default_button_color, padx=30, pady=5
        )
        button.grid(row=7, column=1, sticky=W, pady=20)

        # save button.
        button_save = Button(
            self, text="Save", fg="White", bg=self.default_button_color, padx=30, pady=5, command=self.save_edited_audio
        )
        button_save.grid(row=7, column=2, sticky=E, pady=20)

        # back button.
        back_button = Button(
            self, text="Back", padx=20, command=lambda: self.change_frame(PlaylistFrame)
        )
        back_button.grid(pady=90, padx=30, row=8, column=0, sticky=W)

    def toggle_btn_click(self, button):
        if button["bg"] == self.inactive_color:
            button["bg"] = self.active_color
        else:
            button["bg"] = self.inactive_color
    
    # TODO: go through each sound editing feature on the gui sequentially, add create/update changedAudioSegment each time and at the end of the for loop, we have the new changedAudioSegment
    def save_edited_audio():
        pass


if __name__ == "__main__":
    app = HomeFrame()
    app.mainloop()
