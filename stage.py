import time
import array
import _stage


def color565(r, g, b):
    return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3


class BMP16:
    """Read 16-color BMP files."""

    def __init__(self, filename):
        self.filename = filename
        self.colors = 0

    def read_header(self):
        """Read the file's header information."""

        if self.colors:
            return
        with open(self.filename, 'rb') as f:
            f.seek(10)
            self.data = int.from_bytes(f.read(4), 'little')
            f.seek(18)
            self.width = int.from_bytes(f.read(4), 'little')
            self.height = int.from_bytes(f.read(4), 'little')
            f.seek(46)
            self.colors = int.from_bytes(f.read(4), 'little')

    def read_palette(self):
        """Read the color palette information."""

        palette = array.array('H', (0 for i in range(16)))
        with open(self.filename, 'rb') as f:
            f.seek(self.data - self.colors * 4)
            for color in range(self.colors):
                buffer = f.read(4)
                c = color565(buffer[2], buffer[1], buffer[0])
                palette[color] = (c << 8) | (c >> 8)
        return palette

    def read_data(self, offset=0, size=-1):
        """Read the image data."""

        with open(self.filename, 'rb') as f:
            f.seek(self.data + offset)
            return f.read(size)


class Bank:
    """
    Store graphics for the tiles and sprites.

    A single bank stores exactly 16 tiles, each 16x16 pixels in 16 possible
    colors, and a 16-color palette. We just like the number 16.

    """

    def __init__(self, buffer=None, palette=None):
        self.buffer = buffer
        self.palette = palette

    @classmethod
    def from_bmp16(cls, filename):
        bmp = BMP16(filename)
        bmp.read_header()
        if bmp.width != 16 or bmp.height != 256:
            raise ValueError("Not 16x256!")
        palette = bmp.read_palette()
        buffer = bmp.read_data(0, 2048)
        return cls(buffer, palette)


class Grid:
    """
    A grid is a layer of tiles that can be displayed on the screen. Each square
    can contain any of the 16 tiles from the associated bank.
    """

    def __init__(self, bank, width=8, height=8, palette=None):
        self.buffer = bytearray((width * height) >> 1)
        self.x = 0
        self.y = 0
        self.z = 0
        self.width = width
        self.height = height
        self.bank = bank
        self.palette = paletter or bank.palette
        self.layer = _stage.Layer(width, height, self.bank.buffer,
                                  self.bank.palette, self.buffer)

    def tile(self, x, y, tile=None):
        """Get or set what tile is displayed in the given place."""

        if not 0 <= x < self.width or not 0 <= y < self.height:
            return 0
        b = self.buffer[(x * self.width + y) >> 1]
        if tile is None:
            return b & 0x0f if y & 0x01 else b >> 4
        if y & 0x01:
            b = b & 0xf0 | tile
        else:
            b = b & 0x0f | (tile << 4)
        self.buffer[(x * self.width + y) >> 1] = b

    def move(self, x, y, z=None):
        """Shift the whole layer respective to the screen."""

        self.x = x
        self.y = y
        if z is not None:
            self.z = z
        self.layer.move(x, y)


class Sprite:
    """
    A sprite is a layer containing just a single tile from the associated bank,
    that can be positioned anywhere on the screen.
    """

    def __init__(self, bank, frame, x, y, z=0, rotation=0, palette=None):
        self.bank = bank
        self.palette = palette or bank.palette
        self.frame = frame
        self.rotation = rotation
        self.x = x
        self.y = y
        self.z = z
        self.layer = _stage.Layer(1, 1, self.bank.buffer, self.palette)
        self.layer.move(x, y)
        self.layer.frame(frame, rotation)
        self.px = x
        self.py = y

    def move(self, x, y, z=None):
        """Move the sprite to the given place."""

        self.px = self.x
        self.py = self.y
        self.x = x
        self.y = y
        if z is not None:
            self.z = z
        self.layer.move(x, y)

    def set_frame(self, frame=None, rotation=None):
        """Set the current graphic and rotation of the sprite."""

        if frame is not None:
            self.frame = frame
        if rotation is not None:
            self.rotation = rotation
        self.layer.frame(self.frame, self.rotation)


class Stage:
    """
    Represents what is being displayed on the screen.
    """
    buffer = bytearray(512)

    def __init__(self, display, fps=6):
        self.layers = []
        self.display = display
        self.last_tick = time.monotonic()
        self.tick_delay = 1 / fps

    def tick(self):
        """Wait for the start of the next frame."""
        self.last_tick += self.tick_delay
        wait = max(0, self.last_tick - time.monotonic())
        if wait:
            time.sleep(wait)
        else:
            self.last_tick = time.monotonic()

    def render(self, x0, y0, x1, y1):
        """Update a rectangle of the screen."""
        layers = [l.layer for l in self.layers]
        self.display.block(x0, y0, x1 - 1, y1 - 1)
        _stage.render(x0, y0, x1, y1, layers, self.buffer, self.display.spi)

