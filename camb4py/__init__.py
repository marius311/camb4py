"""

A Python wrapper for CAMB

Example ::

    import camb4py
    camb = camb4py.load('/path/to/camb')
    camb(get_scalar_cls='T')

"""

from camb4py import load, _defaults, read_ini
#del camb4py