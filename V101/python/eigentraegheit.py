import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from uncertainties import ufloat

# Fit Funktion
def T2(a2,p1,p2): # Gerade für Gl.4
    return p1*a2+p2

# Daten einlesen
a_gemessen,T = np.genfromtxt('data/eigentraegheit_gemessen.csv',delimiter=',',unpack=True)
a_gemessen = a_gemessen*10**(-2) #m
T = T #s

# Konstanten
D_m = 3.51*10**(-2) #m Durchmesser
H = 3*10**(-2) #m
m = 222.9*10**(-3) #kg

# Berechnungen
a_real = a_gemessen + H/2

# Daten speichern
data = list(zip(a_gemessen*10**2,a_real*10**2,T))
np.savetxt('data/eigentraegheit_a_real.csv',data,header='a_gemessen[cm],a_real[cm],T[s]',fmt='%1.1f,%1.1f,%1.2f')

data = list(zip((a_real*10**2)**2,T**2))
np.savetxt('data/eigentraegheit_plot.csv',data,header='a^2[cm^2],T^2[s^2]',fmt='%1.1f,%1.2f')

# Curve Fit
params,pcov = curve_fit(T2,a_real**2,T**2)
p1 = ufloat(params[0],np.absolute(pcov[0][0])**0.5)
p2 = ufloat(params[1],np.absolute(pcov[1][1])**0.5)

# D auslesen
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
D = ufloat(Ergebnisse['winkelrichtgroesse']['D[Nm]'],Ergebnisse['winkelrichtgroesse']['D_err[Nm]'])

# I_D berechnen
I_D = D/(2*np.pi)**2*p2

# Ergebnisse Speichern
if not 'eigentraegheit' in Ergebnisse:
    Ergebnisse['eigentraegheit'] = {}
    
Ergebnisse['eigentraegheit']['p1[s^2/m^2]'] = p1.n
Ergebnisse['eigentraegheit']['p1_err[s^2/m^2]'] = p1.s
Ergebnisse['eigentraegheit']['p2[s^2]'] = p2.n
Ergebnisse['eigentraegheit']['p2_err[s^2]'] = p2.s
Ergebnisse['eigentraegheit']['I_D[kg*m^2]'] = I_D.n
Ergebnisse['eigentraegheit']['I_D_err[kg*m^2]'] = I_D.s
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)

# Plot des Fits
a_linspace = np.linspace(np.min(a_real),np.max(a_real),100)
plt.plot((a_linspace*10**2)**2,T2(a_linspace**2,*params),'k-',label='Ausgleichsgerade')
# Plot der Daten
plt.plot((a_real*10**2)**2, T**2, 'ro', label='Messwerte')

# Achsenbeschriftung
plt.xlabel(r'$a^2 \:/\: \si{\square\centi\meter}$')
plt.ylabel(r'$T^2 \:/\: \si{\square\second}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_eigentraegheit.pdf')
