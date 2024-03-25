import sys
import os
import simpleaudio as sa
import unittest
import saturn_cli_example as saturn

argvlen = len(sys.argv)

# NOTE: It looks like there's nothing happening here yet

class TestSounds(unittest.TestCase):
    def test_play_audio(self, file):
        self.assertEqual(True, saturn.play_audio("./sound/coffee-slurp-2.wav"))


class TestCommandLine(unittest.TestCase):
    pass


class EditFile(unittest.TestCase):
    pass
