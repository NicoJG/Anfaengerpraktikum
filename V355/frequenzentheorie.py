import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit

def vMinus_theorie(L,C,Ck):
    return 1/(2 *np.pi * np.sqrt(L/((1/C)+2/(Ck))))

def vPlus_theorie(L,C):
    return 1/(2*np.pi*np.sqrt(L*C))

# Konstanten im Experiment
L = 23.9540 * 10**(-3)
C = 0.7932 *10**(-9)

# Daten einlesen
Ck_gemessen,vPlus_gemessen,vMinus_gemessen = np.genfromtxt('frequenzen.csv',delimiter=',',unpack=True)
vPlus_gemessen = vPlus_gemessen*10**3 # Hz
vMinus_gemessen = vMinus_gemessen*10**3 # Hz
Ck_gemessen = Ck_gemessen*10**(-9) # F

Ck_linspace= np.linspace(0.5,12.5,100)
# Plot der Daten
plt.plot(Ck_gemessen*10**(9), vMinus_gemessen*10**(-3), 'kx', label='Messwerte')
#plt.plot(Ck_gemessen*10**(9), vPlus_gemessen*10**(-3), 'kx', label='Messwerte (v+)')
# Plot der Theoriekurve
plt.plot(Ck_linspace, vMinus_theorie(L,C,Ck_linspace*10**(-9))*10**(-3), 'k-', label='Theoriekurve')
#plt.plot(Ck_linspace, (Ck_linspace/Ck_linspace)*vPlus_theorie(L,C)*10**(-3), 'y-', label='Theoriekurve (v+)')


# Achsenbeschriftung
plt.xlabel(r'$C_\text{k} \:/\: \si{\nano\farad}$')
plt.ylabel(r'$\nu \:/\: \si{\kilo\hertz}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.grid(True,which="both", linestyle='--')

# Speicherort
plt.savefig('build/plot_frequenzentheorie.pdf')



