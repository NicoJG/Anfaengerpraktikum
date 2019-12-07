import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit

# Funktion für Curve Fit:
def f(x,F,E,I,L):
    return F/(2* E * I)* (L*x^2 - (x^3)/3)

# Daten einlesen
x,D0,DM = np.genfromtxt('data/einseitig_rund.csv',delimiter=',',unpack=True)

#Berechnungen
x = x*10**(-3)
D0 = D0*10**(-3)
DM = DM*10**(-3)
D= D0-DM

F = 0.7474 * 9.81 #Gewichtskraft
L = 0.450 #Meter
#I=


# Ausgleichskurve berechnen
#params,pcov = curve_fit(f,x,E,I,L)
#a = params[0]
#b = params[1]

#Fehler berechnen
#a_err = np.absolute(pcov[0][0])**0.5
#b_err = np.absolute(pcov[1][1])**0.5

# Plot der Daten
plt.plot(x, D, 'rx', label='Auslenkung')
# Plot der Ausgleichskurve
#x_linspace = np.linspace(np.min(x),np.max(x),100)
#plt.plot(x_linspace, f(x_linspace,*params), 'k-', label='Ausgleichskurve')

# Achsenbeschriftung
plt.xlabel(r'$x \:/\: \si{\meter}$')
plt.ylabel(r'$D \:/\: \si{\meter}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_einseitig_rund.pdf')