import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from uncertainties import ufloat

# Funktion für Curve Fit:
def f(x,a,b):
    return a*x+b

def I(N):
    return N/(1 - ((90*10**-6)*N))

def L(a):
    return (2*201.4*10**-12)*np.sin(a)

def X(T,a,b):
    return (T - b)/a   
# Daten einlesen
alpha,N0, Nal= np.genfromtxt('data/absorber.csv',delimiter=',',unpack=True)

#Berechnungen
t = 1 #sekunden
N02 = N0 * t
Nal2 = Nal * t
alpha = np.radians(alpha)
T = I(Nal2)/I(N02)

I0 = ufloat(2731,52)
I1 = ufloat(1180,34)
I2 = ufloat(1024,32)

T1 = I1/I0
T2 = I2/I0

a1 = ufloat(-15194732415, 239100069)
b1 = ufloat(1.23,0.01)

d = 201.4 #pikometer 10^-12
lam = L(alpha)

# Ausgleichskurve berechnen
params,pcov = curve_fit(f,lam,T,p0=(-1000,0.5))
a = params[0]
b = params[1]

#Fehler berechnen
a_err = np.absolute(pcov[0][0])**0.5
b_err = np.absolute(pcov[1][1])**0.5


# Plot der Ausgleichskurve
x_linspace = np.linspace(np.min(lam),np.max(lam),100)
plt.plot(x_linspace, f(x_linspace,*params), 'k-', label='Ausgleichskurve')
# Plot der Daten
plt.plot(lam, T, 'ro', label='Messdaten')

# Achsenbeschriftung
plt.xlabel(r'$\lambda \:/\: \si{\meter}$')
plt.ylabel(r'$T$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

#print(a)
#print(a_err)
#print(b)
#print(b_err)

#print(T1)
#print(T2)
#print(X(T1,a1,b1))
#print(X(T2,a1,b1))
#print(X(T2,a1,b1) - X(T1,a1,b1))
# Speicherort
plt.savefig('build/plot_compton.pdf')