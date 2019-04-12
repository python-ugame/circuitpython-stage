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

    def play(self, audio_file):
        self.stop()
        self.last_audio = audioio.AudioOut(board.SPEAKER, audio_file)
        self.last_audio.play()

    def stop(self):
        if self.last_audio:
            self.last_audio.stop()

    def mute(self, value=True):
        self.mute_pin.value = not value


class Display:
    buffer = bytearray(4)

    def __init__(self):
        self.bus = board.DISPLAY.bus
        self.width = board.DISPLAY.width
        self.height = board.DISPLAY.height

    def block(self, x0, y0, x1, y1):
        x0 += 3
        x1 += 3
        y0 += 2
        y1 += 2
        struct.pack_into('>HH', self.buffer, 0, x0, x1)
        self.bus.send(0x2a, self.buffer)
        struct.pack_into('>HH', self.buffer, 0, y0, y1)
        self.bus.send(0x2b, self.buffer)
        self.bus.send(0x2c, b'')


display = Display()
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
