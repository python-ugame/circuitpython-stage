import board
import analogio
import stage
import keypad
import audiocore
import audiopwmio
import time
import supervisor


K_O = 0x01  # A
K_X = 0x02  # B
K_SELECT = 0x04  # X
K_START = 0x08   # Y
K_Z = 0x08   # Y
K_DOWN = 0x10
K_LEFT = 0x20
K_RIGHT = 0x40
K_UP = 0x80


class _Buttons:
    def __init__(self):
        self.keys = keypad.Keys((
            board.SW_A,
            board.SW_B,
            board.SW_X,
            board.SW_Y,
            board.SW_DOWN,
            board.SW_LEFT,
            board.SW_RIGHT,
            board.SW_UP
        ), value_when_pressed=False, pull=True, interval=0.05)
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
        self.audio = audiopwmio.PWMAudioOut(board.AUDIO)

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


audio = _Audio()
display = board.DISPLAY
buttons = _Buttons()
battery = analogio.AnalogIn(board.BAT_SENSE)
