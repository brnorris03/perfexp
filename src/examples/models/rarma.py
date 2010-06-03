#!/usr/bin/python

from math import *
from params import * 
from analysis.tools.tau import PerfExplorer 
from analysis.interfaces import AbstractModel 

class RARMA(AbstractModel):
    '''Model for RandomAccess'''

    def __init__(self):
        pass
    
    def validate(self, params):

        tn = float(modelparams[0])
        tg = float(modelparams[1])
        tu = float(modelparams[2])
        tl = float(modelparams[3])
        ta = float(modelparams[4])
        m = float(modelparams[5])
        tul = float(modelparams[6])

        P = int(params[0])

        if P == 0:
            remoteupdates = 0
            localupdates = numupdates
        else:
            remoteupdates = ((float)(P-2)/P) * tn
            localupdates = tn - remoteupdates

        if P == 2:
            remoteupdates = (1/4.0) * tn

        gups = (P *tn )/((tn *(tg + tu)) + (remoteupdates*(tl + (ta*m) + tul))) 

        if DEBUG == 1:
            print 'GUPS: ', gups

        return gups


