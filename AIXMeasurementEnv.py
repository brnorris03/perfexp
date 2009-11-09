#!/usr/bin/python

import os, commands
from params import *
from TAUCollector import *
from PerfDMFDB import *
from LogPFT import *

class AIXMeasurementEnv:

	def genBatchScript(self, node, tasks_per_node, filename, execmd, destdir):
		
		f = open(filename, 'w')

		print >>f, '#@ job_type = parallel'
		print >>f, '#@ environment = COPY_ALL'
		print >>f, '#@ class = medium'
		if pmodel == 'omp':
			tasks_per_node = 1
		print >>f, '#@ tasks_per_node = ' + str(tasks_per_node)
		print >>f, '#@ node = ' + str(node)
		print >>f, '#@ network.MPI_LAPI = sn_all,not_shared,US'
		print >>f, '#@ wall_clock_limit = 0:55:00'
		print >>f, '#@ output = $(host).$(jobid).$(stepid).out'
		print >>f, '#@ error = $(host).$(jobid).$(stepid).err'
		print >>f, '#@ queue'
		print >>f,  execmd
		print >>f, 'cp *.out *.err ' + destdir + '/' 

		f.close()
	
	def moveData(self, src, dest):
	
        	DataCollector = TAUCollector()
        	dataFormat = DataCollector.getDataFormat()

        	if not os.path.exists(dest):
            		os.makedirs(dest)

        	if dataFormat == 'profiles':
            		moveCommand = 'mv ' + src + '/MULTI__P* ' + src + '/profile* ' + dest + '/'
        	elif dataFormat == 'psrun':	
           		moveCommand = 'mv ' + src + '/*.xml ' + dest + '/'

		if DEBUG==1: 
        		print 'DEBUG:move performance data command: ', moveCommand
       		commands.getstatusoutput(moveCommand)

	def runApp(self, perfCmd):

		if pmodel == 'omp':
			for p in nodes:
				for t in threads:
					os.environ['OMP_NUM_THREADS'] = t
					self.runit(p,t)
		if pmodel == 'mpi': 
   			for p,o in map(None, nodes, cmdlineopts):
        			for t in tasks_per_node:
					self.runit(p,t,o)
                			

	def runit(self,p,t,o):

		if o != None:				
      			cmd = cmdline + ' ' + o
		else:
			cmd = cmdline

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

        
	def loadTrials(self):
		
		DB = PerfDMFDB()

		if pmodel == 'omp':
			for p in nodes:
				for t in threads:

					destdir = datadir + '/' + appname + '-' + expname + '-' + trialname + '-p' + p + 't' + t
					tn = trialname + '-p' + p + 't' + t
		                        #temporary fix

					cpcmd = 'mv -f ' + datadir + '/' + appname + '-' + expname +'-' + tn + '/profile* ' + datadir + '/' + appname + '-' + expname + '-' + tn + '/MULTI*'
					if DEBUG == 1:
						print 'copy profiles: ', cpcmd
					commands.getstatusoutput(cpcmd)
					

					DB.load(destdir, tn)
		elif pmodel == 'mpi':	
			for n in nodes:
				for t in tasks_per_node:
					destdir = datadir + '/' + appname + '-' + expname + '-' + trialname + '-p' + n + 't' + t
					tn = trialname + '-p' + n + 't' + t
		                        #temporary fix
					cpcmd = 'cp ' + datadir + '/' + appname + '-' + expname + '-' + tn + '/profile* ' + datadir + '/' + appname + '-' + expname + '-' + tn + '/MULTI*'
					if DEBUG == 1:
						print 'copy profiles: ', cpcmd

					commands.getstatusoutput(cpcmd)
		

					DB.load(destdir, tn)
	def validateModel(self):				

		model = LogPFT()
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
