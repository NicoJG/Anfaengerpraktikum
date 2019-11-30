import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Funktion für Curve Fit:
def f(x,a,b):
    return a*x+b

# Daten einlesen
# x,y = np.genfromtxt('data/DATEN.csv',delimiter=',',unpack=True)
x = np.linspace(0, 10, 10) # als Bsp
y = x+1/2*np.sin(x) # als Bsp

# Ausgleichskurve berechnen
params,pcov = curve_fit(f,x,y)
print(params)
x_linspace = np.linspace(np.min(x),np.max(x),100)

# Plot der Daten
plt.plot(x, y, 'rx', label='Kurve')
# Plot der Ausgleichskurve
plt.plot(x_linspace, f(x_linspace,*params), 'k-', label='Ausgleichskurve')

# Achsenbeschriftung
plt.xlabel(r'$\alpha \:/\: \si{\ohm}$')
plt.ylabel(r'$y \:/\: \si{\micro\joule}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_NAME.pdf')
