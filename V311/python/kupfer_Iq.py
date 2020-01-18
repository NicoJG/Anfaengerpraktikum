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
Iq,Uh = np.genfromtxt('data/kupfer_Iq.csv',delimiter=',',unpack=True)

#Berechnungen
Iq = Iq #Ampere
Uh = Uh #MilliVolt

B_neu = 1296.08*10**-3 #tesla
e_neu = -1.602*10**-19 #coulomb
d_neu = 18*10**-6 #meter
a_neu = ufloat(0.00137,0.00004)
Iq_neu = 10 #ampere
m_neu = 9.11*10**-31 #kg
L_neu = 1.37 #meter
Q_neu = np.pi * 2*10**-9 #meter^2
R_neu = 2.76 #ohm
n_neu = ufloat(3.28*10**26, 0.10*10**26) # 1/meter^3
j_neu = 1*10**6 #Ampere pro Meter^3
tau_neu = ufloat(1.71*10**-11, 0.05*10**-11)
vd_neu = ufloat(0.0190,0.0006)
h_neu = 6.63*10**-34 
vtotal_neu = ufloat(2.471*10**5,0.025*10**5)

#print("n und n error: ", n(B_neu,e_neu,d_neu,a_neu))
#print("Tau und Tau error: ", T(m_neu,L_neu,e_neu,n_neu,R_neu,Q_neu))
#print("Vdrift und Error: ", V(j_neu,e_neu,n_neu))
#print("Mü und Mü Fehler: ", M(e_neu,n_neu,tau_neu,vd_neu,m_neu,j_neu))
#print("Vtotal und Fehler: ", VT(h_neu,m_neu,n_neu))
#print("L und L Fehler: ", L(tau_neu, vtotal_neu))


# Ausgleichskurve berechnen
params,pcov = curve_fit(f,Iq,Uh)
a = params[0]
b = params[1]

#Fehler berechnen
a_err = np.absolute(pcov[0][0])**0.5
b_err = np.absolute(pcov[1][1])**0.5

# Plot der Ausgleichskurve
x_linspace = np.linspace(np.min(Iq),np.max(Iq),100)
plt.plot(x_linspace, f(x_linspace,*params), 'k-', label='Ausgleichskurve')
# Plot der Daten
plt.plot(Iq, Uh, 'ro', label='Hall-Spannung bei Variation von Iq')

# Achsenbeschriftung
plt.xlabel(r'$I_Q \:/\: \si{\ampere}$')
plt.ylabel(r'$U_H \:/\: \si{\milli\volt}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)


#print("a: ", a)
#print("Fehler von a: ", a_err)
#print("b: ", b)
#print("Fehler von b: ", b_err)

# Speicherort
plt.savefig('build/plot_kupfer_Iq.pdf')