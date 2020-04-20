import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from uncertainties import ufloat

# Funktion für Curve Fit:
def f(x,a,b):
    return a*x+b

# Daten einlesen
N,U = np.genfromtxt('data/regression.csv',delimiter=',',unpack=True)

#Berechnungen
D = (N-1)*6 # mm

# Daten speichern
data = list(zip(N,D,U))
np.savetxt('data/regression_berechnet.csv', data, header='N,D[mm],U[V]', fmt='%1.0f,%1.3f,%2.1f')

# Ausgleichskurve berechnen
params,pcov = curve_fit(f,D,U)
a = params[0]
b = params[1]

#Fehler berechnen
a_err = np.absolute(pcov[0][0])**0.5
b_err = np.absolute(pcov[1][1])**0.5

# Einzelne Daten Speichern
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))

if not 'regression' in Ergebnisse:
    Ergebnisse['regression'] = {}

Ergebnisse['regression']['a'] = a
Ergebnisse['regression']['a_err'] = a_err
Ergebnisse['regression']['b'] = b
Ergebnisse['regression']['b_err'] = b_err
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)


# Plot der Ausgleichskurve
D_linspace = np.linspace(np.min(D),np.max(D),100)
plt.plot(D_linspace, f(D_linspace,*params), 'k-', label='Ausgleichsgerade')
# Plot der Daten
plt.plot(D, U, 'ro', label='Messdaten')

# Achsenbeschriftung
plt.xlabel(r'$D \:/\: \si{\milli\metre}$')
plt.ylabel(r'$U \:/\: \si{\volt}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_regression.pdf')
