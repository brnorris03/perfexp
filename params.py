#!/usr/bin/python

DEBUG = 1

# Parameters for ExperimentDriver

workdir = '/homes/vbui/projects/benchmarks/amg/AMG2006/test'
mpidir = '/disks/large/soft/mpich2-1.2-intel/bin'
cmdline = '/homes/vbui/projects/benchmarks/amg/AMG2006/test/./amg2006 -in /homes/vbui/projects/benchmarks/amg/AMG2006/test/sstruct.in.AMG.FD'
cmdlineopts = ['-P 1 1 1', '-P 1 1 2', '-P 1 2 2', '-P 2 2 2']
threads = ['1']
processes = ['1','2','4','8']
nodes = ['1']
tasks_per_node = ['1']
pmodel = 'mpi'
instrumentation = 'compiletime'
exemode = 'interactive'
batchcmd = 'llsubmit'

# Parameters for MeasurementEnvironment

counters = ['PAPI_TOT_CYC']

# Parameters for DataManager

datadir = '/homes/vbui/projects/benchmarks/amg/AMG2006/test/data'
appname =  'amg'
expname = 'cookie-mpi'
trialname = 'tau-mpi'
cqosloaderdir = '/homes/vbui/projects/experiments/fun3d'
cqosloader = 'CQoSDataLoader_fat_tau.jar'
dbconfig = 'random_access'

# Parameters for Analysis

resultsdir = '/homes/vbui/projects/benchmarks/ra-bp/src/openmp/data-bp/data'
programevent = '.TAU application' 
metric = 'PAPI_TOT_CYC'
xaxislabel = 'Threads'
yaxislabel = 'Time (secs)'
graphtitle = 'RandomAccess: OpenMP'
mhz = '1.9e9'
ptool = 'tau'
l2cacheline = '64'
