import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from uncertainties import ufloat

# Funktion für Curve Fit:
def f(x,a,b):
    return a*x+b
def g(x,a,b):
    return a*x+b

def n(Iq,e,d,a):
    return -Iq /(a * e * d)

def B(x):
    return 245.97*x+66.23

def T(m0,L,e0,n,R,Q):
    return 2*m0*L /( (e0)**2 * n * R * Q)

def V(j,e0,n):
    return -j/(n * e0)

def M(e0,n,tau,vd,m0,j):
    return ((e0)**2 * n * tau * vd )/(2 * m0 * j)

def VT(h,m0,n):
    return ((  (h**2/m0)  *  (((3*n)/(8*np.pi))**2)**(1/3)   )  /m0  )**(1/2)

def L(tau, vd):
    return tau*vd
# Daten einlesen
Ib,Uh = np.genfromtxt('data/silber_Ib.csv',delimiter=',',unpack=True)

#Berechnungen
Ib = Ib #Ampere
Uh = Uh #MilliVolt

B = np.array([66.23,189.22,312.20,435.19,558.17,681.16,804.14,927.13,1050.11,1173.10,1296.08]) * 10**-3

e_neu = -1.602*10**-19 #coulomb
d_neu = 18*10**-6 #meter
a_neu = ufloat(0.0143,0.0006)
Iq_neu = 10 #ampere
m_neu = 9.11*10**-31 #kg
L_neu = 1.37 #meter
Q_neu = np.pi * 2*10**-9 #meter^2
R_neu = 2.76 #ohm
n_neu = ufloat(2.43*10**26, 0.1*10**26) # 1/meter^3
j_neu = 1*10**6 #Ampere pro Meter^3
tau_neu = ufloat(1.85*10**-11, 0.08*10**-11)
vd_neu = ufloat(0.0257,0.0011)
h_neu = 6.63*10**-34 
vtotal_neu = ufloat(2.236*10**5,0.031*10**5)

#print("n und n error: ", n(Iq_neu,e_neu,d_neu,a_neu))
#print("Tau und Tau error: ", T(m_neu,L_neu,e_neu,n_neu,R_neu,Q_neu))
#print("Vdrift und Error: ", V(j_neu,e_neu,n_neu))
#print("Mü und Mü Fehler: ", M(e_neu,n_neu,tau_neu,vd_neu,m_neu,j_neu))
#print("Vtotal und Fehler: ", VT(h_neu,m_neu,n_neu))
#print("L und L Fehler: ", L(tau_neu, vtotal_neu))

# Ausgleichskurve berechnen
params,pcov = curve_fit(f,B,Uh)
a = params[0]
b = params[1]

#Fehler berechnen
a_err = np.absolute(pcov[0][0])**0.5
b_err = np.absolute(pcov[1][1])**0.5

# Plot der Ausgleichskurve
x_linspace = np.linspace(np.min(B),np.max(B),100)
plt.plot(x_linspace, f(x_linspace,*params), 'k-', label='Ausgleichskurve')
# Plot der Daten
plt.plot(B, Uh, 'ro', label='Hall-Spannung bei Variation von Ib')

# Achsenbeschriftung
plt.xlabel(r'$B \:/\: \si{\tesla}$')
plt.ylabel(r'$U_H \:/\: \si{\milli\volt}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

print("a: ", a)
print("Fehler von a: ", a_err)
print("b: ", b)
print("Fehler von b: ", b_err)

# Speicherort
plt.savefig('build/plot_silber_Ib.pdf')