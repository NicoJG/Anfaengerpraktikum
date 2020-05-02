import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.signal import argrelextrema

# Daten einlesen
alpha,N = np.genfromtxt('data/EmissionCu.csv',delimiter=',',unpack=True)

alpha = np.radians(alpha) # rad
N = N # Impulse / s

# Konstanten der Messung
t = 90 * 10**(-6) # s Totzeit des GM-Zählers
d = 201.4 * 10**(-12) # m Gitterkonstante LiF
n = 1 # Beugungsordnung

# Naturkonstanten
h = 4.136*10**(-15) # eV s
c = 2.998*10**(8) # m/s

# Berechnungen
l = 2*d/n * np.sin(alpha) # m Wellenlänge
E = h*c/l # eV Photonenenergie
I = N/1-t*N # Intensität

# Maxima finden
i_max = argrelextrema(N, np.greater, order=20)[0] # Indices der relativen Maxima von N

# Ergebnisse Speichern
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
if not 'Emission' in Ergebnisse:
    Ergebnisse['Emission'] = {}
Ergebnisse['Emission']['K_alpha[eV]'] = E[i_max[2]]
Ergebnisse['Emission']['K_beta[eV]'] = E[i_max[1]]
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
