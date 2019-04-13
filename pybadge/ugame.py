"""
A helper module that initializes the display and buttons for the uGame
game console. See https://hackaday.io/project/27629-game
"""

import board
import digitalio
import gamepad
import stage


K_X = 0x02
K_DOWN = 0x20
K_LEFT = 0x80
K_RIGHT = 0x10
K_UP = 0x40
K_O = 0x01
K_START = 0x04
K_SECLECT = 0x08


display = board.DISPLAY
buttons = gamepad.GamePadShift(
    digitalio.DigitalInOut(board.BUTTON_OUT),
    digitalio.DigitalInOut(board.BUTTON_CLOCK),
    digitalio.DigitalInOut(board.BUTTON_LATCH),
)

audio = stage.Audio(board.SPEAKER, board.SPEAKER_ENABLE)
