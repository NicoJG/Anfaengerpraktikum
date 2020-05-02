import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from uncertainties import ufloat

# Funktion für Curve Fit:
def f(x,a,b):
    return a*x+b

def E(alpha):
    return (h * c)/(2 *d* np.sin(alpha))

# Daten einlesen
theta, N = np.genfromtxt('data/emissionCU.csv',delimiter=',',unpack=True)

#Berechnungen

h = 6.626 *10**-34 #Joule pro Sekunde
c = 299792458 #Meter pro Sekunde
alpha1 = 0.393
alpha2 = 0.353
d = 201.4*10**-12

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
plt.plot(theta, N, 'ro', label='Emmissionsspektrum')

# Achsenbeschriftung
plt.xlabel(r'$\theta \:/\: \si{\circ}$')
plt.ylabel(r'$N \:/\: \frac{\text{Imp}}{\si{\second}}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

print(E(alpha1))
print(E(alpha2))

# Speicherort
plt.savefig('build/plot_emissionCu.pdf')
