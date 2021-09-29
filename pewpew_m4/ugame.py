import board
import stage
import supervisor
import time
import keypad
import audioio
import audiocore


K_X = 0x01
K_DOWN = 0x02
K_LEFT = 0x04
K_RIGHT = 0x08
K_UP = 0x10
K_O = 0x20
K_START = 0x40
K_Z = 0x40
K_SELECT = 0x80


class _Buttons:
    def __init__(self):
        self.keys = keypad.Keys((board.BUTTON_X, board.BUTTON_DOWN,
            board.BUTTON_LEFT, board.BUTTON_RIGHT, board.BUTTON_UP,
            board.BUTTON_O, board.BUTTON_Z), value_when_pressed=False,
            interval=0.05)
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

    def __init__(self, speaker_pin):
        self.muted = True
        self.buffer = bytearray(128)
        self.audio = audioio.AudioOut(speaker_pin)

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
buttons = _Buttons()
audio = _Audio(board.SPEAKER)
