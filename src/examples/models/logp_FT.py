#!/usr/bin/python

from math import *
from analysis.tools.tau import PerfExplorer 
from analysis.interfaces import AbstractModel 
from examples.models.params import FTParams

class FT(AbstractModel):
    '''LogP model for FT'''

    def __init__(self):
        pass
    
    def validate(self, params):

        tc = float(FTParams.modparams['tc'])
        N = int(FTParams.modparams['N'])
        L = float(FTParams.modparams['L'])
        o = float(FTParams.modparams['o'])
        g = float(FTParams.modparams['g'])
        m = int(FTParams.modparams['m'])

        P = int(params[0])

# xeon specific
#        if P > 4:
#            tc = tc * 2

        term1 = tc * N/P * log(N,2)
        term2 = (P - 1) * (L + o)
        term3 = (P - 2) * m * g

        time = term1 + term2 + term3

        if DEBUG == 1:
            print 'Time: ', time

        return time


