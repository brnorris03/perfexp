#!/usr/bin/python

from params import * 
from analysis.interfaces import AbstractMetric

import sys

class L2BW(AbstractMetric):

  def generate(self, f):

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
    else:
      print >>f, '\t\t\tnode_count = int(tr.getField("threads_per_context"))'
    print >>f, '\t\t\tprint \'#\', trialName'

    print >>f, '\t\t\tfor event in trial.getEvents():'

    print >>f, '\t\t\t\tprint \'event: \', event'
    print >>f, '\t\t\t\tl2miss = 0'
    print >>f, '\t\t\t\ttotcyc = 0'
    print >>f, '\t\t\t\tif event == \'' + programevent + '\':'
    print >>f, '\t\t\t\t\tprint "metric: Wall Clock"'
    print >>f, '\t\t\t\t\tfor p in range(node_count):'

    if ptool == 'tau':
      print >>f, '\t\t\t\t\t\tl2miss += trial.getInclusive(p, event, "PAPI_L2_TCM") / 1e6'
      print >>f, '\t\t\t\t\t\ttotcyc += trial.getInclusive(p, event, "PAPI_TOT_CYC") / 1e6'
      print >>f, '\t\t\t\t\tl2miss =  l2miss / (node_count)'
      print >>f, '\t\t\t\t\ttotcyc =  totcyc / (node_count)'
      print >>f, '\t\t\t\t\tdata[node_count] =  (((l2miss * ', l2cacheline, ') / totcyc) * ', mhz, ')'
      print >>f, '\t\t\t\t\toutstr = \'\'.join([app,\'_\', expName, \'["L2BW"] = \', str(data[node_count]), \'\'])'
    elif ptool == 'perfsuite':
      print >>f, '\t\t\t\t\t\tl2miss += trial.getInclusive(p, event, "PAPI_L2_TCM")'
      print >>f, '\t\t\t\t\t\ttotcyc += trial.getInclusive(p, event, "PAPI_TOT_CYC")'
      print >>f, '\t\t\t\t\tl2miss =  l2miss / (node_count - 1)'
      print >>f, '\t\t\t\t\ttotcyc =  totcyc / (node_count - 1)'
      print >>f, '\t\t\t\t\tdata[node_count-1] =  (((l2miss * ', l2cacheline, ') / totcyc) * ', mhz, ')'
      print >>f, '\t\t\t\t\toutstr = \'\'.join([app,\'_\', expName, \'["L2BW"] = \', str(data[node_count-1]), \'\'])'

    print >>f, '\t\t\t\t\tprint outstr'

    print >>f, '\t\t\t\t\tprint \'\\r\\r\''

    print >>f, '\tgeneratePlot(data)'

    print >>f, '\treturn\n'
