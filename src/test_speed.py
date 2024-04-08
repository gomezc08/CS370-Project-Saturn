import saturn_cli
from saturn_cli import CommandLineParser.modify_speed as speed
from saturn_cli import play
import simpleaudio as sa
import pydub.playback as pb

def test_speed():
    sound = sa.WaveObject.from_wave_file("sounds/coffee.wav")
    sound = speed(sound, 2)
    pb.play(sound)