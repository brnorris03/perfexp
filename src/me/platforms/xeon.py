#!/usr/bin/python

import os, commands
from params import *

from me.interfaces import AbstractPlatform

from me.tools.tau import Collector as TAUCollector
from me.tools.gprof import Collector as GprofCollector
from me.tools.ltimer import Collector as LtimerCollector
from storage.tools.tau import PerfDMFDB 
from storage.tools.gprof import Gprof
from analysis.interfaces import AbstractModel

class Generic(AbstractPlatform):

    def moveData(self, src, dest):
    
        DataCollector = LtimerCollector()
        dataFormat = DataCollector.getDataFormat()

        if not os.path.exists(dest):
            os.makedirs(dest)

        if dataFormat == 'profiles':
            moveCommand = 'mv ' + src + '/MULTI__P* ' + src + '/profile* ' + dest + '/'

        	# moveCommand = 'mv ' + src + '/MULTI__P* ' + dest + '/'
                # moveCommand2 = 'mv ' + src + '/profile* ' + dest + '/MULTI__' + counters[0] + '/'
                # moveCommand3 = 'mv ' + dest + '/profile* ' + dest + '/MULTI__' + counters[0] + '/'

            commands.getstatusoutput(moveCommand)
                # commands.getstatusoutput(moveCommand2)
                # commands.getstatusoutput(moveCommand3)
                
            if DEBUG==1: 
                print 'DEBUG:move performance data command: ', moveCommand
                print 'DEBUG:move performance data command: ', moveCommand2
                print 'DEBUG:move performance data command: ', moveCommand3

        elif dataFormat == 'psrun':    
            moveCommand = 'mv ' + src + '/*.xml ' + dest + '/'
            commands.getstatusoutput(moveCommand)
            if DEBUG==1: 
                print 'DEBUG:move performance data command: ', moveCommand
                
        elif dataFormat == 'gprof':
            moveCommand = 'mv ' + src + '/gmon.out* ' + dest + '/'
            commands.getstatusoutput(moveCommand)
            if DEBUG==1: 
                print 'DEBUG:move performance data command: ', moveCommand

        elif dataFormat == 'ltimer':
            moveCommand = 'mv ' + src + '/ltimer.out* ' + dest + '/'
            commands.getstatusoutput(moveCommand)
            if DEBUG==1: 
                print 'DEBUG:move performance data command: ', moveCommand

    def runApp(self, perfCmd):

        DataCollector = LtimerCollector()
        dataFormat = DataCollector.getDataFormat()
        DataCollector.setCounters()


        for p in processes:
            for t in threads:

                if pmodel == 'omp' or pmodel == 'mpi:omp':
                    os.environ['OMP_NUM_THREADS'] = t
                    cmd = perfCmd
                    cmd += cmdline 
                elif pmodel == 'mpi':
                    cmd = mpidir + '/mpirun -np ' + p + ' ' + cmdline +  ' ' + o 
                else:
                    cmd = cmdline  

                    # Run the application in the specified directory    
                if not os.path.exists(workdir): os.makedirs(workdir)
                try: os.chdir(workdir)
                except Exception,e:
                	print >> sys.stderr, 'Exception in ExperimentDriver:  '+str(e)
                dest = datadir + '/' + appname + '-' + expname + '-' + trialname + '-p' + p + 't' + t 

                if not os.path.exists(dest): os.makedirs(dest)
                try: os.chdir(dest)
                except Exception,e:
                    print >> sys.stderr, 'Exception in ExperimentDriver:  '+str(e)

                if DEBUG == 1:
                    print 'DEBUG: executing: ', cmd
                    print 'DEBUG: OMP_NUM_THREADS=', os.environ.get('OMP_NUM_THREADS')
 
                
                if exemode == 'interactive':
                    app_output = os.popen(cmd)
                    fp = open("expout", "w")
                    print >>fp,  app_output.read()
                    fp.close()
                    if DEBUG == 1:
                    	print 'DEBUG: interactive command: ', cmd 
                elif exemode == 'batch':
                    filename = workdir + '/' + 'mpi-p'+ str(p) + '-t' + str(t) +'.ll'
                    self.genBatchScript(p, t, filename, cmd, dest)
                    try: os.path.exists(filename)
                    except Exception,e:
                        print >> sys.stderr, 'Exception: Batch script does not exist  '+str(e)
                    mcmd = 'mv ' + workdir + '/' + 'mpi-p'+ str(p) + '-t' + str(t) + '.ll ' + dest + '/'
                    commands.getstatusoutput(mcmd)
                    if DEBUG == 1: 
                        print 'DEBUG: move ll files: ', mcmd

                    cmd = batchcmd + ' ' + dest + '/' + 'mpi-p'+ str(p) + '-t' + str(t) + '.ll ' 
                    if DEBUG == 1:
                        print 'DEBUG: batch submit command: ', cmd
                    app_output = os.popen(cmd)
                    fp = open("expout", "w")
                    print >>fp,  app_output.read()
                    fp.close()

                self.moveData(workdir, dest)

        
    def loadTrials(self, storage):
        
        #DB = PerfDMFDB()
        DB = storage

        for p in processes:
            for t in threads:
                destdir = datadir + '/' + appname + '-' + expname + '-' + trialname + '-p' + p + 't' + t
                tn = trialname + '-p' + p + '-t' + t
                DB.load(destdir, tn, p,t)


    def validateModel(self, model):

        #model = LogGPFT()
        params = []
        xdata = []
        ydata = []

        if pmodel == 'mpi':
        	for n in processes:
		        P = n
		        params.insert(0,P)
		        result = model.validate(params)
		        xdata.append(P)
		        ydata.append(result)

        elif pmodel == 'omp':
            for n in threads:
                T = n
                params.insert(0,T)
                result = model.validate(params)
                xdata.append(T)
                ydata.append(result)
                
        return xdata, ydata
