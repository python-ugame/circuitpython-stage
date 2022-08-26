import board
import digitalio
import analogio
import keypad
import stage
import audioio
import audiocore


K_X = 0x01
K_DOWN = 0x02
K_LEFT = 0x04
K_RIGHT = 0x08
K_UP = 0x10
K_O = 0x20
K_START = 0x00
K_SELECT = 0x00


class _Buttons:
    def __init__(self):
        self.keys = keypad.Keys((board.X, board.DOWN,
            board.LEFT, board.RIGHT, board.UP,
            board.O), value_when_pressed=False,
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
        return buttons


class _Audio:
    last_audio = None

    def __init__(self, speaker_pin, mute_pin):
        self.muted = True
        self.buffer = bytearray(256)
        self.audio = audioio.AudioOut(speaker_pin)
        self.mute_pin = digitalio.DigitalInOut(mute_pin)
        self.mute_pin.switch_to_output(value=False)

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
        self.mute_pin.value = not value


display = board.DISPLAY
audio = _Audio(board.SPEAKER, board.MUTE)
buttons = _Buttons()
battery = analogio.AnalogIn(board.BATTERY)
