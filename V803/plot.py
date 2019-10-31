import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def f(x,a,b):
    return a*x+b

x,F = np.genfromtxt('data.csv',delimiter=',',unpack=True)

xFit = np.linspace(0,60,50)
params, pcov = curve_fit(f,x,F)

plt.plot(xFit, f(xFit,*params), 'b-', label="Ausgleichsgerade")
plt.plot(x, F, 'ko', label='Messdaten')

plt.xlabel(r'$x \:/\: \si{\centi\meter}$')
plt.ylabel(r'$F \:/\: \si{\joule}$')
plt.legend(loc='best')


# in matplotlibrc leider (noch) nicht möglich
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/plot.pdf')
