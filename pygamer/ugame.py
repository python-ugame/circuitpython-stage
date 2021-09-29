import board
import analogio
import stage
import displayio
import busio
import time
import keypad
import audioio
import audiocore


K_X = 0x01
K_O = 0x02
K_START = 0x04
K_SELECT = 0x08
K_DOWN = 0x10
K_LEFT = 0x20
K_RIGHT = 0x40
K_UP = 0x80

# re-initialize the display for correct rotation and RGB mode

_TFT_INIT = (
    b"\x01\x80\x96" # SWRESET and Delay 150ms
    b"\x11\x80\xff" # SLPOUT and Delay
    b"\xb1\x03\x01\x2C\x2D" # _FRMCTR1
    b"\xb2\x03\x01\x2C\x2D" # _FRMCTR2
    b"\xb3\x06\x01\x2C\x2D\x01\x2C\x2D" # _FRMCTR3
    b"\xb4\x01\x07" # _INVCTR line inversion
    b"\xc0\x03\xa2\x02\x84" # _PWCTR1 GVDD = 4.7V, 1.0uA
    b"\xc1\x01\xc5" # _PWCTR2 VGH=14.7V, VGL=-7.35V
    b"\xc2\x02\x0a\x00" # _PWCTR3 Opamp current small, Boost frequency
    b"\xc3\x02\x8a\x2a"
    b"\xc4\x02\x8a\xee"
    b"\xc5\x01\x0e" # _VMCTR1 VCOMH = 4V, VOML = -1.1V
    b"\x20\x00" # _INVOFF
    b"\x36\x01\xa0" # _MADCTL
    # 1 clk cycle nonoverlap, 2 cycle gate rise, 3 sycle osc equalie,
    # fix on VTL
    b"\x3a\x01\x05" # COLMOD - 16bit color
    b"\xe0\x10\x02\x1c\x07\x12\x37\x32\x29\x2d\x29\x25\x2B\x39\x00\x01\x03\x10" # _GMCTRP1 Gamma
    b"\xe1\x10\x03\x1d\x07\x06\x2E\x2C\x29\x2D\x2E\x2E\x37\x3F\x00\x00\x02\x10" # _GMCTRN1
    b"\x13\x80\x0a" # _NORON
    b"\x29\x80\x64" # _DISPON
)


class _Buttons:
    def __init__(self):
        self.keys = keypad.ShiftRegisterKeys(clock=board.BUTTON_CLOCK,
            data=board.BUTTON_OUT, latch=board.BUTTON_LATCH, key_count=4,
            interval=0.05)
        self.last_state = 0
        self.event = keypad.Event(0, False)
        self.last_z_press = None
        self.joy_x = analogio.AnalogIn(board.JOYSTICK_X)
        self.joy_y = analogio.AnalogIn(board.JOYSTICK_Y)

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
        if buttons & K_START:
            now = time.monotonic()
            if self.last_z_press:
                if now - self.last_z_press > 2:
                    supervisor.set_next_code_file(None)
                    supervisor.reload()
            else:
                self.last_z_press = now
        else:
            self.last_z_press = None
        dead = 15000
        x = self.joy_x.value - 32767
        if x < -dead:
            buttons |= K_LEFT
        elif x > dead:
            buttons |= K_RIGHT
        y = self.joy_y.value - 32767
        if y < -dead:
            buttons |= K_UP
        elif y > dead:
            buttons |= K_DOWN
        return buttons


class _Audio:
    last_audio = None

    def __init__(self, speaker_pin, mute_pin=None):
        self.muted = True
        self.buffer = bytearray(128)
        if mute_pin:
            self.mute_pin = digitalio.DigitalInOut(mute_pin)
            self.mute_pin.switch_to_output(value=not self.muted)
        else:
            self.mute_pin = None
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
        if self.mute_pin:
            self.mute_pin.value = not value


displayio.release_displays()
_tft_spi = busio.SPI(clock=board.TFT_SCK, MOSI=board.TFT_MOSI)
_fourwire = displayio.FourWire(_tft_spi, command=board.TFT_DC,
                               chip_select=board.TFT_CS, reset=board.TFT_RST)
display = displayio.Display(_fourwire, _TFT_INIT, width=160, height=128,
                            rotation=0, backlight_pin=board.TFT_LITE,
                            auto_refresh=False, auto_brightness=True)
del _TFT_INIT
buttons = _Buttons()
audio = _Audio(board.SPEAKER, board.SPEAKER_ENABLE)
