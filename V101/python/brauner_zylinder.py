import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from scipy import stats
from uncertainties import ufloat

### Kann leider nicht richtig sein, aber erstmal die anderen berechnen

T = np.genfromtxt('data/brauner_zylinder_gemessen.csv',delimiter=',',unpack=True)
T = T #s

# Konstanten
d = 7.495*10**(-2) #m
L = 3*10**(-2) #m
m = 1119.3*10**(-3) #kg

# Mittelwert berechnen
T_mean = ufloat(np.mean(T),stats.sem(T)) #s

# D und I_D auslesen
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))

D = ufloat(Ergebnisse['winkelrichtgroesse']['D[Nm]'],Ergebnisse['winkelrichtgroesse']['D_err[Nm]'])

I_D = ufloat(Ergebnisse['eigentraegheit']['I_D[kg*m^2]'],Ergebnisse['eigentraegheit']['I_D_err[kg*m^2]'])

# Trägheitsmoment berechnen
I_gemessen = ((T_mean**2)*D)/(2*np.pi)**2 - I_D 

I_Theorie = (1/2)*m*(d/2)**2

DeltaI = I_Theorie-I_gemessen

# Ergebnisse Speichern
if 'brauner_zylinder' not in Ergebnisse:
    Ergebnisse['brauner_zylinder'] = {}

Ergebnisse['brauner_zylinder']['T_mean[s]'] = T_mean.n
Ergebnisse['brauner_zylinder']['T_mean_err[s]'] = T_mean.s
Ergebnisse['brauner_zylinder']['I_gemessen[kg*m^2]'] = I_gemessen.n
Ergebnisse['brauner_zylinder']['I_gemessen_err[kg*m^2]'] = I_gemessen.s
Ergebnisse['brauner_zylinder']['I_Theorie'] = I_Theorie
Ergebnisse['brauner_zylinder']['DeltaI'] = DeltaI.n
Ergebnisse['brauner_zylinder']['DeltaI_err'] = DeltaI.s
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)