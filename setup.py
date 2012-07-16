import os
from numpy.distutils.command.build import build as _build
from numpy.distutils.core import setup
import numpy.distutils.fcompiler as FC
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
        
        
    def get_openmp_flags(self, fcompiler):
        """Hack to get OpenMP flags. Only gnu and intel will works, other are single threaded."""
        fc_name = {v:k for (k,(_,v,_)) in FC.fcompiler_class.items()}.get(fcompiler.__class__)
        if fc_name is not None:
            if fc_name.startswith('gnu'):
                return ['-fopenmp']
            elif fc_name.startswiths('intel'):
                return ['-openmp']
        return []
        
        
    def get_fcompiler(self):
        """Get an fcompiler (including some hacks) or print error message if not found."""
        fcompiler = FC.new_fcompiler(compiler=self.fcompiler,
                                     verbose=self.verbose,
                                     dry_run=self.dry_run,
                                     force=self.force,
                                     c_compiler=self.compiler)
        
        if fcompiler is None:
            raise DistutilsError('Could not find Fortran compiler. See setup.cfg to specify one.')
            
        fcompiler.customize(self.distribution)
        fcompiler.customize_cmd(self)
        fcompiler.show_customization()
        
        #Hack because sometimes the executable linker is missing
        if not fcompiler.linker_exe: fcompiler.linker_exe = fcompiler.linker_so

        return fcompiler

        
    def run(self):
        _build.run(self)
        
        if not self.no_builtin and (self.force or not os.path.exists(os.path.join(self.build_lib,'pycamb','camb'))):
            
            fcompiler = self.get_fcompiler()
            
            src_dir = os.path.join('pycamb','src')

            self.copy_file(os.path.join(src_dir,'HighLExtrapTemplate_lenspotentialCls.dat'), os.path.join(self.build_lib,'pycamb'))
    
            openmp_flags = self.get_openmp_flags(fcompiler)
            compile_flags = openmp_flags + ['-cpp',fcompiler.module_dir_switch+os.path.join(self.build_temp,src_dir)]
            link_flags = openmp_flags
            
            obj_files = fcompiler.compile([os.path.join(src_dir,'%s.f90'%o) for o in self.objs],
                                           extra_postargs=compile_flags,
                                           output_dir=self.build_temp)
                
            fcompiler.link_executable(obj_files,
                                      'camb',
                                      output_dir=os.path.join(self.build_lib,'pycamb'),
                                      extra_postargs=link_flags)

        
        
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
