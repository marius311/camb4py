"""

A Python wrapper for CAMB

Example ::

    import pycamb
    camb = pycamb.load('/path/to/camb')
    camb(get_scalar_cls='T')

"""

from pycamb import load, _defaults, read_ini
del pycamb