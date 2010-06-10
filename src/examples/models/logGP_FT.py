#!/usr/bin/python

from math import *
from analysis.interfaces import AbstractModel 
from examples.models.params import LogGPFTParams

class LogGPFT(AbstractModel):

    def validate(self,params):

        tc = float(LogGPFTParams.modparams['tc'])
        N = int(LogGPFTParams.modparams['N'])
        L = float(LogGPFTParams.modparams['L'])
        o = float(LogGPFTParams.modparams['o'])
        g = float(LogGPFTParams.modparams['g'])
        G = float(LogGPFTParams.modparams['G'])
        m = int(LogGPFTParams.modparams['m'])

        P = int(params[0])        
 
# xeon specific       
#        if tc > 4:
#            tc = tc * 2

        term1 = tc * N/P * N * log(N,2)
        term2 = ((P-1) * o) + (tc * N/P * N * log(N,2))
        term3 = ((P-1) * m * g) + (m * N/P * G) + L
        term4 = o + (N/P -1) * max(term2, term3)
        term5 = (P - 1) * o
        term6 = (P - 2) * g * m
        term7 = N/P * G * m
        term8 = term1 + term4 + term5 + term6 + term7 + L
        term9 = tc * ((N/P))*N*log(N,2)        

        time = term8 + term9

        if DEBUG == 1:
            print 'Time: ', time

        return time
