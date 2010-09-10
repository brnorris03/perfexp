#!/usr/bin/python

import os, commands
from me.tools.tau import Collector as TAUCollector
from me.tools.gprof import Collector as GprofCollector
from me.tools.notimer import Collector as NoTimer
from storage.tools.gprof import Gprof 
from me.params import MEParams
from storage.params import DBParams

class Kraken:

	def genBatchScript(self, node, tasks_per_node, filename, execmd, destdir):
		
		f = open(filename, 'w')

		print >>f, '#!/bin/bash'
		print >>f, '#PBS -N ' + jobname
		print >>f, '#PBS -j oe'
		maxprocs = int(node) * int(tasks_per_node)
		print >>f, '#PBS -l walltime=' + walltime + ',size=' + maxprocs
		print >>f, '#PBS -A ' + accountname
		print >>f, 'date'
		print >>f, 'export MPICH_UNEX_BUFFER_SIZE=' + buffersize
		print >>f, 'export MPICH_MAX_SHORT_MSG_SIZE='+ msgsize
		if pmodel == 'omp' or pmodel == 'mpi:omp':
			print >>f, 'export OMP_NUM_THREADS=' + tasks_per_node
		print >>f, 'ulimit -c ' + stacksize
		print >>f, 'cd ' + workdir
		print >>f,  'aprun -n ' + str(maxprocs) + ' -N '+ tasks_per_node + ' ' + execmd
		print >>f, 'cp *.out *.err *.o* ' + destdir + '/' 

		f.close()
	
	def moveData(self, src, dest):
	
        	DataCollector = NoTimer()
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
       		commands.getstatusoutput(moveCommand)

	def runApp(self, perfCmd):

		if MEParams.meparams['pmodel'] == "omp":
			for p in MEParams.meparams['nodes'].split():
				for t in MEParams.meparams['threads'].split():
					self.runit(p,t)
		if MEParams.meparams['pmodel'] == "mpi": 
   			for p in MEParams.meparams['nodes'].split():
        			for t in MEParams.meparams['tasks_per_node'].split():
					self.runit(p,t)
		if MEParams.meparams['pmodel'] == "mpi:omp":	                
			for p in MEParams.meparams['nodes'].split():
				for t in MEParams.meparams['threads'].split():
					self.runit(p,t)

                if MEParams.meparams['pmodel'] == "serial":
                        self.runit(1,1)


	def runit(self,p,t):

       		cmd  = MEParams.meparams['cmdline'] 

		if MEParams.meparams['DEBUG'] == "1":
           		print 'DEBUG: executing: ', cmd
       			print 'DEBUG: OMP_NUM_THREADS=', os.environ.get('OMP_NUM_THREADS')

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
				
		if MEParams.meparams['exemode'] == "interactive":
       			app_output = os.popen(cmd)
			fp = open("expout", "w")
       			print >>fp,  app_output.read()
			fp.close()
			if MEParams.meparams['DEBUG'] == "1":
				print 'DEBUG: interactive command: ', cmd 
		elif MEParams.meparams['exemode'] == "batch":
			filename = MEParams.meparams['workdir'] + '/' + 'mpi-p'+ p + '-t' + t +'.pbs'
			self.genBatchScript(p, t, filename, cmd, dest)
			try: os.path.exists(filename)
               		except Exception,e:
       	        		print >> sys.stderr, 'Exception: Batch script does not exist  '+str(e)
			mcmd = 'mv ' + MEParams.meparams['workdir'] + '/' + 'mpi-p'+ p + '-t' + t + '.pbs ' + dest + '/'
			commands.getstatusoutput(mcmd)
			if MEParams.meparams['DEBUG'] == "1": 
				print 'DEBUG: move ll files: ', mcmd

			cmd = MEParams.meparams['batchcmd'] + ' ' + dest + '/' + 'mpi-p'+ p + '-t' + t + '.pbs ' 
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
			for p in MEParams.meparams['nodes'].split():
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
			for n in MEParams.meparams['nodes'].split():
				for t in MEParams.meparams['tasks_per_node'].split():
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
			for n in MEParams.meparams['nodes'].split():
				for t in MEParams.meparams['tasks_per_node'].split():

					P = int(n) * int(t)
					params.insert(0,P)
					result = model.validate(params)
					xdata.append(P)
					ydata.append(result)

		return xdata, ydata			
