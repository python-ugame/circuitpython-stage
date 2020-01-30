import board
import digitalio
import gamepad
import stage
import supervisor
import time


K_X = 0x01
K_DOWN = 0x02
K_LEFT = 0x04
K_RIGHT = 0x08
K_UP = 0x10
K_O = 0x20
K_START = 0x40
K_Z = 0x40
K_SELECT = 0x00


class _Buttons:
    def __init__(self):
        self.buttons = gamepad.GamePad(
            digitalio.DigitalInOut(board.BUTTON_X),
            digitalio.DigitalInOut(board.BUTTON_DOWN),
            digitalio.DigitalInOut(board.BUTTON_LEFT),
            digitalio.DigitalInOut(board.BUTTON_RIGHT),
            digitalio.DigitalInOut(board.BUTTON_UP),
            digitalio.DigitalInOut(board.BUTTON_O),
            digitalio.DigitalInOut(board.BUTTON_Z),
        )
        self.last_z_press = None

    def get_pressed(self):
        buttons = self.buttons.get_pressed()
        if buttons & K_Z:
            now = time.monotonic()
            if self.last_z_press:
                if now - self.last_z_press > 2:
                    supervisor.reload()
            else:
                self.last_z_press = now
        else:
            self.last_z_press = None
        return buttons


display = board.DISPLAY
buttons = _Buttons()
audio = stage.Audio(board.P5)
