#!/usr/bin/python

import os, commands
from me.tools.hpctoolkit import Collector 
from storage.tools.hpctoolkit import HPCToolkitDB 
from me.params import MEParams
from storage.params import DBParams

class iForge:
	def __init__(self):
		self.env = ''

	def genBatchScript(self, node, tasks_per_node, threads, i,filename, execmd, destdir):

		DataCollector = Collector()
                dataFormat = DataCollector.getDataFormat()
		ccmd = DataCollector.getCommand()
		options = DataCollector.setCounters()

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

		dest = MEParams.meparams['workdir'] + '/' + DBParams.dbparams['appname'] + '-' + DBParams.dbparams['expname'] + '-' + DBParams.dbparams['trialname'] + '-p' + node + 't' + tasks_per_node + 't2' + threads + 'i'+i

		if dataFormat == 'psrun':
			execmd = ccmd  + ' ' + execmd
			if MEParams.meparams['counters']:
				DataCollector.setCounters()
				print >>f, 'setenv PS_HWPC_CONFIG ' + dest + '/events.xml'
				self.env += 'PS_HWPC_CONFIG=' + dest + '/events.xml '
		elif dataFormat == 'hpcstruct':
			execmd = ccmd + ' ' + options + ' ' + execmd 

                print >>f, 'cd ' +  dest

                if MEParams.meparams['inputfiles']:
                        for i in MEParams.meparams['inputfiles'].split():
                                print >>f, 'cp ' + MEParams.meparams['inputdir'] + '/' + i + ' ' + dest

                print >>f, 'cp ' + MEParams.meparams['execdir'] + '/' + MEParams.meparams['exec'] + ' ' + dest

                print >>f, 'wait'

		if dataFormat == 'hpcstruct':
			print >>f, dataFormat + ' ./' + MEParams.meparams['exec']

		if MEParams.meparams['pmodel'] == 'mpi':
			if MEParams.meparams['mpicmd'] == 'mpirun_rsh':
				print >>f,  MEParams.meparams['mpidir'] + '/' + MEParams.meparams['mpicmd'] + ' -ssh  -np ${NP} -hostfile ${PBS_NODEFILE}' + ' ' + self.env + execmd
			elif MEParams.meparams['mpicmd'] == 'mpiexec':
				print >>f, MEParams.meparams['mpidir'] + ' -n ${NP} -f ${PBS_NODEFILE}' + ' ' +  execmd        
		else:	
			print >>f, execmd

	        print >>f, 'echo \'Job Completion time :\''		
		print >>f, 'date'

		f.close()
	
	def runApp(self):
		
		for p in MEParams.meparams['nodes'].split():
			for t in MEParams.meparams['tasks_per_node'].split():
				for t2 in MEParams.meparams['threads'].split():
					for i in MEParams.meparams['input'].split():
						self.runit(p,t,t2,i)

	def runit(self,p,t,t2,i):

                cmd = MEParams.meparams['exec']

                if MEParams.meparams['DEBUG'] == "1":
                        print 'DEBUG: executing: ', cmd
                        print 'DEBUG: OMP_NUM_THREADS=', os.environ.get('OMP_NUM_THREADS')

                # Run the application in the specified directory                          
                if not os.path.exists(MEParams.meparams['workdir']): os.makedirs(MEParams.meparams['workdir'])
                try: os.chdir(MEParams.meparams['workdir'])
                except Exception,e:
                        print >> sys.stderr, 'Exception in ExperimentDriver:  '+str(e)
                dest = MEParams.meparams['workdir'] + '/' + DBParams.dbparams['appname'] + '-' + DBParams.dbparams['expname'] + '-' + DBParams.dbparams['trialname'] + '-p' + p + 't' + t + 't2' + t2 + 'i'+i
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

			if MEParams.meparams['run'] == "yes":	
				app_output = os.popen(cmd)
				fp = open("expout", "w")
				print >>fp,  app_output.read()
				fp.close()

        
	def loadTrials(self, storage):
		
		#DB = PerfDMFDB()
		DB = storage

		if MEParams.meparams['pmodel'] == "omp":
			for p in MEParams.meparams['processes'].split():
				for t in MEParams.meparams['threads'].split():

					destdir = MEParams.dbparams['workdir'] + '/' + DBParams.dbparams['appname'] + '-' + DBParams.dbparams['expname'] + '-' + DBParams.dbparams['trialname'] + '-p' + p + 't' + t
					tn = DBParams.dbparams['trialname'] + '-p' + p + 't' + t
					DB.load(destdir, tn)

		elif MEParams.meparams['pmodel'] == "mpi":	
			for p in MEParams.meparams['nodes'].split():
				for t in MEParams.meparams['tasks_per_node'].split():
					for t2 in MEParams.meparams['threads'].split():
						for i in MEParams.meparams['input'].split():
							destdir = MEParams.meparams['workdir'] + '/' + DBParams.dbparams['appname'] + '-' + DBParams.dbparams['expname'] + '-' + DBParams.dbparams['trialname'] + '-p' + p + 't' + t + 't2' + t2 + 'i'+i
					
							tn = DBParams.dbparams['trialname'] + '-p' + p + 't' + t + 't2'+ t2 + 'i'+i

							DB.load(destdir, tn)
					
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
