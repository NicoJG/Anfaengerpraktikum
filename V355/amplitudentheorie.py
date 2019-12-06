import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit

def I_Theorie(U,w,Ck,R,L,C):
    Z = w*L - 1/w * (1/C + 1/Ck)
    return U/np.sqrt(4*w**2 * Ck**2 * R**2 * Z**2 + (1/(w*Ck) - w*Ck*Z**2 + w* R**2 * Ck)**2)

def func(L,C,c):
    return 2* np.pi/(2 *np.pi * np.sqrt(L/((1/C)+2/(c))))

L = 23.9540 * 10**(-3) #H
C = 0.8212 * 10**(-9) #F
R = 48 #Ohm
U = 10 #V
UPlus = 8 #V
UMinus = 7.5 #V

#Ck , vPlus , vMinus = np.genfromtxt('frequenzen.csv', delimiter=",", unpack=True)
Ck , vMinusgemessen , vMinusTheorie = np.genfromtxt('frequenzentheorie.csv', delimiter=",", unpack=True)
Ck = Ck* 10**(-9) #F
#vPlus = vPlus * 10**(3) #Hz
#vMinus = vMinus * 10**(3) #Hz
vMinusgemessen = vMinusgemessen * 10**(3) #Hz
vMinusTheorie = vMinusTheorie * 10**(3) #Hz

Ck_ , U2Plus, U2Minus, Uk = np.genfromtxt('amplitude.csv', delimiter=",", unpack=True)
#U2Plus = U2Plus * (1/2)
#U2Minus = U2Minus * (1/2)

I2Plus = U2Plus / R
I2Minus = U2Minus / R
Ik = Uk / R

I1 = U / R
wMinus = 2 * np.pi * vMinusTheorie
wPlusTheorie = 35884 * 2 * np.pi

c= np.linspace(2,12,100)


# Plot der Daten
plt.plot(Ck_, I2Plus, 'rx', label=r'I2+ \text{gemessen}')
#plt.plot(Ck_, I2Minus, 'gx', label=r'I2- \text{gemessen}')
plt.plot(c, I_Theorie(UPlus,wPlusTheorie,c*10**(-9),R,L,C), 'y', label=r'I2+ \text{berechnet}')
#plt.plot(c, I_Theorie(UMinus,func(L,C,c*10**(-9)),c*10**(-9),R,L,C), 'b', label=r'I2- \text{berechnet}')

# Achsenbeschriftung
plt.xlabel(r'$C_\text{k} \:/\: \si{\nano\farad}$')
plt.ylabel(r'$I \:/\: \si{\ampere}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_amplitudentheorie.pdf')