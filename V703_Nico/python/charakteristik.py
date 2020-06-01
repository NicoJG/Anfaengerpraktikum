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

U,N,I = np.genfromtxt('data/Kennlinie.dat',delimiter=',',unpack=True)

# Konstanten der Messung
t = 60 #s Integrationszeit

# Kennlinie mit Fehlern speichen
data = list(zip(U,N,np.sqrt(N)))
np.savetxt('data/Kennlinie_mit_Fehler.csv', data, header='U[V], N[Imp]', fmt='%3.0f,%4.0f+-%2.0f')

# Fehler berechnen
N = uarray(N,np.sqrt(N))

# Umrechnung
N = N/t # Impulse pro sekunde
I = I*10**(-6) #A

# Plateaugrenzen (Indizes)
i1 = 5
i2 = 33
# Ausgleichsgerade des Plateaus
def N_fit(U,a,b):
    return U*a+b

params,pcov = curve_fit(N_fit,U[i1:i2],noms(N[i1:i2]),sigma=stds(N[i1:i2]))
a = ufloat(params[0],np.absolute(pcov[0][0])**0.5)
b = ufloat(params[1],np.absolute(pcov[1][1])**0.5)

# Plateauanstieg
deltaN =  N_fit(U[i2-1],a,b) - N_fit(U[i1],a,b) #Impulse pro Sekunde
percent = (N_fit(U[i2-1],a,b)/N_fit(U[i1],a,b) - 1)*100 #%
per100V = percent*100/(U[i2-1]-U[i1]) #% pro 100 V

###############################
## Ergebnisse Speichern JSON
###############################
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
if not 'Charakteristik' in Ergebnisse:
    Ergebnisse['Charakteristik'] = {}
Ergebnisse['Charakteristik']['a'] = '{:1.5f}'.format(a)
Ergebnisse['Charakteristik']['b'] = '{:1.5f}'.format(b)
Ergebnisse['Charakteristik']['Anstieg[Imp/s]'] = '{}'.format(deltaN)
Ergebnisse['Charakteristik']['Anstieg[%]'] = '{}'.format(percent)
Ergebnisse['Charakteristik']['Anstieg[%/100V]'] = '{}'.format(per100V)

json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)

###############################
## Plots
###############################
# Plot der Ausgleichsgerade
U_linspace = np.linspace(U[i1],U[i2-1],100)
plt.plot(U_linspace,N_fit(U_linspace,*params),'k-', label='Ausgleichsgerade')
# Plot der Messdaten
plt.errorbar(U, unp.nominal_values(N), yerr=unp.std_devs(N), fmt='ro', label='Messdaten')

# Achsenbeschriftung
plt.xlabel(r'$U \:/\: \si{\volt}$')
plt.ylabel(r'$N \:/\: \si{\frac{Impulse}{\second}}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_charakteristik.pdf')