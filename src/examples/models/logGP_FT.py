#!/usr/bin/python

from math import *
from params import * 
from analysis.interfaces import AbstractModel 

class LogGPFT(AbstractModel):

    def validate(self,params):

        tc = float(modelparams[0])
        N = int(modelparams[1])
        L = float(modelparams[2])
        o = float(modelparams[3])
        g = float(modelparams[4])
        G = float(modelparams[5])
        m = int(modelparams[6])

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
