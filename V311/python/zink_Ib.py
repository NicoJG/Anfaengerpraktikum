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

def T(m0,e0,n,rho):
    return 2*m0/( (e0)**2 * n * rho )

def V(j,e0,n):
    return -j/(n * e0)

def M(e0,n,tau,vd,m0,j):
    return ((e0)**2 * n * tau * vd )/(2 * m0 * j)

def VT(h,m0,n):
    return ((  (h**2/m0)  *  (((3*n)/(8*np.pi))**2)**(1/3)   )  /m0  )**(1/2)

def L(tau, vd):
    return tau*vd

# Daten einlesen
Ib,Uh = np.genfromtxt('data/zink_Ib.csv',delimiter=',',unpack=True)

#Berechnungen
Ib = Ib #Ampere
Uh = Uh*10**-3 #Volt

B = np.array([66.23,189.22,312.20,435.19,558.17,681.16,804.14,927.13,1050.11,1173.10,1296.08]) * 10**-3

e_neu = -1.602*10**-19 #coulomb
d_neu = 0.037*10**-3 #meter
Iq_neu = 8 #ampere
m_neu = 9.11*10**-31 #kg
L_neu = 1.73 #meter
Q_neu = np.pi * 2*10**-9 #meter^2
rho_neu = 0.06 *10**-6 #ohm
j_neu = 1*10**6 #Ampere pro Meter^3
h_neu = 6.63*10**-34


# Ausgleichsgerade berechnen
params,pcov = curve_fit(f,B,Uh)
a = params[0]
b = params[1]

#Fehler berechnen
a_err = np.absolute(pcov[0][0])**0.5
b_err = np.absolute(pcov[1][1])**0.5

# Plot der Ausgleichsgerade
x_linspace = np.linspace(np.min(B),np.max(B),100)
plt.plot(x_linspace, f(x_linspace,*params), 'k-', label='Ausgleichsgerade')
# Plot der Daten
plt.plot(B, Uh, 'ro', label='Hall-Spannung bei Variation von Ib')

# Achsenbeschriftung
plt.xlabel(r'$B \:/\: \si{\tesla}$')
plt.ylabel(r'$U_H \:/\: \si{\volt}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

a_neu = ufloat(a,a_err)
n_neu = ufloat(7.45*10**28,0.29*10**28) # 1/meter^3
tau_neu = ufloat(1.59*10**-14,0.06*10**-14)
vd_neu = ufloat(8.38*10**-5,0.33*10**-5)
vtotal_neu = ufloat(1.508*10**6,0.020*10**6)

#print("n und n error: ", n(Iq_neu,e_neu,d_neu,a_neu))
#print("Tau3 und Tau3 error: ", T(m_neu,e_neu,n_neu,rho_neu))
# print("Vdrift3 und Error: ", V(j_neu,e_neu,n_neu))
#print("Mü und Mü Fehler: ", M(e_neu,n_neu,tau_neu,vd_neu,m_neu,j_neu))
#print("Vtotal und Fehler: ", VT(h_neu,m_neu,n_neu))
print("L und L Fehler: ", L(tau_neu, vtotal_neu))

#print("a3: ", a)
#print("Fehler von a3: ", a_err)
#print("b3: ", b)
#print("Fehler von b3: ", b_err)


# Speicherort
plt.savefig('build/plot_zink_Ib.pdf')