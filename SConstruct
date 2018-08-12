import os, sys
try:
    import bldutil
    glob_build = True 
    srcroot = '../..'
    Import('env bindir libdir pkgdir')
except:
    glob_build = False
    srcroot = os.environ.get('RSFSRC', '../..')
    sys.path.append(os.path.join(srcroot,'framework'))
    import bldutil
    env = bldutil.Debug() 
    bindir = pkgdir = libdir = None
targets = bldutil.UserSconsTargets()
 # C mains
targets.c = '''
treq ytxrna2
'''
 # Python targets
targets.py = '''
gray
'''
try:  # distributed version
    Import('env root pkgdir bindir')
    env = env.Clone()
except: # local version
    env = bldutil.Debug()
    root = None
    bindir = pkgdir = None
targets.build_all(env, glob_build, srcroot, bindir, libdir, pkgdir)