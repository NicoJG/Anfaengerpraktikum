import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from uncertainties import ufloat
from uncertainties.unumpy import uarray
from uncertainties import unumpy as unp

# Daten einlesen
alpha,N_Al = np.genfromtxt('data/ComptonAl.csv',delimiter=',',unpack=True)
alpha,N_0 = np.genfromtxt('data/ComptonOhne.csv',delimiter=',',unpack=True)

alpha = np.radians(alpha) # rad
N_Al_per_s = N_Al # Impulse / s
N_0_per_s = N_0 # Impulse / s

# Konstanten der Messung
t = 200 # s Integrationszeit
tau = 90 * 10**(-6) # s Totzeit des GM-Zählers
d = 201.4 * 10**(-12) # m Gitterkonstante LiF
n = 1 # Beugungsordnung

# Berechnungen
N_Al = uarray(N_Al_per_s,np.sqrt(N_Al_per_s*t)/t) # Absolute Anzahl der Impulse
N_0 = uarray(N_0_per_s,np.sqrt(N_0_per_s*t)/t)

l = 2*d/n * np.sin(alpha) # m Wellenlänge
I_Al = N_Al/(1-tau*N_Al) # Intensität
I_0 = N_0/(1-tau*N_0) # Intensität
T = I_Al/I_0 # Transmission


# Ausgleichsgerade erstellen
def T_fit(l,a,b):
    return a*l+b
def l_fit(T,a,b):
    return (T-b)/a

params,pcov = curve_fit(T_fit,l,unp.nominal_values(T),sigma=unp.std_devs(T),p0=[-1000000,0.5])
a = ufloat(params[0],np.absolute(pcov[0][0])**0.5)
b = ufloat(params[1],np.absolute(pcov[1][1])**0.5)


###### Compton Wellenlänge
t = 300 #s Integrationszeit
# Messergebnisse
I0 = 2731 # Impulse
I1 = 1180 # Impulse
I2 = 1024 # Impulse

# Unsicherheiten mitnehmen
I0 = ufloat(I0,np.sqrt(I0))
I1 = ufloat(I1,np.sqrt(I1))
I2 = ufloat(I2,np.sqrt(I2))

# Berechnungen
T_1 = I1/I0
T_2 = I2/I0

l_1 = l_fit(T_1,a,b)
l_2 = l_fit(T_2,a,b)
l_c = l_2 - l_1


# Ergebnisse Speichern
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
if not 'Transmission' in Ergebnisse:
    Ergebnisse['Transmission'] = {}
Ergebnisse['Transmission']['a'] = a.n
Ergebnisse['Transmission']['a_err'] = a.s
Ergebnisse['Transmission']['b'] = b.n
Ergebnisse['Transmission']['b_err'] = b.s
Ergebnisse['Transmission']['I0'] = I0.n
Ergebnisse['Transmission']['I0_err'] = I0.s
Ergebnisse['Transmission']['I1'] = I1.n
Ergebnisse['Transmission']['I1_err'] = I1.s
Ergebnisse['Transmission']['I2'] = I2.n
Ergebnisse['Transmission']['I2_err'] = I2.s
Ergebnisse['Transmission']['T_1'] = T_1.n
Ergebnisse['Transmission']['T_1_err'] = T_1.s
Ergebnisse['Transmission']['T_2'] = T_2.n
Ergebnisse['Transmission']['T_2_err'] = T_2.s
Ergebnisse['Transmission']['l_1'] = l_1.n
Ergebnisse['Transmission']['l_1_err'] = l_1.s
Ergebnisse['Transmission']['l_2'] = l_2.n
Ergebnisse['Transmission']['l_2_err'] = l_2.s
Ergebnisse['Transmission']['l_c'] = l_c.n
Ergebnisse['Transmission']['l_c_err'] = l_c.s
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)

# uarrays wieder zurückrechnen
alpha = np.degrees(alpha)
N_Al_err = unp.std_devs(N_Al)
N_Al = unp.nominal_values(N_Al)
N_0_err = unp.std_devs(N_0)
N_0 = unp.nominal_values(N_0)
I_Al_err = unp.std_devs(I_Al)
I_Al = unp.nominal_values(I_Al)
I_0_err = unp.std_devs(I_0)
I_0 = unp.nominal_values(I_0)
T_err = unp.std_devs(T)
T = unp.nominal_values(T)

# Tabelle Speichern
data = np.column_stack([alpha,N_Al,N_Al_err,N_0,N_0_err,I_Al,I_Al_err,I_0,I_0_err,T,T_err])
np.savetxt('data/Compton.csv',data,header='alpha,N_Al,N_0,I_Al,I_0,T',fmt='%.1f,%.1f+-%.1f,%i+-%i,%.1f+-%.1f,%i+-%i,%.3f+-%.3f')

# Plot der Ausgleichsgerade
l_linspace = np.linspace(np.min(l),np.max(l),100)
plt.plot(l_linspace,T_fit(l_linspace,*params), 'k-', label='Ausgleichsgerade')
# Plot der Daten
plt.errorbar(l, unp.nominal_values(T), yerr=unp.std_devs(T), fmt='ro', label='Messdaten')

# Achsenbeschriftung
plt.xlabel(r'$\lambda \:/\: \si{\metre}$')
plt.ylabel(r'$T$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_transmission.pdf')