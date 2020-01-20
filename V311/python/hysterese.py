import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from uncertainties import ufloat

# Funktion für Curve Fit:
def f(x,a,b):
    return a*x+b

# Daten einlesen
Ib,B1,B2 = np.genfromtxt('data/hysterese.csv',delimiter=',',unpack=True)

#Berechnungen
Ib = Ib #Ampere
B1 = B1 #Millitesla
B2 = B2 #Millitesla

# Ausgleichsgerade berechnen
params,pcov = curve_fit(f,Ib,(B2+B1)/2)
a = params[0]
b = params[1]

#Fehler berechnen
a_err = np.absolute(pcov[0][0])**0.5
b_err = np.absolute(pcov[1][1])**0.5

# Plot der Ausgleichsgerade
x_linspace = np.linspace(np.min(Ib),np.max(Ib),100)
plt.plot(x_linspace, f(x_linspace,*params), 'k-', label='Ausgleichsgerade')
# Plot der Daten
plt.plot(Ib, B1, 'ro', label='Steigendes B-Feld')
plt.plot(Ib, B2, 'bo', label='Fallendes B-Feld')

# Achsenbeschriftung
plt.xlabel(r'$I_B \:/\: \si{\ampere}$')
plt.ylabel(r'$B \:/\: \si{\milli\tesla}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

#print("a: ", a)
#print("Fehler von a: ", a_err)
#print("b: ", b)
#print("Fehler von b: ", b_err)

# Speicherort
plt.savefig('build/plot_hysterese.pdf')
