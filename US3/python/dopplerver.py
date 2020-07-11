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

def alpha(theta):
    return np.pi/2 - np.arcsin(np.sin(np.deg2rad(theta)) * cL/cP)

def G(dF, alpha):
    return (dF * cL)/(2 * F0 * np.cos(alpha) )
# Daten einlesen
v, f15, f30, f60 = np.genfromtxt('data/dopplerver.csv',delimiter=',',unpack=True)
s, f1, I1, f2, I2 = np.genfromtxt('data/profil.csv',delimiter=',',unpack=True)

#Berechnungen
cL = 1800 #meter pro sekunde
cP = 2700 #meter pro sekunde
F0 = 2000000 #hertz

# Ausgleichskurve berechnen
#params,pcov = curve_fit(f,x,y)
#a = params[0]
#b = params[1]

#Fehler berechnen
#a_err = np.absolute(pcov[0][0])**0.5
#b_err = np.absolute(pcov[1][1])**0.5

# Einzelne Daten Speichern
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
if not 'Winkel' in Ergebnisse:
    Ergebnisse['Winkel'] = {}
Ergebnisse['Winkel']['alpha1'] = alpha(15)
Ergebnisse['Winkel']['alpha2'] = alpha(30)
Ergebnisse['Winkel']['alpha3'] = alpha(60)
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)

#print(G(f15, alpha(15)))
#print(G(f30, alpha(30)))
#print(G(f60, alpha(60)))

# Plot der Ausgleichskurve
#x_linspace = np.linspace(np.min(x),np.max(x),100)
#plt.plot(x_linspace, f(x_linspace,*params), 'k-', label='Ausgleichskurve')
# Plot der Daten

plt.plot(G(f15, alpha(15)), f15/np.cos(alpha(15)), 'ro', label='Messwerte')

# Achsenbeschriftung
plt.xlabel(r'$v \:/\: \si{\frac{\meter}{\second}}$')
plt.ylabel(r'$\frac{\Delta \nu _{15}}{\cos{\alpha}}  \:/\: \si{\hertz}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_dopplerver1.pdf')
plt.clf()

plt.plot(G(f30, alpha(30)), f15/np.cos(alpha(30)), 'ro', label='Messwerte')

# Achsenbeschriftung
plt.xlabel(r'$v \:/\: \si{\frac{\meter}{\second}}$')
plt.ylabel(r'$\frac{\Delta \nu _{30}}{\cos{\alpha}}  \:/\: \si{\hertz}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/plot_dopplerver2.pdf')

plt.clf()

plt.plot(G(f60, alpha(60)), f15/np.cos(alpha(60)), 'ro', label='Messwerte')

# Achsenbeschriftung
plt.xlabel(r'$v \:/\: \si{\frac{\meter}{\second}}$')
plt.ylabel(r'$\frac{\Delta \nu _{60}}{\cos{\alpha}}  \:/\: \si{\hertz}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/plot_dopplerver3.pdf')

plt.clf()

#print('Geschwindigkeit für 1:',G(f1, alpha(15)) )

plt.plot(s,G(f1, alpha(15)), 'ro', label='Werte von v1')
plt.plot(s,G(f2, alpha(15)), 'bo', label='Werte von v2')

# Achsenbeschriftung
plt.xlabel(r'$s \:/\: \si{\milli\meter}$')
plt.ylabel(r'$v  \:/\: \si{\frac{\meter}{\second}}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/plot_profil1.pdf')

plt.clf()

plt.plot(s,I1, 'ro', label='Messwerte von I1')
plt.plot(s,I2, 'bo', label='Messwerte von I2')

# Achsenbeschriftung
plt.xlabel(r'$s \:/\: \si{\milli\meter}$')
plt.ylabel(r'$I  \:/\: \si{\frac{100\volt\squared}{\second}}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/plot_profil3.pdf')
