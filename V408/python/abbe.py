####### Use /default/matplotlibrc and /default/header-matplotlib.tex
import os
import pathlib
os.environ['MATPLOTLIBRC'] = (pathlib.Path(__file__).absolute().parent.parent.parent / 'default' / 'matplotlibrc').__str__()
os.environ['TEXINPUTS'] =  (pathlib.Path(__file__).absolute().parent.parent.parent / 'default').__str__() + ':'
#######
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from uncertainties import ufloat
import json

# Messdaten einlesen
g,b,B = np.genfromtxt('data/abbe_neu.csv',delimiter=',',unpack=True)

# Konstanten der Messung
G = 3 # cm

# Abbildungsmaßstab
V = B/G

## Ausgleichsgeraden
def f(x,a,b):
    return a*x + b

# für g
params_g,pcov_g = curve_fit(f,(1+1/V),g)
a_g = ufloat(params_g[0],np.absolute(pcov_g[0][0])**0.5)
b_g = ufloat(params_g[1],np.absolute(pcov_g[1][1])**0.5)

# für b
params_b,pcov_b = curve_fit(f,(1+V),b)
a_b = ufloat(params_b[0],np.absolute(pcov_b[0][0])**0.5)
b_b = ufloat(params_b[1],np.absolute(pcov_b[1][1])**0.5)

################################
## Werte speichern
################################

# mit Json
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
if not 'Abbe' in Ergebnisse:
    Ergebnisse['Abbe'] = {}
Ergebnisse['Abbe']['a_g'] = '{}'.format(a_g)
Ergebnisse['Abbe']['b_g'] = '{}'.format(b_g)
Ergebnisse['Abbe']['a_b'] = '{}'.format(a_b)
Ergebnisse['Abbe']['b_b'] = '{}'.format(b_b)
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)

# als Tabelle
data = list(zip(g,b,B,V,(1+1/V),(1+V)))
np.savetxt('data/abbe_tabelle.csv', data, header='g[cm],b[cm],B[cm],V[],(1+1/V),(1+V)', fmt='%i,%2.1f,%1.1f,%1.3f,%1.3f,%1.3f')


################################
## Plots
################################

## Plot g'
print("Plot nach Abbe für g")

# Plot der Ausgleichsgerade
g_linspace = np.linspace(np.min(1+1/V),np.max(1+1/V),100)
plt.plot(g_linspace, f(g_linspace,*params_g), 'k-', label="Ausgleichsgerade")

# Plot der Daten
plt.plot((1+1/V), g, 'ro', label='Messwerte')

# Achsenbeschriftung
plt.xlabel(r'$(1+1/V)$')
plt.ylabel(r'$g \:/\: \si{\centi\metre}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_abbe_g.pdf')
plt.clf()

## Plot b'
print("Plot nach Abbe für b")

# Plot der Ausgleichsgerade
b_linspace = np.linspace(np.min(1+V),np.max(1+V),100)
plt.plot(b_linspace, f(b_linspace,*params_b), 'k-', label="Ausgleichsgerade")

# Plot der Daten
plt.plot((1+V), b, 'ro', label='Messwerte')

# Achsenbeschriftung
plt.xlabel(r'$(1+V)$')
plt.ylabel(r'$b \:/\: \si{\centi\metre}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_abbe_b.pdf')