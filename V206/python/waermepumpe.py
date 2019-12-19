import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from uncertainties import ufloat

# Funktion für Curve Fit:
#def f(x,a,b):
    #return a*x+b

# Daten einlesen
t,pa,pb,T1,T2,N = np.genfromtxt('data/waermepumpe.csv',delimiter=',',unpack=True)

#Berechnungen
t = t * 60 #in Sekunden
pa = (pa + 1) * 100000 #in Pascal
pb = (pb + 1) * 100000 #in Pascal
T1 = T1 + 273.15 #in Kelvin
T2 = T2 + 273.15 #in Kelvin
N = N

# Ausgleichskurve berechnen
#params,pcov = curve_fit(f,x,y)
#a = params[0]
#b = params[1]

#Fehler berechnen
#a_err = np.absolute(pcov[0][0])**0.5
#b_err = np.absolute(pcov[1][1])**0.5

# Plot der Ausgleichskurve
#x_linspace = np.linspace(np.min(x),np.max(x),100)
#plt.plot(x_linspace, f(x_linspace,*params), 'k-', label='Ausgleichskurve')
# Plot der Daten
plt.plot(t, T1, 'ro', label='Verlauf von T1')
plt.plot(t, T2, 'bo', label='Verlauf von T2')

# Achsenbeschriftung
plt.xlabel(r'$\t \:/\: \si{\second}$')
plt.ylabel(r'$T \:/\: \si{\kelvin}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_NAME.pdf')
