import subprocess, sys
from .camb4py import get_default_executable

camb_exec = get_default_executable()

if camb_exec is None:
    print("camb4py was installed without built-in CAMB.\nRe-install camb4py with built-in CAMB to use this feature.")
else:
    subprocess.call([camb_exec]+sys.argv[1:])
