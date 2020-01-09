import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit


# Funktion für Curve Fit:

def D_Theorie(x,E):
    return (1.2077 * 9.81)/(2* E * ((0.010**4)/12))* x

def D_fit(x,E):
    return D_Theorie(x,E)

# Daten einlesen
x,D0,DM = np.genfromtxt('data/einseitig_eckig.csv',delimiter=',',unpack=True)

#Berechnungen
x = x*10**(-3) #in meter
D0 = D0*10**(-3) #in meter
DM = DM*10**(-3) #meter
D= D0-DM #meter 

X = 0.446*x**2 - (x**3)/3 
# Ausgleichskurve berechnen
params,pcov = curve_fit(D_fit,X,D)
E = params[0]

#Fehler berechnen
E_err = np.absolute(pcov[0][0])**0.5


# Plot der Ausgleichskurve
x_linspace = np.linspace(np.min(X),np.max(X),100)
plt.plot(x_linspace, D_fit(x_linspace,*params)*10**3, 'k-', label='Ausgleichsgerade')
# Plot der Daten
plt.plot(X, D*10**3, 'ro', label='Auslenkung')

# Achsenbeschriftung
plt.xlabel(r'$Lx^2 - \frac{x^3}{3} \:/\: \si{\cubic\meter}$')
plt.ylabel(r'$D \:/\: \si{\milli\meter}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.grid(True,which="both", linestyle='--')

# Speicherort
plt.savefig('build/plot_einseitig_eckig.pdf')

print('E2:',E*10**(-9))
print('Fehler von E2',E_err*10**(-9))