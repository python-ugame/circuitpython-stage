# Board support for the stage game library on the ELECFREAKS Retro Arcade.
# stage.Stage scales displays wider than 256 pixels by 2 unless told
# otherwise: pass scale=1 to use the panel's native 320x240.
import time

import audiocore
import audiopwmio
import board
import keypad
import supervisor

K_O = 0x01  # A
K_X = 0x02  # B
K_Z = 0x04  # MENU
K_START = 0x04  # MENU
K_DOWN = 0x08
K_LEFT = 0x10
K_RIGHT = 0x20
K_UP = 0x40


class _Buttons:
    def __init__(self):
        self.keys = keypad.Keys(
            (
                board.BUTTON_A,
                board.BUTTON_B,
                board.BUTTON_MENU,
                board.BUTTON_DOWN,
                board.BUTTON_LEFT,
                board.BUTTON_RIGHT,
                board.BUTTON_UP,
            ),
            value_when_pressed=False,
            pull=True,
            interval=0.05,
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
        self.audio = audiopwmio.PWMAudioOut(board.SPEAKER)

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


display = board.DISPLAY
display.auto_refresh = False
buttons = _Buttons()
audio = _Audio()
