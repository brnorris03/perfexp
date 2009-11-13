#!/usr/bin/env python
from distutils.core import setup

verbose=1

setup (name = "PerfExp", version = "0.1",
       description = "PerfExp",
       url="http://trac.mcs.anl.gov/projects/performance/wiki/PerfexpPy",
       author="PerfExp developers",
       author_email="vbui@mcs.anl.gov, norris@mcs.anl.gov",
       package_dir = {'perfexp': 'src'},
       packages = ['perfexp',
                   'perfexp.analysis', 'perfexp.analysis.metrics', 'perfexp.analysis.tools', 
                   'perfexp.me', 'perfexp.me.platforms', 'perfexp.me.tools',
                   'perfexp.storage', 'perfexp.storage.tools',
                   'perfexp.util',
                   'perfexp.vis', 'perfexp.vis.tools',
                   'perfexp.examples', 'perfexp.examples.drivers', 'perfexp.examples.models'],
       scripts = ['scripts/perfexp'],
      )
