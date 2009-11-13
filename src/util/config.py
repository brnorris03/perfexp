#!/usr/bin/env python
import os, sys, distutils.sysconfig

def getperfexpPkgDir():
    """Return the full path to the site-packages directory under the 
    perfexp installation prefix (standard distutils installation).
    
    If 'prefix' is supplied, use it instead of the computed location
    of the installed perfexp script.
    """
    
    prefix = None
    perfexp_execdir = os.path.dirname(os.path.realpath(sys.argv[0]))
    
    # first check whether we are in source tree
    pos = perfexp_execdir.find('src')
    if pos > 0:
        prefix = perfexp_execdir[:pos]
        if os.path.exists(os.path.join(prefix,'src','analysis','metrics')): 
            return os.path.join(prefix, 'src'), prefix
    
    # else look for installed version
    pos = perfexp_execdir.find('perfexp')  # installed location
    if pos > 0:
        prefix = perfexp_execdir[:pos]
        if not os.path.exists(os.path.join(prefix,'analysis','metrics')): 
            prefix = None

    if not prefix: return None, None  # give up
    
    libdirname = distutils.sysconfig.get_config_var('LIB')
    if libdirname is None: 
        # True for python versions < 2.5
        libdirname = 'lib'
    thedir =  os.path.join(prefix,libdirname,'python' + distutils.sysconfig.get_python_version(), 'site-packages', 'perfexp')
    newdir=''

    if not os.path.exists(thedir):
        files = []
        # Look for the parent of site-packages
        for file in os.listdir(prefix):
            fulldir = os.path.join(prefix, file)
            if os.path.isdir(fulldir):
                for x in os.listdir(fulldir):
                    if os.path.isdir(os.path.join(fulldir,x)):
                        if x.startswith('python' + distutils.sysconfig.get_python_version()):
                            fulldir = os.path.join(fulldir, x)
                        elif x == 'python': 
                            fulldir = os.path.join(fulldir, x)
                        else: continue
                        for y in os.listdir(fulldir):
                            if y == 'site-packages':
                                newdir =  os.path.join(fulldir, 'site-packages', 'perfexp')
                                break 
            if newdir: 
                thedir = newdir
                break
    
    if not os.path.exists(thedir):
        print >> sys.stderr, 'Cannot find the location where perfexp modules have been installed, please add the path to your PYTHONPATH environment variable.'
        sys.exit(1)

    theparent = os.path.dirname(thedir)
    return (thedir, theparent)

def setPythonPath():

    # Set the python path
    (perfexpPath, perfexpParent) = getperfexpPkgDir()
   
    if os.path.exists(perfexpPath): 
        sys.path.append(perfexpParent)
        sys.path.append(perfexpPath)
        sys.path.append(os.path.join(perfexpPath,'examples'))
    
    
    if 'PERFEXP_DEBUG' in os.environ.keys():
        if os.environ['PERFEXP_DEBUG'] == "1":
            sys.stderr.write('The perfexp module directory is %s\n' % perfexpPath)
            sys.stderr.write('Full Python path: %s\n' % sys.path)


    try:
        from analysis.interfaces import AbstractModel
    except:
        sys.stderr.write('perfexp ERROR: Could not set the Python path, please add the perfexp ' \
                         + 'installation to the PYTHONPATH environment variable.')
        sys.stderr.write('\nFull Python path: %s' % sys.path)
        sys.exit(1)
 

if __name__ == "__main__":

    # Self test
    setPythonPath()

