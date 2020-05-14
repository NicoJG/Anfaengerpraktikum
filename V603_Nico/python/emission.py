import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.signal import argrelextrema
from uncertainties import ufloat
from uncertainties import unumpy as unp
from uncertainties.umath import *

# Daten einlesen
theta,N = np.genfromtxt('data/EmissionCu.csv',delimiter=',',unpack=True)

theta = np.radians(theta) # rad
N = N # Impulse / s

# Konstanten der Messung
t = 90 * 10**(-6) # s Totzeit des GM-Zählers
d = 201.4 * 10**(-12) # m Gitterkonstante LiF
n = 1 # Beugungsordnung

# Naturkonstanten
h = 4.136*10**(-15) # eV s
c = 2.998*10**(8) # m/s

# Berechnungen
l = 2*d/n * np.sin(theta) # m Wellenlänge
E = h*c/l # eV Photonenenergie
I = N/(1-t*N) # Intensität

# Maxima finden
i_max = argrelextrema(N, np.greater, order=20)[0] # Indices der relativen Maxima von N

# Berechnung der K Energien mit Fehler der Schrittweite
dtheta = np.radians(0.1)
theta_alpha = ufloat(theta[i_max[2]],dtheta)
theta_beta = ufloat(theta[i_max[1]],dtheta)

l_alpha = 2*d/n * sin(theta_alpha) # m Wellenlänge
l_beta = 2*d/n * sin(theta_beta) # m Wellenlänge

E_alpha = h*c/l_alpha # eV Photonenenergie
E_beta = h*c/l_beta # eV Photonenenergie


# Ergebnisse Speichern
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
if not 'Emission' in Ergebnisse:
    Ergebnisse['Emission'] = {}
Ergebnisse['Emission']['K_alpha[eV]'] = E_alpha.n
Ergebnisse['Emission']['K_alpha_err'] = E_alpha.s
Ergebnisse['Emission']['K_beta[eV]'] = E_beta.n
Ergebnisse['Emission']['K_beta_err'] = E_beta.s
Ergebnisse['Emission']['theta_alpha[degree]'] = (theta_alpha/np.pi*180).n
Ergebnisse['Emission']['theta_alpha_err'] = (theta_alpha/np.pi*180).s
Ergebnisse['Emission']['theta_beta[degree]'] = (theta_beta/np.pi*180).n
Ergebnisse['Emission']['theta_beta_err'] = (theta_beta/np.pi*180).s
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)

# Plot der Daten
plt.axvline(l[i_max[2]],-1000,6000, color='r', linestyle='--', linewidth=1, label=r'$K_\alpha$ Linie')
plt.axvline(l[i_max[1]],-1000,6000, color='r', linestyle=':', linewidth=1, label=r'$K_\beta$ Linie')
plt.plot(l, N, 'k-', label='Messdaten')
plt.annotate('Bremsberg', xy=(l[i_max[0]],500),xycoords='data',
                xytext=(-50, 30), textcoords='offset points',
                arrowprops=dict(arrowstyle="->"))

# Achsenbeschriftung
plt.xlabel(r'$\lambda \:/\: \si{\metre}$')
plt.ylabel(r'$N \:/\: \si{Impulse\per\second}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_emission.pdf')
