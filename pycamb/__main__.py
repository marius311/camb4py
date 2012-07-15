import subprocess, os, sys

camb_exec = os.path.join(os.path.dirname(os.path.abspath(__file__)),'camb')

if os.path.exists(camb_exec):
    subprocess.call([camb_exec]+sys.argv[1:])
else:
    print "pycamb was installed without built in CAMB.\nPlease re-install pycamb to use this feature."
