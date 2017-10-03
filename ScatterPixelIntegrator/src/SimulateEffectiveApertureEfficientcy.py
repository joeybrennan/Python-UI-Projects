# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 11:53:47 2017

@author: Joe
"""
import numpy as np

def simulateEffectiveApertureEfficiency(wavelen,EOAX,EOAM,PAEX,PAEM,PW):
    EOAS = np.linspace(EOAM,EOAX,np.size(wavelen))
    PAES = np.linspace(PAEM,PAEX,np.size(wavelen))
    AppEff = []
    for EOAN,PAEN in zip(EOAS,PAES):
        AppEff.append(np.exp((PW**2)*(-0.5)*(1/(EOAN**2)))*PAEN)
        
    return AppEff