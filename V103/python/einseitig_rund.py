import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit

F = 0.7474 * 9.81 #Gewichtskraft
L = 0.450 #Meter
I= (np.pi/4) * 0.005**4 #Meter^4

# Funktion für Curve Fit:

def D_Theorie(x,E):
    return (0.7474 * 9.81)/(2* E * ((np.pi/4) * 0.005**4))* x

def D_fit(x,E):
    return D_Theorie(x,E)

# Daten einlesen
x,D0,DM = np.genfromtxt('data/einseitig_rund.csv',delimiter=',',unpack=True)

#Berechnungen
x = x*10**(-3)
D0 = D0*10**(-3)
DM = DM*10**(-3)
D= D0-DM
X = (0.450*x**2 - (x**3)/3)
# Ausgleichskurve berechnen
params,pcov = curve_fit(D_fit,X,D)
E = params[0]

#Fehler berechnen
E_err = np.absolute(pcov[0][0])**0.5


# Plot der Daten
plt.plot(X, D*10**(3), 'rx', label='Auslenkung')
# Plot der Ausgleichskurve
x_linspace = np.linspace(np.min(X),np.max(X),100)
plt.plot(x_linspace, D_fit(x_linspace,*params)*10**(3), 'k-', label='Ausgleichskurve')

# Achsenbeschriftung
plt.xlabel(r'$Lx^2 - \frac{x^3}{3} \:/\: \si{\cubic\meter}$')
plt.ylabel(r'$D \:/\: \si{\milli\meter}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.grid(True,which="both", linestyle='--')

# Speicherort
plt.savefig('build/plot_einseitig_rund.pdf')

#print('E1:',E*10**(-9))
#print('Fehler von E1',E_err*10**(-9))

r = np.array([0.01,0.01,0.01,0.01,0.0105,0.0105,0.0105,0.0105,0.01,0.01,])
print("Mittelwert: ", np.mean(r))
print("Abweichung: ", np.std(r,ddof=1))
