#!/usr/bin/python

import os, commands
from me.tools.tau import Collector as TAUCollector
from me.tools.gprof import Collector as GprofCollector
from me.tools.notimer import Collector as NoTimer
from storage.tools.gprof import Gprof 

class Kraken:

	def genBatchScript(self, node, tasks_per_node, filename, execmd, destdir):
		
		f = open(filename, 'w')

		print >>f, '#!/bin/bash'
		print >>f, '#PBS -N ' + jobname
		print >>f, '#PBS -j oe'
		maxprocs = int(node) * int(tasks_per_node)
		print >>f, '#PBS -l walltime=' + walltime + ',size=' + str(maxprocs)
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
			
		if DEBUG==1: 
        		print 'DEBUG:move performance data command: ', moveCommand
       		commands.getstatusoutput(moveCommand)

	def runApp(self, perfCmd):

		if pmodel == 'omp':
			for p in nodes:
				for t in threads:
					self.runit(p,t)
		if pmodel == 'mpi': 
   			for p in nodes:
        			for t in tasks_per_node:
					self.runit(p,t)
		if pmodel == 'mpi:omp':	                
			for p in nodes:
				for t in threads:
					self.runit(p,t)

	def runit(self,p,t):

       		cmd  = cmdline 

		if DEBUG == 1:
           		print 'DEBUG: executing: ', cmd
       			print 'DEBUG: OMP_NUM_THREADS=', os.environ.get('OMP_NUM_THREADS')

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
				
		if exemode == 'interactive':
       			app_output = os.popen(cmd)
			fp = open("expout", "w")
       			print >>fp,  app_output.read()
			fp.close()
			if DEBUG == 1:
				print 'DEBUG: interactive command: ', cmd 
		elif exemode == 'batch':
			filename = workdir + '/' + 'mpi-p'+ str(p) + '-t' + str(t) +'.pbs'
			self.genBatchScript(p, t, filename, cmd, dest)
			try: os.path.exists(filename)
               		except Exception,e:
       	        		print >> sys.stderr, 'Exception: Batch script does not exist  '+str(e)
			mcmd = 'mv ' + workdir + '/' + 'mpi-p'+ str(p) + '-t' + str(t) + '.pbs ' + dest + '/'
			commands.getstatusoutput(mcmd)
			if DEBUG == 1: 
				print 'DEBUG: move ll files: ', mcmd

			cmd = batchcmd + ' ' + dest + '/' + 'mpi-p'+ str(p) + '-t' + str(t) + '.pbs ' 
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

		if pmodel == 'omp':
			for p in nodes:
				for t in threads:

					destdir = datadir + '/' + appname + '-' + expname + '-' + trialname + '-p' + p + 't' + t
					tn = trialname + '-p' + p + 't' + t
		                        #temporary fix

					# cpcmd = 'mv -f ' + datadir + '/' + appname + '-' + expname +'-' + tn + '/profile* ' + datadir + '/' + appname + '-' + expname + '-' + tn + '/MULTI*'
					# if DEBUG == 1:
					#	print 'copy profiles: ', cpcmd
					# commands.getstatusoutput(cpcmd)
					

					DB.load(destdir, tn,p,t)
		elif pmodel == 'mpi':	
			for n in nodes:
				for t in tasks_per_node:
					destdir = datadir + '/' + appname + '-' + expname + '-' + trialname + '-p' + n + 't' + t
					tn = trialname + '-p' + n + 't' + t
		                        #temporary fix
					cpcmd = 'cp ' + datadir + '/' + appname + '-' + expname + '-' + tn + '/profile* ' + datadir + '/' + appname + '-' + expname + '-' + tn + '/MULTI*'
					# if DEBUG == 1:
					#	print 'copy profiles: ', cpcmd

					commands.getstatusoutput(cpcmd)
					tn = trialname + '-p' + n + '-t' + t

					DB.load(destdir, tn, n,t)
					
	def validateModel(self, model):				
		

		params = []
		xdata = []
		ydata = []
		
		if pmodel == 'mpi':
			for n in nodes:
				for t in tasks_per_node:

					P = int(n) * int(t)
					params.insert(0,P)
					result = model.validate(params)
					xdata.append(P)
					ydata.append(result)

		return xdata, ydata			
