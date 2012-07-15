import subprocess, os, sys

if os.path.exists('camb'):
    subprocess.call(['camb']+sys.argv[1:])
else:
    print "pycamb installed without built in CAMB. Please re-install pycamb to use this feature."
