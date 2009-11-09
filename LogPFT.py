#!/usr/bin/python

from math import *
from params import * 
from PerfExplorer import *

class LogPFT:

    def validate(self, params):

        tc = float(modelparams[0])
        N = int(modelparams[1])
        L = float(modelparams[2])
        o = float(modelparams[3])
        g = int(modelparams[4])

        P = int(params[0])

        p = float(P/2)

        term1 = tc * N/P * log(N,2)
        term2 = 2 * (p - 1) * (L + o)
        term3 = 2 * (p - 2) * g

        time = term1 + term2 + term3

        return time


