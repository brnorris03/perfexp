#!/usr/bin/python

from math import *
from analysis.tools.tau import PerfExplorer 
from analysis.interfaces import AbstractModel 
from examples.models.params import RARMAParams

class RARMA(AbstractModel):
    '''Model for RandomAccess'''

    def __init__(self):
        pass
    
    def validate(self, params):
        

        tn = float(RARMAParams.modparams['tn'])
        tg = float(RARMAParams.modparams['tg'])
        tu = float(RARMAParams.modparams['tu'])
        tl = float(RARMAParams.modparams['tl'])
        ta = float(RARMAParams.modparams['ta'])
        m = float(RARMAParams.modparams['m'])
        tul = float(RARMAParams.modparams['tul'])

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

        if RARMAParams.modparams['DEBUG'] == "1":
            print 'GUPS: ', gups

        return gups


