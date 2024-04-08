# Command Line Audio Player

This documentation provides information on a simple command-line audio player written in Python. The audio player allows users to play, list, and rename audio files, as well as play multiple files sequentially or overlapping.

## Usage

```bash
python src/saturn_cli.py [options] [arguments]
```

### Options

- `-h`, `--help`: Print the help message.
- `-c`, `--count`: Count the number of arguments.
- `-p`, `--play`: Play a single audio file.
- `-s`, `--sequential`: Play multiple audio files sequentially.
- `-o`, `--overlap`: Play multiple audio files overlapping each other.
- `-l`, `--list`: List all audio files in the current directory recursively.
- `-r`, `--rename`: Rename an audio file.
- `-t`, `--transcode`: Change audio format.
- `-b`, `--play-backwards`: Play a file backward.
- `-a`, `--concatenate`: Concatenate audio files.
- `-z`, `--change-speed`: speedup audio file
- `-w`, `--change-pitch`: Change pitch of audio file

## Commands

### `play` Command

```bash
python src/saturn_cli.py --play file_path
```

- Play a single audio file specified by `file_path`.
- Note that file types other than `.wav` are not supported on Windows.

### `sequential` Command

```bash
python src/saturn_cli.py --sequential file1 file2 ... fileN
```

- Play multiple audio files sequentially. Provide the file paths as arguments.

### `overlap` Command

```bash
python src/saturn_cli.py --overlap file1 file2 ... fileN
```

- Play multiple audio files overlapping each other. Provide the file paths as arguments.

### `list` Command

```bash
python src/saturn_cli.py --list
```

- List all audio files in the current directory recursively.

### `rename` Command

```bash
python src/saturn_cli.py --rename original_name new_name
```

- Rename an audio file. Provide the original and new names as arguments.

### `transcode` Command

```bash
python src/saturn_cli.py --transcode original_name new_name file_extension
```

- Change audio format. Provide the original file name, new file name, and the desired file extension.

### `play-backwards` Command

```bash
python src/saturn_cli.py --play-backwards file_path
```

- Play a file backward. Provide the file path as an argument.

### `concatenate` Command

```bash
python src/saturn_cli.py --concatenate file_path1 file_path2 ... new_name extension
```

- Concatenate audio files into one file. Provide file paths, the new name, and the file extension.

### `speedup` Command

```bash
python src/saturn_cli.py --change-speed file_path number
```

- Play a file sped up. Provide file name, as well as a number above 1.

### `change-pitch` Command

```bash
python src/saturn_cli.py --change-pitch file_path number
```

- Play a file with a different pitch. Provide file name, as well as how many semitones you want to raise the pitch. 

## Examples

1. Display the help message:

```bash
python src/saturn_cli.py --help
```

2. Count the number of arguments:

```bash
python src/saturn_cli.py --count arg1 arg2 arg3
```

3. Play a single audio file:

```bash
python src/saturn_cli.py --play audio_file.wav
```

4. Play multiple audio files sequentially:

```bash
python src/saturn_cli.py --sequential file1.wav file2.wav file3.wav
```

5. Play multiple audio files overlapping:

```bash
python src/saturn_cli.py --overlap file1.wav file2.wav file3.wav
```

6. List all audio files in the current directory:

```bash
python src/saturn_cli.py --list
```

7. Rename an audio file:

```bash
python src/saturn_cli.py --rename old_name.wav new_name.wav
```

8. Change audio format:

```bash
python src/saturn_cli.py --transcode original_name new_name file_extension
```

9. Play a file backward:

```bash
python src/saturn_cli.py --play-backwards audio_file.wav
```

10. Concatenate audio files:

```bash
python src/saturn_cli.py --concatenate file1.wav file2.wav new_file.wav wav
```

11. Play a file sped up:

```bash
python src/saturn_cli.py --change-speed file1.wav 2.0
```

12. Play a file with altered pitch:

```bash
python src/saturn_cli.py --change-pitch file1.wav 6.0
```

## Note

- Make sure to provide valid file paths and follow the specified command syntax.

## Implementation Details

The audio player is implemented in Python and uses the following libraries:

- `simpleaudio`: for playing `.wav` files.
- `pydub`: for handling various audio file formats and playback functionality.
- `threading`: for concurrent playback of multiple files.
- `os`: for file and directory operations.

The command-line parser (`CommandLineParser` class) is responsible for parsing the provided arguments and executing the corresponding commands. The supported commands include playing, listing, renaming, changing formats, playing backward, and concatenating audio files. Ensure that the required dependencies are installed before using the command-line audio player.