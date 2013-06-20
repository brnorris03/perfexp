# This file is part of Contractor
# Original author: Daniel Taylor, dan@programmer-art.org
# (c) 2008-2010 UChicago Argonne, LLC
# (c) 2011 Tech-X Corporation
# (c) 2013 UChicago Argonne LLC
# For copying information, see the file LICENSE

#!/usr/bin/env python


"""
    Cores
    =====
    Functionality to find the number of cores in a system. Finding the number of
    cores on a system is operating system and sometimes architecture specific.
    What this script does is provide a cross-platform, simple to use way to find
    the number of cpus on a system by wrapping a bunch of os-specific
    functionality in a simple function.
    
    If your operating system or architecture are not yet supported please file
    a bug with information on how to retrieve the number of cpus.
    
    Usage
    -----
    See the get_num_cores() function.
    
    Systems That Should Be Supported
    --------------------------------
    These systems should be supported, but not all may have been tested to be
    supported.
    
        - Linux
        - Mac OS X
        - FreeBSD, OpenBSD, NetBSD, DragonFlyBSD, PC-BSD
        - Solaris
        - Windows Vista
        - BeOS R5, Haiku
        - AIX
        - HP-UX
    
    Testing
    -------
    Please list all tested systems here for reference. Thanks!
    
        - Linux i686 (amd64 Ubuntu 7.04)
        - Linux i686 (4 dual-core Opteron Ubuntu 7.04)
        - Darwin i386 (Core 2 Duo Mac OS X)
        - Darwin ppc (G4 Mac OS X)
        - SunOS i386 (Core 2 Duo Solaris)
        - FreeBSD i386
        - PC-BSD i386 (Core 2 Duo)
        - BeOS BePC (Core 2 Duo Haiku nightly build)
    
    Authors
    -------
    Daniel G. Taylor <dan@programmer-art.org>
    Boyana Norris <norris@mcs.anl.gov>
    
    Contributers
    ------------
    Jens Taylor <jensyt@gmail.com> - Testing
"""

import os, os.path
from utils import grep
from messages import err,warn,info,debug
from globals import Globals

def ParConfig(default = 1, dynamic=False):
    '''Helper function to ensure exactly one instance of the ParConfig_Singleton class exists.'''
    parconfig = None
    try:
        parconfig = ParConfig_Singleton()
    except ParConfig_Singleton, s: 
        parconfig = s
    return parconfig

def get_num_cores(default = 1, dynamic = False):
    '''Shortcut to getting number of cores.'''
    return ParConfig().get_num_cores(default, dynamic)

def set_num_cores(ncores, caching = True, dynamic = False):
    '''Shortcut to setting number of cores.'''
    return ParConfig().set_num_cores(ncores, caching, dynamic)

class ParConfig_Singleton:

    __single = None  # Used for ensuring singleton instance
    def __init__(self):
        if ParConfig_Singleton.__single:
            raise ParConfig_Singleton.__single 
        ParConfig_Singleton.__single = self
        self._cores = 0 # number of processes to use for parallel builds
        self._maxcores = 0 # number of available cores
        self._caching = False
        self._dynamic = False
        pass

    def set_num_cores(self, ncores, caching = True, dynamic=False):
        """
        Set the number of processes to use, overriding the automatic determination
        """
        self._cores = ncores
        self._caching = caching
        self._dynamic = dynamic
    

    def get_num_cores(self, default = 1, dynamic=False):
        """
        Get the number of cpu cores on a system, or the default if the correct
        number cannot be found.
        
        Usage
        -----
        The get_num_cores function will return either the number of cores on the
        current system or the default number, which is set to 1 or whatever you
        pass into the function. When caching is used the function will only
        query the system once, and on subsequent calls return that same number.
        
        cores = get_num_cores()    # Return the number of cores or default (1)
        
        cores = get_num_cores(2)   # Return the number of cores or 2
        
        @param default: Default number of cores to return if the real number cannot
                        be found.
        @type default: int
        @param caching: Whether or not to cache the results for subsequent calls
        @type caching: bool
	    @param dynamic: Use load information to select the number of cores to use
	    @type dynamic: bool
        @return: The number of cpus or the default
        """

        if self._cores and self._caching:
            cores = int(self._cores)
        else:
            # Set the default number of cores
            cores = default
        
            # Get the system and cpu names
            try:
                import platform
                pinfo = platform.uname()
            except:
                try:
                    pinfo = os.uname()
                except:
                    warn("No platform.uname or system.uname present...")
                    return default
            
            system = pinfo[0]
            cpu = pinfo[4]
            Globals().system = system
            Globals().cpu = cpu
            debug("System,cpu: %s,%s" % (system,cpu))
            
            error_msg = "Unable to find the number of cpu cores (%s, %s)\n" % \
                        (system, cpu)
            error_msg += "Please report this error along with information on how to" + \
                         " find the number of cpu cores on your system."
            
            # Try and find the cpu core count using os-specific techniques
            if system in ["Linux", "SunOS"]:
                # Check the newer sysfs on Linux for cpu information
                if system == "Linux" and os.access("/sys/devices/cpu", os.R_OK):
                    cores = len(os.listdir("/sys/devices/cpu"))
                else:
                    # Check the older procfs for Linux and other Unix
                    if os.access("/proc/cpuinfo", os.R_OK):
                        cores = len(grep(open("/proc/cpuinfo").read(), "^processor"))
                    else:
                        warn(error_msg)
            elif system in ["FreeBSD", "NetBSD", "OpenBSD", "DragonFly", "Darwin"]:
                # Get the number of cpus from the sysctl utility
                try:
                    cores = int(os.popen("sysctl -n hw.ncpu").read())
                except:
                    if system == "Darwin":
                        try:
                            # Use the system profiler utility if we can
                            system_info = os.popen("system_profiler -detailLevel mini")
                            found = False
                            for line in system_info.readlines():
                                if "Number Of Cores: " in line:
                                    # The utility outputs something like:
                                    # Total Number Of Cores: X
                                    # Pull off the last word and convert it to an int
                                    cores = int(line.split(" ")[-1])
                                    found = True
                                    break
                            if not found:
                                warn(error_msg)
                        except:
                            warn(error_msg)
                    else:
                        warn(error_msg)
            elif system == "Windows":
                # Get the number of cpus from the WinSAT.exe utility if possible
                # TODO: Test this and also find the Windows installation path
                # automagically somehow instead of hard coding C:\\
                try:
                    sysinfo = os.popen("C:\Windows\System32\WinSAT.exe features").read()
                    cores = int(grep(sysinfo, ".*Number of Cores :")[0].split(":")[1])
                except:
                    warn(error_msg)
            elif system in ["Haiku", "BeOS"]:
                # Get the number of cpus from the sysinfo utility
                try:
                    sysinfo = os.popen("sysinfo").read()
                    cores = len(grep(sysinfo, ".*CPU #"))
                except:
                    warn(error_msg)
            elif system == "AIX":
                # Get the number of cpus from the lsdev or lscfg utilities
                # TODO: Someone with AIX test this!
                try:
                    procinfo = os.popen("lsdev -C").read()
                    cores = len(grep(procinfo, ".*Process"))
                except:
                    try:
                        cfginfo = os.popen("lscfg -v").read()
                        cores = len(grep(cfginfo, ".*proc"))
                    except:
                        try:
                            cores = len(os.popen("bindprocessor -q").read().split( \
                                    ":")[1].split(" "))
                        except:
                            warn(error_msg)
            elif system == "HP-UX":
                # Get the number of cpus from the ioscan utility
                # TODO: Someone with HP-UX test this!
                try:
                    procinfo = os.popen("ioscan -C processor").read()
                    cores = len(grep(procinfo, ".*processor"))
                except:
                    warn(error_msg)
            else:
                warn(error_msg)
    
            if cores: 
                self._maxcores = cores
                if not self._caching: self._cores = cores
    
        
        # While not perfect, checking current load is useful to avoid swamping the machine
        # check the 1, 5, and 15-minute loads
        if not self._caching and (dynamic or self._dynamic) and hasattr(os,"getloadavg"):
            if self._maxcores: cores = self._maxcores
            loads = [x for x in os.getloadavg()]
            if cores < max(loads) and cores <= loads[0]: cores = 1
            if cores > loads[0]: cores -= int(loads[0])
            if cores < 1: cores = 1
            self._cores  = cores
        
        return cores

