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
        self.root = Tk()
        self.bg_color = "#ead6b8"
        self.screen_size = "950x500"
        self.screen_title = "Saturn Sound Archive"
        self.saturn_instance = Saturn(sys.argv, len(sys.argv))
        self.db = PlaylistManager()
        
    def home_screen(self):
        # initialize screen.
        self.root.geometry(self.screen_size)
        self.root.configure(bg=self.bg_color)
        self.root.title(self.screen_title)
        
        # create title page.
        Label(self.root, text="Saturn Sound Archive", font=("Arial", 25), padx=50, pady=5, fg="Black", bg=self.bg_color).pack(padx=50, pady=5)
        self.root_img = Image.open('./saturn.png')
        self.root_img_tk = ImageTk.PhotoImage(self.root_img)
        self.root_label = Label(self.root, image=self.root_img_tk)
        self.root_label.pack(pady=20)  
        
        # create/configure sound button to move to our next screen.
        self.root_btn = Button(self.root, text="Continue", command=self.playlists_screen, padx=50, pady=5, fg="Black", bg=self.bg_color)
        self.root_btn.pack(pady=20)
    
    def show_playlists_screen(self):
        self.root.destroy()
        next_screen = PlaylistsScreen(self)
        next_screen.playlist_screen()

class PlaylistsScreen():
    def __init__(self):   
        self.gui = Gui()
        self.playlist = Toplevel()
    
    def playlist_screen(self):
        pass

    def show_playlists_screen(self):
        self.gui.root.destroy()
        next_screen = PlaylistsScreen(self)
        next_screen.playlist_screen()
        
class 