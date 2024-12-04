import audiobusio
import audiocore
import board
import busio
import digitalio
import displayio
import busdisplay
import fourwire
import keypad
import microcontroller
import os
import supervisor
import time


K_X = 0x10
K_O = 0x20
K_Z = 0x40
K_START = 0x40
K_SELECT = 0x80
K_DOWN = 0x08
K_LEFT = 0x04
K_RIGHT = 0x02
K_UP = 0x01


class _Buttons:
    def __init__(self):
        self.keys = keypad.Keys((
                board.BUTTON_UP,
                board.BUTTON_RIGHT,
                board.BUTTON_LEFT,
                board.BUTTON_DOWN,
                board.BUTTON_X,
                board.BUTTON_O,
                board.BUTTON_Z,
            ),
            value_when_pressed=False,
        )
        self.last_state = 0
        self.event = keypad.Event(0, False)
        self.last_z_press = None

    def get_pressed(self):
        buttons = self.last_state
        events = self.keys.events
        while events:
            if events.get_into(self.event):
                bit = 1 << self.event.key_number
                if self.event.pressed:
                    buttons |= bit
                    self.last_state |= bit
                else:
                    self.last_state &= ~bit
        if buttons & K_Z:
            now = time.monotonic()
            if self.last_z_press:
                if now - self.last_z_press > 2:
                    os.chdir('/')
                    supervisor.set_next_code_file(None)
                    supervisor.reload()
            else:
                self.last_z_press = now
        else:
            self.last_z_press = None
        return buttons


class _Audio:
    last_audio = None

    def __init__(self):
        self.muted = True
        self.buffer = bytearray(128)
        self.gain = digitalio.DigitalInOut(board.AUDIO_GAIN)
        self.gain.switch_to_output(value=0)
        self.audio = audiobusio.I2SOut(
            board.AUDIO_BCLK,
            board.AUDIO_LRCLK,
            board.AUDIO_DATA,
        )

    def play(self, audio_file, loop=False):
        if self.muted:
            return
        self.stop()
        wave = audiocore.WaveFile(audio_file, self.buffer)
        self.audio.play(wave, loop=loop)

    def stop(self):
        self.audio.stop()

    def mute(self, value=True):
        self.muted = value

board.DISPLAY.auto_refresh = False

display = board.DISPLAY
buttons = _Buttons()
audio = _Audio()
