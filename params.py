#!/usr/bin/python

DEBUG = 1

# Parameters for ExperimentDriver

workdir = '/u/home/ac/vtbui/projects/benchmarks/ra/openmp'
mpidir = ' '
cmdline = 'poe /u/home/ac/vtbui/projects/benchmarks/ra/openmp/./random_access'
threads = ['1','2','4','8','16']
processes = ['1']
nodes = ['1']
tasks_per_node = ['1','2','4','8','16']
pmodel = 'mpi'
instrumentation = 'runtime'
exemode = 'batch'
batchcmd = 'llsubmit'

# Parameters for MeasurementEnvironment

counters = ['P_WALL_CLOCK_TIME', 'PAPI_TOT_CYC', 'PAPI_TOT_INS']

# Parameters for DataManager

datadir = '/homes/vbui/projects/benchmarks/ra-bp/data-mpi'
appname =  'randomaccess'
expname = 'mpi'
trialname = 'aix-tau'
cqosloaderdir = '/homes/vbui/projects/experiments/fun3d'
cqosloader = 'CQoSDataLoader_fat_tau.jar'
dbconfig = 'random_access'

# Parameters for Analysis

resultsdir = '/homes/vbui/projects/benchmarks/ra-bp/results-mpi'
programevent = '.TAU application' 
metric = 'PAPI_TOT_CYC'
xaxislabel = 'Processes'
yaxislabel = 'Cycles'
graphtitle = 'RandomAccess: MPI'
mhz = '1.9e9'
ptool = 'tau'
l2cacheline = '64'
