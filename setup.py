#!/usr/bin/env python

import os, urllib.request, urllib.error, urllib.parse, tarfile
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
        ('no-openmp', None,  "compile without OpenMP"),
        ]
    
    boolean_options = _build.boolean_options + ['no-builtin', 'no_openmp']
        
    def initialize_options(self):
        _build.initialize_options(self)
        self.no_builtin = None
        self.no_openmp = None
        
        
    def get_openmp_flags(self, fcompiler):
        """Hack to get OpenMP flags. Only gnu and intel will work, others are single threaded."""
        if not self.no_openmp:
            fc_name = {v:k for (k,(_,v,_)) in list(FC.fcompiler_class.items())}.get(fcompiler.__class__)
            if fc_name is not None:
                if fc_name.startswith('gnu'):
                    return ['-fopenmp']
                elif fc_name.startswith('intel'):
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
        if not fcompiler.linker_exe: 
            fcompiler.linker_exe = fcompiler.linker_so[:1]

        return fcompiler


    def download_file(self,url,target):
        """
        Download a file, raises HTTPError on fail
        """
        webFile = urllib.request.urlopen(url)
        localFile = open(target,'w')
        localFile.write(webFile.read())
        webFile.close()
        localFile.close()


    def run(self):
        """ Modified to compile CAMB. """
        
        _build.run(self)
        
        if not self.no_builtin and (self.force or not os.path.exists(os.path.join(self.build_lib,'camb4py','camb'))):
            
            fcompiler = self.get_fcompiler()

            src_tgz = "CAMB.tar.gz"
            src_dir = os.path.join(self.build_temp,"camb")
            if not os.path.exists(src_tgz): 
                print("Downloading CAMB from http://camb.info/CAMB.tar.gz...")
                self.download_file("http://camb.info/CAMB.tar.gz", src_tgz)
            if not os.path.exists(self.build_temp): os.makedirs(self.build_temp)
            tarfile.open(src_tgz).extractall(self.build_temp)
            for f in os.listdir(src_dir):
                if 'F90' in f: os.rename(os.path.join(src_dir,f), os.path.join(src_dir,f.replace('F90','f90')))

            templ = os.path.join(src_dir,'HighLExtrapTemplate_lenspotentialCls.dat')
            if os.path.exists(templ): 
                self.copy_file(templ, os.path.join(self.build_lib,'camb4py'))
    
    
            openmp_flags = self.get_openmp_flags(fcompiler)
            compile_flags = openmp_flags + ['-cpp']
            if fcompiler.module_dir_switch is not None: 
                compile_flags += [fcompiler.module_dir_switch+src_dir]
            link_flags = openmp_flags
            
            obj_files = fcompiler.compile([os.path.join(src_dir,'%s.f90'%o) for o in self.objs],
                                           extra_postargs=compile_flags,)
#                                           output_dir=self.build_temp)
                
            fcompiler.link_executable(obj_files,
                                      'camb',
                                      output_dir=os.path.join(self.build_lib,'camb4py'),
                                      extra_postargs=link_flags)

        
        
setup(
  name='camb4py',
  version='0.1.0',
  author='Marius Millea',
  author_email='mmillea@ucdavis.edu',
  packages=['camb4py'],
  url='http://pypi.python.org/pypi/camb4py/',
  license='LICENSE.txt',
  description='A Python wrapper for the popular cosmology code CAMB.',
  long_description=open('README.rst').read(),
  cmdclass={'build':build}
)
