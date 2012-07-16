import os
from numpy.distutils.command.build import build as _build
from numpy.distutils.core import setup
from numpy.distutils.fcompiler import new_fcompiler
from distutils.errors import DistutilsError


class build(_build):
    
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
    
    user_options = _build.user_options + [
        ('no-builtin', None,  "don't compile or install the built-in CAMB"),
        ]
    
    boolean_options = _build.boolean_options + ['no-builtin']
        
    def initialize_options(self):
        _build.initialize_options(self)
        self.no_builtin = None
        
    def run(self):
        _build.run(self)
        
        if not self.no_builtin and (self.force or not os.path.exists(os.path.join(self.build_lib,'pycamb','camb'))):
            
            self.fcompiler = new_fcompiler(compiler=self.fcompiler,
                                           verbose=self.verbose,
                                           dry_run=self.dry_run,
                                           force=self.force,
                                           c_compiler=self.compiler)
            
            if self.fcompiler is None:
                raise DistutilsError('Could not find Fortran compiler. See setup.cfg to specify one.')
                
            self.fcompiler.customize(self.distribution)
            self.fcompiler.customize_cmd(self)
            self.fcompiler.show_customization()
                
            src_dir = os.path.join('pycamb','src')

            self.copy_file(os.path.join(src_dir,'HighLExtrapTemplate_lenspotentialCls.dat'), os.path.join(self.build_lib,'pycamb'))

            #Hack because sometimes the executable linker is missing
            if not self.fcompiler.linker_exe: self.fcompiler.linker_exe = self.fcompiler.linker_so
    
            obj_files = self.fcompiler.compile([os.path.join(src_dir,'%s.f90'%o) for o in self.objs],
                                               extra_postargs=['-cpp',self.fcompiler.module_dir_switch+os.path.join(self.build_temp,src_dir)],
                                               output_dir=self.build_temp)
                
            self.fcompiler.link_executable(obj_files,'camb',output_dir=os.path.join(self.build_lib,'pycamb'))

        
        
setup(
  name='pycamb',
  version='0.1.0',
  author='Marius Millea',
  author_email='mmillea@ucdavis.edu',
  packages=['pycamb'],
  url='http://pypi.python.org/pypi/pycamb/',
  license='LICENSE.txt',
  description='A Python wrapper for the popular cosmology code CAMB.',
  long_description=open('README').read(),
  cmdclass={'build':build}
)
