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
t,N = np.genfromtxt('data/Rhodium.dat',delimiter=',',unpack=True)

# Untergrundrate einlesen
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
N_U = ufloat_fromstr(Ergebnisse['Untergrundrate[Imp/s]'])

# Messkonstanten
dt = 15 #s Integrationszeit

# Umrechnungen
N = unp.uarray(N,np.sqrt(N))
N = N - N_U*dt # Imp/30s Untergrund abgezogen
lnN = unp.log(N)

###################################
## Langlebig
# Ausgleichsrechnung langlebig
def lnN_fit(t,a,b):
    return a*t+b
i_l = np.where(t == 300)[0][0]
i_l = 17
params_l,pcov_l = curve_fit(lnN_fit,t[i_l:],noms(lnN[i_l:]),sigma=stds(lnN[i_l:]))
a_l = ufloat(params_l[0],np.absolute(pcov_l[0][0])**0.5) # a=-lambda
b_l = ufloat(params_l[1],np.absolute(pcov_l[1][1])**0.5)

# Halbwertszeit langlebig berechnen
T_l = unp.log(2)/(-1*a_l)
# Zeit in Minuten und Sekunden Umrechnen
T_l_min = np.floor(T_l.n/60)
T_l_sec = (T_l/60 - T_l_min)*60
####################################

############################
## Kurzlebig
i_k = np.where(t == 210)[0][0]+1
i_k = 14
print(i_k)
# Messdaten korrigieren
lnN_k = unp.log(N[:i_k] - unp.exp(lnN_fit(t[:i_k],a_l,b_l)))

# Ausgleichsgerade
params_k,pcov_k = curve_fit(lnN_fit,t[:i_k],noms(lnN_k),sigma=stds(lnN_k))
a_k = ufloat(params_k[0],np.absolute(pcov_k[0][0])**0.5) # a=-lambda
b_k = ufloat(params_k[1],np.absolute(pcov_k[1][1])**0.5)

# Halbwertszeit kurzlebig berechnen
T_k = unp.log(2)/(-1*a_k)
# Zeit in Minuten und Sekunden Umrechnen
T_k_min = np.floor(T_k.n/60)
T_k_sec = (T_k/60 - T_k_min)*60
############################

# Ergebnisse speichern JSON
if not 'Rhodium' in Ergebnisse:
    Ergebnisse['Rhodium'] = {}
Ergebnisse['Rhodium']['a_l'] = '{}'.format(a_l)
Ergebnisse['Rhodium']['b_l'] = '{}'.format(b_l)
Ergebnisse['Rhodium']['T_l[s]'] = '{:3.1f}'.format(T_l)
Ergebnisse['Rhodium']['T_l[min]'] = '{} min + '.format(T_l_min) + '({:2.0f}) sec'.format(T_l_sec)
Ergebnisse['Rhodium']['a_k'] = '{}'.format(a_k)
Ergebnisse['Rhodium']['b_k'] = '{}'.format(b_k)
Ergebnisse['Rhodium']['T_k[s]'] = '{}'.format(T_k)
Ergebnisse['Rhodium']['T_k[min]'] = '{} min + '.format(T_k_min) + '({:2.0f}) sec'.format(T_k_sec)
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)

################
## PLOTS
################

# Plot der Ausgleichsgerade langlebig
t_l_linspace = np.linspace(t[i_l],np.max(t))
plt.plot(t_l_linspace,lnN_fit(t_l_linspace,*params_l),'k-', label='Ausgleichsgerade (langlebig)')

# Plot der Ausgleichsgerade kurzlebig
t_k_linspace = np.linspace(np.min(t),t[i_k-1])
plt.plot(t_k_linspace,lnN_fit(t_k_linspace,*params_k),'k--', label='Ausgleichsgerade (kurzlebig)')

# Plot der korrigierten Messwerte
plt.errorbar(t[:i_k], noms(lnN_k), yerr=stds(lnN_k), fmt='bo', ecolor='cornflowerblue', elinewidth=1.5, label='korrigierte Messpunkte')

# Plot der Messwerte
plt.errorbar(t, noms(lnN), yerr=stds(lnN), fmt='ro', ecolor='lightcoral', elinewidth=1.5, label='Messpunkte')


# Achsenbeschriftung
plt.xlabel(r'$t \:/\: \si{\second}$')
plt.ylabel(r'$\ln(N-N_0)$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_Rhodium.pdf')