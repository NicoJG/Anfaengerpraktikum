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
x,y,z = np.genfromtxt('data/NAME.csv',delimiter=',',unpack=True)

#Berechnungen
x_new = x
y_new = y
z_new = x+y

# Daten speichern
data = list(zip(x_new,y_new,z))
np.savetxt('data/NAME.csv', data, header='x[Ohm],y[J],z[V]', fmt='%1.1f,%1.3f,%i')
# Nicht so wie hier die alten Daten überschreiben!
# fmt = format (Genauigkeit,...)

# Ausgleichskurve berechnen
params,pcov = curve_fit(f,x,y)
a = params[0]
b = params[1]

#Fehler berechnen
a_err = np.absolute(pcov[0][0])**0.5
b_err = np.absolute(pcov[1][1])**0.5

# Einzelne Daten Speichern
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
if not 'Kategorie' in Ergebnisse:
    Ergebnisse['Kategorie'] = {}
Ergebnisse['Kategorie']['a[A]'] = a
Ergebnisse['Kategorie']['a_err[A]'] = a_err
Ergebnisse['Kategorie']['b[V]'] = b
Ergebnisse['Kategorie']['b_err[V]'] = b_err
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)


# Plot der Ausgleichskurve
x_linspace = np.linspace(np.min(x),np.max(x),100)
plt.plot(x_linspace, f(x_linspace,*params), 'k-', label='Ausgleichskurve')
# Plot der Daten
plt.plot(x, y, 'ro', label='Kurve')

# Achsenbeschriftung
plt.xlabel(r'$\alpha \:/\: \si{\ohm}$')
plt.ylabel(r'$y \:/\: \si{\micro\joule}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_NAME.pdf')
