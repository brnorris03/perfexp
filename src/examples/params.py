#!/usr/bin/python

DEBUG = 1

# Parameters for ExperimentDriver

workdir = '/homes/vbui/projects/benchmarks/amg/AMG2006/test'
mpidir = '/disks/large/soft/mpich2-1.2-intel/bin'
cmdline = '/homes/vbui/projects/benchmarks/amg/AMG2006/test/./amg2006 -in /homes/vbui/projects/benchmarks/amg/AMG2006/test/sstruct.in.AMG.FD'
cmdlineopts = ['-P 1 1 1', '-P 1 1 2', '-P 1 2 2', '-P 2 2 2']
threads = ['2']
processes = ['1','2','4','8']
nodes = ['1','2','4','8','16','32','64']
# nodes = ['64']
tasks_per_node =  ['16']
pmodel = 'mpi'
instrumentation = 'compiletime'
exemode = 'interactive'
batchcmd = 'llsubmit'

# Parameters for MeasurementEnvironment

counters = ['PAPI_TOT_CYC']

# Parameters for DataManager

datadir = '/homes/vbui/projects/benchmarks/ft-c'
appname =  'ft'
expname = 'ft-bp-mpi'
trialname = 'ft-tau-mpi'
cqosloaderdir = '/homes/vbui/projects/experiments/fun3d'
cqosloader = 'CQoSDataLoader_fat_tau.jar'
dbconfig = 'benchmarks'

# Parameters for Analysis

resultsdir = '/homes/vbui/projects/benchmarks/ft-c'
programevent = '.TAU application' 
metric = 'time.WallClock'
metricparams = {'name':'PAPI_TOT_CYC'}
xaxislabel = 'MPI Processes'
yaxislabel = 'Time (secs)'
graphtitle = 'FT: MPI, Tasks=16'
mhz = '1.9e9'
ptool = 'tau'
l2cacheline = '64'

# Parameters for Models

modelparams = ['0.1','100','4','4','5','6']
legend = ['Measured', 'LogP']
