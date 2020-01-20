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

tau, vd = sympy.var('tau vd')

f = tau * vd

#print(f)
#print(error(f,err_vars=[tau,vd]))
#print()

# Daten einlesen
Ib,Uh = np.genfromtxt('data/kupfer_Ib.csv',delimiter=',',unpack=True)

#Berechnungen
Ib = Ib #Ampere
Uh = Uh*10**-3 #Volt
#Iq = np.array([0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5])

e_neu = -1.602*10**-19 #coulomb
d_neu = 18*10**-6 #meter
Iq_neu = 10 #ampere
m_neu = 9.11*10**-31 #kg
L_neu = 1.37 #meter
Q_neu = np.pi * 2*10**-9 #meter^2
R_neu = 2.76 #ohm
j_neu = 1*10**6 #Ampere pro Meter^3
h_neu = 6.63*10**-34 


#A = ufloat(245.97,9.81)
#B = ufloat(66.23,30.45)

B = np.array([66.23,189.22,312.20,435.19,558.17,681.16,804.14,927.13,1050.11,1173.10,1296.08]) * 10**-3

# Ausgleichsgerade berechnen
params,pcov = curve_fit(g,B,Uh)
a = params[0]
b = params[1]

#Fehler berechnen
a_err = np.absolute(pcov[0][0])**0.5
b_err = np.absolute(pcov[1][1])**0.5

# Plot der Ausgleichsgerade
x_linspace = np.linspace(np.min(B),np.max(B),100)
plt.plot(x_linspace, g(x_linspace,*params), 'k-', label='Ausgleichsgerade')
# Plot der Daten
plt.plot(B, Uh, 'ro', label='Hall-Spannung bei Variation von Ib')

# Achsenbeschriftung
plt.xlabel(r'$B \:/\: \si{\tesla}$')
plt.ylabel(r'$U_H \:/\: \si{\volt}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)


a_neu = ufloat(a,a_err)
n_neu = ufloat(2.42*10**29, 0.09*10**29) # 1/meter^3
tau_neu = ufloat(2.32*10**-14,0.09*10**-14)
vd_neu = ufloat(2.58*10**-5,0.10*10**-5)
vtotal_neu = ufloat(2.233*10**6,0.028*10**6)

m_atom = 63.5*1.67*10**-27 #kilogram
rho = 8.96 *1000 #kilogram pro m^3
print("z1 und z Fehler: ", z(rho,n_neu,m_atom))

#print("n1 und n1 error: ", n(Iq_neu,e_neu,d_neu,a_neu))
#print("Tau1 und Tau1 error: ", T(m_neu,L_neu,e_neu,n_neu,R_neu,Q_neu))
#print("Vdrift und Error: ", V(j_neu,e_neu,n_neu))
#print("Mü und Mü Fehler: ", M(e_neu,n_neu,tau_neu,vd_neu,m_neu,j_neu))
#print("Vtotal und Fehler: ", VT(h_neu,m_neu,n_neu))
#print("L und L Fehler: ", L(tau_neu, vtotal_neu))


#print("a1: ", a)
#print("Fehler von a1: ", a_err)
#print("b1: ", b)
#print("Fehler von b1: ", b_err)

# Speicherort
plt.savefig('build/plot_kupfer_Ib.pdf')