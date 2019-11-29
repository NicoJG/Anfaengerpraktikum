import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def f(x,a,b):
    return a*x + b

U_C,t = np.genfromtxt('data/entladekurve.csv',delimiter=',',unpack=True)
t=t*10**(-3) #Seconds
U_C = U_C #Volts

U_0 = 1 #Spannung bei t=0

tRange = np.linspace(np.min(t),np.max(t),100)
params, pcov = curve_fit(f,t,np.log(U_C))

print(params)
print(params[0], '1/s')
print('RC=',1/params[0],' s')
print('RC(10%)=',1.7*10**(-3)/2.3,' s')

plt.plot(t*10**3,np.log(U_C/U_0),'kx', label='Gemessen')
plt.plot(tRange*10**3,f(tRange,*params),'k-', label='Ausgleichsgerade')
#plt.xlim(np.min(t),np.max(t))
#plt.ylim(np.min(U_C),np.max(U_C))
#plt.yscale('log', basey=np.e)
plt.xlabel(r'$t \:/\: \si{\milli\second}$')
plt.ylabel(r'$\ln\left(\frac{U_C}{U_0}\right) \:/\: \si{\volt}$')
plt.legend(loc='best')

plt.grid(True,which="both", linestyle='--')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.show()
plt.savefig('build/plot_entladekurve.pdf')