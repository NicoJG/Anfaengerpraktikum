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
N_Al = N_Al_per_s*t # Absolute Anzahl der Impulse
N_0 = N_0_per_s*t
N_Al = uarray(N_Al,np.sqrt(N_Al)) # Anzahl mit Unsicherheit
N_0 = uarray(N_0,np.sqrt(N_0))
l = 2*d/n * np.sin(alpha) # m Wellenlänge
I_Al = N_Al/1-tau*N_Al # Intensität
I_0 = N_0/1-tau*N_0 # Intensität
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
# Messergebnisse
I_0 = 2731 # Impulse
I_1 = 1180 # Impulse
I_2 = 1024 # Impulse

# Berechnungen
T_1 = I_1/I_0
T_2 = I_2/I_0

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
Ergebnisse['Transmission']['T_1'] = T_1
Ergebnisse['Transmission']['T_2'] = T_2
Ergebnisse['Transmission']['l_1'] = l_1.n
Ergebnisse['Transmission']['l_1_err'] = l_1.s
Ergebnisse['Transmission']['l_2'] = l_2.n
Ergebnisse['Transmission']['l_2_err'] = l_2.s
Ergebnisse['Transmission']['l_c'] = l_c.n
Ergebnisse['Transmission']['l_c_err'] = l_c.s
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)

# print(unp.std_devs(T))
# print(N_Al)

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