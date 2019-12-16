import numpy as np
import matplotlib.pyplot as plt
import json
from scipy.optimize import curve_fit
from uncertainties import ufloat

def U(f,a):
    return 1/(np.sqrt(1+(2*np.pi*f)**2*a))

f,U_C,a_g,a = np.genfromtxt('data/gemessen_und_a.csv',delimiter=',',unpack=True)

f = f #Hz
U_C = U_C #V
U_G = 1 #V

params,pcov = curve_fit(U,f,U_C/U_G)

param_a = params[0]
param_a_err = np.absolute(pcov[0][0])**0.5

RC = ufloat(param_a,param_a_err)**0.5

RC_Ergebnisse = json.load(open('data/RC_Ergebnisse.json','r'))
RC_Ergebnisse['spannung_a[s]'] = param_a
RC_Ergebnisse['spannung_a_err[s]'] = param_a_err
RC_Ergebnisse['spannung_RC[s]'] = RC.n
RC_Ergebnisse['spannung_RC_err[s]'] = RC.s
json.dump(RC_Ergebnisse, open('data/RC_Ergebnisse.json','w'), indent=4)

f_linspace = np.linspace(np.min(f),np.max(f),1000)

#plt.plot(f,np.log(U_C/U_G),'kx',label='Gemessen')
plt.plot(f_linspace,U(f_linspace,*params),'k-',label='Ausgleichsrechnung')
plt.plot(f,U_C/U_G,'ro',label='Gemessen')

plt.xscale('log')

plt.xlabel(r'$f \:/\: \si{\hertz}$')
plt.ylabel(r'$\frac{U_C}{U_0}$')

plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
#plt.show()
plt.savefig('build/plot_spannungen.pdf')