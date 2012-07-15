"""

A Python wrapper for CAMB

Example ::

    import pycamb
    camb = pycamb.pycamb('/path/to/camb')
    camb(get_scalar_cls='T')

"""

from pycamb import load, _defaults
del pycamb