####### Use /default/matplotlibrc and /default/header-matplotlib.tex
import os
import pathlib
os.environ['MATPLOTLIBRC'] = (pathlib.Path(__file__).absolute().parent.parent.parent / 'default' / 'matplotlibrc').__str__()
os.environ['TEXINPUTS'] =  (pathlib.Path(__file__).absolute().parent.parent.parent / 'default').__str__() + ':'
#######
import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from uncertainties import ufloat

# Funktion für Curve Fit:
def f(x,a,b):
    return a*x+b
def f2(x,a):
    return a*x  
def c(a):
    return 1/a
# Daten einlesen
l2,Ua2,ta2,Ur2,tr2 = np.genfromtxt('data/impulsecho.csv',delimiter=',',unpack=True)

#Berechnungen
l2 = l2/1000 #meter

# Ausgleichskurve berechnen
params,pcov = curve_fit(f,l2,tr2/2)
a = params[0]
b = params[1]

#Fehler berechnen
a_err = np.absolute(pcov[0][0])**0.5
b_err = np.absolute(pcov[1][1])**0.5

a_c = ufloat(a,a_err)

# Einzelne Daten Speichern
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
if not 'Impulsech' in Ergebnisse:
    Ergebnisse['Impulsech'] = {}
Ergebnisse['Impulsech']['a[A]'] = a
Ergebnisse['Impulsech']['a_err[A]'] = a_err
Ergebnisse['Impulsech']['b[V]'] = b
Ergebnisse['Impulsech']['b_err[V]'] = b_err
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)

#print("C_I: ",c(a_c) )

# Plot der Ausgleichskurve
x_linspace = np.linspace(np.min(l2),np.max(l2),100)
plt.plot(x_linspace, f(x_linspace,*params), 'k-', label='Ausgleichskurve')
# Plot der Daten
plt.plot(l2, tr2/2, 'ro', label='Messwerte')

# Achsenbeschriftung
plt.xlabel(r'$l \:/\: \si{\meter}$')
plt.ylabel(r'$t \:/\: \si{\micro\second}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_impulsecho.pdf')

plt.clf()

G = np.log(Ur2/Ua2)

# Ausgleichskurve berechnen
params2,pcov2 = curve_fit(f2,l2,G)
a2 = params2[0]
#b2 = params2[1]

#Fehler berechnen
a2_err = np.absolute(pcov2[0][0])**0.5
#b2_err = np.absolute(pcov2[1][1])**0.5

# Einzelne Daten Speichern
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
if not 'Impuls2' in Ergebnisse:
    Ergebnisse['Impuls2'] = {}
Ergebnisse['Impuls2']['a[A]'] = a2
Ergebnisse['Impuls2']['a_err[A]'] = a2_err
#Ergebnisse['Impuls2']['b[V]'] = b2
#Ergebnisse['Impuls2']['b_err[V]'] = b2_err
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)

# Plot der Ausgleichskurve
x_linspace2 = np.linspace(0,np.max(l2),100)
plt.plot(x_linspace2, f2(x_linspace2,*params2), 'k-', label='Ausgleichskurve')
# Plot der Daten
plt.plot(l2,G , 'bo', label='Messwerte')

# Achsenbeschriftung
plt.xlabel(r'$l \:/\: \si{\meter}$')
plt.ylabel(r'$\ln(\frac{U_\text{R}}{U_\text{A}})')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/plot_impuls2.pdf')
