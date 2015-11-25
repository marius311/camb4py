=======
camb4py
=======

**Note:** `CAMB <https://github.com/cmbant/CAMB>`_ now has a built-in Python wrapper which is faster than this wrapper and gives you access to more internals, so I recommend checking that out first. This package might still be useful e.g. in some cases if you have an older version of CAMB with some custom modifications. 

Features
========

`camb4py` lets you call `CAMB <http://www.camb.info>`_ from `Python`. In particular, 

* Call your existing and modified CAMB versions
* Call the built-in version of CAMB that comes with `camb4py`
* Automatically calculate *derivatives*
* No disk I/O, fast enough to be used in realistic sampling codes


Installation
============

To install `camb4py`, download and extract the package, and from the top folder run::

    python setup.py build
    python setup.py install

Troubleshooting
---------------

* Python attemps to automatically configure your Fortran compiler and compile flags. 
  If this fails for some reason, you can configure it by hand in the file ``setup.cfg``. 

* Alternatively, if you already have your own version of CAMB compiled and 
  would just like to use that, append ``--no-builtin`` to the ``build`` command 
  or make the corresponding change to ``setup.cfg``
           
* If you want to disable OpenMP, append ``--no-openmp`` to the ``build`` command
  or make the corresponding change in ``setup.cfg``.

* If you don't have root permissions, you can append ``--user`` to the ``install``
  command to put `camb4py` underneath your home folder.
           
Usage
=====

First load a CAMB executable with, ::

    import camb4py
    camb = camb4py.load()                    #use built-in CAMB
    camb = camb4py.load('/path/to/camb')     #or specify own CAMB
    
``load`` also takes an argument ``defaults`` which can be path to an ini file,
an already loaded ini file, or a dictionary, that specifies values for parameters not
set manually, ::

     camb4py.load(defaults='/path/to/params.ini') 
     
The call to ``load`` returns a function ``camb`` which can then be called with some parameters.
The names of the parameters are exactly as they appear in the ini file. For example, ::

    result = camb(get_scalar_cls=True, ombh2=.0225)
    result = camb(**{'get_scalar_cls':True, 'ombh2':.0225})     #Same thing but passing a dictionary

will get the scalar Cl's with all parameters at their default values except for ``ombh2``. 


The result is a dictionary containing the contents of any files written by CAMB 
(automatically converted to `Numpy` arrays) as well as whatever it printed out to the screen. 
A typical output looks like this, ::

    {'scalar': array([[  2.00000000e+00,   1.52550000e-10,   7.41090000e-15,  4.57960000e-13],
                      ..., 
                      [  2.20000000e+03,   1.71360000e-11,   7.77430000e-13, -5.70770000e-14]]),
     'stdout': 'Age of universe/GYr  =  13.794\nReion redshift'...}  

.. note :: All `camb4py` objects have documentation which can be accessed by typing
           the name of the object followed by a question mark, e.g. ``camb4py.load?`` 

Derivatives
-----------

To calculate numerical derivatives, use ``camb.derivative(dparam, params, epsilon)``. 
For example, to take the derivative with respect to ``ombh2``, you could do, ::

    result = camb.derivative('ombh2', {'get_scalar_cls':True, 'ombh2':.0225}, 1e-4)
    result = camb.derivative('ombh2', dict(get_scalar_cls=True, ombh2=0225), 1e-4)      #Again, different way to input parameters
    


Details
=======

`camb4py` works by creating `named pipes <http://en.wikipedia.org/wiki/Named_pipe>`_ 
for the CAMB input and output files. When CAMB is called, it reads/writes to these pipes.
This means everything is stored in memory and there is no disk I/O. The only "wasted" time 
is spent translating the outputs to/from text which is about 10ms per file. 
This procedure also has the advantage that it lets one use any number of
existing CAMB executables on the fly in one session, and does not crash `Python` in the event of a CAMB crash.

Authors
=======

CAMB is written by Antony Lewis and Anthony Challinor.

This wrapper is written by Marius Millea (feel free to email questions/comments to `<mmillea@ucdavis.edu>`_)
