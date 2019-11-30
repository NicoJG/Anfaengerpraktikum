import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


f,U_C,phi = np.genfromtxt('data/phasen.csv',delimiter=',',unpack=True)
f = f #Hz
U_C = U_C #V
phi = phi #rad

phi_linspace = np.linspace(np.min(phi),np.max(phi),100)

plt.subplot(111,projection='polar')
plt.plot(phi,U_C,'kx',label='Gemessen')
plt.plot(phi_linspace,np.cos(phi_linspace),'k-',label='Erwartet')

#plt.xlabel(r'$f \:/\: \si{\hertz}$')
#plt.ylabel(r'$\varphi')
plt.legend(loc='best')

plt.grid(True,which="both", linestyle='--')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.show()
plt.savefig('build/plot_polar.pdf')