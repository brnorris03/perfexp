#!/usr/bin/python

from params import * 
from analysis.interfaces import AbstractMetric

import sys

class WallClock(AbstractMetric):

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
                wallSum = 0
                if event == '@PROGRAM_EVENT@':
                    print "metric: Wall Clock"
                    for p in range(node_count):
'''

        if self.params['name']  == 'Time' or self.params['name'] == 'P_WALL_CLOCK_TIME':
            buf += '''        
                        wallClock = trial.getInclusive(p, event, '@METRIC@')
                        allSum += wallClock / 1000000
                        data[node_count] = wallSum / node_count
                        outstr = ''.join([app,'_', expName, '["WallClock"] = ', str(data[node_count]), ''])
'''
        elif self.params['name'] == 'PAPI_TOT_CYC':
            buf += '''
                        wallClock = trial.getInclusive(p, event, "PAPI_TOT_CYC")/@MHZ@
                        wallSum += wallClock
                        data[node_count] = wallSum / (node_count)
                        outstr = ''.join([app,'_', expName, '["WallClock"] = ', str(data[node_count]), ''])
'''
        buf += '''
    
                        print outstr
                        print '\\r\\r'

    generatePlot(data)

    return
'''
    
        # Specialize the template
        buf = buf.replace('@APPNAME@',appname)
        if pmodel == 'mpi':
            buf = buf.replace('@PROCS@','node_count')
        else:
            buf = buf.replace('@PROCS@','threads_per_context')
        buf = buf.replace('@PROGRAM_EVENT@',programevent)
        buf = buf.replace('@MHZ@',mhz)
            
        return buf        
