import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from uncertainties import ufloat

# Funktion für Curve Fit:
def f(x,a,b):
    return a*x+b

def t(E):
    return np.arcsin((h * c)/(2 * d * E))

def sigma(E,Z):
    return Z - ((E)/(r) - (a**2 * Z**4)/4)**0.5

# Daten einlesen
theta,N = np.genfromtxt('data/bragg.csv',delimiter=',',unpack=True)

#Berechnungen
n = 1
h = 6.62607015 * 10 **(-34)
c = 299792458
d = 201.4 * 10**(-12)
e = 1.602176634 * 10 **(-19)
r = 13.6 * e
a = 7.297352 * 10**(-3)


Ge = 11.1031 * 1000
Br = 13.4737 * 1000
Rb = 15.1997 * 1000
Sr = 16.1046 * 1000 
Zr = 17.9976 * 1000

print(sigma(Ge*e,32))
print(sigma(Br*e,35))
print(sigma(Rb*e,37))
print(sigma(Sr*e,38))
print(sigma(Zr*e,40))


# Ausgleichskurve berechnen
#params,pcov = curve_fit(f,x,y)
#a = params[0]
#b = params[1]

#Fehler berechnen
#a_err = np.absolute(pcov[0][0])**0.5
#b_err = np.absolute(pcov[1][1])**0.5

# Plot der Ausgleichskurve
#x_linspace = np.linspace(np.min(x),np.max(x),100)
#plt.plot(x_linspace, f(x_linspace,*params), 'k-', label='Ausgleichskurve')
# Plot der Daten
plt.plot(theta, N, 'ro', label='Spektrum')

# Achsenbeschriftung
plt.xlabel(r'$\theta \:/\: \si{\circ}$')
plt.ylabel(r'$N \:/\: \frac{\text{Imp}}{\si{\second}}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_spektrum.pdf')
