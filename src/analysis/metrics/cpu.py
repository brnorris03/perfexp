#!/usr/bin/python

from params import * 

from analysis.interfaces import AbstractMetric

import sys

class MFLIPS(AbstractMetric):

    def generate(self, analyzer=None):

        # The PerfExplorer script template
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
                fpins = 0
                totcyc = 0
                if event == '@PROGRAM_EVENT@':
                    print "metric: Wall Clock"
                    for p in range(node_count):

                        fpins += trial.getInclusive(p, event, "PAPI_FP_INS") * @SCALING_FACTOR@
                        totcyc += trial.getInclusive(p, event, "PAPI_TOT_CYC") * @SCALING_FACTOR@
                        fpins = fpins / node_count
                        totcyc =  totcyc / node_count
                        data[node_count-1] =  (fpins / (totcyc/@MHZ@))
                        outstr = ''.join([app,'_', expName, '["L2BW"] = ', str(data[node_count-1]), ''])

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
        buf.replace('@PROGRAM_EVENT@',programevent)
        buf.replace('@MHZ@',str(mhz))
        if analyzer:
            buf.replace('@SCALING_FACTOR@',analyzer.getScalingFactor())
        else:
            buf.replace('@SCALING_FACTOR@', '1')
            
        return buf
        
