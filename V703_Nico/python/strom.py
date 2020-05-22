####### Use /default/matplotlibrc and /default/header-matplotlib.tex
import os
import pathlib
os.environ['MATPLOTLIBRC'] = (pathlib.Path(__file__).absolute().parent.parent.parent / 'default' / 'matplotlibrc').__str__()
os.environ['TEXINPUTS'] =  (pathlib.Path(__file__).absolute().parent.parent.parent / 'default').__str__() + ':'
#######
import matplotlib.pyplot as plt
import numpy as np
import json
from uncertainties import ufloat
from uncertainties import unumpy as unp
from uncertainties.unumpy import uarray
from uncertainties.unumpy import (nominal_values as noms, std_devs as stds)
from scipy.optimize import curve_fit

# Werte einlesen
U,I,N = np.genfromtxt('data/Zaehlrohrstrom.dat',delimiter=',',unpack=True)

# Konstanten der Messung
t = 60 #s Messzeit

# Naturkonstanten
e = 1.602*10**(-19) #C

# Fehler
N = uarray(N,np.sqrt(N))
I = uarray(I,0.05)

# Umrechnung
N = N/t #Imp/s
U = U #V
I = I*10**(-6) #A

# Berechnungen
Z = I/(e*N)

# Ausgleichsgerade
def Z_fit(I,a,b):
    return I*a+b

params,pcov = curve_fit(Z_fit,noms(I),noms(Z),sigma=stds(Z),p0=[10**10,10**10])
a = ufloat(params[0],np.absolute(pcov[0][0])**0.5)
b = ufloat(params[1],np.absolute(pcov[1][1])**0.5)

###############################
## Ergebnisse Speichern JSON
###############################
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
if not 'Strom' in Ergebnisse:
    Ergebnisse['Strom'] = {}
Ergebnisse['Strom']['a'] = '{}'.format(a)
Ergebnisse['Strom']['b'] = '{}'.format(b)
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)

###############################
## Plots
###############################
# Plot der Ausgleichsgerade
I_linspace = np.linspace(np.min(noms(I)),np.max(noms(I)),100)
plt.plot(I_linspace*10**(6),Z_fit(I_linspace,*params),'k-', label='Ausgleichsgerade')
# Plot der Messdaten
plt.errorbar(noms(I*10**(6)), noms(Z), yerr=stds(Z),xerr=stds(I*10**(6)), fmt='ro', label='Messdaten')

# Achsenbeschriftung
plt.xlabel(r'$I \:/\: \si{\micro\coulomb}$')
plt.ylabel(r'$Z$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0.2, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_strom.pdf')