import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from uncertainties import ufloat

# Funktion für Curve Fit:
def f(x,a,b):
    return a*x+b

# Daten einlesen
N,U = np.genfromtxt('data/werte.csv',delimiter=',',unpack=True)

#Berechnungen
D = (N-1) * 6 #in mm

# Ausgleichskurve berechnen
params,pcov = curve_fit(f,D,U)
a = params[0]
b = params[1]

#Fehler berechnen
a_err = np.absolute(pcov[0][0])**0.5
b_err = np.absolute(pcov[1][1])**0.5


# Plot der Ausgleichskurve
x_linspace = np.linspace(np.min(D),np.max(D),100)
plt.plot(x_linspace, f(x_linspace,*params), 'k-', label='Ausgleichskurve')
# Plot der Daten
plt.plot(D, U, 'ro', label='Kurve')

# Achsenbeschriftung
plt.xlabel(r'$D \:/\: \si{\milli\meter}$')
plt.ylabel(r'$U \:/\: \si{\volt}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

print(a)
print(a_err)
print(b)
print(b_err)

# Speicherort
plt.savefig('build/plot_werte.pdf')
