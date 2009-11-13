#!/usr/bin/python

from params import * 

import sys

class WallClock:

  def writeMetricMethod(self, f):

    print >>f, 'def glue():'

    #parameter: app name                                                    
    print >>f, '\tapp = \'' + appname + '\''

    print >>f, '\tgetParameters()'
    print >>f, '\texperiments = loadExperiments(app)'
    print >>f, '\tprint \'Found \', len(experiments), \'experiments.\''
    print >>f, '\tdata = {}'

    print >>f, '\tfor exp in experiments:'
    print >>f, '\t\t# load trials'

    print >>f, '\t\texpName = exp.getName()'

    print >>f, '\t\ttrials = Utilities.getTrialsForExperiment(app, expName)'
    print >>f, '\t\ttotalTrials = trials.size()'
    print >>f, '\t\tprint \'\\rLoaded \', totalTrials, \'trials\''

    print >>f, '\t\tfor tr in trials:'
    print >>f, '\t\t\ttrial = TrialResult(tr)'
    print >>f, '\t\t\ttrialName = trial.getName()'
    print >>f, '\t\t\ttrialNamePieces = trialName.split(\'_\')'
    print >>f, '\t\t\tprint \'\\rLooking at trial \', trialName'

    print >>f, '\t\t\textractor = ExtractNonCallpathEventOperation(trial)'
    print >>f, '\t\t\textracted = extractor.processData().get(0)'

    if pmodel == 'mpi': 
      print >>f, '\t\t\tnode_count = int(tr.getField("node_count"))'
    elif pmodel == 'omp':
      print >>f, '\t\t\tnode_count = int(tr.getField("threads_per_context"))'
    print >>f, '\t\t\tprint \'#\', trialName'

    print >>f, '\t\t\tfor event in trial.getEvents():'

    print >>f, '\t\t\t\tprint \'event: \', event'
    print >>f, '\t\t\t\twallSum = 0'
    print >>f, '\t\t\t\tif event == \'' + programevent + '\':'
    print >>f, '\t\t\t\t\tprint "metric: Wall Clock"'
    print >>f, '\t\t\t\t\tfor p in range(node_count):'

    if metric  == 'Time' or metric == 'P_WALL_CLOCK_TIME':
      print >>f, '\t\t\t\t\t\twallClock = trial.getInclusive(p, event, \''+ metric + '\')'
      print >>f, '\t\t\t\t\t\twallSum += wallClock / 1000000'
      print >>f, '\t\t\t\t\tdata[node_count] = wallSum / node_count'
      print >>f, '\t\t\t\t\toutstr = \'\'.join([app,\'_\', expName, \'["WallClock"] = \', str(data[node_count]), \'\'])'
    elif metric == 'PAPI_TOT_CYC':
      print >>f, '\t\t\t\t\t\twallClock = trial.getInclusive(p, event, "PAPI_TOT_CYC")/' + mhz 
      print >>f, '\t\t\t\t\t\twallSum += wallClock'
      print >>f, '\t\t\t\t\tdata[node_count] = wallSum / (node_count)'
      print >>f, '\t\t\t\t\toutstr = \'\'.join([app,\'_\', expName, \'["WallClock"] = \', str(data[node_count]), \'\'])'


    print >>f, '\t\t\t\t\tprint outstr'

    print >>f, '\t\t\t\t\tprint \'\\r\\r\''

    print >>f, '\tgeneratePlot(data)'

    print >>f, '\treturn\n'
