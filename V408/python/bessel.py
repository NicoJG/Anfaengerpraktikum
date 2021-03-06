import numpy as np
from uncertainties import ufloat
from scipy import stats
import json

# Messwerte einlesen
e,g1,g2 = np.genfromtxt('data/bessel.csv', delimiter=',', unpack=True)

# Abstand der Linsenpositionen berechnen
d = g2-g1

# Brennweite berechnen
f = (e**2 - d**2)/(4*e)
f_mean = ufloat(np.mean(f),stats.sem(f))

# Ergebnisse Speichern JSON
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
if not 'Bessel' in Ergebnisse:
    Ergebnisse['Bessel'] = {}
Ergebnisse['Bessel']['f_mean[cm]'] = '{}'.format(f_mean)
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)

# Ergebnisse Speichern Tabelle
data = list(zip(e,g1,g2,d,f))
np.savetxt('data/bessel_tabelle.csv', data, header='e[cm],g1[cm],g2[cm],d[cm],f[cm]', fmt='%i,%2.1f,%2.1f,%2.1f,%2.2f')

