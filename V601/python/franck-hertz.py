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

# Rohdaten in Spannungsdifferenzen
dU_B = dx*xSkala

# Mittelwert der Spannungsdifferenzen
dU_B_mean = ufloat(np.mean(dU_B),stats.sem(dU_B))

# Tabelle Speichern
data = list(zip(dx,dU_B))
np.savetxt('data/franck-hertz.csv', data, header='dx[Kästchen],dU_b[V]', fmt='%i,%1.2f')

# Ergebnisse speichern
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
if not 'Franck-Hertz' in Ergebnisse:
    Ergebnisse['Franck-Hertz'] = {}
Ergebnisse['Franck-Hertz']['dU_B_mean'] = "{}".format(dU_B_mean)
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)