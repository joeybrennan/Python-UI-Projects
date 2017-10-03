# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 11:58:01 2017

This program pasrse the Modal data for each mode and angle

returns: modelist, Pw angles, Azi angles, Mode Amps

@author: Joe
"""
import pandas as pd
import numpy as np
import os

def loadModalData(indexFileName,scanFileNameTemplate,folder):
    indexFilepath = os.path.join(folder,indexFileName)
    angleResolvedFileIndex,inclinationAngles,azimuthalAngles = loadIndexFile(indexFilepath)
    amps,modeList = loadScanFiles(scanFileNameTemplate,folder,angleResolvedFileIndex,inclinationAngles,azimuthalAngles)
    
    return amps,modeList,inclinationAngles,azimuthalAngles
    

def loadIndexFile(path):
    data = pd.read_csv(path,delimiter='\t',skiprows= 1)
    
    inclinationAngles = np.unique(data.PWdeg)
    azimuthalAngles = np.unique(data.AZIdeg)
    SDI = data.INDEX.astype(np.int)

    ##row - different inclination , column - different azimuthals
    angleResolvedFileIndex = SDI.reshape(len(inclinationAngles),len(azimuthalAngles))
    return angleResolvedFileIndex,inclinationAngles,azimuthalAngles

def loadScanFiles(scanFileNameTemplate,folder,angleResolvedFileIndex,inclinationAngles,azimuthalAngles):
    ## Read the first file and extract number of modes and modes from it 
    index = angleResolvedFileIndex[0,0]
    scanfilePath = os.path.join(folder,scanFileNameTemplate %(index))
    data = pd.read_csv(scanfilePath,delimiter='\t',skiprows=(1,1))

    ##Complie list of modes
    modes = [Mode(Type,nn,mm)for Type, nn , mm , magAn,argAn in zip(data.type,data.m,data.n,data.magA,data.argA)]

    amps = np.empty(angleResolvedFileIndex.shape + (len(modes), ), dtype=np.complex)

    for incIndx, _ in enumerate(inclinationAngles):
        for azimIdx, _ in enumerate(azimuthalAngles):
            scanfilePath = os.path.join(folder,scanFileNameTemplate %(angleResolvedFileIndex[incIndx,azimIdx]))
            data = pd.read_csv(scanfilePath,delimiter='\t',skiprows=(1,1))

            amps[incIndx, azimIdx,:] = data.magA * np.exp(1j*data.argA)

    return amps, modes
           
class Mode(object):
    Type = ""
    n = 0
    l = 0
    
    def __init__(self,Type,n,l):
        self.Type = Type
        self.n = n
        self.l = l
    
    def __str__(self):
        return str(self.__dict__)

    def __eq__(self,other):
        return self.__dict__ == other.__dict__
    
    