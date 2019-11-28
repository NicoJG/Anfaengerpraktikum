import matplotlib.pyplot as plt
import numpy as np

U_C,t = np.genfromtxt('data/entladekurve.csv',delimiter=',',unpack=True)

plt.plot(t,U_C,'ko', label='Abgelesene Punkte')
#plt.xlim(np.min(t),np.max(t))
#plt.ylim(np.min(U_C),np.max(U_C))
#plt.yscale('log', basey=2.0)
plt.xlabel(r'$t \:/\: \si{\milli\second}$')
plt.ylabel(r'$U_C \:/\: \si{\volt}$')
plt.legend(loc='best')

plt.grid(True,which="both", linestyle='--')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.show()
plt.savefig('build/plot_entladekurve.pdf')