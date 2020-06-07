####### Use /default/matplotlibrc and /default/header-matplotlib.tex
import os
import pathlib
os.environ['MATPLOTLIBRC'] = (pathlib.Path(__file__).absolute().parent.parent.parent / 'default' / 'matplotlibrc').__str__()
os.environ['TEXINPUTS'] =  (pathlib.Path(__file__).absolute().parent.parent.parent / 'default').__str__() + ':'
#######
import numpy as np
from uncertainties import ufloat
import json
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

Pos,U250,U300,U350,U400,U450 = np.genfromtxt('data/verschiebung.csv', delimiter=',', unpack=True)

U_B = np.array([250,300,350,400,450]) #V
U_D = np.array([U250, U300, U350, U400, U450])

# Umrechnung
Inch = 2.54 #cm
Kaestchenbreite = Inch/4
D = Pos*Kaestchenbreite # cm

# Ausgleichsgeraden Berechnen
def D_fit(U_D,a,b):
    return a*U_D + b

a = []
a_err = []
b = []
b_err = []

for i in range(0,U_B.size):
    params,pcov = curve_fit(D_fit,U_D[i][1:D.size],D[1:D.size])
    a.append(params[0])
    a_err.append(np.absolute(pcov[0][0])**0.5)
    b.append(params[1])
    b_err.append(np.absolute(pcov[1][1])**0.5)

# Ergebnisse als Tabelle speichern
data = list(zip(U_B,a,a_err,b,b_err))
np.savetxt('data/verschiebung_ausgleichsrechnung.csv', data, header='U_B[V],a[cm/V],b[cm]', fmt='%i,%1.4f+-%1.4f,%1.3f+-%1.3f')


###########################
## Plots der Verschiebung
###########################

print('Plot der Verschiebung')

colors = ['blue','orange','green','red','violet']

for i in range(0,U_B.size):
    U_D_linspace = np.linspace(np.min(U_D[i])-1,np.max(U_D[i])+1,3)
    # Plot der Ausgleichsgerade
    plt.plot(U_D_linspace,D_fit(U_D_linspace,a[i],b[i]), color=colors[i], linestyle='-', label=r'Ausgleichsgerade für $U_B=\SI{{{U_B}}}{{\volt}}$'.format(U_B=U_B[i]))

for i in range(0,U_B.size):
    # Plot der Messwerte
    plt.plot(U_D[i],D, 'o', color=colors[i], label=r'Messwerte für $U_B=\SI{{{U_B}}}{{\volt}}$'.format(U_B=U_B[i]))

# Achsenbeschriftung
plt.xlabel(r'$U_D \:/\: \si{\volt}$')
plt.ylabel(r'$D \:/\: \si{\centi\meter}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend(fontsize='x-small')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_verschiebung.pdf')
plt.clf()

##################################
## Empfindlichkeit
##################################

print('Plot der Empfindlichkeit')

# Ausgleichsgerade berechnen
def a_fit(U_B,p1,p2):
    return p1/U_B + p2

params,pcov = curve_fit(a_fit,U_B,a,sigma=a_err)
p1 = ufloat(params[0],np.absolute(pcov[0][0])**0.5)
p2 = ufloat(params[1],np.absolute(pcov[1][1])**0.5)

# Theoriewert bestimmen
p = 1.9 #cm
L = 14.3 #cm
d = 0.38 #cm
pLdurch2d = p*L/(2*d) # cm

## Ergebnisse Speichern JSON
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
if not 'Verschiebung' in Ergebnisse:
    Ergebnisse['Verschiebung'] = {}
Ergebnisse['Verschiebung']['p1[cm]'] = '{}'.format(p1)
Ergebnisse['Verschiebung']['p2[cm]'] = '{}'.format(p2)
Ergebnisse['Verschiebung']['pLdurch2d[cm]'] = '{}'.format(pLdurch2d)
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)

##################################
## Plot der Empfindlichkeit
##################################

# Plot der Ausgleichsgerade
U_B_linspace = np.linspace(np.min(U_B),np.max(U_B),3)
plt.plot(1/U_B_linspace,a_fit(U_B_linspace,*params), 'k-', label='Ausgleichsgerade')

# Plot der Steigungen
plt.errorbar(1/U_B,a,yerr=a_err, fmt='ro', label='Berechnete Steigungen')

# Achsenbeschriftung
plt.xlabel(r'$\frac{1}{U_B} \:/\: \si{\per\volt}$')
plt.ylabel(r'$a \:/\: \si{\frac{\centi\meter}{\volt}}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_empfindlichkeit.pdf')

