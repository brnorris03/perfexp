#!/usr/bin/python

from params import *
from analysis.metrics.time import WallClock
from analysis.interfaces import AbstractAnalyzer
from vis.tools.pylab import Plotter
import commands, sys, os

class Hpcc(AbstractAnalyzer):

    def runAnalysis(self, metric):

        ydata = []

	if nodes and tasks_per_node:
	    for p in nodes:
                for t in tasks_per_node:
                    filename = datadir + '/' + appname + '-' + expname + '-' + trialname + '-' + 'p' + p +'t' + t + '/' + 'hpccoutf.txt'
                    f = file(filename)
                    for line in f:
#                        if 'Real' in line:
                        if 'Billion(10^9)' in line:
                            break
                    words = line.split()
#   	            i = words.index('seconds')
#		    avgtime = float(words[i-1])	
                    avgtime = float(words[0]) * 1e9
                    ydata.append(str(avgtime))

	else:
            for p in processes:
                for t in threads:
                    filename = datadir + '/' + appname + '-' + expname + '-' + trialname + '-' + 'p' + p +'t' + t + '/' + 'gprof.out'
                    f = file(filename)
                    for line in f:
                        if 'sample hit' in line:
                            break
                    words = line.split()
                    i = words.index('seconds')
                    ydata.append(str(float(words[i-1])))

        self.writeGeneratePlot(ydata)
                 
    def writeGeneratePlot(self, ydata):

        xdata = []
        plotter = Plotter()

        if pmodel == 'mpi':
	    if nodes:
                for n in nodes:
                    P = n
                    xdata.append(P)

            else:	
                for n in processes:
                    P = n
                    xdata.append(P)
        elif pmodel == 'omp':
            for n in threads:
                T=n
                xdata.append(T)

        plotter.genPlot(xdata, ydata)

        cmd = 'chmod u+x ' + plotfilename 
        commands.getstatusoutput(cmd)
        moveResultsCommand = 'mv ' + os.getcwd() + '/'+ plotfilename + ' ' + resultsdir
        commands.getstatusoutput(moveResultsCommand)




