import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit

# Konstanten
L = 23.9540 * 10**(-3) #H
C = 0.8212 * 10**(-9) #F
R = 48 #Ohm
U = 10 #V
UPlus = 8 #V
UMinus = 7.5 #V

# Theorie Formeln
def I_Theorie(U0,w,Ck): # I(Ck) alles andere sind konstanten bzw. w wird auch berechnet
    Z = w*L - 1/w * (1/C + 1/Ck)
    return U0/np.sqrt(4*w**2 * Ck**2 * R**2 * Z**2 + (1/(w*Ck) - w*Ck*Z**2 + w* R**2 * Ck)**2)

def wMinus_Theorie(L,C,Ck):
    return 1/np.sqrt(L/((1/C)+2/(Ck))) #- 1.5*10**(3)

def wPlus_Theorie(L,C,Ck):
    return 1/np.sqrt(L*C)

# Messwerte
Ck_gemessen , vPlus_gemessen , vMinus_gemessen = np.genfromtxt('frequenzen.csv', delimiter=",", unpack=True)
Ck_gemessen = Ck_gemessen* 10**(-9) #F
vPlus_gemessen = vPlus_gemessen * 10**(3) #Hz
vMinus_gemessen = vMinus_gemessen * 10**(3) #Hz

Ck_gemessen_2 , U2Plus_gemessen, U2Minus_gemessen, Uk_gemessen = np.genfromtxt('amplitude.csv', delimiter=",", unpack=True)
Ck_gemessen_2 = Ck_gemessen_2*10**(-9) #F
I2Plus_gemessen = U2Plus_gemessen / R #A
I2Minus_gemessen = U2Minus_gemessen / R #A
Ik_gemessen = Uk_gemessen / R #A

print(I2Plus_gemessen)
print(I2Minus_gemessen)


Ck_linspace = np.linspace(1.5,12.5,100)*10**(-9) #F


# Plot der Messwerte
plt.plot(Ck_gemessen_2*10**(9), I2Plus_gemessen, 'rx', label=r'I2+ gemessen')
plt.plot(Ck_gemessen_2*10**(9), I2Minus_gemessen, 'yx', label=r'I2- gemessen')

# Plot der Theoriekurve
plt.plot(Ck_linspace*10**(9), I_Theorie(UPlus,wPlus_Theorie(L,C,Ck_linspace),Ck_linspace), 'g-', label=r'I2+ berechnet')
plt.plot(Ck_linspace*10**(9), I_Theorie(UMinus,wMinus_Theorie(L,C,Ck_linspace),Ck_linspace), 'b-', label=r'I2- berechnet')

# Achsenbeschriftung
plt.xlabel(r'$C_\text{k} \:/\: \si{\nano\farad}$')
plt.ylabel(r'$I \:/\: \si{\ampere}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.grid(True,which="both", linestyle='--')

# Speicherort
plt.savefig('build/plot_amplitudentheorie.pdf')