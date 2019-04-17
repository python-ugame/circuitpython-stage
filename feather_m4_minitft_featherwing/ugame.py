from collections import namedtuple
import board
from micropython import const
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.pwmout import PWMOut
import stage
import displayio

BUTTON_RIGHT = const(7)
BUTTON_DOWN = const(4)
BUTTON_LEFT = const(3)
BUTTON_UP = const(2)
BUTTON_SEL = const(11)
BUTTON_A = const(10)
BUTTON_B = const(9)

Buttons = namedtuple("Buttons", "up down left right a b select")

button_mask = ((1 << BUTTON_RIGHT) |
                (1 << BUTTON_DOWN) |
                (1 << BUTTON_LEFT) |
                (1 << BUTTON_UP) |
                (1 << BUTTON_SEL) |
                (1 << BUTTON_A) |
                (1 << BUTTON_B))

_INIT_SEQUENCE = bytearray(
    b"\x01\x80\x96"  # SWRESET and Delay 150ms
    b"\x11\x80\xff"  # SLPOUT and Delay
    b"\xb1\x03\x01\x2C\x2D"  # _FRMCTR1
    b"\xb2\x03\x01\x2C\x2D"  # _FRMCTR2
    b"\xb3\x06\x01\x2C\x2D\x01\x2C\x2D"  # _FRMCTR3
    b"\xb4\x01\x07"  # _INVCTR line inversion
    b"\xc0\x03\xa2\x02\x84"  # _PWCTR1 GVDD = 4.7V, 1.0uA
    b"\xc1\x01\xc5"  # _PWCTR2 VGH=14.7V, VGL=-7.35V
    b"\xc2\x02\x0a\x00"  # _PWCTR3 Opamp current small, Boost frequency
    b"\xc3\x02\x8a\x2a"
    b"\xc4\x02\x8a\xee"
    b"\xc5\x01\x0e"  # _VMCTR1 VCOMH = 4V, VOML = -1.1V
    b"\x20\x00"  # _INVOFF
    b"\x36\x01\x68"  # _MADCTL bottom to top refresh
    # 1 clk cycle nonoverlap, 2 cycle gate rise, 3 sycle osc equalie,
    # fix on VTL
    b"\x3a\x01\x05"  # COLMOD - 16bit color
    b"\xe0\x10\x02\x1c\x07\x12\x37\x32\x29\x2d\x29\x25\x2B\x39\x00\x01\x03\x10"  # _GMCTRP1 Gamma
    b"\xe1\x10\x03\x1d\x07\x06\x2E\x2C\x29\x2D\x2E\x2E\x37\x3F\x00\x00\x02\x10"  # _GMCTRN1
    b"\x13\x80\x0a" # _NORON
    b"\x29\x80\x64"  # _DISPON
)

i2c = board.I2C()
spi = board.SPI()
ss = Seesaw(i2c, 0x5E)
backlight = PWMOut(ss, 5)
backlight.duty_cycle = int(255 * min(max(1 - 0.1, 0.0), 1.0))
ss.pin_mode_bulk(button_mask, ss.INPUT_PULLUP)
displayio.release_displays()
while not spi.try_lock():
    pass
spi.configure(baudrate=24000000)
spi.unlock()
ss.pin_mode(8, ss.OUTPUT)
ss.digital_write(8, True)  # Reset the Display via Seesaw
display_bus = displayio.FourWire(spi,
                                 command=board.D10,
                                 chip_select=board.D9)
display = displayio.Display(display_bus, _INIT_SEQUENCE, width=160, height=80, rowstart=24)
ss.pin_mode_bulk(button_mask, ss.INPUT_PULLUP)

def buttons():
    """
    Return a set of buttons with current push values
    """
    button_values = ss.digital_read_bulk(button_mask)
    return Buttons(*[not button_values & (1 << button) for button in
                     (BUTTON_UP, BUTTON_DOWN, BUTTON_LEFT, BUTTON_RIGHT,
                      BUTTON_A, BUTTON_B, BUTTON_SEL)])
