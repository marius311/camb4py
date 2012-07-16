import subprocess, sys
from pycamb import get_default_executable

camb_exec = get_default_executable()

if camb_exec is None:
    print "pycamb was installed without built-in CAMB.\nRe-install pycamb with built-in CAMB to use this feature."
else:
    subprocess.call([camb_exec]+sys.argv[1:])
