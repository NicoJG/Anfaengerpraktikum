import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

f,U_C,a_gemessen,a = np.genfromtxt('data/gemessen_und_a.csv',delimiter=',',unpack=True)

f = f #Hz
a = a*10**(-3) #s

#Berechne die Phasenverschiebung
phi = a*f*2*np.pi

data = list(zip(f,phi))

np.savetxt('data/phasen.csv',data,header='f[Hz],phi[]',fmt='%i,%1.3f')

#plot
def f_(x,a):
    return np.arctan(-2*np.pi*x*a)

params,pcov = curve_fit(f_,f,phi)

print(params[0],' s')

f_linspace = np.linspace(np.min(f),np.max(f),100)


plt.plot(f,phi,'kx',label='Gemessen')
plt.plot(f_linspace,f_(f_linspace,*params),'k-',label='Ausgleichsrechnung')

plt.xlabel(r'$f \:/\: \si{\hertz}$')
plt.ylabel(r'$\varphi')
plt.legend(loc='best')

plt.grid(True,which="both", linestyle='--')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.show()
plt.savefig('build/plot_phasen.pdf')