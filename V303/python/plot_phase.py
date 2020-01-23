import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from uncertainties import ufloat

# Funktion für Curve Fit:
def U_fit(phi,a,b):
    return 2/np.pi * a * np.cos(phi+b)

# Daten einlesen
phi,U,U_noise = np.genfromtxt('data/phasen.csv',delimiter=',',unpack=True)

#Berechnungen
phi = np.radians(phi) #rad

# Ausgleichskurven berechnen
params,pcov = curve_fit(U_fit,phi,U)
a = params[0]
b = params[1]
params_noise,pcov_noise = curve_fit(U_fit,phi,U_noise)
a_noise = params_noise[0]
b_noise = params_noise[1]

#Fehler berechnen
a_err = np.absolute(pcov[0][0])**0.5
b_err = np.absolute(pcov[1][1])**0.5
a_noise_err = np.absolute(pcov_noise[0][0])**0.5
b_noise_err = np.absolute(pcov_noise[1][1])**0.5

# Einzelne Daten Speichern
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))

if not 'phase' in Ergebnisse:
    Ergebnisse['phase'] = {}

Ergebnisse['phase']['a[V]'] = a
Ergebnisse['phase']['a_err[V]'] = a_err
Ergebnisse['phase']['b[V]'] = b
Ergebnisse['phase']['b_err[V]'] = b_err
Ergebnisse['phase']['a_noise[V]'] = a_noise
Ergebnisse['phase']['a_noise_err[V]'] = a_noise_err
Ergebnisse['phase']['b_noise[V]'] = b_noise
Ergebnisse['phase']['b_noise_err[V]'] = b_noise_err
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)

# linspace
phi_linspace = np.linspace(np.min(phi),np.max(phi),100)
#################
# Plot ohne Noise
#################

# Plot der Ausgleichskurve
plt.plot(phi_linspace, U_fit(phi_linspace,*params), 'k-', label='Ausgleichskurve')
# Plot der Daten
plt.plot(phi, U, 'ro', label='Messdaten')

# Achsenbeschriftung
plt.xlabel(r'$\varphi \:/\: \si{\radian}$')
plt.ylabel(r'$U_\text{out} \:/\: \si{\volt}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_phase.pdf')

plt.clf()

#################
# Plot mit Noise
#################

# Plot der Ausgleichskurve
plt.plot(phi_linspace, U_fit(phi_linspace,*params_noise), 'k-', label='Ausgleichskurve')
# Plot der Daten
plt.plot(phi, U_noise, 'ro', label='Messdaten')

# Achsenbeschriftung
plt.xlabel(r'$\varphi \:/\: \si{\radian}$')
plt.ylabel(r'$U_\text{out} \:/\: \si{\volt}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_phase_noise.pdf')
