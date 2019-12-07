import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit

F = 4718.8 * 9.81 #Gewichtskraft
L = 0.555 #Meter
I= (0.010**4)/12 #Meter^4

# Funktion für Curve Fit:

def D_Theorie(x,F,E,I,L):
    if x <= (L/2):
        return F/(48* E * I)* (3* L**(2)*x - (4*x**2))
    else:
         return F/(48* E * I)* ((4*x**2) - (12* L * x**2) + (9* L**2 *x) - (L**3))

def D_fit(x,E):
    return D_Theorie(x,F,E,I,L)

# Daten einlesen
x,D0,DM = np.genfromtxt('data/zweiseitig_eckig.csv',delimiter=',',unpack=True)

#Berechnungen
x = x*10**(-3)
D0 = D0*10**(-3)
DM = DM*10**(-3)
D= D0-DM

# Ausgleichskurve berechnen
params,pcov = curve_fit(D_fit,x,D)
a = params[0]

#Fehler berechnen
E_err = np.absolute(pcov[0][0])**0.5


# Plot der Daten
plt.plot(x*10**(3), D*10**(3), 'rx', label='Auslenkung')
# Plot der Ausgleichskurve
x_linspace = np.linspace(np.min(x),np.max(x),100)
plt.plot(x_linspace*10**(3), D_fit(x_linspace,*params)*10**(3), 'k-', label='Ausgleichskurve')

# Achsenbeschriftung
plt.xlabel(r'$x \:/\: \si{\milli\meter}$')
plt.ylabel(r'$D \:/\: \si{\milli\meter}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.grid(True,which="both", linestyle='--')

# Speicherort
plt.savefig('build/plot_zweiseitig_eckig.pdf')

print('E3:',a*10**(-9))
print('Fehler von E3',E_err*10**(-9))