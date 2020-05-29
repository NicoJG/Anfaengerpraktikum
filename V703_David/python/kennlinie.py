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
from uncertainties.unumpy import uarray
from uncertainties.unumpy import (nominal_values as noms, std_devs as stds)

# Funktion für Curve Fit:
def f(x,a,b):
    return a*x+b

def tau(N1,N2,N3):
    return (N1 + N2 - N3)/(2*N1*N2)

def Z(I,N):
    return (I)/(e * N)
# Daten einlesen
U,N = np.genfromtxt('data/kennlinie.csv',delimiter=',',unpack=True)
U2,I = np.genfromtxt('data/zaehlrohrstrom.csv',delimiter=',',unpack=True)

I_neu = uarray(I,0.05)

#Berechnungen
N_neu = uarray(N,np.sqrt(N))
N_t = N_neu/60

N1 = ufloat(96041, np.sqrt(96041))/120
N1_2 = ufloat(158479, np.sqrt(158479))/120
N2 = ufloat(76518, np.sqrt(76518))/120     
e = 1.602176634 * 10 **(-19)

Z1 = Z(I_neu[0],N_t[3])
Z2 = Z(I_neu[1],N_t[8])
Z3 = Z(I_neu[2],N_t[13])
Z4 = Z(I_neu[3],N_t[18])
Z5 = Z(I_neu[4],N_t[23])
Z6 = Z(I_neu[5],N_t[28])
Z7 = Z(I_neu[6],N_t[33])
Z8 = Z(I_neu[7],N_t[38])

Z_ges_wert = (noms(Z1),noms(Z2),noms(Z3),noms(Z4),noms(Z5),noms(Z6),noms(Z7),noms(Z8))
Z_ges_err = (stds(Z1),stds(Z2),stds(Z3),stds(Z4),stds(Z5),stds(Z6),stds(Z7),stds(Z8))
Z_ges = uarray(Z_ges_wert,Z_ges_err)
# Ausgleichskurve berechnen
params,pcov = curve_fit(f,U[5:33],noms(N_t[5:33]),sigma=stds(N_t[5:33]))

a = params[0]
b = params[1]

#Fehler berechnen
a_err = np.absolute(pcov[0][0])**0.5
b_err = np.absolute(pcov[1][1])**0.5

a1 = ufloat(a,a_err)
b1 = ufloat(b,b_err)

# Einzelne Daten Speichern
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
if not 'Parameter' in Ergebnisse:
    Ergebnisse['Parameter'] = {}
Ergebnisse['Parameter']['a[A]'] = a
Ergebnisse['Parameter']['a_err[A]'] = a_err
Ergebnisse['Parameter']['b[V]'] = b
Ergebnisse['Parameter']['b_err[V]'] = b_err
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)

#print("Steigung pro 100V: ",((a1*100 + b1) - b1)/b1 )
#print("Totzeit:",tau(N1,N2,N1_2))
#print("Z1: ",Z(I_neu[0],N_t[3])) 
#print("Z2: ",Z(I_neu[1],N_t[8]))
#print("Z3: ",Z(I_neu[2],N_t[13]))
#print("Z4: ",Z(I_neu[3],N_t[18]))
#print("Z5: ",Z(I_neu[4],N_t[23]))
#print("Z6: ",Z(I_neu[5],N_t[28]))
#print("Z7: ",Z(I_neu[6],N_t[33]))
#print("Z8: ",Z(I_neu[7],N_t[38]))

# Plot der Ausgleichskurve
x_linspace = np.linspace(np.min(U[5:33]),np.max(U[5:33]),100)
plt.plot(x_linspace, f(x_linspace,*params), 'k-', label='Ausgleichskurve')
# Plot der Daten
plt.plot(U, noms(N_t), 'ro', label='Kurve')
plt.errorbar(U, noms(N_t), yerr=stds(N_t), fmt='ro', label='Messdaten')
# Achsenbeschriftung
plt.xlabel(r'$U \:/\: \si{\volt}$')
plt.ylabel(r'$N \:/\: \si{\text{Imp}\per\second}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_kennlinie.pdf')
plt.clf()
#
#x_linspace2 = np.linspace(np.min(),np.max(),100)
#plt.plot(x_linspace2, f(x_linspace2,*params), 'k-', label='Ausgleichskurve')

plt.plot(I,Z_ges_wert, 'o', label='Messwerte')
plt.errorbar(I, noms(Z_ges), yerr=stds(Z_ges), fmt='ro', label='Messdaten')
plt.xlabel(r'$I \:/\: \si{\micro\ampere}$')
plt.ylabel(r'$Z$')

plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_zaehlstrom.pdf')
