import numpy as np
import json
from uncertainties import ufloat
from scipy import stats

# Messdaten einlesen
N = np.genfromtxt('data/Untergrund.csv',delimiter=',',unpack=True)

# Mittelwert und Standardfehler berechnen
N_mean = ufloat(np.mean(N),stats.sem(N))

# Pro Sekunde
t = 300 #s Integrationszeit
N_per_s = N_mean/t

# Ergebnisse Speichern Json
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
Ergebnisse['Untergrundrate[Imp/300s]'] = '{}'.format(N_mean)
Ergebnisse['Untergrundrate[Imp/s]'] = '{}'.format(N_per_s)
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)