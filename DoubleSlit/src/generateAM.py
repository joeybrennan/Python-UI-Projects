from scipy.special import hermite
import numpy as np
from math import factorial as fact
from scipy.integrate import quad
import matplotlib.pyplot as plt

def doubleSlit(wavelen, modeNum, Zin):
    #Initial paras
    m = np.linspace(0,modeNum,modeNum+1,dtype=np.int)
    z = Zin
    d = 3*wavelen
    t = 6*wavelen
    Wo = 1.5*wavelen
    
    #Define Bounds
    a1 = -d - t/2
    b1 = -t/2
    a2 = t/2
    b2 = d + t/2

    #Generate AM values
    AM1 = []
    for mn in m:
        AM1.append(quad(genHermiteMode, a1,b2,args=(mn,Wo,a1,b1,a2,b2))[0])
      
    W = Wz(Wo,z,wavelen)
    R = Rz(Wo,z,wavelen)
    x = np.linspace(-30*wavelen,30*wavelen,1001)
    
    #Reconstruct Electric Field 
    ET = Efield(AM1, W, R, phi(W,R,wavelen), x, m, wavelen, z)
    
    return x,ET
    
def Efield(modeAmps, W, R, phiz, x, m, wavelen, z):
    ET = []
    k = (2*np.pi)/wavelen
    for xn in x:
        En = []
        for i,mn in enumerate(m):
            En.append(modeAmps[i]*genHermiteModeM(xn,mn,W)*np.exp(-1j*k*((xn**2/(2*R)))+1j*(mn+0.5)*phiz)*np.exp(-1j*k*z))
        #print(En)
        ET.append(sum(np.asarray(En)))
    ET = np.asarray(ET)

    return ET
    
def Wz(Wo,z,wavelen):
    if z ==0:
        return Wo
    else:
        return np.sqrt(Wo**2*(1+((wavelen*z)/(np.pi*Wo**2))**2))
def Rz(Wo,z,wavelen):
    if z == 0:
        return np.inf
    else:
        return z*(1+((np.pi*Wo**2)/(wavelen*z))**2)
def phi(W,R,wavelen):
    return np.arctan((np.pi*W**2)/(wavelen*R))
    
        
def genHermiteMode(x, m, W, a1,b1,a2,b2):
    if a1 <= x <= b1:
        return  ((1/(np.sqrt(np.pi)*np.power(2,m-0.5)*fact(m)*W))**0.5)*hermite(m)(np.sqrt(2)*(x/W))*np.exp(-x**2/W**2)  
        
    elif a2 <= x <= b2:
        return ((1/(np.sqrt(np.pi)*np.power(2,m-0.5)*fact(m)*W))**0.5)*hermite(m)(np.sqrt(2)*(x/W))*np.exp(-x**2/W**2)    
    else:
        return 0
def genHermiteModeM(x, m, W):
    return ((1/(np.sqrt(np.pi)*np.power(2,m-0.5)*fact(m)*W))**0.5)*(hermite(m)(np.sqrt(2)*(x/W)))*np.exp(-1*(x**2/W**2))
    
