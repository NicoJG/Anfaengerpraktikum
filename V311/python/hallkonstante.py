import numpy as np
from uncertainties import ufloat

e0 = -1.602*10**(-19) #C

nK1 = ufloat(2.42,0.09)*10**29
nS1 = ufloat(9.58,0.34)*10**28
nZ1 = ufloat(-7.45,0.29)*10**28

nK2 = ufloat(3.27,0.09)*10**29
nS2 = ufloat(-2.145,0.007)*10**28
nZ2 = ufloat(-5.045,0.02)*10**27

def RH(n):
    return 1/(n*e0)

print('nK1: ',RH(nK1))
print('nS1: ',RH(nS1))
print('nZ1: ',RH(nZ1))
print('nK2: ',RH(nK2))
print('nS2: ',RH(nS2))
print('nZ2: ',RH(nZ2))