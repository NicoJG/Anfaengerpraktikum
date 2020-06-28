####### Use /default/matplotlibrc and /default/header-matplotlib.tex
import os
import pathlib
os.environ['MATPLOTLIBRC'] = (pathlib.Path(__file__).absolute().parent.parent.parent / 'default' / 'matplotlibrc').__str__()
os.environ['TEXINPUTS'] =  (pathlib.Path(__file__).absolute().parent.parent.parent / 'default').__str__() + ':'
#######
import matplotlib.pyplot as plt
import numpy as np
from uncertainties.unumpy import (nominal_values as noms, std_devs as stds)
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
l1,Ua1,ta1,Ur1,tr1 = np.genfromtxt('data/durchschallung.csv',delimiter=',',unpack=True)

#Berechnungen
l1 = l1/1000 #meter

# Ausgleichskurve berechnen
params,pcov = curve_fit(f,l1,tr1)
a = params[0]
b = params[1]

#Fehler berechnen
a_err = np.absolute(pcov[0][0])**0.5
b_err = np.absolute(pcov[1][1])**0.5

a_c = ufloat(a,a_err)

# Einzelne Daten Speichern
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
if not 'Durchsch' in Ergebnisse:
    Ergebnisse['Durchsch'] = {}
Ergebnisse['Durchsch']['a[A]'] = a
Ergebnisse['Durchsch']['a_err[A]'] = a_err
Ergebnisse['Durchsch']['b[V]'] = b
Ergebnisse['Durchsch']['b_err[V]'] = b_err
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)

#print("C_D: ",c(a_c) )

# Plot der Ausgleichskurve
x_linspace = np.linspace(np.min(l1),np.max(l1),100)
plt.plot(x_linspace, f(x_linspace,*params), 'k-', label='Ausgleichskurve')
# Plot der Daten
plt.plot(l1, tr1, 'ro', label='Messwerte')

# Achsenbeschriftung
plt.xlabel(r'$l \:/\: \si{\meter}$')
plt.ylabel(r'$t \:/\: \si{\micro\second}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_durchschallung.pdf')
plt.clf()

G = np.log(Ur1/Ua1)

# Ausgleichskurve berechnen
params2,pcov2 = curve_fit(f2,l1,G)
a2 = params2[0]
#b2 = params2[1]

#Fehler berechnen
a2_err = np.absolute(pcov2[0][0])**0.5
#b2_err = np.absolute(pcov2[1][1])**0.5

# Einzelne Daten Speichern
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
if not 'Durchsch2' in Ergebnisse:
    Ergebnisse['Durchsch2'] = {}
Ergebnisse['Durchsch2']['a[A]'] = a2
Ergebnisse['Durchsch2']['a_err[A]'] = a2_err
#Ergebnisse['Durchsch2']['b[V]'] = b2
#Ergebnisse['Durchsch2']['b_err[V]'] = b2_err
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)

# Plot der Ausgleichskurve
x_linspace2 = np.linspace(0,np.max(l1),100)
plt.plot(x_linspace2, f2(x_linspace2,*params2), 'k-', label='Ausgleichskurve')
# Plot der Daten
plt.plot(l1,G , 'bo', label='Messwerte')

# Achsenbeschriftung
plt.xlabel(r'$l \:/\: \si{\meter}$')
plt.ylabel(r'$\ln(\frac{U_\text{R}}{U_\text{A}})')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/plot_durchschallung2.pdf')