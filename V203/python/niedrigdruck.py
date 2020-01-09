import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from uncertainties import ufloat

# Funktion für Curve Fit:
# Formel benutzt: ln(p) = -L/R*1/T + const
def f(x,a,b):
    return a*x+b

# Daten einlesen
T,p = np.genfromtxt('data/niedrigdruck.csv',delimiter=',',unpack=True)

#Berechnungen
T = T + 273.15 #Kelvin
p = p*10**(-3) + 1 #bar
p = p*10**5 #Pascal

#Konstanten
p0 = p[0]
R = 8.314 #J / (mol K)

# Curve Fit
params,pcov = curve_fit(f,1/T,np.log(p))
a = ufloat(params[0],np.absolute(pcov[0][0])**0.5)
b = ufloat(params[1],np.absolute(pcov[1][1])**0.5)

# L berechnen
L = -a*R

# Ergebnisse laden
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))

# Ergebnisse in die Dictonary
if not 'niedrigdruck' in Ergebnisse:
    Ergebnisse['niedrigdruck'] = {}

Ergebnisse['niedrigdruck']['a'] = a.n
Ergebnisse['niedrigdruck']['a_err'] = a.s
Ergebnisse['niedrigdruck']['b'] = b.n
Ergebnisse['niedrigdruck']['b_err'] = b.s
Ergebnisse['niedrigdruck']['L'] = L.n
Ergebnisse['niedrigdruck']['L_err'] = L.s

# Ergebnisse Speichern
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)

# Plot der Ausgleichsgerade
T_linspace = np.linspace(np.min(T),np.max(T),100)
plt.plot(1/T_linspace, f(1/T_linspace,*params), 'k-', label='Ausgleichsgerade')

# Plot der Daten
plt.plot(1/T, np.log(p), 'ro', label='gemessene Werte')

# Achsenbeschriftung
plt.xlabel(r'$\frac{1}{T} \:/\: \si{\per\kelvin}$')
plt.ylabel(r'$\ln \left( p \right)$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_niedrigdruck.pdf')
