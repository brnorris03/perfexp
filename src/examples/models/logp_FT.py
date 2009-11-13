#!/usr/bin/python

from math import *
from params import * 
from perfexp.analysis.tools.tau import PerfExplorer 
from perfexp.analysis.model import AbstractModel 

class FT(AbstractModel):
    '''LogP model for FT'''

    def __init__(self):
        pass
    
    def validate(self, params):

        tc = float(modelparams[0])
        N = int(modelparams[1])
        L = float(modelparams[2])
        o = float(modelparams[3])
        g = int(modelparams[4])

        P = int(params[0])

        term1 = tc * N/P * log(N,2)
        term2 = (P - 1) * (L + o)
        term3 = (P - 2) * g

        time = term1 + term2 + term3

        return time


