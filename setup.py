from distutils.core import setup

setup(
   name='pycamb',
   version='0.1.0',
   author='Marius Millea',
   author_email='mmillea@ucdavis.edu',
   py_modules=['pycamb'],
   url='http://pypi.python.org/pypi/pycamb/',
   license='LICENSE.txt',
   description='A Python wrapper for the popular cosmological code CAMB.',
   long_description=open('README').read(),
)

