- #### NOTE: Install dependencies with `python -m pip install -r ./requirements.txt` in the root directory of the project

- ### NOTE: This project requires either ffmpeg (linux) or libav (windows) to be installed on your system.
  - ### In addition, it now requires a SQL client.

- ### HOW TO RUN GUI: Run `python .\src\gui.py` frnom the command line.
  - ### You can also run our program from the command line interface (CLI). See the docs folder for reference on how to do this.  

# Project Saturn

**TODO:**

- [x] tests!!!!
- [x] comments (new and update big block comment under class name)
- [ ] update documetation.md with new functions
- [x] gui backend object
- [x] convert to mp3
- [x] saving and playing in the edit frame
- [x] testing clustering with larger sound files.
- [ ] Fix deleting playlists
- [ ] Autodelete songs on startup?

LIMITATIONS:
- Files with long titles are incompatible with the db stuff

**DONE:**

- [x] play function
- [x] -p flag : calls play function
- [x] sequential play function
- [x] overlapping play function
- [x] -s : calls sequential play function
- [x] -o : calls overlapping play function
- [x] suppress error messages
- [x] mp3 flac etc support!!!!

**EPOCH ONE REQS:**

- [x] A user must be able to interact with your program from the command line via a simple text-based interface.
- [x] From that command-line interface, the user should be able to get a list of available commands.
- [x] A user must be able to get a list of available sounds to play.
- [x] A user must be able to play back a single sound.
- [x] A user must be able to listen to multiple sounds simultaneously (i.e., layer multiple sounds on top of each other).
- [x] A user must be able to listen to a sequence of sounds.
- [x] A user must be able to rename a sound.
- [x] These requirements may be met either with a single large command-line program that implements all of them, or by a suite of smaller command-line programs that focus on a subset of features

**EPOCH TWO REQS:**

Part a: enhanced ways to listen to sounds.
Our goal is to offer users a variety of distinctive methods to listen to sounds and customize them, enabling them to edit and save their creations effortlessly.

- [x] Insert audio clips in the middle of a sound during editing.
- [x] Rename an audio file.
- [x] Change sound audio format.
- [x] Play a sound backwards.
- [x] Concatenate audio file.
- [x] Adjust speed of sound clip.
- [x] Adjust sound pitch.

Part b: ways to characterize and organize the sounds.
Our goal is to establish a comprehensive database and empower users to categorize and organize sounds efficiently. Users will have the flexibility to specify the table column for sorting purposes, enhancing their ability to navigate and manage sound data effectively.

- [x] Sort playlist by title.
- [x] Sort playlist by date.
- [x] Sort playlist by sound length.

Part c:

- [x] Unit testing (Saturn CLI)
- [x] Unit testing (Database)

**EPOCH THREE REQS:**

part a: setting up a gui using tkinter.
Our goal is to fully implement the gui and bridge our backend and databases using an mvc architecture.
- [x] Create frame for home, playlist, sound, and edit screens.
- [x] Connect database to gui.
- [x] Use database implementation to show all playlists in our screen.
- [x] Select, add, and remove playlist feature on gui.
- [x] Use database implementation to show all sounds in specified playlist.
- [x] Play, remove sound from playlist, and edit features for a sound.
- [x] Sort by feature on gui to sort sounds in a playlist by title, length, or date added.
- [x] Use sound features developed in epoch 1 to allow user to edit a specified sound.
- [x] Save feature to save an edited sound.

part b: machine learning with clustering.

part c: setting up a backend.
Our goal is to extend our sound features from command line to something the gui can utilize.
- [x]


**GROUP MEMBERS:**

- [x] Neel Troeger
- [x] Chris Gomez
- [x] Aidan von Buschwaldt
- [x] Jas Liu

**EPOCH TWO CONTRIBUTIONS:**

- [x] Chris Gomez: DBConnector.py, PlaylistManager.py, UML diagram, started gui.py, and contributed to unit_testing.py, story map, and user stories.
- [x] Neel: Audio transcoding, audio concatenation, audio reversal, unit testing for the cli.

**EPOCH TWO CHALLENGES AND MODIFICATION ANTICIPATIONS:**

- [x] Chris Gomez: I tackled the challenge of setting up a connection to a MySQL workbench on my laptop. It was my first time dealing with database connections, cursors, and writing queries. Despite the initial difficulties, I successfully established the link. Looking ahead, I plan to move away from using lists to manage playlist sounds and focus on optimizing query performance through indexing strategies.
- [x] Neel Troeger: Pydub was very easy to work with, providing an interface to manipulate audio files using ffmpeg/libav. Writing the audio transcoding command was quick and easy, but the audio concatenation was a bit more difficult, mostly because of how many inputs it took. I also had to write a function to reverse audio files, which was not very hard, but I learned that my earlier implementation for Epoch 1 did not work as expected. The most difficult part was writing the unit tests, since we went such along time without writing any. At least now that they exist, we can continue to add more as we add more features. 

**PROJECT INDIVIDUAL CONTRIBUTIONS:**

- [x] Chris Gomez: 
    - Implemented DBConnector.py
    - Implemented PlaylistManager.py
    - Implemented gui.py
    - Contributed to use_cases
    - Contributed to gui_backend.py

**INDIVIDUAL REFLECTIONS:**

- [x] Chris Gomez: The gui was the biggest learning curve I had to spend a whole saturday flipping through yt tutorials and when it came to integrating, I had to redo my gui a few times to make it more elegant and fit some sort of software design rather than having a bunch of random functions. Another big challenge was the embedded sql aspect using python since we had just learnt it this last semester in databases. I wish we had came up with like a pause/play button. I also would have loved to have some sort of media sounds storage system so we weren't reliant on a directory. I also would love to make the gui visually more organized because I feel it is a little messy. 