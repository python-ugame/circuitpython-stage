import board
import digitalio
import gamepad
import stage


K_X = 0x01
K_DOWN = 0x02
K_LEFT = 0x04
K_RIGHT = 0x08
K_UP = 0x10
K_O = 0x20
K_START = 0x40
K_Z = 0x40
K_SELECT = 0x00


display = board.DISPLAY
buttons = gamepad.GamePad(
    digitalio.DigitalInOut(board.BUTTON_X),
    digitalio.DigitalInOut(board.BUTTON_DOWN),
    digitalio.DigitalInOut(board.BUTTON_LEFT),
    digitalio.DigitalInOut(board.BUTTON_RIGHT),
    digitalio.DigitalInOut(board.BUTTON_UP),
    digitalio.DigitalInOut(board.BUTTON_O),
    digitalio.DigitalInOut(board.BUTTON_Z),
)
audio = stage.Audio(board.P5)
