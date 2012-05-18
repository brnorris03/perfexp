#!/usr/bin/python

import os, commands
from me.tools.perfsuite import Collector 
from storage.tools.gprof import Gprof 
from me.params import MEParams
from storage.params import DBParams

class iForge:

	def genBatchScript(self, node, tasks_per_node, threads, i,filename, execmd, destdir):

		DataCollector = Collector()
                dataFormat = DataCollector.getDataFormat()
		ccmd = DataCollector.getCommand()

		f = open(filename, 'w')

		print >>f, '#!/bin/tcsh'
		print >>f, '#PBS -l walltime=' + MEParams.meparams['walltime']
		print >>f, '#PBS -l nodes='+node+':ppn='+tasks_per_node
		print >>f, '#PBS -V'
		print >>f, '#PBS -q '+ MEParams.meparams['queue']
		print >>f, '#PBS -N ' + MEParams.meparams['jobname']
		print >>f, '#PBS -A ' + MEParams.meparams['accountname']
                print >>f, '#PBS -W x=NACCESSPOLICY:SINGLEJOB'
		print >>f, 'cd ' + destdir
		print >>f, 'setenv NP `wc -l ${PBS_NODEFILE} | cut -d\'/\' -f1`'


		dest = DBParams.dbparams['datadir'] + '/' + DBParams.dbparams['appname'] + '-' + DBParams.dbparams['expname'] + '-' + DBParams.dbparams['trialname'] + '-p' + node + 't' + tasks_per_node + 't2' + threads + 'i'+i

		if dataFormat == 'psrun':
			print >>f, 'setenv PS_HWPC_CONFIG ' + dest + '/events.xml'
			execmd = ccmd  + ' ' + execmd

		if MEParams.meparams['inputfiles']:
			for i in MEParams.meparams['inputfiles'].split():
				print >>f, 'ln -s ' + MEParams.meparams['inputdir'] + '/' + i + ' ' + dest + '/./' + i

		if MEParams.meparams['pmodel'] == 'mpi':
			print >>f,  MEParams.meparams['mpidir'] + ' -ssh  -np ${NP} -hostfile ${PBS_NODEFILE}' + ' ' + execmd
		else:	
			print >>f, execmd

	        print >>f, 'echo \'Job Completion time :\''		
		print >>f, 'date'

		f.close()
	
	def moveData(self, src, dest):
	
        	DataCollector = Collector()
        	dataFormat = DataCollector.getDataFormat()

        	if not os.path.exists(dest):
            		os.makedirs(dest)

        	if dataFormat == 'profiles':
            		moveCommand = 'mv ' + src + '/MULTI__P* ' + src + '/profile* ' + dest + '/'
        	elif dataFormat == 'psrun':	
           		moveCommand = 'mv ' + src + '/*.xml ' + dest + '/'
        	elif dataFormat == 'gprof':	
           		moveCommand = 'mv ' + src + '/gmon* ' + dest + '/'
		elif dataFormat == 'notimer':
		        moveCommand = ''
			
		if MEParams.meparams['DEBUG']=="1": 
        		print 'DEBUG:move performance data command: ', moveCommand
#       		commands.getstatusoutput(moveCommand)
                        os.popen(moveCommand)

	def runApp(self, perfCmd):
		
		for p in MEParams.meparams['nodes'].split():
			for t in MEParams.meparams['tasks_per_node'].split():
				for t2 in MEParams.meparams['threads'].split():
					for i in MEParams.meparams['input'].split():
						self.runit(p,t,t2,i)

	def runit(self,p,t,t2,i):

                cmd = MEParams.meparams['cmdline']

                if MEParams.meparams['DEBUG'] == "1":
                        print 'DEBUG: executing: ', cmd
                        print 'DEBUG: OMP_NUM_THREADS=', os.environ.get('OMP_NUM_THREADS')

                # Run the application in the specified directory                          
                if not os.path.exists(MEParams.meparams['workdir']): os.makedirs(MEParams.meparams['workdir'])
                try: os.chdir(MEParams.meparams['workdir'])
                except Exception,e:
                        print >> sys.stderr, 'Exception in ExperimentDriver:  '+str(e)
                dest = DBParams.dbparams['datadir'] + '/' + DBParams.dbparams['appname'] + '-' + DBParams.dbparams['expname'] + '-' + DBParams.dbparams['trialname'] + '-p' + p + 't' + t + 't2' + t2 + 'i'+i
                if not os.path.exists(dest): os.makedirs(dest)
                try: os.chdir(dest)
                except Exception,e:
                        print >> sys.stderr, 'Exception in ExperimentDriver:  '+str(e)

                if MEParams.meparams['exemode'] == "interactive":
                        app_output = os.popen(cmd)
                        fp = open("expout", "w")
                        print >>fp,  app_output.read()
                        fp.close()
                        if MEParams.meparams['DEBUG'] == "1":
                                print 'DEBUG: interactive command: ', cmd
                elif MEParams.meparams['exemode'] == "batch":
                        filename = MEParams.meparams['workdir'] + '/' + 'p'+ p + '-t' + t + 't2' + t2 + '.iforge'
                        self.genBatchScript(p, t, t2,i, filename, cmd, dest)
                        try: os.path.exists(filename)
                        except Exception,e:
                                print >> sys.stderr, 'Exception: Batch script does not exist  '+str(e)
                        mcmd = 'mv ' + MEParams.meparams['workdir'] + '/' + 'p'+ p + '-t' + t + 't2' + t2 + '.iforge ' + dest + '/'
                        commands.getstatusoutput(mcmd)
                        if MEParams.meparams['DEBUG'] == "1":
                                print 'DEBUG: move iforge files: ', mcmd

                        cmd = MEParams.meparams['batchcmd'] + ' ' + dest + '/' + 'p'+ p + '-t' + t + 't2' + t2 + '.iforge '
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

		if MEParams.meparams['pmodel'] == "omp":
			for p in MEParams.meparams['processes'].split():
				for t in MEParams.meparams['threads'].split():

					destdir = DBParams.dbparams['datadir'] + '/' + DBParams.dbparams['appname'] + '-' + DBParams.dbparams['expname'] + '-' + DBParams.dbparams['trialname'] + '-p' + p + 't' + t
					tn = DBParams.dbparams['trialname'] + '-p' + p + 't' + t
		                        #temporary fix

					# cpcmd = 'mv -f ' + datadir + '/' + appname + '-' + expname +'-' + tn + '/profile* ' + datadir + '/' + appname + '-' + expname + '-' + tn + '/MULTI*'
					# if DEBUG == 1:
					#	print 'copy profiles: ', cpcmd
					# commands.getstatusoutput(cpcmd)
					

					DB.load(destdir, tn,p,t)
		elif MEParams.meparams['pmodel'] == "mpi":	
			for n in MEParams.meparams['processes'].split():
				for t in MEParams.meparams['threads'].split():
					destdir = DBParams.dbparams['datadir'] + '/' + DBParams.dbparams['appname'] + '-' + DBParams.dbparams['expname'] + '-' + DBParams.dbparams['trialname'] + '-p' + n + 't' + t
					tn = DBParams.dbparams['trialname'] + '-p' + n + 't' + t
		                        #temporary fix
					cpcmd = 'cp ' + DBParams.dbparams['datadir'] + '/' + DBParams.dbparams['appname'] + '-' + DBParams.dbparams['expname'] + '-' + tn + '/profile* ' + DBParams.dbparams['datadir'] + '/' + DBParams.dbparams['appname'] + '-' + DBParams.dbparams['expname'] + '-' + tn + '/MULTI*'
					# if DEBUG == 1:
					#	print 'copy profiles: ', cpcmd

					commands.getstatusoutput(cpcmd)
					tn = DBParams.dbparams['trialname'] + '-p' + n + '-t' + t

					DB.load(destdir, tn, n,t)
					
	def validateModel(self, model):				
		

		params = []
		xdata = []
		ydata = []
		
		if MEParams.meparams['pmodel'] == "mpi":
			for n in MEParams.meparams['processes'].split():
				for t in MEParams.meparams['threads'].split():

					P = int(n) * int(t)
					params.insert(0,P)
					result = model.validate(params)
					xdata.append(P)
					ydata.append(result)

		return xdata, ydata			
