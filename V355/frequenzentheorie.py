import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit

def func(L,C,Ckneu):
    return 1/(2 *np.pi * np.sqrt(L/((1/C)+2/(Ckneu))))


# Daten einlesen
Ck,vg,vg2 = np.genfromtxt('frequenzentheorie.csv',delimiter=',',unpack=True)
vg = vg*1000
L = 23.9540 * 10**(-3)
C = 0.7932 *10**(-9)
Ckneu = Ck*10**(-9)

x= np.linspace(0.5,12,1000)
# Plot der Daten
plt.plot(Ck, vg, 'rx', label=r'v \text{gemessen}')
plt.plot(x, func(L,C,x*10**(-9)), 'b', label=r'v \text{berechnet}')


# Achsenbeschriftung
plt.xlabel(r'$C_\text{k} \:/\: \si{\nano\farad}$')
plt.ylabel(r'$f \:/\: \si{\hertz}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_frequenzentheorie.pdf')



