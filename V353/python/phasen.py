import numpy as np
import matplotlib.pyplot as plt
import json
from scipy.optimize import curve_fit

f,U_C,a_gemessen,a = np.genfromtxt('data/gemessen_und_a.csv',delimiter=',',unpack=True)

f = f #Hz
a = a*10**(-3) #s

#Berechne die Phasenverschiebung
phi = a*f*2*np.pi

data = list(zip(f,U_C,a_gemessen,a*10**3,phi))

np.savetxt('data/phasen.csv',data,header='f[Hz],U_C[V],a_gemessen[ms],a[ms],phi[]',fmt='%i,%1.3f,%1.3f,%1.3f,%1.3f')

#plot
def f_(x,a):
    return -np.arctan(-2*np.pi*x*a)

params,pcov = curve_fit(f_,f,phi)

RC_Ergebnisse = json.load(open('data/RC_Ergebnisse.json','r'))
RC_Ergebnisse['phase[s]'] = params[0]
RC_Ergebnisse['phase_err[s]'] = np.absolute(pcov[0][0])**0.5
json.dump(RC_Ergebnisse,open('data/RC_Ergebnisse.json','w'),indent=4)

f_linspace = np.linspace(np.min(f),np.max(f),1000)


plt.plot(f_linspace,f_(f_linspace,*params),'k-',label='Ausgleichsrechnung')
plt.plot(f,phi,'ro',label='Gemessen')

plt.xscale('log')

plt.xlabel(r'$f \:/\: \si{\hertz}$')
plt.ylabel(r'$\varphi \:/\: \si{\radian}')

plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
#plt.show()
plt.savefig('build/plot_phasen.pdf')