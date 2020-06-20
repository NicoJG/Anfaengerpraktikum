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

# Daten einlesen
l1,Ua1,ta1,Ur1,tr1 = np.genfromtxt('data/durchschallung.csv',delimiter=',',unpack=True)
l2,Ua2,ta2,Ur2,tr2 = np.genfromtxt('data/impulsecho.csv',delimiter=',',unpack=True)

#Berechnungen


# Ausgleichskurve berechnen
params,pcov = curve_fit(f,l2/100,tr2/2)
a = params[0]
b = params[1]

#Fehler berechnen
a_err = np.absolute(pcov[0][0])**0.5
b_err = np.absolute(pcov[1][1])**0.5

# Einzelne Daten Speichern
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
if not 'Impulsech' in Ergebnisse:
    Ergebnisse['Impulsech'] = {}
Ergebnisse['Impulsech']['a[A]'] = a
Ergebnisse['Impulsech']['a_err[A]'] = a_err
Ergebnisse['Impulsech']['b[V]'] = b
Ergebnisse['Impulsech']['b_err[V]'] = b_err
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)


# Plot der Ausgleichskurve
x_linspace = np.linspace(np.min(l2/100),np.max(l2/100),100)
plt.plot(x_linspace, f(x_linspace,*params), 'k-', label='Ausgleichskurve')
# Plot der Daten
plt.plot(l2/100, tr2/2, 'ro', label='Kurve')

# Achsenbeschriftung
plt.xlabel(r'$l \:/\: \si{\centi\meter}$')
plt.ylabel(r'$t \:/\: \si{\second}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_impulsecho.pdf')
