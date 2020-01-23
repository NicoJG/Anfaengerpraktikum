import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from uncertainties import ufloat

# Funktion für Curve Fit:
def U_fit(r,a):
    return a/(r**2)

# Daten einlesen
r,U = np.genfromtxt('data/led.csv',delimiter=',',unpack=True)

# Einheiten Umrechnen
r = r * 10**(-2) #m
r_gut = r[5:]
U_gut = U[5:]

print(r)
print(U)
print(U_gut)

# Curve Fit
params,pcov = curve_fit(U_fit,r_gut,-U_gut)
a = params[0]
a_err = np.absolute(pcov[0][0])**0.5

# Einzelne Daten Speichern
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))

if not 'led' in Ergebnisse:
    Ergebnisse['led'] = {}

Ergebnisse['led']['a[V*m**2]'] = a
Ergebnisse['led']['a_err[V*m**2]'] = a_err
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)

# linspace
r_linspace = np.linspace(np.min(r),np.max(r),100)

# Plot der Ausgleichskurve
#plt.plot(r_linspace, U_fit(r_linspace,*params), 'k-', label='Ausgleichskurve')
# Plot der Daten
plt.plot(r, -U, 'ro', label='Messdaten')
plt.plot(r_gut, -U_gut, 'bo', label='Messdaten')

# Achsenbeschriftung
plt.xlabel(r'$r \:/\: \si{\meter}$')
plt.ylabel(r'$|U_\text{out}| \:/\: \si{\volt}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_led.pdf')