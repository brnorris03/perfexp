#!/usr/bin/python

from analysis.interfaces import AbstractMetric
from analysis.params import ANSParams
from storage.params import DBParams
from me.params import MEParams

import sys

class FLOPS(AbstractMetric):

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
                fpops = 0
                cycles = 0
                flop = 0
                if event == '@PROGRAM_EVENT@':
                    print "metric: Flop"
                    for p in range(node_count): 
                       fpops += trial.getInclusive(p, event, "PAPI_FP_OPS")
                       cycles += trial.getInclusive(p, event, "PAPI_TOT_CYC")
                    fpops = fpops/node_count
                    cycles = cycles / node_count
                    flop = (fpops / cycles) * @MHZ@ 
                    data[node_count] = flop
                    outstr = ''.join([app,'_', expName, '["FLOPS"] = ', str(data[node_count]), ''])
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
        buf = buf.replace('@PROGRAM_EVENT@', ANSParams.ansparams['programevent'])
        buf = buf.replace('@MHZ@',ANSParams.ansparams['mhz'])
            
        return buf        
