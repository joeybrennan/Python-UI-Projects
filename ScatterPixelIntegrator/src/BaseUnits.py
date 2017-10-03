'''
Created on 26 Jul 2017

@author: Joe
'''
import numpy as np
from __init__ import ureg,Q_

def baseUnits(a):
    if isinstance(a,(list,np.ndarray)):
        out = []
        for an in a:
            out.append(an.to_base_units().magnitude)
        return out
    else:
        return (a.to_base_units().magnitude)
