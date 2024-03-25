# NOTE: Install dependencies with `python -m pip install -r ./requirements.txt` in the root directory of the project

# NOTE: This requires ffmpeg to be installed on your system
- if on windows, use `scoop install ffmpeg`
- if on mac, use `brew install ffmpeg`
- if on linux use your package manager to install ffmpeg
  - ex. `sudo apt-get install ffmpeg`
  - ex. `sudo pacman -S ffmpeg`
  - ex. `sudo dnf install ffmpeg`

**TODO:** Give basic instructions for running your program. Note it needs Python version 3.10 or higher.

# Project Saturn                                                                                 
**TODO:**       
- [ ] tests!!!!
- [ ] comments (new and update big block comment under class name)
- [ ] update documetation.md with new functions


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

## Group member contributions
- Neel Troeger: Code, Documentation, Use cases
- Chris Gomez: Code, Use cases
- Aidan von Buschwaldt: Use cases
- Jas Liu: Code, Use cases

## Code Testing

To test the functionality of the code we performed manual testing. We tested all functions and their respective flags.

To see full documentation of the project so far, please see the documentation.md file in the `docs` directory of the project.
