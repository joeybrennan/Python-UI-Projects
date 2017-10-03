# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 15:53:03 2017

This program integrates over the Azi and PW angles to find the absorbtion 
and performance of the pixel

returns: absolute eff, aperture eff for each Azi

@author: Joe
"""

import numpy as np
from scipy.integrate import simps
import cmath

def integratePixelPerformance(amps,modeList,inclinationAngles,azimuthalAngles,AbosrbtionChannels,ApertureArea):
    
    inclinationAnglesStep = inclinationAngles[1] - inclinationAngles[0]
    azimuthalAnglesStep = azimuthalAngles[1] - azimuthalAngles[0]
    Z0 = 376.73
    Power = 1
    maxPowerIncident = ApertureArea*(Power/Z0)
    
    apertureData = np.empty((len(azimuthalAngles),len(inclinationAngles)))
    #absoluteEffAzi = []
    
    #Iterate through each azimuthal angle
    for azimIdx, _ in enumerate(azimuthalAngles):
        modeAmplitudes = amps[:,azimIdx,:]
        #absoluteEffInc = []
        #Iterate through each inclination angle
        for incIndx, _ in enumerate(inclinationAngles):
            absCouplingResult = []
            #Calculate coupling to absorbtion modes
            for absMode in AbosrbtionChannels:
                #cycle through modeamps for each inclination angle
                modeAmp = modeAmplitudes[incIndx]
                absorbtionValue = absMode[0]
                absorbtionModes = absMode[1]
                
                #Dot product of the modeAmps and absorbtionModes
                r,phi = cmath.polar(np.dot(modeAmp.conj(),absorbtionModes))
                absCouplingResult.append((r**2)*absorbtionValue)
                
            #Adds Contribution from all absorbtion modes
            absCouplingSum = np.sum(absCouplingResult)
            
            cosInc = np.cos(np.deg2rad(inclinationAngles[incIndx]))
            sinInc = np.sin(np.deg2rad(inclinationAngles[incIndx]))
            
            apertureData[azimIdx,incIndx] = absCouplingSum/(cosInc*maxPowerIncident)
            #absoluteEffInc.append((absCouplingSum/(cosInc*maxPowerIncident))*np.deg2rad(inclinationAnglesStep)*sinInc)
        #absoluteEffAzi.append(np.sum(absoluteEffInc)*np.deg2rad(azimuthalAnglesStep))
    #absoluteEff = np.sum(absoluteEffAzi)/(4*np.pi)
    
    #Normalisation due to symmetry about azimuthal 
    apertureData = apertureData
    
    inclinationAnglesRad=np.deg2rad(inclinationAngles)
    azimuthalAnglesRad = np.deg2rad(azimuthalAngles)
    sinThe = np.sin(inclinationAnglesRad)
    simsAbsoluteEff = 2*simps([simps(sinThe*apertureData[aziIdx,:],inclinationAnglesRad) for aziIdx,_ in enumerate(azimuthalAngles)],azimuthalAnglesRad)/(4*np.pi)
    
    return simsAbsoluteEff,apertureData