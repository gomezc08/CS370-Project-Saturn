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


class CommandLineParser:
    """
    A class that parses command line arguments and executes corresponding commands.

    Args:
        argv (list): The list of command line arguments.

    Attributes:
        argv (list): The list of command line arguments.
        argvlen (int): The length of the command line arguments.
        isPlaying (bool): A flag indicating whether audio is currently being played.
        audioFormats (list): A list of audio formats.
    Methods:
        print_help: Print the help message.
        count_arguments: Count the number of arguments passed.
        play: Play a file using the simpleaudio library.
        play_overlap: Play files overlapping using the play method and threading.
        play_sequential: Play files sequentially using the play method.
        play_command: Play a file using the play method.
        overlap_command: Play files overlapping using the play_overlap method.
        sequential_command: Play files sequentiall using the play method.
        list_command: Print all files in the current directory recursively with audio file extensions.
        rename_command: Rename an audio file.
        transcode_command: Change audio format.
        play_backwards_command: Play a file backward.
        concatenate_command: Concatenate audio files.
        parse_arguments: Parse the command line arguments and execute the corresponding command.
    """

    def __init__(self, argv):
        # initialize the command line parser
        self.argv = argv
        self.argvlen = len(argv)
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

    def print_help(self):
        # this is hacky, but it is the only way to get the help message to print nicely without too much work
        print(
            "Commands:            Description:                                 Usage:"
        )
        print(
            "\n-h,--help            Print this help message.                     python {} --help".format(
                self.argv[0]
            )
        )
        print(
            "-c,--count           Count the number of arguments.               python {} --count".format(
                self.argv[0]
            )
        )
        print(
            "-p,--play            Play a file.                                 python {} --play file_path".format(
                self.argv[0]
            )
        )
        print(
            "-s,--sequential      Play files sequentially.                     python {} --sequential file_path1 file_path2 ...".format(
                self.argv[0]
            )
        )
        print(
            "-o,--overlap         Play files overlapping each other.           python {} --overlap file_path1 file_path2 ...".format(
                self.argv[0]
            )
        )
        print(
            "-l,--list            List audio files in the current directory.   python {} --list".format(
                self.argv[0]
            )
        )
        print(
            "-r,--rename          Rename an audio file.                        python {} --rename original_name new_name".format(
                self.argv[0]
            )
        )
        print(
            "-t,--transcode       Change audio format.                         python {} --transcode original_file.wav new_file.mp3".format(
                self.argv[0]
            )
        )
        print(
            "-b,--play-backwards  Play a file backward.                        python {} --play-backwards file_path".format(
                self.argv[0]
            )
        )
        print(
            "-a,--concatenate     Concatenate audio files.                     python {} --concatenate file_path1 file_path2 ... new_name extension".format(
                self.argv[0]
            )
        )
        sys.exit(0)

    def count_arguments(self):
        # count the number of arguments passed
        print(
            "counted ",
            self.argvlen - 2,
            " argument" + "s" if self.argvlen - 2 > 1 else "",
        )
        sys.exit(0)

    def play(self, file_path):
        # play a file using the simpleaudio library
        if file_path.endswith(".wav"):
            self.isPlaying = True
            wave_obj = sa.WaveObject.from_wave_file(file_path)
            play_obj = wave_obj.play()
            play_obj.wait_done()
            self.isPlaying = False
        else:
            self.isPlaying = True
            sound = AudioSegment.from_file(
                file_path,
                format=(
                    file_path.split(".")[-1]
                    if file_path[0] != "."
                    else file_path[1:].split(".")[-1]
                ),
            )
            playback.play(sound)
            self.isPlaying = False

    def play_overlap(self, queue):
        # play files overlapping using the play method
        # and threading to play multiple files at the same time
        threads = []
        for file_path in queue:
            thread = threading.Thread(target=self.play, args=(file_path,))
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def play_sequential(self, queue):
        # play files sequentially using the play method
        while not self.isPlaying and queue:
            for file_path in queue:
                print("Playing:", file_path)
                self.play(file_path)
                queue = queue[1:]

    def play_command(self):
        # play a file using the play method
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
        # play files overlapping using the play_overlap method
        file_paths = []
        if self.argvlen > 2:
            for i in self.argv[2:]:
                file_paths.append(i)
                print("I am now playing files overlapping each other:", i)
            self.play_overlap(file_paths)
        else:
            print(
                "Error: Please provide file paths after the --overlap or -o option.",
                file=sys.stderr,
            )
            sys.exit(1)

    def sequential_command(self):
        # play files sequentially using the play method
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
        # print all files in the current directory recursively with audio file extensions
        # this WILL not work if the cwd is /src/
        for root, dirs, files in os.walk(os.getcwd()):
            for file in files:
                if file.endswith(tuple(self.audioFormats)):
                    print(os.path.join(root, file))

    def rename_command(self):
        # rename an audio file, take the original name and the new one, doesn't change file extension
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
        # Change audio format
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
        # play a file using the play method
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
        # concatenate multiple audio files (>2) into one file
        # take the file paths, the new name, the new file extension, and the crossfade amount
        # TODO fix this shit
        if self.argvlen > 4:
            file_paths = self.argv[2:-3]
            crossfade = self.argv[-3]
            new_name = (
                self.argv[-2].split(".")[0]
                if self.argv[-2][0] != "."
                else "." + self.argv[-2][1:].split(".")[0]
            )
            extension = (
                self.argv[-1].split(".")[-1]
                if self.argv[-1][0] != "."
                else self.argv[-1][1:].split(".")[-1]
            )
            sound = AudioSegment.from_file(file_paths[0], format=extension)
            for file_path in file_paths[1:]:
                sound = sound.append(
                    AudioSegment.from_file(file_path, format=extension),
                    crossfade=crossfade,
                )
            sound.export(new_name + "." + extension, format=extension)
        else:
            print(
                "Error: Please provide at least three arguments after the --concatenate or -a option.",
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
                sound = AudioSegment.from_file(file_path,
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
            semitones = float(self.argv[3])  # The number of semitones to shift the pitch
            if file_path[0] == ".":
                file_path = str(os.getcwd()) + file_path[1:]
            print("Playing", file_path, "with pitch changed by", semitones, "semitones.")
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
            print("Error: Please provide a file path and the number of semitones to shift the pitch.", file=sys.stderr)
            sys.exit(1)

    def parse_arguments(self):
        # parse the command line arguments and execute the corresponding command
        command = self.argv[1] if len(self.argv) > 1 else None

        match command:
            case None | "--help" | "-h":
                self.print_help()
            case "-c" | "--count":
                self.count_arguments()
            case "-p" | "--play":
                self.play_command()
            case "-s" | "--sequential":
                self.sequential_command()
            case "-o" | "--overlap":
                self.overlap_command()
            case "-l" | "--list":
                self.list_command()
            case "-r" | "--rename":
                self.rename_command()
            case "-t" | "--transcode":
                self.transcode_command()
            case "-b" | "--play-backwards":
                self.play_backwards_command()
            case "-a" | "--concatenate":
                self.concatenate_command()
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
    parser.parse_arguments()
