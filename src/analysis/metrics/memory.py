#!/usr/bin/python

from params import * 
from analysis.interfaces import AbstractMetric

import sys

class L2BW(AbstractMetric):

    def generate(self, analyzer=None):
        buf = '''
def glue():

    app = '@APPNAME@'
    
    getParameters()
    experiments = loadExperiments(app)
    print 'Found ', len(experiments), 'experiments.'
    data = {}

    for exp in experiments:
        # load trials

        expName = exp.getName()

        trials = Utilities.getTrialsForExperiment(app, expName)
        totalTrials = trials.size()
        print '\\rLoaded ', totalTrials, 'trials'

        for tr in trials:
            trial = TrialResult(tr)
            trialName = trial.getName()
            trialNamePieces = trialName.split('_')
            print '\\rLooking at trial ', trialName

            extractor = ExtractNonCallpathEventOperation(trial)
            extracted = extractor.processData().get(0)
            node_count = int(tr.getField('@PROCS@'))
'''
        if ptool.lower() == 'perfsuite': 
            buf += '''
            node_count -= 1
            '''
        buf += '''
            print '#', trialName

            for event in trial.getEvents():

                print 'event: ', event
                l2miss = 0
                ttotcyc = 0
                if event == '@PROGRAM_EVENT@':
                    print "metric: Wall Clock"
                    for p in range(node_count):

                        l2miss += trial.getInclusive(p, event, "PAPI_L2_TCM") * @SCALING_FACTOR@
                        totcyc += trial.getInclusive(p, event, "PAPI_TOT_CYC") * @SCALING_FACTOR@
                        l2miss =  l2miss / (node_count)
                        ttotcyc =  totcyc / (node_count)
                        data[node_count] =  (((l2miss * @L2_CACHELINE@) / totcyc) * @MHZ@)
                        outstr = ''.join([app,'_', expName, '["L2BW"] = ', str(data[node_count]), ''])

                        print outstr
                        print '\\r\\r'

    generatePlot(data)

    return
'''
        # Specialize the template
        buf.replace('@APPNAME@',appname)
        if pmodel == 'mpi':
            buf.replace('@PROCS@','node_count')
        else:
            buf.replace('@PROCS@','threads_per_context')
        buf.replace('@PROGRAM_EVENT@', programevent)
        buf.replace('@L2_CACHELINE@', l2cacheline)
        buf.replace('@MHZ@',mhz)
        if analyzer:
            buf.replace('@SCALING_FACTOR@',analyzer.getScalingFactor())
        else:
            buf.replace('@SCALING_FACTOR@', '1')
            
        return buf
        