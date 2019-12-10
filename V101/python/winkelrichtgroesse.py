import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit

# Funktion für Curve Fit:
def M_fit(phi,D):
    return D*phi

# Daten einlesen
phi,F = np.genfromtxt('data/kraft_gemessen.csv',delimiter=',',unpack=True)

phi = np.radians(phi) #rad
F = F #N

R = 28.7 * 10**(-2) #m
M = R*F

# Daten speichern
#data = list(zip(x_new,y_new,z))
#np.savetxt('data/NAME.csv', data, header='x[Ohm],y[J],z[V]', fmt='%1.1f,%1.3f,%i')
# Nicht so wie hier die alten Daten überschreiben!
# fmt = format (Genauigkeit,...)

# Ausgleichskurve berechnen
params,pcov = curve_fit(M_fit,phi,M)
D = params[0] #Nm

#Fehler berechnen
D_err = np.absolute(pcov[0][0])**0.5

# Einzelne Daten Speichern
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
Ergebnisse['D[Nm]'] = D
Ergebnisse['D_err[Nm]'] = D_err
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)


# Plot der Ausgleichskurve
phi_linspace = np.linspace(np.min(phi),np.max(phi),100)
plt.plot(phi_linspace, M_fit(phi_linspace,*params), 'k-', label='Ausgleichskurve')
# Plot der Daten
plt.plot(phi, M, 'rx', label='Messwerte')

# Achsenbeschriftung
plt.xlabel(r'$\varphi \:/\: \si{\radian}$')
plt.ylabel(r'$R \cdot F \:/\: \si{\newton\meter}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.grid(True,which="both", linestyle='--')

# Speicherort
plt.savefig('build/plot_winkelrichtgroesse.pdf')
