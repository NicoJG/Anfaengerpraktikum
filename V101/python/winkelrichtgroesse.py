import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from uncertainties import ufloat

# Funktion für Curve Fit:
def M_fit(phi,a):
    return a*phi

# Daten einlesen
phi,F = np.genfromtxt('data/kraft_gemessen.csv',delimiter=',',unpack=True)

phi = np.radians(phi) #rad
F = F #N

R = 28.7 * 10**(-2) #m
M = R*F

# Daten speichern
data = list(zip(phi,F,M))
np.savetxt('data/winkelrichtgroesse.csv', data, header='phi[rad],F[N],RF[V]', fmt='%i,%1.2f,%1.3f')
# Nicht so wie hier die alten Daten überschreiben!
# fmt = format (Genauigkeit,...)

# Ausgleichskurve berechnen
params,pcov = curve_fit(M_fit,phi,M)
a = ufloat(params[0],np.absolute(pcov[0][0])**0.5) #Nm

D = a #Nm

# Einzelne Daten Speichern
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))

if not 'winkelrichtgroesse' in Ergebnisse:
    Ergebnisse['winkelrichtgroesse'] = {}

Ergebnisse['winkelrichtgroesse']['a[Nm]'] = a.n
Ergebnisse['winkelrichtgroesse']['a_err[Nm]'] = a.s
Ergebnisse['winkelrichtgroesse']['D[Nm]'] = D.n
Ergebnisse['winkelrichtgroesse']['D_err[Nm]'] = D.s
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)


# Plot der Ausgleichskurve
phi_linspace = np.linspace(np.min(phi),np.max(phi),100)
plt.plot(phi_linspace, M_fit(phi_linspace,*params), 'k-', label='Ausgleichskurve')
# Plot der Daten
plt.plot(phi, M, 'ro', label='Messwerte')

# Achsenbeschriftung
plt.xlabel(r'$\varphi \:/\: \si{\radian}$')
plt.ylabel(r'$R \cdot F \:/\: \si{\newton\meter}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_winkelrichtgroesse.pdf')
