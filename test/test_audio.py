"""
Class to test all audio functions.
- play
- play_overlap
- play_sequential
TODO: not really working right now?
"""

import sys

sys.path.append("../src")
import unittest
from saturn_cli import CommandLineParser as saturn


class TestSounds(unittest.TestCase):
    sound1 = "../sounds/coffee-slurp-2.wav"
    sound2 = "../sounds/toaster-2.wav"
    sounds = [sound1, sound2]
    parser = saturn(sys.argv)

    def test_play_audio(self):
        print("TESTING PLAY CALLED")
        self.assertTrue(self.parser.play_audio(self.sound1))

    def test_play_overlap(self):
        print("TESTING PLAY OVERLAP CALLED")
        for i in self.sounds:
            self.assertTrue(self.parser.play_audio(i))

    def test_play_sequential(self):
        print("TESTING PLAY SEQUENTIAL CALLED")
        self.assertTrue(self.parser.play_sequential(self.sounds))


if __name__ == "__main__":
    unittest.main(verbosity=2)
