import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from uncertainties import ufloat

def p_fit(T,a,b,c,d):
    return a*T**3 + b*T**2 + c*T + d

# Daten einlesen
T,p = np.genfromtxt('data/hochdruck.csv',delimiter=',',unpack=True)

#Berechnungen
T = T + 273.15 #Kelvin
p = p + 1 #bar
p = p*10**5 #Pascal

# Curve Fit
params,pcov = curve_fit(p_fit,T,p)

# Parameter
a = ufloat(params[0],np.absolute(pcov[0][0])**0.5)
b = ufloat(params[1],np.absolute(pcov[1][1])**0.5)
c = ufloat(params[2],np.absolute(pcov[2][2])**0.5)
d = ufloat(params[3],np.absolute(pcov[3][3])**0.5)


# Ergebnisse laden
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))

# Ergebnisse in die Dictonary
if not 'hochdruck' in Ergebnisse:
    Ergebnisse['hochdruck'] = {}

Ergebnisse['hochdruck']['a'] = a.n
Ergebnisse['hochdruck']['a_err'] = a.s
Ergebnisse['hochdruck']['b'] = b.n
Ergebnisse['hochdruck']['b_err'] = b.s
Ergebnisse['hochdruck']['c'] = c.n
Ergebnisse['hochdruck']['c_err'] = c.s
Ergebnisse['hochdruck']['d'] = d.n
Ergebnisse['hochdruck']['d_err'] = d.s

# Ergebnisse Speichern
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)

# Plot der Ausgleichskurve
T_linspace = np.linspace(np.min(T),np.max(T),100)
plt.plot(T_linspace, p_fit(T_linspace,*params)*10**(-6), 'k-', label='Ausgleichskurve')

# Plot der Daten
plt.plot(T, p*10**(-6), 'ro', label='gemessene Werte')

# Achsenbeschriftung
plt.xlabel(r'$T \:/\: \si{\kelvin}$')
plt.ylabel(r'$p \:/\: \si{\mega\pascal}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_hochdruck.pdf')