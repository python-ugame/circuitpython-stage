import ustruct
import time


class ST7735R:
    """A minimal driver for the 128x128 version of the ST7735 SPI display."""

    def __init__(self, spi, dc, rotation=0x06):
        self.spi = spi
        spi.try_lock()
        self.dc = dc
        self.dc.switch_to_output(value=1)
        spi.configure()
        for command, data, delay in (
            (b'\x01', b'', 120),
            (b'\x11', b'', 120),
            (b'\x36', bytes(((rotation & 0x07) << 5,)), 0),
            (b'\x3a', b'\x05', 0),
            (b'\xb4', b'\x07', 0),
            (b'\xb1', b'\x01\x2c\x2d', 0),
            (b'\xb2', b'\x01\x2c\x2d', 0),
            (b'\xb3', b'\x01\x2c\x2d\x01\x2c\x2d', 0),
            (b'\xc0', b'\x02\x02\x84', 0),
            (b'\xc1', b'\xc5', 0),
            (b'\xc2', b'\x0a\x00', 0),
            (b'\xc3', b'\x8a\x2a', 0),
            (b'\xc4', b'\x8a\xee', 0),
            (b'\xc5', b'\x0e', 0),
            (b'\x20', b'', 0),
            (b'\xe0', b'\x02\x1c\x07\x12\x37\x32\x29\x2d'
             b'\x29\x25\x2B\x39\x00\x01\x03\x10', 0),
            (b'\xe1', b'\x03\x1d\x07\x06\x2E\x2C\x29\x2D'
             b'\x2E\x2E\x37\x3F\x00\x00\x02\x10', 0),
            (b'\x13', b'', 10),
            (b'\x29', b'', 100),
        ):
            self.write(command, data)
            time.sleep(delay / 1000)
        spi.configure(baudrate=24000000, polarity=0, phase=0)
        self.dc.value = 0

    def block(self, x0, y0, x1, y1):
        """Prepare for updating a block of the screen."""
        xpos = ustruct.pack('>HH', x0 + 2, x1 + 2)
        ypos = ustruct.pack('>HH', y0 + 3, y1 + 3)
        self.write(b'\x2a', xpos)
        self.write(b'\x2b', ypos)
        self.write(b'\x2c')
        self.dc.value = 1

    def write(self, command=None, data=None):
        """Send command and/or data to the display."""

        if command is not None:
            self.dc.value = 0
            self.spi.write(command)
        if data:
            self.dc.value = 1
            self.spi.write(data)

    def clear(self, color):
        """Clear the display with the given color."""

        self.block(0, 0, 127, 127)
        pixel = color.to_bytes(2, 'big')
        data = pixel * 256
        for count in range(64):
            self.write(None, data)
