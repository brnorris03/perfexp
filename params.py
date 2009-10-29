#!/usr/bin/python

DEBUG = 1

# Parameters for ExperimentDriver

workdir = '/homes/vbui/projects/benchmarks/ra-bp/src/openmp'
mpidir = '/disks/large/soft/mpich2-1.2-intel/bin'
cmdline = '/homes/vbui/projects/benchmarks/ra-bp/src/openmp/./random_access'
threads = ['1','2','4','8']
processes = ['1']
nodes = ['1']
tasks_per_node = ['1']
pmodel = 'omp'
instrumentation = 'compiletime'
exemode = 'interactive'
batchcmd = 'llsubmit'

# Parameters for MeasurementEnvironment

counters = ['PAPI_TOT_CYC']

# Parameters for DataManager

datadir = '/homes/vbui/projects/benchmarks/ra-bp/src/openmp/data'
appname =  'randomaccess'
expname = 'cookie-omp'
trialname = 'tau-omp'
cqosloaderdir = '/homes/vbui/projects/experiments/fun3d'
cqosloader = 'CQoSDataLoader_fat_tau.jar'
dbconfig = 'random_access'

# Parameters for Analysis

resultsdir = '/homes/vbui/projects/benchmarks/ra-bp/src/openmp/data'
programevent = '.TAU application' 
metric = 'PAPI_TOT_CYC'
xaxislabel = 'Threads'
yaxislabel = 'Time (secs)'
graphtitle = 'RandomAccess: OpenMP'
mhz = '2.8e9'
ptool = 'tau'
l2cacheline = '64'
