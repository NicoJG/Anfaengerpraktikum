import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from uncertainties import ufloat

# Funktion für Curve Fit:
def f(x,a,b):
    return a*x+b

def Ik(imin,imax):
    return imin + (imax - imin)/2

def E(alpha):
    return (h * c)/(2 *d* np.sin(alpha))

def sigma(E,Z):
    return Z - (E/R_inf - (alph**2 * Z**4)/4)**(0.5)

# Daten einlesen
thetagrad1,N1 = np.genfromtxt('data/brom.csv',delimiter=',',unpack=True)
thetagrad2,N2 = np.genfromtxt('data/gallium.csv',delimiter=',',unpack=True)
thetagrad3,N3 = np.genfromtxt('data/rubidium.csv',delimiter=',',unpack=True)
thetagrad4,N4 = np.genfromtxt('data/strontium.csv',delimiter=',',unpack=True)
thetagrad5,N5 = np.genfromtxt('data/zink.csv',delimiter=',',unpack=True)
thetagrad6,N6 = np.genfromtxt('data/zirkonium.csv',delimiter=',',unpack=True)

#Berechnungen
h = 6.626 *10**-34 #Joule pro Sekunde
c = 299792458 #Meter pro Sekunde
d = 201.4*10**-12
e = 1.602176634 * 10 **(-19)
R_inf = 13.6 * e
alph = 7.297352 * 10**(-3)
z1 = 35
z2 = 31
z3 = 37
z4 = 38
z5 = 30
z6 = 40

theta1 = np.radians(thetagrad1)
theta2 = np.radians(thetagrad2)
theta3 = np.radians(thetagrad3)
theta4 = np.radians(thetagrad4)
theta5 = np.radians(thetagrad5)
theta6 = np.radians(thetagrad6)

thetak1 = 13.2
thetak2 = 17.35
thetak3 = 11.80
thetak4 = 11.1
thetak5 = 18.7
thetak6 = 9.95

Zgesamt = [z1,z2,z3,z4,z5,z6]
Egesamt = [E(np.radians(thetak1)), E(np.radians(thetak2)), E(np.radians(thetak3)),E(np.radians(thetak4)),E(np.radians(thetak5)),E(np.radians(thetak6))]

sigmagesamt = [3.84,3.67,4.11,4.12,3.63,4.28]

# Ausgleichskurve berechnen
params,pcov = curve_fit(f,Zgesamt,np.sqrt(Egesamt))
a = params[0]
b = params[1]

#Fehler berechnen
a_err = np.absolute(pcov[0][0])**0.5
b_err = np.absolute(pcov[1][1])**0.5

#Einzelne Daten Speichern
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
if not 'IK' in Ergebnisse:
    Ergebnisse['IK'] = {}
Ergebnisse['IK']['Brom'] = Ik(np.amin(N1),np.amax(N1))
Ergebnisse['IK']['Gallium'] = Ik(np.amin(N2),np.amax(N2))
Ergebnisse['IK']['Rubidium'] = Ik(np.amin(N3),np.amax(N3))
Ergebnisse['IK']['Strontium'] = Ik(np.amin(N4),np.amax(N4))
Ergebnisse['IK']['Zink'] = Ik(np.amin(N5),np.amax(N5))
Ergebnisse['IK']['Zirkonium'] = Ik(np.amin(N6),np.amax(N6))
if not 'E' in Ergebnisse:
    Ergebnisse['E'] = {}
Ergebnisse['E']['Brom'] = E(np.radians(thetak1))/e
Ergebnisse['E']['Gallium'] = E(np.radians(thetak2))/e
Ergebnisse['E']['Rubidium'] = E(np.radians(thetak3))/e
Ergebnisse['E']['Strontium'] = E(np.radians(thetak4))/e
Ergebnisse['E']['Zink'] = E(np.radians(thetak5))/e
Ergebnisse['E']['Zirkonium'] = E(np.radians(thetak6))/e
if not 'Sigma' in Ergebnisse:
    Ergebnisse['Sigma'] = {}
Ergebnisse['Sigma']['Brom'] = sigma(E(np.radians(thetak1)),z1) 
Ergebnisse['Sigma']['Gallium'] = sigma(E(np.radians(thetak2)),z2) 
Ergebnisse['Sigma']['Rubidium'] = sigma(E(np.radians(thetak3)),z3) 
Ergebnisse['Sigma']['Strontium'] = sigma(E(np.radians(thetak4)),z4) 
Ergebnisse['Sigma']['Zink'] = sigma(E(np.radians(thetak5)),z5) 
Ergebnisse['Sigma']['Zirkonium'] = sigma(E(np.radians(thetak6)),z6)
if not 'Moseley' in Ergebnisse:
    Ergebnisse['Moseley'] = {}
Ergebnisse['Moseley']['a'] = a
Ergebnisse['Moseley']['a_err'] = a_err
Ergebnisse['Moseley']['b'] = b
Ergebnisse['Moseley']['b_err'] = b_err
Ergebnisse['Moseley']['a^2'] = a**2
Ergebnisse['Moseley']['a_err^2'] = a_err**2
Ergebnisse['Moseley']['a^2'] = a**2/e
Ergebnisse['Moseley']['a_err^2'] = a_err**2/e
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)

ryd = ufloat(a,a_err)
print(((ufloat(a,a_err))**2)/e)
print(((ufloat(a,a_err))**2))


# Plot der Daten
plt.plot(thetagrad1, N1, '.', label='Brom')
plt.plot(thetagrad2, N2, '.', label='Gallium')
plt.plot(thetagrad3, N3, '.', label='Rubidium')
plt.plot(thetagrad4, N4, '.', label='Strontium')
plt.plot(thetagrad5, N5, '.', label='Zink')
plt.plot(thetagrad6, N6, '.', label='Zirkonium')

# Achsenbeschriftung
plt.xlabel(r'$\theta \:/\: \si{\degree}$')
plt.ylabel(r'$N \:/\: \frac{\text{Imp}}{\si{\second}}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_absorption.pdf')
plt.clf()

## Plot der Ausgleichskurve
x_linspace = np.linspace(np.min(Zgesamt),np.max(Zgesamt),100)
plt.plot(x_linspace, f(x_linspace,*params), 'k-', label='Ausgleichskurve')

plt.plot(Zgesamt, np.sqrt(Egesamt), 'o', label='Messwerte')

plt.xlabel(r'$Z$')
plt.ylabel(r'$\sqrt{E_\text{K,abs} \:/\: \si{\joule}}$')

plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_rydberg.pdf')