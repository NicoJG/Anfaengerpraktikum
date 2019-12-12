import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit

def f(x,a,b):
    return a*x + b

U_C,t = np.genfromtxt('data/entladekurve.csv',delimiter=',',unpack=True)
t=t*10**(-3) #Seconds
U_C = U_C #Volts

U_0 = 1 #Spannung bei t=0

tRange = np.linspace(np.min(t),np.max(t),100)
params, pcov = curve_fit(f,t,np.log(U_C))

a = params[0]
a_err = np.absolute(pcov[0][0])**0.5
b = params[1]
b_err = np.absolute(pcov[1][1])**0.5
RC = 1/a
RC_err = (a_err/a)*RC

RC_10 = 1.7*10**(-3)/2.3

#ln(U_c/U_0) speichern
lnUCU0 = np.log(U_C/U_0)

data = list(zip(U_C,t*10**3,lnUCU0))
np.savetxt('data/entladekurve_mit_log.csv',data,header='U_C[V],t[ms],ln(U_C/U_0)[]',fmt='%1.2f,%1.2f,%1.2f')

#Save in RC_Ergebnisse.json
RC_Ergebnisse = json.load(open('data/RC_Ergebnisse.json','r'))
RC_Ergebnisse['entladekurve_a[1/s]'] = a
RC_Ergebnisse['entladekurve_a_err[1/s]'] = a_err
RC_Ergebnisse['entladekurve_b[1/s]'] = b
RC_Ergebnisse['entladekurve_b_err[1/s]'] = b_err
RC_Ergebnisse['entladekurve[s]'] = RC
RC_Ergebnisse['entladekurve_err[s]'] = RC_err
json.dump(RC_Ergebnisse, open('data/RC_Ergebnisse.json','w'), indent=4)

plt.plot(tRange*10**3,f(tRange,*params),'k-', label='Ausgleichsgerade')
plt.plot(t*10**3,np.log(U_C/U_0),'rx', label='Gemessen')
#plt.xlim(np.min(t),np.max(t))
#plt.ylim(np.min(U_C),np.max(U_C))
#plt.yscale('log', basey=np.e)
plt.xlabel(r'$t \:/\: \si{\milli\second}$')
plt.ylabel(r'$\ln\left(\frac{U_C}{U_0}\right)$')
plt.legend(loc='best')

plt.grid(True,which="both", linestyle='--')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
#plt.show()
plt.savefig('build/plot_entladekurve.pdf')