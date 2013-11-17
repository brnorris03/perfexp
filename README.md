perfexp
=======

Python Infrastructure for Managing Performance Experiments

Directory organization:
=================

src/
 |_ analysis/            
    |_ metrics/
    |_ tools/
 |_ examples/
    |_ drivers/
    |_ models/
 |_ me/
    |_ platforms/
    |_ tools/
 |_ storage/
    |_ tools/
 |_ util/
 |_ vis/
    |_ tools/


Installing
==========

Installation is optional (scripts will work from the source directories). To install:

    python setup.py install

To install in an alternate location:

    python setup.py install --prefix=/path/to/insallation/dir

To run a script from source directories:

    export PYTHONPATH=<perfexp_location>/src:$PYTHONPATH

Running
=======

Usage: 

'''
   $ perfexp <drivermodule>
'''

The driver module is a Python module in your Python path. Some examples are included in the examples/drivers directory.
You can try them with:

* perfexp examples.drivers.ExperimentDriver
* perfexp examples.drivers.DataManagerDriver
* perfexp examples.drivers.AnalysisDriver
* perfexp examples.drivers.ModelDriver

Running a performance experiment
===========================

1. Go to perfexp/src/examples/params and add parameter values in params.txt for the ExperimentDriver and DataManager
section. Parameters that are required must have a value. Other parameters are needed only for running on specific
systems. The required parameters are specified below under the section 'Parameter Definitions'.

Optional: It is possible to define more then one parameter file in order to run multiple sets of experiments. The
parameter files must be named uniquely in the params directory.

2. Go to perfexp/src/examples/drivers and specify the measurement environment and performance collection mode in
ExperimentDriver.py. For example, to run on an AIX platform and collect data with TAU, add the following lines to the
header of ExperimentDriver.py

'''
from me.platforms.aix import BluePrint
from me.tools.tau import Collector as TAUCollector
'''

In the main function, add the following lines to ExperimentDriver.py

'''
measurementEnvironment = BluePrint()
dataCollector = TAUCollector()
'''

Optional: To collect hardware counters in the run, specify the hardware counter names for the 'counters' parameter in params.txt. For example:

'''
counters = PAPI_TOT_CYC PAPI_FP_OPS PAPI_TOT_INS
'''

3. Go to perfexp/src/me/platforms/ and specify in platform python script the performance collection mode. For example,
to collect data with TAU, add the following line in the heaader:

'''
from me.tools.tau import Collector 
'''

4. Set the PERFEXPDIR environment variable to the location of perfexp top directory.

5. Go to the perfexp top directory and run the script to start the experiment:

'''
$ scripts/perfexp examples.drivers.ExperimentDriver
'''

6. When the jobs finish running, the datadir (parameter from the DataManager section) will store the output from each
run for the experiment

Analysis of the results of a performance experiment
=======================================

1. Go to perfexp/src/examples and add parameter values in params.txt for the DataManager and Analysis section.
Parameters that are required must have a value. Other parameters are needed only for specific analysis tools.

2. Go to perfexp/src/examples/drivers and specify the analysis tool in AnalysisDriver.py. For example, if PerfExplorer
is the analysis tool, add the following line to the header of AnalysisDriver.py

'''
from analysis.tools.tau import PerfExplorer
'''

In the main function, add the following line to AnalysisDriver.py

'''
analysis = PerfExplorer()
'''

If using PerfExplorer for analysis, also specify the performance metric in AnalysisDriver.py. For example, to use
wall-clock time as the analysis metric, add the following line to the header of AnalysisDriver

'''
from analysis.metrics.time import WallClock
'''

In the main function, add the following line to AnalysisDriver.py

'''
metric = WallClock(params={})
'''

3. Go to the perfexp top directory and run the script to analyze the performance data:

'''
$ scripts/perfexp examples.drivers.AnalysisDriver
'''

4. When the analysis is complete, the resultsdir (parameter from the Analysis section) will store the analysis results


Modeling the performance of an application
=================--------------------

1. Go to perfexp/src/examples and add parameter values in params.txt for the Modeling and Analysis section. Parameters
that are required must have a value. Other parameters are needed only for specific models. For example, here are some
additional parameters needed to model HPCC RandomAccess:

'''
tn: number of updates
tg: time to generate a random value
tu = time to perform an update
tl = time to get a lock
ta = time to send/receive a message
m = message size
tul = time to unlock
'''

2. Go to perfexp/src/examples/drivers and specify the performance model in ModelDriver.py. For example, to model
RandomAccess by plotting and for an AIX platform, add the following line to the header of ModelDriver.py

'''
from examples.models.rarma import RARMA
from vis.tools.pylab import Plotter
from me.platforms.aix import BluePrint as AIXMeasurementEnv
'''

In the main function, add the following line to ModelDriver.py

'''
vm = AIXMeasurementEnv()
plotter = Plotter()
model = RARMA()
'''

3. Go to the perfexp top directory and run the script to model the application:

'''
$ scripts/perfexp examples.drivers.ModelDriver
'''

4. When the modeling is complete, the resultsdir (parameter from the Analysis section) will store the analysis results


Parameter definitions for ExperimentDriver section
======================================

* workdir (required): scratch directory where files can be autogenerated; typically the directory where the executable is located
* mpidir: location of mpirun or mpiexec 
* inputdir: location of input files for running code
* inputfiles: list of input file names used for running code
* cmdline (required): command to execute the program (include the directory)
* threads (required): number of threads
* processes (required): number of processes
* nodes (required): number of nodes
* tasks_per_node (required): number of tasks per node, this is the same as the number of processes
* pmodel (required): programming model #for MPI, mpi; for OpenMP, omp; for hybrid MPI/OpenMP, mpi:omp, for serial codes, serial 
* instrumentation: performance measurement instrumentation (manual, compiletime, runtime)
* exemode (required): mode of execution (batch, interactive)
* batchcmd: runtime command for a job submission
* jobname: name of job for script
* walltime: walltime for job script
* maxprocessor: maximum number of processor for job script
* accountname: account name for job script
* buffersize: amount of memory for MPI buffering
* msgsize: MPI message size
* stacksize: stack size
* counters: performance counters (PAPI or native counter names)
* commode: communication protocol mode #for internet, IP; for user space,US
* smt: to enable simultaneous multithreading (yes or no)
* memorysize: size of memory in bytes
* queue: name of the job queue, this is system dependent

Parameter definitions for DataManager section:
==================================

* datadir (required): location where output from program is stored
* appname (required): application name
* expname (required): experiment name
* trialname (required): trial name
* cqosloaderdir: location of cqos loader file
* cqosloader: name of cqos loader file
* dbconfig: name of database configuration

Parameter definitions for the Analysis section:
==================================

* resultsdir (required): directory name where analysis results will be stored
* programevent: program event for analysis of performance data from TAU
* metric: performance metric
* metricparams: parameters in performance metric
* xaxislabel (required): x axis label for performance graph
* yaxislabel (required): y axis label for performance graph
* graphtitle (required): graph title
* mhz: processor speed
* ptool: performance tool # If using TAU, tau; if using PerfSuite, perfsuite
* l2cacheline: L2 cache line size
* plotfilename (required): name of plotter script


Parameter definitions for the Modeling section
==================================

* legend (required): legend for measured and modeled data; for example, measured modeled
