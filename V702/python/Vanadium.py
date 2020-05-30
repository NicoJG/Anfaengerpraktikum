####### Use /default/matplotlibrc and /default/header-matplotlib.tex
import os
import pathlib
os.environ['MATPLOTLIBRC'] = (pathlib.Path(__file__).absolute().parent.parent.parent / 'default' / 'matplotlibrc').__str__()
os.environ['TEXINPUTS'] =  (pathlib.Path(__file__).absolute().parent.parent.parent / 'default').__str__() + ':'
#######
import numpy as np
from uncertainties import (ufloat,ufloat_fromstr,unumpy as unp)
from uncertainties.unumpy import (nominal_values as noms, std_devs as stds)
from uncertainties.umath import *
import json
import matplotlib.pyplot as plt

# Messdaten einlesen
t,N = np.genfromtxt('data/Vanadium.dat',delimiter=',',unpack=True)

# Untergrundrate einlesen
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
N_U = ufloat_fromstr(Ergebnisse['Untergrundrate[Imp/s]'])

# Messkonstanten
dt = 30 #s Integrationszeit

# Umrechnungen
N_per_s = unp.uarray(N,np.sqrt(N))/dt
N = N_per_s - N_U
# N = unp.log(N,10)

################
## PLOTS
################

# Plot der Messwerte
plt.errorbar(t-dt/2, noms(N), yerr=stds(N), xerr=dt/2, fmt='ro', ecolor='lightcoral', elinewidth=1.5, label='Messpunkte')
plt.yscale('log')

# Achsenbeschriftung
plt.xlabel(r'$t \:/\: \si{\second}$')
plt.ylabel(r'$N \:/\: \si{\frac{Imp}{\second}}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_Vanadium.pdf')