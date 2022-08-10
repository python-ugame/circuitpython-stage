"""
Converts images to the 4-bit PNG format required by Stage.
"""

import sys
from PIL import Image


filename = sys.argv[1]
image = Image.open(filename)
image = image.convert(mode='P', dither=Image.Dither.NONE,
                      palette=Image.Palette.ADAPTIVE, colors=16)
filename = filename.rsplit('.', 1)[0] + '.png'
image.save(filename, 'png', bits=4)
