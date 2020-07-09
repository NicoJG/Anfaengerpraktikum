import numpy as np
from uncertainties import ufloat
from scipy import stats
import json

# Rohdaten einlesen
dx = np.genfromtxt('data/franck-hertz_rohdaten.csv', delimiter=',', unpack=True)

# Konstanten der Messung
T = 180 #°C
xSkalaKaestchen = 194 # Kästchen
xSkalaSpannung = 60 # V
xSkala = xSkalaSpannung/xSkalaKaestchen

# Naturkonstanten
e = 1.602*10**(-19) # C
eV = 1.602*10**(-19) # eV
c = 2.998*10**8 # m/s
h = 4.136*10**(-15) # eV/s

# Rohdaten in Spannungsdifferenzen
dU_B = dx*xSkala

# Mittelwert der Spannungsdifferenzen
dU_B_mean = ufloat(np.mean(dU_B),stats.sem(dU_B))

# erste Anregungsenergie
E_01 = e*dU_B_mean/eV # eV aber ist genau dU_B_mean weil eV

# Wellenlänge
l = h*c/E_01

# Tabelle Speichern
data = list(zip(dx,dU_B))
np.savetxt('data/franck-hertz.csv', data, header='dx[Kästchen],dU_b[V]', fmt='%i,%1.2f')

# Ergebnisse speichern
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
if not 'Franck-Hertz' in Ergebnisse:
    Ergebnisse['Franck-Hertz'] = {}
Ergebnisse['Franck-Hertz']['dU_B_mean[V]'] = "{}".format(dU_B_mean)
Ergebnisse['Franck-Hertz']['E_01[eV]'] = "{}".format(E_01)
Ergebnisse['Franck-Hertz']['lambda[m]'] = "{}".format(l)
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)