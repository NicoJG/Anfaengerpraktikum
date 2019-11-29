import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def U(f,RC):
    return 1/np.sqrt(1+(2*np.pi*f)**2*RC**2)

f,U_C,a_g,a = np.genfromtxt('data/gemessen_und_a.csv',delimiter=',',unpack=True)

f = f #Hz
U_C = U_C #V
U_G = 1 #V

params,pcov = curve_fit(U,f,U_C/U_G)

print(params[0],' s')

f_linspace = np.linspace(np.min(f),np.max(f),100)

plt.plot(f,U_C/U_G,'kx',label='Gemessen')
#plt.plot(f,np.log(U_C/U_G),'kx',label='Gemessen')
plt.plot(f_linspace,U(f_linspace,*params),'k-',label='Ausgleichsrechnung')

plt.xlabel(r'$f \:/\: \si{\hertz}$')
plt.ylabel(r'$\frac{U_C}{U_0} \:/\: \si{\volt}$')
plt.legend(loc='best')

plt.grid(True,which="both", linestyle='--')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.show()
plt.savefig('build/plot_spannungen.pdf')