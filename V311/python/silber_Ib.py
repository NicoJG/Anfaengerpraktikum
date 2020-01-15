import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from uncertainties import ufloat

# Funktion für Curve Fit:
def f(x,a,b):
    return a*x+b

# Daten einlesen
Ib,Uh = np.genfromtxt('data/silber_Ib.csv',delimiter=',',unpack=True)

#Berechnungen
Ib = Ib #Ampere
Uh = Uh #MilliVolt


# Ausgleichskurve berechnen
params,pcov = curve_fit(f,Ib,Uh)
a = params[0]
b = params[1]

#Fehler berechnen
a_err = np.absolute(pcov[0][0])**0.5
b_err = np.absolute(pcov[1][1])**0.5

# Plot der Ausgleichskurve
x_linspace = np.linspace(np.min(Ib),np.max(Ib),100)
plt.plot(x_linspace, f(x_linspace,*params), 'k-', label='Ausgleichskurve')
# Plot der Daten
plt.plot(Ib, Uh, 'ro', label='Hall-Spannung bei Variation von Ib')

# Achsenbeschriftung
plt.xlabel(r'$I_B \:/\: \si{\ampere}$')
plt.ylabel(r'$U_H \:/\: \si{\milli\volt}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_silber_Ib.pdf')