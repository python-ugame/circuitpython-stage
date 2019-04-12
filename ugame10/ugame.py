"""
A helper module that initializes the display and buttons for the uGame
game console. See https://hackaday.io/project/27629-game
"""

import board
import digitalio
import busio
import audioio
import analogio
import struct
import gamepad


K_X = 0x01
K_DOWN = 0x02
K_LEFT = 0x04
K_RIGHT = 0x08
K_UP = 0x10
K_O = 0x20


class Audio:
    last_audio = None

    def __init__(self):
        self.mute_pin = digitalio.DigitalInOut(board.MUTE)
        self.mute_pin.switch_to_output(value=1)
        self.audio = audioio.AudioOut(board.SPEAKER)

    def play(self, audio_file, loop=False):
        self.stop()
        wave = audioio.WaveFile(audio_file)
        self.audio.play(wave, loop=loop)

    def stop(self):
        self.audio.stop()

    def mute(self, value=True):
        self.mute_pin.value = not value


display = board.DISPLAY
buttons = gamepad.GamePad(
    digitalio.DigitalInOut(board.X),
    digitalio.DigitalInOut(board.DOWN),
    digitalio.DigitalInOut(board.LEFT),
    digitalio.DigitalInOut(board.RIGHT),
    digitalio.DigitalInOut(board.UP),
    digitalio.DigitalInOut(board.O),
)

audio = Audio()

battery = analogio.AnalogIn(board.BATTERY)
