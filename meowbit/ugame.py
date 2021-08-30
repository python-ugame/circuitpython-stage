import board
import stage
import busio
import time
import keypad
import audiocore


K_X = 0x01
K_O = 0x02
K_DOWN = 0x04
K_LEFT = 0x08
K_RIGHT = 0x10
K_UP = 0x20
K_Z = 0x40

display = board.DISPLAY
display.auto_brightness = True
display.auto_refresh = False


class _Buttons:
    def __init__(self):
        self.keys = keypad.Keys((board.BTNA, board.BTNB, board.DOWN,
            board.LEFT, board.RIGHT, board.UP),
            value_when_pressed=False, interval=0.05)
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
        self.audio = board.BUZZ

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
buttons = _Buttons()
