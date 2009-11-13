#!/usr/bin/python

from params import * 

import sys

class FLIPSIneff:

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
    else:
      print >>f, '\t\t\tnode_count = int(tr.getField("threads_per_context"))'
    print >>f, '\t\t\tprint \'#\', trialName'

    print >>f, '\t\t\tfor event in trial.getEvents():'

    print >>f, '\t\t\t\tprint \'event: \', event'
    print >>f, '\t\t\t\tgstalls = 0'
    print >>f, '\t\t\t\tfpineff = 0'
    print >>f, '\t\t\t\tif event == \'' + programevent + '\':'
    print >>f, '\t\t\t\t\tprint "metric: Wall Clock"'

    print >>f, '\t\t\t\t\tderived, GlobalStalls = deriveMetric(extracted, "PAPI_RES_STL", "PAPI_TOT_CYC", DeriveMetricOperation.DIVIDE)'
    print >>f, '\t\t\t\t\tderived2, FpIns = deriveMetric(extracted, "PAPI_FP_INS", "PAPI_TOT_INS", DeriveMetricOperation.DIVIDE)'

    print >>f, '\t\t\t\t\tfor p in range(node_count):'

    if ptool == 'tau':
      print >>f, '\t\t\t\t\t\tgstalls += derived.getInclusive(p, event, GlobalStalls) / 1e6'
      print >>f, '\t\t\t\t\t\tfpineff += derived2.getInclusive(p, event, FpIns) / 1e6'
      print >>f, '\t\t\t\t\tgstalls = gstalls / (node_count)'
      print >>f, '\t\t\t\t\tfpineff =  fpineff / (node_count)'
      print >>f, '\t\t\t\t\tdata[node_count] =  gstalls * fpineff'
      print >>f, '\t\t\t\t\toutstr = \'\'.join([app,\'_\', expName, \'["FLIPSIneff"] = \', str(data[node_count]), \'\'])'
    elif ptool == 'perfsuite':
      print >>f, '\t\t\t\t\t\tgstalls += derived.getInclusive(p, event, GlobalStalls)'
      print >>f, '\t\t\t\t\t\tfpineff += derived2.getInclusive(p, event, FpIns)'
      print >>f, '\t\t\t\t\tgstalls = gstalls / (node_count - 1)'
      print >>f, '\t\t\t\t\tfpineff =  fpineff / (node_count - 1)'
      print >>f, '\t\t\t\t\tdata[node_count-1] =  gstalls * fpineff'
      print >>f, '\t\t\t\t\toutstr = \'\'.join([app,\'_\', expName, \'["FLIPSIneff"] = \', str(data[node_count-1]), \'\'])'

    print >>f, '\t\t\t\t\tprint outstr'

    print >>f, '\t\t\t\t\tprint \'\\r\\r\''

    print >>f, '\tgeneratePlot(data)'

    print >>f, '\treturn\n'
