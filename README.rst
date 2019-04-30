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

The API reference is available at `<http://circuitpython-stage.readthedocs.io>`_.

stage
=====
.. automodule:: stage
   :members:


ugame
=======
.. module:: ugame

.. data:: display

    An initialized display, that can be used for creating Stage objects.

.. data:: buttons

    An instance of ``GamePad`` or other similar class, that has a
    ``get_pressed`` method for retrieving a bit mask of pressed buttons. That
    value can be then checked with & operator against the constants: ``K_UP``,
    ``K_DOWN``, ``K_LEFT``, ``K_RIGHT``, ``K_X``, ``K_O`` and on some platforms
    also: ``K_START`` and ``K_SELECT``.

.. data:: audio

    And instance of the ``Audio`` or other similar class, that has ``play``,
    ``stop`` and ``mute`` methods.
