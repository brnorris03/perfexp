#!/usr/bin/python

import os, commands,sys

from me.interfaces import AbstractPlatform
from me.tools.tau import Collector as TAUCollector
from me.tools.gprof import Collector as GprofCollector
from me.tools.ltimer import Collector as LtimerCollector
from storage.tools.tau import PerfDMFDB 
from storage.tools.gprof import Gprof
from analysis.interfaces import AbstractModel
from me.params import MEParams
from storage.params import DBParams

class Generic(AbstractPlatform):

    def moveData(self, src, dest):
    
        DataCollector = TAUCollector()
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
                
            if MEParams.meparams['DEBUG']=="1": 
                print 'DEBUG:move performance data command: ', moveCommand
#                print 'DEBUG:move performance data command: ', moveCommand2
#                print 'DEBUG:move performance data command: ', moveCommand3

        elif dataFormat == 'psrun':    
            moveCommand = 'mv ' + src + '/*.xml ' + dest + '/'
            commands.getstatusoutput(moveCommand)
            if MEParams.meparams['DEBUG']=="1": 
                print 'DEBUG:move performance data command: ', moveCommand
                
        elif dataFormat == 'gprof':
            moveCommand = 'mv ' + src + '/gmon.out* ' + dest + '/'
            commands.getstatusoutput(moveCommand)
            if MEParams.meparams['DEBUG']=="1": 
                print 'DEBUG:move performance data command: ', moveCommand

        elif dataFormat == 'ltimer':
            moveCommand = 'mv ' + src + '/ltimer.out* ' + dest + '/'
            commands.getstatusoutput(moveCommand)
            if MEParams.meparams['DEBUG']=="1": 
                print 'DEBUG:move performance data command: ', moveCommand

    def runApp(self, perfCmd):

        for p in MEParams.meparams['processes'].split():
            for t in MEParams.meparams['threads'].split():

                if MEParams.meparams['pmodel'] == "omp" or MEParams.meparams['pmodel'] == "mpi:omp":
                    os.environ['OMP_NUM_THREADS'] = t
                    cmd = perfCmd
                    cmd += MEParams.meparams['cmdline'] 
                elif MEParams.meparams['pmodel'] == 'mpi':
                    cmd = MEParams.meparams['mpidir'] + ' -np ' + p + ' ' + MEParams.meparams['cmdline'] +  ' ' + o 
                elif MEParams.meparams['pmodel'] == 'serial':
                    cmd = MEParams.meparams['cmdline']  

                    # Run the application in the specified directory    
                if not os.path.exists(MEParams.meparams['workdir']): os.makedirs(MEParams.meparams['workdir'])
                try: os.chdir(MEParams.meparams['workdir'])
                except Exception,e:
                	print >> sys.stderr, 'Exception in ExperimentDriver:  '+str(e)
                dest = DBParams.dbparams['datadir'] + '/' + DBParams.dbparams['appname'] + '-' + DBParams.dbparams['expname'] + '-' + DBParams.dbparams['trialname'] + '-p' + p + 't' + t 

                if not os.path.exists(dest): os.makedirs(dest)
                try: os.chdir(dest)
                except Exception,e:
                    print >> sys.stderr, 'Exception in ExperimentDriver:  '+str(e)

                if MEParams.meparams['DEBUG'] == "1":
                    print 'DEBUG: executing: ', cmd
                    print 'DEBUG: OMP_NUM_THREADS=', os.environ.get('OMP_NUM_THREADS')
 
                
                if MEParams.meparams['exemode'] == "interactive":
                    app_output = os.popen(cmd)
                    fp = open("expout", "w")
                    print >>fp,  app_output.read()
                    fp.close()
                    if MEParams.meparams['DEBUG'] == "1":
                    	print 'DEBUG: interactive command: ', cmd 
                elif MEParams.meparams['exemode'] == "batch":
                    filename = MEParams.meparams['workdir'] + '/' + 'mpi-p'+ p + '-t' + t +'.ll'
                    self.genBatchScript(p, t, filename, cmd, dest)
                    try: os.path.exists(filename)
                    except Exception,e:
                        print >> sys.stderr, 'Exception: Batch script does not exist  '+str(e)
                    mcmd = 'mv ' + MEParams.meparams['workdir'] + '/' + 'mpi-p'+ p + '-t' + t + '.ll ' + dest + '/'
                    commands.getstatusoutput(mcmd)
                    if MEParams.meparams['DEBUG'] == "1": 
                        print 'DEBUG: move ll files: ', mcmd

                    cmd = MEParams.meparams['batchcmd'] + ' ' + dest + '/' + 'mpi-p'+ p + '-t' + t + '.ll ' 
                    if MEParams.meparams['DEBUG'] == "1":
                        print 'DEBUG: batch submit command: ', cmd
                    app_output = os.popen(cmd)
                    fp = open("expout", "w")
                    print >>fp,  app_output.read()
                    fp.close()

                self.moveData(MEParams.meparams['workdir'], dest)

        
    def loadTrials(self, storage):
        
        #DB = PerfDMFDB()
        DB = storage

        for p in MEParams.meparams['processes'].split():
            for t in MEParams.meparams['threads'].split():
                destdir = DBParams.dbparams['datadir'] + '/' + DBParams.dbparams['appname'] + '-' + DBParams.dbparams['expname'] + '-' + DBParams.dbparams['trialname'] + '-p' + p + 't' + t
                tn = DBParams.dbparams['trialname'] + '-p' + p + '-t' + t
                DB.load(destdir, tn, p,t)


    def validateModel(self, model):

        #model = LogGPFT()
        params = []
        xdata = []
        ydata = []

        if MEParams.meparams['pmodel'] == "mpi":
        	for n in MEParams.meparams['processes'].split():
		        P = n
		        params.insert(0,P)
		        result = model.validate(params)
		        xdata.append(P)
		        ydata.append(result)

        elif MEParams.meparams['pmodel'] == "omp":
            for n in MEParams.meparams['threads'].split():
                T = n
                params.insert(0,T)
                result = model.validate(params)
                xdata.append(T)
                ydata.append(result)
                
        return xdata, ydata
