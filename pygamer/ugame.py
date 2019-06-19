"""
A helper module that initializes the display and buttons for the uGame
game console. See https://hackaday.io/project/27629-game
"""

import board
import digitalio
import analogio
import gamepadshift
import stage
import displayio
import busio
import time


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
    b"\x36\x01\xa8" # _MADCTL
    # 1 clk cycle nonoverlap, 2 cycle gate rise, 3 sycle osc equalie,
    # fix on VTL
    b"\x3a\x01\x05" # COLMOD - 16bit color
    b"\xe0\x10\x02\x1c\x07\x12\x37\x32\x29\x2d\x29\x25\x2B\x39\x00\x01\x03\x10" # _GMCTRP1 Gamma
    b"\xe1\x10\x03\x1d\x07\x06\x2E\x2C\x29\x2D\x2E\x2E\x37\x3F\x00\x00\x02\x10" # _GMCTRN1
    b"\x13\x80\x0a" # _NORON
    b"\x29\x80\x64" # _DISPON
)
displayio.release_displays()
_tft_spi = busio.SPI(clock=board.TFT_SCK, MOSI=board.TFT_MOSI)
_tft_spi.try_lock()
_tft_spi.configure(baudrate=24000000)
_tft_spi.unlock()
_fourwire = displayio.FourWire(_tft_spi, command=board.TFT_DC,
                               chip_select=board.TFT_CS)
_reset = digitalio.DigitalInOut(board.TFT_RST)
_reset.switch_to_output(value=0)
time.sleep(0.05)
_reset.value = 1
time.sleep(0.05)
display = displayio.Display(_fourwire, _TFT_INIT, width=160, height=128,
                            rotation=0, backlight_pin=board.TFT_LITE)
del _TFT_INIT
display.auto_brightness = True


class Buttons:
    def __init__(self):
        self.buttons = gamepadshift.GamePadShift(
            digitalio.DigitalInOut(board.BUTTON_CLOCK),
            digitalio.DigitalInOut(board.BUTTON_OUT),
            digitalio.DigitalInOut(board.BUTTON_LATCH),
        )
        self.joy_x = analogio.AnalogIn(board.JOYSTICK_X)
        self.joy_y = analogio.AnalogIn(board.JOYSTICK_Y)

    def get_pressed(self):
        pressed = self.buttons.get_pressed()
        dead = 15000
        x = self.joy_x.value - 32767
        if x < -dead:
            pressed |= K_LEFT
        elif x > dead:
            pressed |= K_RIGHT
        y = self.joy_y.value - 32767
        if y < -dead:
            pressed |= K_UP
        elif y > dead:
            pressed |= K_DOWN
        return pressed


buttons = Buttons()
audio = stage.Audio(board.SPEAKER, board.SPEAKER_ENABLE)
