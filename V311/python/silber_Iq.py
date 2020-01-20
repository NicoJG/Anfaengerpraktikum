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

def n(B,e,d,a):
    return -B /(a * e * d)

def z(rho,n,m):
    return rho/(n * m)

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
Iq,Uh = np.genfromtxt('data/silber_Iq.csv',delimiter=',',unpack=True)

#Berechnungen
Iq = Iq #Ampere
Uh = Uh*10**-3 #MilliVolt

B_neu = 1296.08*10**-3 #tesla
e_neu = -1.602*10**-19 #coulomb
d_neu = 0.026*10**-3 #meter
m_neu = 9.11*10**-31 #kg
L_neu = 1.73 #meter
Q_neu = np.pi * 2*10**-9 #meter^2
R_neu = 0.58 #ohm
j_neu = 1*10**6 #Ampere pro Meter^3
h_neu = 6.63*10**-34

# Ausgleichsgerade berechnen
params,pcov = curve_fit(f,Iq,Uh)
a = params[0]
b = params[1]

#Fehler berechnen
a_err = np.absolute(pcov[0][0])**0.5
b_err = np.absolute(pcov[1][1])**0.5

# Plot der Ausgleichsgerade
x_linspace = np.linspace(np.min(Iq),np.max(Iq),100)
plt.plot(x_linspace, f(x_linspace,*params), 'k-', label='Ausgleichsgerade')
# Plot der Daten
plt.plot(Iq, Uh, 'ro', label='Hall-Spannung bei Variation von Iq')

# Achsenbeschriftung
plt.xlabel(r'$I_Q \:/\: \si{\ampere}$')
plt.ylabel(r'$U_H \:/\: \si{\volt}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

#print("a: ", a)
#print("Fehler von a: ", a_err)
#print("b: ", b)
#print("Fehler von b: ", b_err)

a_neu = ufloat(a,a_err)
n_neu = ufloat(2.145*10**28,0.007*10**28) # 1/meter^3
tau_neu = ufloat(1.571*10**-12,0.005*10**-12)
vd_neu = ufloat(0.0002910,0.0000009)
vtotal_neu = ufloat(9.956*10**5,0.011*10**5)

m_atom = 107.9*1.67*10**-27 #kilogram
rho = 10.5 *1000 #kilogram pro m^3
print("z2 und z Fehler: ", z(rho,n_neu,m_atom))

#print("n und n error: ", n(B_neu,e_neu,d_neu,a_neu))
#print("Tau und Tau error: ", T(m_neu,L_neu,e_neu,n_neu,R_neu,Q_neu))
#print("Vdrift und Error: ", V(j_neu,e_neu,n_neu))
#print("Mü und Mü Fehler: ", M(e_neu,n_neu,tau_neu,vd_neu,m_neu,j_neu))
#print("Vtotal und Fehler: ", VT(h_neu,m_neu,n_neu))
#print("L und L Fehler: ", L(tau_neu, vtotal_neu))

# Speicherort
plt.savefig('build/plot_silber_Iq.pdf')