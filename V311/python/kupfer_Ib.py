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

Iq, e, d, a = sympy.var('Iq e d a')

f = -Iq / a * e * d 

#print(f)
#print(error(f))
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

print("n und n error: ", n(Iq_neu,e_neu,d_neu,a_neu))

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

print("a: ", a)
print("Fehler von a: ", a_err)
print("b: ", b)
print("Fehler von b: ", b_err)

# Speicherort
plt.savefig('build/plot_kupfer_Ib.pdf')