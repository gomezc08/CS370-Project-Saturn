- #### NOTE: Install dependencies with `python -m pip install -r ./requirements.txt` in the root directory of the project

- ### NOTE: This project requires either ffmpeg (linux) or libav (windows) to be installed on your system.
  - ### In addition, it now requires a SQL client.

## CONNECTING TO MYSQL WORKBENCH

- [x] Start by downloading the SQLTools extension developed by Matheus Teixeira.
- [x] Navigate to SQLtools extensions, accessible from the left panel.
- [x] Click on "add new connection", then select "Search VSCode marketplace".
- [x] Locate and install "SQLTools MySQL/MariaDB" from the available options, typically found as the first link.
- [x] On SQLTools Settings tab, click on MySQL and enter the following information...
- [x] Connection name: saturn_sql
- [x] Server Address: localhost
- [x] Port: 3307
- [x] Database: soundarchive
- [x] Username: root
- [x] Password word: whatever you want but I suggest Ask on connect. Here is the password: !WhitmanMemo08?
- [x] Test/save the connection.
- [x] Before running SQL commands each time, make sure you connect/disconnect to the database. You can use the SQLTools to view tables/data of our playlists.

# Project Saturn

**TODO:**

- [x] tests!!!!
- [x] comments (new and update big block comment under class name)
- [ ] update documetation.md with new functions
- [x] gui backend object
- [x] convert to mp3
- [x] saving and playing in the edit frame
- [ ] testing clustering with larger sound files.
- [ ] Fix deleting playlists

**DONE:**

- [x] play function
- [x] -p flag : calls play function
- [x] sequential play function
- [x] overlapping play function
- [x] -s : calls sequential play function
- [x] -o : calls overlapping play function
- [x] suppress error messages
- [x] mp3 flac etc support!!!!

## EPOCH ONE REQS

- [x] A user must be able to interact with your program from the command line via a simple text-based interface.
- [x] From that command-line interface, the user should be able to get a list of available commands.
- [x] A user must be able to get a list of available sounds to play.
- [x] A user must be able to play back a single sound.
- [x] A user must be able to listen to multiple sounds simultaneously (i.e., layer multiple sounds on top of each other).
- [x] A user must be able to listen to a sequence of sounds.
- [x] A user must be able to rename a sound.
- [x] These requirements may be met either with a single large command-line program that implements all of them, or by a suite of smaller command-line programs that focus on a subset of features

## EPOCH TWO REQS

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

## Group members

- Neel Troeger
- Chris Gomez
- Aidan von Buschwaldt
- Jas Liu

## Epoch Two Contributions.

- Chris Gomez: DBConnector.py, PlaylistManager.py, UML diagram, started gui.py, and contributed to unit_testing.py, story map, and user stories.
- Neel: Audio transcoding, audio concatenation, audio reversal, unit testing for the cli.

## Epoch Two Challenges and modification anticipations.

- Chris Gomez: I tackled the challenge of setting up a connection to a MySQL workbench on my laptop. It was my first time dealing with database connections, cursors, and writing queries. Despite the initial difficulties, I successfully established the link. Looking ahead, I plan to move away from using lists to manage playlist sounds and focus on optimizing query performance through indexing strategies.
- Neel Troeger: Pydub was very easy to work with, providing an interface to manipulate audio files using ffmpeg/libav. Writing the audio transcoding command was quick and easy, but the audio concatenation was a bit more difficult, mostly because of how many inputs it took. I also had to write a function to reverse audio files, which was not very hard, but I learned that my earlier implementation for Epoch 1 did not work as expected. The most difficult part was writing the unit tests, since we went such along time without writing any. At least now that they exist, we can continue to add more as we add more features. 

## Command Lines.

- python .\PlaylistManager.py in database directory to initialize playlists and create an example playlist and add sounds to it and view it (part b of epoch 2)!
