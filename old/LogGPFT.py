#!/usr/bin/python

from math import *
from params import * 

class LogGPFT:

    def validate(self,params):

        tc = float(modelparams[0])
        N = int(modelparams[1])
        L = float(modelparams[2])
        o = float(modelparams[3])
        g = int(modelparams[4])
        G = int(modelparams[5])

        P = int(params[0])        
        n = float(N/3)

        term1 = tc * n/P * log(n,2)
        term2 = ((P-1) * o) + (tc * n * n * log(n,2))
        term3 = ((P-1) * g) + (n * n * G) + L
        term4 = o + (n/P -1) * max(term2, term3)
        term5 = (P - 1) * o
        term6 = (P - 2) * g
        term7 = n/P * n * G
        term8 = term1 + term4 + term5 + term6 + term7 + L
        term9 = tc * ((n*n)/(P))*n*log(n,2)*2        

        time = term8 + term9

        if DEBUG == 1:
            print 'Time: ', time

        return time
