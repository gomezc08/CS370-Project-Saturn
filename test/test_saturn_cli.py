import unittest
import sys
from io import StringIO
from unittest.mock import patch, MagicMock

sys.path.append("src")
from saturn_cli import Saturn, CommandLineParser
from pydub import AudioSegment


class TestSaturn(unittest.TestCase):

    def test_getSound(self):
        saturn = Saturn([], 0)
        file_path = "sounds/coffee.wav"
        expected_format = "wav"
        expected_sound = AudioSegment.from_file(file_path, format=expected_format)
        actual_sound = saturn.getSound(file_path)
        self.assertEqual(actual_sound, expected_sound)

    @patch("pydub.playback.play")
    def test_play_method_wav(self, mock_wave_object):
        saturn = Saturn([], 0)
        saturn.play("sounds/coffee.wav")
        mock_wave_object.assert_called_once()

    @patch("pydub.AudioSegment.from_file")
    @patch("pydub.playback.play")
    def test_play_method_non_wav(self, mock_play, mock_audio_segment):
        saturn = Saturn([], 0)
        saturn.play("sounds/test.mp3")
        mock_audio_segment.assert_called_once_with("sounds/test.mp3", format="mp3")
        mock_play.assert_called_once()

    @patch("pydub.AudioSegment.from_file")
    @patch("pydub.playback.play")
    def test_play_overlap(self, mock_play, mock_audio_segment):
        saturn = Saturn([], 0)
        with patch("sys.stdout", new=StringIO()) as fake_out:
            saturn.play_overlap(["sounds/coffee.wav", "sounds/coffee-slurp-2.wav"])
            self.assertIn(
                "I am now playing the following overlapping each other:",
                fake_out.getvalue(),
            )
        mock_audio_segment.assert_any_call("sounds/coffee.wav", format="wav")
        mock_audio_segment.assert_any_call("sounds/coffee-slurp-2.wav", format="wav")
        self.assertEqual(mock_play.call_count, 2)

    @patch("pydub.AudioSegment.from_file")
    @patch("pydub.playback.play")
    def test_play_sequential(self, mock_play, mock_audio_segment):
        saturn = Saturn([], 0)
        with patch("sys.stdout", new=StringIO()) as fake_out:
            saturn.play_sequential(["sounds/coffee.wav", "sounds/coffee-slurp-2.wav"])
            self.assertIn("Playing:", fake_out.getvalue())
        mock_audio_segment.assert_any_call("sounds/coffee.wav", format="wav")
        mock_audio_segment.assert_any_call("sounds/coffee-slurp-2.wav", format="wav")
        self.assertEqual(mock_play.call_count, 2)

    @patch("os.walk")
    def test_list_command(self, mock_walk):
        mock_walk.return_value = [("", [], ["sounds/coffee.wav", "sounds/test.mp3"])]
        saturn = Saturn([], 0)
        with patch("builtins.print") as mock_print:
            saturn.list_command()
            mock_print.assert_any_call("sounds/coffee.wav")
            mock_print.assert_any_call("sounds/test.mp3")

    # Add more tests for other methods as needed


class TestCommandLineParser(unittest.TestCase):

    def test_parse_arguments_help(self):
        with patch("sys.argv", ["script.py", "--help"]):
            with self.assertRaises(SystemExit) as cm:
                CommandLineParser(sys.argv)
            self.assertEqual(cm.exception.code, 0)

    def test_parse_arguments_invalid_command(self):
        with patch("sys.argv", ["script.py", "invalid_command"]):
            with patch("sys.stderr", new=StringIO()) as fake_err:
                with self.assertRaises(SystemExit) as cm:
                    CommandLineParser(sys.argv)
                self.assertEqual(cm.exception.code, 1)
                self.assertIn("error, unexpected arguments", fake_err.getvalue())

    # Add more tests for other commands as needed


if __name__ == "__main__":
    unittest.main()
