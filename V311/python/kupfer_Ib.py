import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from uncertainties import ufloat
import uncertainties.unumpy as unp
import sympy



# Funktion für Curve Fit:
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
    return ((e0)**2 *n * tau * vd )/(2 * m0 * j)

def error(f, err_vars=None):
    from sympy import Symbol, latex
    s = 0
    latex_names = dict()
    
    if err_vars == None:
        err_vars = f.free_symbols
        
    for v in err_vars:
        err = Symbol('latex_std_' + v.name)
        s += f.diff(v)**2 * err**2
        latex_names[err] = '\\sigma_{' + latex(v) + '}'
        
    return latex(sympy.sqrt(s), symbol_names=latex_names)

m0, e0, n, tau, vd, j  = sympy.var('m_0 e_0 n tau vd j')

f = ((e0)**2 *n * tau * vd )/(2 * m0 * j)

#print(f)
#print(error(f,err_vars=[n,tau,vd]))
#print()

# Daten einlesen
Ib,Uh = np.genfromtxt('data/kupfer_Ib.csv',delimiter=',',unpack=True)

#Berechnungen
Ib = Ib #Ampere
Uh = Uh #MilliVolt
#Iq = np.array([0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5])

e_neu = -1.602*10**-19 #coulomb
d_neu = 18 *10**-6 #meter
a_neu = ufloat(0.0143,0.0006)
Iq_neu = 10 #ampere
m_neu = 9.11*10**-31 #kg
L_neu = 1.37 #meter
Q_neu = np.pi * ((0.1*10**-3)/2)**2
R_neu = 2.76 #ohm
n_neu = ufloat(2.43*10**26, 0.1*10**26) # 1/meter^3
j_neu = 1*10**-6 #Ampere pro Meter^3
tau_neu = ufloat(1.85*10**-11, 0.08*10**-11)
vd_neu = ufloat(2.57*10**-14,0.11*10**-14)

#print("n und n error: ", n(Iq_neu,e_neu,d_neu,a_neu))
#print("Tau und Tau error: ", T(m_neu,L_neu,e_neu,n_neu,R_neu,Q_neu))
#print("Vdrift und Error: ", V(j_neu,e_neu,n_neu))
print("Mü und Mü Fehler: ", M(e_neu,n_neu,tau_neu,vd_neu,m_neu,j_neu))

#A = ufloat(245.97,9.81)
#B = ufloat(66.23,30.45)

B = np.array([66.23,189.22,312.20,435.19,558.17,681.16,804.14,927.13,1050.11,1173.10,1296.08]) * 10**-3

# Ausgleichskurve berechnen
params,pcov = curve_fit(g,B,Uh)
a = params[0]
b = params[1]

#Fehler berechnen
a_err = np.absolute(pcov[0][0])**0.5
b_err = np.absolute(pcov[1][1])**0.5

# Plot der Ausgleichskurve
x_linspace = np.linspace(np.min(B),np.max(B),100)
plt.plot(x_linspace, g(x_linspace,*params), 'k-', label='Ausgleichskurve')
# Plot der Daten
plt.plot(B, Uh, 'ro', label='Hall-Spannung bei Variation von Ib')

# Achsenbeschriftung
plt.xlabel(r'$B \:/\: \si{\tesla}$')
plt.ylabel(r'$U_H \:/\: \si{\milli\volt}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

#print("a: ", a)
#print("Fehler von a: ", a_err)
#print("b: ", b)
#print("Fehler von b: ", b_err)

# Speicherort
plt.savefig('build/plot_kupfer_Ib.pdf')