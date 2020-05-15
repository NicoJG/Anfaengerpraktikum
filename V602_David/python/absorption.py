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

# Daten einlesen
thetagrad1,N1 = np.genfromtxt('data/brom.csv',delimiter=',',unpack=True)
thetagrad2,N2 = np.genfromtxt('data/gallium.csv',delimiter=',',unpack=True)
thetagrad3,N3 = np.genfromtxt('data/rubidium.csv',delimiter=',',unpack=True)
thetagrad4,N4 = np.genfromtxt('data/strontium.csv',delimiter=',',unpack=True)
thetagrad5,N5 = np.genfromtxt('data/zink.csv',delimiter=',',unpack=True)
thetagrad6,N6 = np.genfromtxt('data/zirkonium.csv',delimiter=',',unpack=True)

#Berechnungen
theta1 = np.radians(thetagrad1)
theta2 = np.radians(thetagrad2)
theta3 = np.radians(thetagrad3)
theta4 = np.radians(thetagrad4)
theta5 = np.radians(thetagrad5)
theta6 = np.radians(thetagrad6)

theta1min = np.amin(N1)


# Ausgleichskurve berechnen
#params,pcov = curve_fit(f,thetagrad,N)
#a = params[0]
#b = params[1]

#Fehler berechnen
#a_err = np.absolute(pcov[0][0])**0.5
#b_err = np.absolute(pcov[1][1])**0.5

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
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)


# Plot der Ausgleichskurve
#x_linspace = np.linspace(np.min(thetagrad),np.max(thetagrad),100)
#plt.plot(x_linspace, f(x_linspace,*params), 'k-', label='Ausgleichskurve')
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