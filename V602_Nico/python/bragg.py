####### Use /default/matplotlibrc and /default/header-matplotlib.tex
import os
import pathlib
os.environ['MATPLOTLIBRC'] = (pathlib.Path(__file__).absolute().parent.parent.parent / 'default' / 'matplotlibrc').__str__()
os.environ['TEXINPUTS'] =  (pathlib.Path(__file__).absolute().parent.parent.parent / 'default').__str__() + ':'
#######
import numpy as np
import matplotlib.pyplot as plt
import json
from scipy.signal import argrelextrema

# Messdaten einlesen
theta,N = np.genfromtxt('data/Bragg.dat',delimiter=',',unpack=True)

# Umrechnung
theta = np.deg2rad(theta) # rad
N = N # Imp/s

# Maxima finden
i_max = argrelextrema(N, np.greater, order=20)[0] # Indices der relativen Maxima von N
N_Max = N[i_max[0]]
theta_Max = theta[i_max[0]]

# Ergebnisse speichern
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
if not 'Bragg' in Ergebnisse:
    Ergebnisse['Bragg'] = {}
Ergebnisse['Bragg']['N_Max'] = N_Max
Ergebnisse['Bragg']['theta_Max[°]'] = np.rad2deg(theta_Max)
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)

# Plot der Messdaten
plt.plot(np.rad2deg(theta),N,'k.',label='Messwerte')

# Achsenbeschriftung
plt.xlabel(r'$\theta \:/\: \si{\degree}$')
plt.ylabel(r'$N \:/\: \si{\frac{Impulse}{\second}}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Plot speichern
plt.savefig('build/plot_bragg.pdf')