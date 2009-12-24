#!/usr/bin/python

from math import *
from params import * 
from analysis.tools.tau import PerfExplorer 
from analysis.interfaces import AbstractModel 

class FT(AbstractModel):
    '''LogP model for FT'''

    def __init__(self):
        pass
    
    def validate(self, params):

        tc = float(modelparams[0])
        N = int(modelparams[1])
        L = float(modelparams[2])
        o = float(modelparams[3])
        g = float(modelparams[4])
        m = int(modelparams[5])

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


