import sys
import os
import threading
import simpleaudio as sa
from pydub import AudioSegment
from pydub.effects import speedup
import pydub.playback as playback
import pydub.effects as effects
import librosa
import soundfile as sf
import pandas as pd


class Saturn:
    """
    The Saturn class represents a command-line interface for audio file manipulation.

    Attributes:
        argv (list): The list of command-line arguments.
        argvlen (int): The length of the argv list.
        isPlaying (bool): Indicates whether an audio file is currently being played.
        audioFormats (list): A list of supported audio file formats.

    Methods:
        getInstance(): Returns an instance of the Saturn class.
        print_help(): Prints the help message with available commands and their usage.
        count_arguments(): Counts the number of arguments passed.
        play(file_path): Plays an audio file.
        play_overlap(queue): Plays multiple audio files overlapping each other.
        play_sequential(queue): Plays multiple audio files sequentially.
        play_command(): Executes the play command.
        overlap_command(): Executes the overlap command.
        sequential_command(): Executes the sequential command.
        list_command(): Lists all audio files in the current directory.
        rename_command(): Renames an audio file.
        transcode_command(): Changes the audio format of a file.
        play_backwards_command(): Plays an audio file backwards.
    """

    def __init__(self, argv, argvlen):

        self.argv = argv
        self.argvlen = argvlen

        self.isPlaying = False
        # small list of audio formats
        # necessary for the list command
        self.audioFormats = [
            ".wav",
            ".mp3",
            ".ogg",
            ".flac",
            ".m4a",
            ".wma",
            ".aiff",
            ".alac",
            ".aac",
            ".amr",
            ".au",
            ".awb",
            ".dct",
            ".dss",
            ".dvf",
            ".gsm",
            ".iklax",
            ".ivs",
            ".m4p",
            ".mmf",
            ".mpc",
            ".msv",
            ".nmf",
            ".nsf",
            ".oga",
            ".mogg",
            ".opus",
            ".ra",
            ".rm",
            ".raw",
            ".sln",
            ".tta",
            ".vox",
            ".wv",
            ".webm",
            ".8svx",
        ]

    def getInstance(argv, argvlen):
        """
        if an instance of Saturn already exists, return it
        otherwise, create a new instance
        """
        if not hasattr(Saturn, "_instance"):
            Saturn._instance = Saturn(argv=argv, argvlen=argvlen)
        return Saturn._instance

    def print_help(self):
        """print the help message with available commands and their usage"""

        # this is kinda an insane way to do this but its so much cleaner than a bunch of print statements
        df = pd.DataFrame(columns=["Command", "Description", "Usage"])
        commands = [
            {
                "Command": "-h,--help",
                "Description": "Print this help message.",
                "Usage": f"python {self.argv[0]} --help",
            },
            {
                "Command": "-c,--count",
                "Description": "Count the number of arguments.",
                "Usage": f"python {self.argv[0]} --count",
            },
            {
                "Command": "-p,--play",
                "Description": "Play a file.",
                "Usage": f"python {self.argv[0]} --play file_path",
            },
            {
                "Command": "-s,--sequential",
                "Description": "Play files sequentially.",
                "Usage": f"python {self.argv[0]} --sequential file_path1 file_path2 ...",
            },
            {
                "Command": "-o,--overlap",
                "Description": "Play files overlapping each other.",
                "Usage": f"python {self.argv[0]} --overlap file_path1 file_path2 ...",
            },
            {
                "Command": "-l,--list",
                "Description": "List audio files in the current directory.",
                "Usage": f"python {self.argv[0]} --list",
            },
            {
                "Command": "-r,--rename",
                "Description": "Rename an audio file.",
                "Usage": f"python {self.argv[0]} --rename original_name new_name",
            },
            {
                "Command": "-t,--transcode",
                "Description": "Change audio format.",
                "Usage": f"python {self.argv[0]} --transcode original_file.wav new_file.mp3",
            },
            {
                "Command": "-b,--play-backwards",
                "Description": "Play a file backward.",
                "Usage": f"python {self.argv[0]} --play-backwards file_path",
            },
            {
                "Command": "-a,--concatenate",
                "Description": "Concatenate audio files.",
                "Usage": f"python {self.argv[0]} --concatenate file1 file2 file3 ... name.extension crossfade",
            },
        ]

        for command in commands:
            df = df._append(command, ignore_index=True)

        print(df.to_string(index=False))
        sys.exit(0)

    def count_arguments(self):
        """count the number of arguments passed"""
        print(
            "counted ",
            self.argvlen - 2,
            " argument" + "s" if self.argvlen - 2 > 1 else "",
        )
        sys.exit(0)

    def getSound(self, file_path):
        return AudioSegment.from_file(
            file_path,
            format=(
                file_path.split(".")[-1]
                if file_path[0] != "."
                else file_path[1:].split(".")[-1]
            ),
        )

    def play(self, file_path):
        """play an audio file"""
        self.isPlaying = True
        sound = self.getSound(file_path)
        playback.play(sound)
        self.isPlaying = False

    def play_overlap(self, queue):
        """play files overlapping using the play method
        and threading to play multiple files at the same time"""
        threads = []
        print(f"I am now playing the following overlapping each other: {queue}")
        for file_path in queue:
            thread = threading.Thread(target=self.play, args=(file_path,))
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def play_sequential(self, queue):
        """play files sequentially using the play method"""
        while not self.isPlaying and queue:
            for file_path in queue:
                print("Playing:", file_path)
                self.play(file_path)
                queue = queue[1:]

    def play_command(self):
        """play a file using the play method"""
        if self.argvlen > 2:
            file_path = self.argv[2]
            if file_path[0] == ".":
                file_path = str(os.getcwd()) + file_path[1:]
            print("I am now playing", file_path)
            self.play(file_path)
        else:
            print(
                "Error: Please provide a file path after the --play or -p option.",
                file=sys.stderr,
            )
            sys.exit(1)

    def overlap_command(self):
        """play files overlapping using the play_overlap method"""
        file_paths = []
        if self.argvlen > 2:
            for i in self.argv[2:]:
                file_paths.append(i)
            self.play_overlap(file_paths)
        else:
            print(
                "Error: Please provide file paths after the --overlap or -o option.",
                file=sys.stderr,
            )
            sys.exit(1)

    def sequential_command(self):
        """play files sequentially using the play method"""
        file_paths = []
        if self.argvlen > 2:
            for i in self.argv[2:]:
                file_paths.append(i)
            print(file_paths)
            self.play_sequential(file_paths)
        else:
            print(
                "Error: Please provide file paths after the --sequential or -s option.",
                file=sys.stderr,
            )
            sys.exit(1)

    def list_command(self):
        """print all files in the current directory recursively with audio file extensions"""
        # this WILL not work if the cwd is /src/
        # dirs is necessary for the os.walk function, don't remove it
        for root, dirs, files in os.walk(os.getcwd()):
            for file in files:
                if file.endswith(tuple(self.audioFormats)):
                    print(os.path.join(root, file))

    def rename_command(self):
        """rename an audio file, take the original name and the new one, doesn't change file extension"""
        if self.argvlen > 3:
            original_name = self.argv[2]
            extension = (
                original_name.split(".")[-1]
                if original_name[0] != "."
                else original_name[1:].split(".")[-1]
            )
            new_name = self.argv[3]
            if "." not in new_name[1:] or "." not in original_name[1:]:
                print("Error: Please provide the file extension(s).", file=sys.stderr)
                sys.exit(1)
            elif original_name[1:].split(".")[-1] != new_name[1:].split(".")[-1]:
                print(
                    "This function does not convert between audio formats. Using original file extension..."
                )
            new_name = (
                new_name.split(".")[0]
                if new_name[0] != "."
                else "." + new_name[1:].split(".")[0] + "." + extension
            )
            os.rename(original_name, new_name)
        else:
            print(
                "Error: Please provide two arguments after after the --rename or -r option.",
                file=sys.stderr,
            )
            sys.exit(1)

    def transcode_command(self):
        """Transcode an audio file to a different format."""
        # Usage: python saturn_cli.py -t original_file new_file
        if self.argvlen == 4:
            original_file = self.argv[2]
            new_file = self.argv[3]

            # Determine file extensions
            original_extension = (
                original_file.split(".")[-1]
                if original_file[0] != "."
                else original_file[1:].split(".")[-1]
            )
            new_extension = (
                new_file.split(".")[-1]
                if new_file[0] != "."
                else new_file[1:].split(".")[-1]
            )

            # Load the audio and export it to the new format
            sound = AudioSegment.from_file(original_file, format=original_extension)
            sound.export(new_file, format=new_extension)
            print(
                f"File transcoded successfully from {original_extension} to {new_extension}"
            )

        else:
            print("Error: Please provide two arguments after the -t option.")
            sys.exit(1)

    def play_backwards_command(self):
        """play a file using the play method"""
        if self.argvlen > 2:
            file_path = self.argv[2]
            if file_path[0] == ".":
                file_path = str(os.getcwd()) + file_path[1:]
            print("I am now playing", file_path)
            self.isPlaying = True
            # can't use the play function because it only takes the file path.
            # this will have to be ammended in the future
            # TODO ^
            sound = AudioSegment.from_file(
                file_path,
                format=(
                    file_path.split(".")[-1]
                    if file_path[0] != "."
                    else file_path[1:].split(".")[-1]
                ),
            )
            playback.play(sound.reverse())
            self.isPlaying = False
        else:
            print(
                "Error: Please provide a file path after the --play or -p option.",
                file=sys.stderr,
            )
            sys.exit(1)

    def concatenate_command(self):
        """concatenate audio files with crossfade amount (if not supplied, then 0)"""
        # python saturn_cli.py -a file1 file2 file3 ... new_name.extension crossfade
        if self.argvlen > 4:
            file_paths = self.argv[2:-3]
            new_name = self.argv[-2]
            extension = new_name.split(".")[-1]
            crossfade = self.argv[-1] if self.argv[-1].isdigit() else 0
            if "." not in new_name[1:]:
                print("Error: Please provide the file extension.", file=sys.stderr)
                sys.exit(1)
            new_name = (
                new_name.split(".")[0]
                if new_name[0] != "."
                else "." + new_name[1:].split(".")[0] + "." + extension
            )
            sounds = [AudioSegment.from_file(f) for f in file_paths]
            combined = sounds[0]
            for sound in sounds[1:]:
                combined = combined.append(sound, crossfade=0)
            combined.export(new_name, format=extension)
        else:
            print(
                "Error: Please provide at least two file paths and a new name with extension after the --concatenate or -a option.",
                file=sys.stderr,
            )
            sys.exit(1)

    def change_speed_command(self):
        # change the speed of an audio file
        # Note: seems to warp the quality of the audio (maybe need to separate tempo and pitch?)
        # Need to add an error if value is below 1
        if self.argvlen > 3:
            file_path = self.argv[2]
            speed = float(self.argv[3])
            if file_path[0] == ".":
                file_path = str(os.getcwd()) + file_path[1:]
            print("I am now playing", file_path)
            sound = AudioSegment.from_file(
                file_path,
                format=(
                    file_path.split(".")[-1]
                    if file_path[0] != "."
                    else file_path[1:].split(".")[-1]
                ),
            )
            sound = speedup(sound, speed)
            playback.play(sound)
        else:
            print(
                "Error: Please provide a file path and a speed after the --change-speed or -z option.",
                file=sys.stderr,
            )
            sys.exit(1)

    def change_pitch_command(self):
        # Change the pitch of an audio file
        if self.argvlen > 3:
            file_path = self.argv[2]
            semitones = float(
                self.argv[3]
            )  # The number of semitones to shift the pitch
            if file_path[0] == ".":
                file_path = str(os.getcwd()) + file_path[1:]
            print(
                "Playing", file_path, "with pitch changed by", semitones, "semitones."
            )
            # Load the audio file with librosa and shift the pitch
            y, sr = librosa.load(file_path, sr=None)
            y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=semitones)
            # Save the pitch-shifted audio to a temporary file
            temp_file_path = "temp_pitch_shifted.wav"
            # Use soundfile to write the pitch-shifted audio to a temporary file
            sf.write(temp_file_path, y_shifted, sr)
            # Load the pitch-shifted audio with pydub
            sound_with_changed_pitch = AudioSegment.from_file(temp_file_path)
            # Play the modified audio directly
            playback.play(sound_with_changed_pitch)
            # Remove the temporary file
            os.remove(temp_file_path)
        else:
            print(
                "Error: Please provide a file path and the number of semitones to shift the pitch.",
                file=sys.stderr,
            )
            sys.exit(1)


class CommandLineParser:
    """
    A class that parses command line arguments and executes corresponding commands.

    Attributes:
        argv (list): The list of command line arguments.

    Methods:
        __init__(self, argv): Initializes the CommandLineParser object.
        parse_arguments(self): Parses the command line arguments and executes the corresponding command.
    """

    def __init__(self, argv):
        self.argv = argv
        # call saturn's getInstance method to get an instance of the Saturn class
        self.saturn = Saturn.getInstance(argv, len(argv))
        self.parse_arguments()

    def parse_arguments(self):
        """
        Parses the command line arguments and executes the corresponding command.
        """
        command = self.argv[1] if len(self.argv) > 1 else None

        match command:
            case None | "--help" | "-h":
                self.saturn.print_help()
            case "-c" | "--count":
                self.saturn.count_arguments()
            case "-p" | "--play":
                self.saturn.play_command()
            case "-s" | "--sequential":
                self.saturn.sequential_command()
            case "-o" | "--overlap":
                self.saturn.overlap_command()
            case "-l" | "--list":
                self.saturn.list_command()
            case "-r" | "--rename":
                self.saturn.rename_command()
            case "-t" | "--transcode":
                self.saturn.transcode_command()
            case "-b" | "--play-backwards":
                self.saturn.play_backwards_command()
            case "-a" | "--concatenate":
                self.saturn.concatenate_command()
            case "-z" | "--change-speed":
                self.change_speed_command()
            case "-w" | "--change-pitch":
                self.change_pitch_command()
            case _:
                errors = self.argv[1:]
                print(
                    self.argv[0],
                    "error, unexpected arguments ",
                    errors,
                    file=sys.stderr,
                )
                print("Try", self.argv[0], "--help")
                sys.exit(1)


if __name__ == "__main__":
    # create a command line parser and parse the command line arguments
    parser = CommandLineParser(sys.argv)
