import os
from numpy.distutils.command.build import build as _build
from numpy.distutils.core import setup
from numpy.distutils.misc_util import Configuration
from numpy.distutils.fcompiler import new_fcompiler

config = Configuration('pycamb',
   name='pycamb',
   version='0.1.0',
   author='Marius Millea',
   author_email='mmillea@ucdavis.edsetuptoolsu',
   packages=['pycamb'],
   url='http://pypi.python.org/pypi/pycamb/',
   license='LICENSE.txt',
   description='A Python wrapper for the popular cosmological code CAMB.',
   long_description=open('README').read(),
   derr=None,
)

class build_camb(_build):
    objs = ['constants',
            'utils',
            'subroutines',
            'inifile',
            'recfast',
            'power_tilt',
            'reionization',
            'modules',
            'bessels',
            'lensing',
            'equations',
            'halofit',
            'SeparableBispectrum',
            'cmbmain',
            'camb',
            'inidriver']
    
    def run(self):
        
        if not os.path.exists(os.path.join(self.build_lib,'pycamb','camb')):
        
            self.fcompiler = new_fcompiler(compiler=self.fcompiler,
                                           verbose=self.verbose,
                                           dry_run=self.dry_run,
                                           force=self.force,
                                           c_compiler=self.compiler)
            
            if self.fcompiler is not None:
                self.fcompiler.customize(self.distribution)
                self.fcompiler.customize_cmd(self)
                self.fcompiler.show_customization()
    
            src_dir = os.path.join('pycamb','src')
            obj_files = self.fcompiler.compile([os.path.join(src_dir,'%s.f90'%o) for o in self.objs],
                                               extra_postargs=['-cpp',self.fcompiler.module_dir_switch+src_dir],
                                               output_dir=self.build_temp)
            
            self.fcompiler.link_executable(obj_files,'camb',output_dir=os.path.join(self.build_lib,'pycamb'))
        
        
class build(_build):
    def get_sub_commands(self):
        return _build.get_sub_commands(self) + ['build_camb']
    
    
setup(cmdclass={'build':build, 'build_camb': build_camb},**config.todict())
