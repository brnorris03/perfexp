#!/usr/bin/python

from params import *
from analysis.metrics.time import WallClock
from analysis.interfaces import AbstractAnalyzer
from vis.tools.pylab import Plotter
import commands, sys, os, dircache

class Ltimer(AbstractAnalyzer):

    def runAnalysis(self, metric):

        ydata = []
	
	if pmodel == 'omp':
	    
	    for p in  nodes:
                for t in threads:
                    dirname = datadir + '/' + appname + '-' + expname + '-' + trialname + '-' + 'p' + p +'t' + t 
		    files = dircache.listdir(dirname)
                    for ff in files:
        		if ff.find('.err'):
                		break

                    filename = datadir + '/' + appname + '-' + expname + '-' + trialname + '-' + 'p' + p +'t' + t + '/' + ff
                    f = file(filename)
                    lines = f.read().split('\n')

                    lines[1] = lines[1].replace('Real','')
                    lines[1] = lines[1].replace(' ','')
                    ydata.append(str(float(lines[1])))


	else:
            for p in processes:
                for t in threads:
                    filename = datadir + '/' + appname + '-' + expname + '-' + trialname + '-' + 'p' + p +'t' + t + '/' + 'ltimer.out'
                    f = file(filename)
                    line =f.readline()
                    words = line.rsplit()
                    words[0] = words[0].replace('user','')
                    ydata.append(str(float(words[0])))

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




