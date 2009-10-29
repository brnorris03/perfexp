#!/usr/bin/python

import os, commands
from params import *
from TAUCollector import *
from PerfDMFDB import *

class XeonMeasurementEnv:

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

		DataCollector = TAUCollector()
		DataCollector.setCounters()
		cmd = ''

		for p in processes:
        		for t in threads:

				if pmodel == 'omp' or pmodel == 'mpi:omp':
                			os.environ['OMP_NUM_THREADS'] = t
					cmd = cmdline
				elif pmodel == 'mpi':
					cmd = mpidir + '/mpirun -np ' + p + ' ' + cmdline 
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

		for p in processes:
			for t in threads:
				destdir = datadir + '/' + appname + '-' + expname + '-' + trialname + '-p' + p + 't' + t
				tn = trialname + '-p' + p + '-t' + t
				DB.load(destdir, tn)

