"""
A helper module that initializes the display and buttons for the uGame
game console. See https://hackaday.io/project/27629-game
"""

import board
import digitalio
import gamepad
import stage
import displayio
import busio


K_X = 0x01
K_DOWN = 0x02
K_LEFT = 0x04
K_RIGHT = 0x08
K_UP = 0x10
K_O = 0x20
K_START = 0x40
K_SELECT = 0x00


_INIT_SEQUENCE = (
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
    b"\x36\x01\x10" # _MADCTL bottom to top refresh
    # 1 clk cycle nonoverlap, 2 cycle gate rise, 3 sycle osc equalie,
    # fix on VTL
    b"\x3a\x01\x05" # COLMOD - 16bit color
    b"\xe0\x10\x02\x1c\x07\x12\x37\x32\x29\x2d\x29\x25\x2B\x39\x00\x01\x03\x10" # _GMCTRP1 Gamma
    b"\xe1\x10\x03\x1d\x07\x06\x2E\x2C\x29\x2D\x2E\x2E\x37\x3F\x00\x00\x02\x10" # _GMCTRN1
    b"\x13\x80\x0a" # _NORON
    b"\x29\x80\x64" # _DISPON
)


class DummyAudio:
    def play(self, f, loop=False):
        pass

    def stop(self):
        pass

    def mute(self, mute):
        pass


displayio.release_displays()
_tft_spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
_tft_spi.try_lock()
_tft_spi.configure(baudrate=24000000)
_tft_spi.unlock()
_fourwire = displayio.FourWire(_tft_spi, command=board.A3,
                               chip_select=board.A2, reset=board.A4)
display = displayio.Display(_fourwire, _INIT_SEQUENCE, width=160, height=128,
                            rotation=0, backlight_pin=board.A5)
display.auto_brightness = True
buttons = gamepad.GamePad(
    digitalio.DigitalInOut(board.SCL),
    digitalio.DigitalInOut(board.D12),
    digitalio.DigitalInOut(board.D11),
    digitalio.DigitalInOut(board.D9),
    digitalio.DigitalInOut(board.D10),
    digitalio.DigitalInOut(board.D7),
    digitalio.DigitalInOut(board.SDA),
)
audio = DummyAudio()
