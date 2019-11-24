import numpy as np

def I_Theorie(U,w,Ck,R,L,C):
    Z = w*L - 1/w * (1/C + 1/Ck)
    return U/np.sqrt(4*w**2 * Ck**2 * R**2 * Z**2 + (1/(w*Ck) - w*Ck*Z**2 + w* R**2 * Ck)**2)

L = 23.9540 * 10**(-3) #H
C = 0.8212 * 10**(-9) #F
R = 48 #Ohm
U = 10 #V
UPlus = 8 #V
UMinus = 7.5 #V

Ck , vPlus , vMinus = np.genfromtxt('frequenzen.csv', delimiter=",", unpack=True)
Ck = Ck* 10**(-9) #F
vPlus = vPlus * 10**(3) #Hz
vMinus = vMinus * 10**(3) #Hz

Ck_ , U2Plus, U2Minus, Uk = np.genfromtxt('amplitude.csv', delimiter=",", unpack=True)

I2Plus = U2Plus / R
I2Minus = U2Minus / R
Ik = Uk / R

I1 = U / R

I2Plus_Theorie = I_Theorie(UPlus,2*np.pi*vPlus,Ck,R,L,C)
I2Minus_Theorie = I_Theorie(UMinus,2*np.pi*vMinus,Ck,R,L,C)
Ik_Theorie = I1 - I2Minus_Theorie

print('I2Plus: ',I2Plus)
print('I2Plus_Theorie',I2Plus_Theorie)
print()
print('I2Minus: ',I2Minus)
print('I2Minus_Theorie',I2Minus_Theorie)
print()
print('Ik: ',Ik)
print('Ik_Theorie',Ik_Theorie)
