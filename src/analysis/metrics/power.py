#!/usr/bin/python

from analysis.interfaces import AbstractMetric
from analysis.params import ANSParams
from storage.params import DBParams
from me.params import MEParams

import sys

class Power(AbstractMetric):

    def __init__(self, params={}):
        self.params = params
        if 'name' not in self.params.keys():
            self.params['name'] = 'Time'

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

            print '#', trialName

            for event in trial.getEvents():

                print 'event: ', event
                ops = 0
                cycles = 0
                l1tca = 0
                l2tca = 0
                power = 0
                if event == '@PROGRAM_EVENT@':
                    print "metric: power"
                    for p in range(node_count): 
                       ops += trial.getInclusive(p, event, "PAPI_TOT_INS")
                       cycles += trial.getInclusive(p, event, "PAPI_TOT_CYC")
                       l1tca += trial.getInclusive(p, event,"PAPI_L1_TCA")
                       l2tca += trial.getInclusive(p, event,"PAPI_L2_TCA")

                    ops = ops / node_count
                    cycles = cycles / node_count
                    l1tca = l1tca / node_count
                    l2tca = l2tca / node_count
                    power = (((ops / cycles) * .0459)  * 108.5) + (((l1tca/cycles) * .0017) * 108.5) + (((l2tca/cycles) * .0171) * 108.5) +  97.66
                    data[node_count] = power
                    outstr = ''.join([app,'_', expName, '["OPS"] = ', str(data[node_count]), ''])
'''
        buf += '''
    
                    print outstr
                    print '\\r\\r'

    generatePlot(data)

    return
'''
    
        # Specialize the template
        buf = buf.replace('@APPNAME@',DBParams.dbparams['appname'])
        if MEParams.meparams['pmodel'] == "mpi":
            buf = buf.replace('@PROCS@','node_count')
        else:
            buf = buf.replace('@PROCS@','threads_per_context')
        buf = buf.replace('@PROGRAM_EVENT@',ANSParams.ansparams['programevent'])
        buf = buf.replace('@MHZ@',ANSParams.ansparams['mhz'])
            
        return buf        
