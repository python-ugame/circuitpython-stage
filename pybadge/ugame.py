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


K_X = 0x02
K_DOWN = 0x20
K_LEFT = 0x80
K_RIGHT = 0x10
K_UP = 0x40
K_O = 0x01
K_START = 0x04
K_SECLECT = 0x08

# re-initialize the display for correct rotation and RGB mode
displayio.release_displays()
_tft_spi = busio.SPI(clock=board.TFT_SCK, MOSI=board.TFT_MOSI)
_tft_spi.try_lock()
_tft_spi.configure(baudrate=24000000)
_tft_spi.unlock()
_fourwire = displayio.FourWire(_tft_spi, command=board.TFT_DC,
                               chip_select=board.TFT_CS)
display = displayio.Display(_fourwire, b'\x36\x01\xa8', width=160, height=128,
                            rotation=0, backlight_pin=board.TFT_LITE)
display.auto_brightness = True

buttons = gamepad.GamePadShift(
    digitalio.DigitalInOut(board.BUTTON_OUT),
    digitalio.DigitalInOut(board.BUTTON_CLOCK),
    digitalio.DigitalInOut(board.BUTTON_LATCH),
)

audio = stage.Audio(board.SPEAKER, board.SPEAKER_ENABLE)
