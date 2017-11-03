Stage – a Tile and Sprite Engine
********************************

Stage is a library that lets you display tile grids and sprites on SPI-based
RGB displays in CircuitPython. It is mostly made with video games in mind, but
it can be useful in making any kind of graphical user interface too.

For performance reasons, a part of this library has been written in C and has
to be compiled as part of the CircuitPython firmware as the ``_stage`` module.
For memory saving reasons, it's best if this library is also included in the
firmware, as a frozen module.


API Reference
*************

stage
=====
.. automodule:: stage
   :members:

st7735r
=======
.. automodule:: st7735
   :members:

ugame
=======
.. automodule:: ugame
   :members:

