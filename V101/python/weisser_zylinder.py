import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from scipy import stats
from uncertainties import ufloat

### Kann leider nicht richtig sein, aber erstmal die anderen berechnen

T = np.genfromtxt('data/weisser_zylinder_gemessen.csv',delimiter=',',unpack=True)
T = T #s

# Konstanten
d = 8*10**(-2) #m
H = 13.93*10**(-2) #m
m = 1546.6*10**(-3) #kg

# Mittelwert berechnen
T_mean = ufloat(np.mean(T),stats.sem(T)) #s

# D und I_D auslesen
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))

D = ufloat(Ergebnisse['winkelrichtgroesse']['D'],Ergebnisse['winkelrichtgroesse']['D_err'])

I_D = ufloat(Ergebnisse['eigentraegheit']['I_D'],Ergebnisse['eigentraegheit']['I_D_err'])

# Trägheitsmoment berechnen
I_gemessen = ((T_mean**2)*D)/(2*np.pi)**2 - I_D 

I_Theorie = (1/4)*m*(d/2)**2+(1/12)*m*H**2

DeltaI = I_Theorie-I_gemessen

# Ergebnisse Speichern
if 'weisser_zylinder' not in Ergebnisse:
    Ergebnisse['weisser_zylinder'] = {}

Ergebnisse['weisser_zylinder']['T_mean[s]'] = T_mean.n
Ergebnisse['weisser_zylinder']['T_mean_err[s]'] = T_mean.s
Ergebnisse['weisser_zylinder']['I_gemessen'] = I_gemessen.n
Ergebnisse['weisser_zylinder']['I_gemessen_err'] = I_gemessen.s
Ergebnisse['weisser_zylinder']['I_Theorie'] = I_Theorie
Ergebnisse['weisser_zylinder']['DeltaI'] = DeltaI.n
Ergebnisse['weisser_zylinder']['DeltaI_err'] = DeltaI.s
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)