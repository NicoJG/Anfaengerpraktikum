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
from scipy.optimize import curve_fit

# Messdaten einlesen
t,N = np.genfromtxt('data/Vanadium.dat',delimiter=',',unpack=True)

# Untergrundrate einlesen
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
N_U = ufloat_fromstr(Ergebnisse['Untergrundrate[Imp/s]'])

# Messkonstanten
dt = 30 #s Integrationszeit

# Umrechnungen
N = unp.uarray(N,np.sqrt(N))
N = N - N_U*dt # Imp/30s Untergrund abgezogen
lnN = unp.log(N)

# Ausgleichsrechnung
def lnN_fit(t,a,b):
    return a*t+b
params,pcov = curve_fit(lnN_fit,t,noms(lnN),sigma=stds(lnN))
params,pcov = curve_fit(lnN_fit,t,noms(lnN),sigma=stds(lnN))
a = ufloat(params[0],np.absolute(pcov[0][0])**0.5) # a=-lambda
b = ufloat(params[1],np.absolute(pcov[1][1])**0.5)

# Ausgleichsrechnung 2 nur bis t=420
i_t_max = np.where(t == 570)[0][0]
print(i_t_max)
params2,pcov2 = curve_fit(lnN_fit,t[:i_t_max],noms(lnN[:i_t_max]),sigma=stds(lnN[:i_t_max]))
a2 = ufloat(params2[0],np.absolute(pcov2[0][0])**0.5) # a=-lambda
b2 = ufloat(params2[1],np.absolute(pcov2[1][1])**0.5)

# Halbwertszeit berechnen
T = unp.log(2)/(-1*a)
# Zeit in Minuten und Sekunden Umrechnen
T_min = np.floor(T.n/60)
T_sec = (T/60 - T_min)*60
# Halbwertszeit berechnen
T2 = unp.log(2)/(-1*a2)
# Zeit in Minuten und Sekunden Umrechnen
T2_min = np.floor(T2.n/60)
T2_sec = (T2/60 - T2_min)*60

# Ergebnisse speichern JSON
if not 'Vanadium' in Ergebnisse:
    Ergebnisse['Vanadium'] = {}
Ergebnisse['Vanadium']['a'] = '{}'.format(a)
Ergebnisse['Vanadium']['b'] = '{}'.format(b)
Ergebnisse['Vanadium']['T[s]'] = '{}'.format(T)
Ergebnisse['Vanadium']['T[min]'] = '{} min + '.format(T_min) + '({}) sec'.format(T_sec)
Ergebnisse['Vanadium']['a2'] = '{}'.format(a2)
Ergebnisse['Vanadium']['b2'] = '{}'.format(b2)
Ergebnisse['Vanadium']['T2[s]'] = '{}'.format(T2)
Ergebnisse['Vanadium']['T2[min]'] = '{} min + '.format(T2_min) + '({}) sec'.format(T2_sec)
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)

################
## PLOTS
################

# Plot der Ausgleichsgerade
t_linspace = np.linspace(np.min(t),np.max(t))
plt.plot(t_linspace,lnN_fit(t_linspace,*params), 'k-', label='Ausgleichsgerade')
# Plot der Ausgleichsgerade 2
t2_linspace = np.linspace(np.min(t),np.max(t[i_t_max]))
# plt.plot(t2_linspace,lnN_fit(t2_linspace,*params2), 'b--', label='Ausgleichsgerade 2')

# Plot der Messwerte
plt.errorbar(t, noms(lnN), yerr=stds(lnN), fmt='ro', ecolor='lightcoral', elinewidth=1.5, label='Messpunkte')
# plt.yscale('log')

# Achsenbeschriftung
plt.xlabel(r'$t \:/\: \si{\second}$')
plt.ylabel(r'$\ln(N-N_0)$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_Vanadium.pdf')