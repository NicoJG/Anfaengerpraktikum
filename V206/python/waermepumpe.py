import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from uncertainties import ufloat
from scipy import stats

# Funktion für Curve Fit:
def T(t,a,b,c):
    return a*t**2 + b*t + c

def dT(t, a, b):
    return 2*a*t + b

def T_err(t, a, aerr, b, berr, c, cerr):
    return ((2*a*t*aerr)**2 + (t*berr)**2 + (cerr))**0.5

def dT_err(t, a, aerr, b, berr):
    return ((2*t*aerr)**2 + (berr)**2)**0.5

def v(v_w, c_w, dichte_w, cm_k, dT1, N):
    return (v_w * c_w * dichte_w + cm_k) * dT1 * 1/N

def dv(v_w, c_w, dichte_w, cm_k, dT1, ddT1, N, dN):
    return (((v_w * c_w * dichte_w + cm_k) * 1/(N) * ddT1)**2 + (-(v_w * c_w * dichte_w + cm_k) * dT1 * 1/(N**2) * dN)**2)**0.5
# Daten einlesen
t,pa,pb,T1,T2,N = np.genfromtxt('data/waermepumpe.csv',delimiter=',',unpack=True)

#Berechnungen
t = t * 60 #in Sekunden
pa = (pa + 1) * 100000 #in Pascal
pb = (pb + 1) * 100000 #in Pascal
T1 = T1 + 273.15 #in Kelvin
T2 = T2 + 273.15 #in Kelvin
N = N

#Berechnungen für v
dichte_w = 998.21 #kg pro m^3
v_w = 0.003 #m^3 
c_w = 4157.0 #Joule pro Kilo und Kelvin
cm_k = 750.0 #Joule pro Kelvin

#Berechnungen für T1 Err
a = 3.5689 * 10**(-6)
b = -0.0188
c = 295.4911
aerr = 0.1842 * 10**(-6)
berr = 0.0003
cerr = 0.1081

# Ausgleichskurve berechnen
params1,pcov = curve_fit(T,t,T1)
a1 = params1[0]
b1 = params1[1]
c1 = params1[2]

#Fehler berechnen
a1_err = np.absolute(pcov[0][0])**0.5
b1_err = np.absolute(pcov[1][1])**0.5
c1_err = np.absolute(pcov[2][2])**0.5

# Ausgleichskurve berechnen
params2,pcov = curve_fit(T,t,T2)
a2 = params2[0]
b2 = params2[1]
c2 = params2[2]

#Fehler berechnen
a2_err = np.absolute(pcov[0][0])**0.5
b2_err = np.absolute(pcov[1][1])**0.5
c2_err = np.absolute(pcov[2][2])**0.5

# Aufgabe c
# Ableitungen
t_4 = np.array([5,10,15,20])
t_4 = t_4 * 60 
n_4 = np.array([125,125,130,116])
dT1_4 = np.array([0.0230,0.0200,0.0170,0.0130])
ddT1_4 = np.array([0.0003,0.0004,0.0004,0.0005])
n = 117.68 
dn = 4.46

#print("Die 4 Werte für nü: ", v(v_w, c_w, dichte_w, cm_k, dT1_4, n))
#print("Die 4 Werte für dnü: ", dv(v_w, c_w, dichte_w, cm_k, dT1_4, ddT1_4, n, dn))



#print("dT1: ",dT(t_4,a1,b1))
#print("dT2: ",dT(t_4,a2,b2))
#print("N gemittelt: ", np.mean(N))
#print("Fehler von N: ", stats.sem(N))

#print("dT1_err bei 300s: ",dT_err(300, a, aerr, b, berr))
#print("dT1_err bei 600s: ",dT_err(600, a, aerr, b, berr))
#print("dT1_err bei 900s: ",dT_err(900, a, aerr, b, berr))
#print("dT1_err bei 1200s: ",dT_err(1200, a, aerr, b, berr))

#print("a1: ",a1)
#print("Fehler von a1: ", a1_err)
#print("b1: ",b1)
#print("Fehler von b1: ", b1_err)
#print("c1: ",c1)
#print("Fehler von c1: ", c1_err)

#print("a2: ",a2)
#print("Fehler von a2: ", a2_err)
#print("b2: ",b2)
#print("Fehler von b2: ", b2_err)
#print("c2: ",c2)
#print("Fehler von c2: ", c2_err)

# Plot der Ausgleichskurve
t_linspace = np.linspace(np.min(t),np.max(t),100)
plt.plot(t_linspace, T(t_linspace,*params1), 'r-', label='Ausgleichskurve für T1')
plt.plot(t_linspace, T(t_linspace,*params2), 'b-', label='Ausgleichskurve für T2')
# Plot der Daten
plt.plot(t, T1, 'ro', label='Verlauf von T1')
plt.plot(t, T2, 'bo', label='Verlauf von T2')



# Achsenbeschriftung
plt.xlabel(r'$t \:/\: \si{\second}$')
plt.ylabel(r'$T \:/\: \si{\kelvin}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_waermepumpe.pdf')
