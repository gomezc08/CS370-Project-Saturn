- #### NOTE: Install dependencies with `python -m pip install -r ./requirements.txt` in the root directory of the project

- ### NOTE: This project requires either ffmpeg (linux) or libav (windows) to be installed on your system.
  - ### In addition, it now requires a SQL client.

- ### HOW TO RUN GUI: Run `python .\src\gui.py` frnom the command line.
  - ### You can also run our program from the command line interface (CLI). See the docs folder for reference on how to do this.  

# Project Saturn

**TODO:**

- [x] tests!!!!
- [x] comments (new and update big block comment under class name)
- [x] update documetation.md with new functions
- [x] gui backend object
- [x] convert to mp3
- [x] saving and playing in the edit frame
- [x] testing clustering with larger sound files.
- [x] Fix deleting playlists

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
Our goal is to be able to cluster similar sounds (our way to group by generes).
- [x] Create clustering algorithm.
- [x] Embed clustering algorithm in gui to create playlists for each cluster.
- [x] Test implementation on real sounds in gui.


part c: setting up a backend.
Our goal is to extend our sound features from command line to something the gui can utilize (acting as our controller).
- [x] Modify speed.
- [x] Modify pitch.
- [x] Indicate if user wants to reverse a sounds or not.
- [x] Allow user to add another sound to edited sound.
- [x] Allow user to specify a sound to randomly insert in edited sound.
- [x] Give user the choice whether to play edited version or original.
- [x] Set up clustering algorithm.


**GROUP MEMBERS:**

- [x] Neel Troeger
- [x] Chris Gomez
- [x] Aidan von Buschwaldt
- [x] Jas Liu

**PROJECT INDIVIDUAL CONTRIBUTIONS:**

- [x] Chris Gomez: 
    - Implemented DBConnector.py
    - Implemented PlaylistManager.py
    - Implemented SQL.sql
    - Implemented gui.py
    - Contributed to gui_backend.py
    - Contributed to use_cases
    - Contributed to story maps
- Neel Troeger:
    - Implemented gui_backend.py
    - Implemented ml.py
    - Contributed to gui.py
    - Contributed to use cases and story maps
    - Implemented cli
    - Wrote tests for cli

**INDIVIDUAL REFLECTIONS:**

- [x] Chris Gomez: The gui was the biggest learning curve I had to spend a whole saturday flipping through yt tutorials and when it came to integrating, I had to redo my gui a few times to make it more elegant and fit some sort of software design rather than having a bunch of random functions. Another big challenge was the embedded sql aspect using python since we had just learnt it this last semester in databases. I wish we had came up with like a pause/play button. I also would have loved to have some sort of media sounds storage system so we weren't reliant on a directory. I also would love to make the gui visually more organized because I feel it is a little messy.

- Neel Troeger: Because of how the cli was setup (for single use cases), I had to create a new backend for the gui. This was more of a challenge than I thought, since I wasn't working directly on implementing the gui, and what I originally had in my head was likely not what Chris had in his head. This led to a lot of back and forth between us to make sure the gui and backend were in sync. In addition, since the backend is set-up to load a single audio file and change only that, implementing it was a bit more difficult than reusing code from the cli. Implementing the clustering was less difficult, since I am taking a machine learning class this semester. I used DBSCAN (Density-Based Spatial Clustering of Applications with Noise) to cluster the sounds, mostly because that way I didn't have to pre-specify a target number of clusters, which would aid in scalability in future usage. I still had to figure out how to extract features from the sound files, which was a bit of a challenge, but was resolved by using the librosa library.