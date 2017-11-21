import array
import pprint


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
                palette[color] = ((c & 0xff) << 8) | (c >> 8)
        return palette

    def read_data(self, offset=0, size=-1):
        """Read the image data."""

        with open(self.filename, 'rb') as f:
            f.seek(self.data + offset)
            return f.read(size)


class Font:
    def __init__(self, buffer):
        self.buffer = buffer

    @classmethod
    def from_bmp16(cls, filename):
        bmp = BMP16(filename)
        bmp.read_header()
        if bmp.width != 8 or bmp.height != 1024:
            raise ValueError("A 8x1024 16-color BMP expected!")
        data = bmp.read_data()
        self = cls(bytearray(2048))
        c = 0
        x = 0
        y = 7
        for b in data:
            self.pixel(c, x, y, b >> 4)
            x += 1
            self.pixel(c, x, y, b & 0x0f)
            x += 1
            if x >= 8:
                x = 0
                y -= 1
                if y < 0:
                    y = 7
                    c += 1
        del data
        self.palette = bmp.read_palette()
        return self

    def pixel(self, c, x, y, color):
        index = (127 - c) * 16 + 2 * y + x // 4
        bit = (x % 4) * 2
        color = color & 0x03
        self.buffer[index] |= color << bit


font = Font.from_bmp16("font.bmp")
pprint.pprint(font.buffer)
pprint.pprint(font.palette.tobytes())
