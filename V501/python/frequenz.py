import numpy as np
import json
from scipy import stats
from uncertainties import ufloat,ufloat_fromstr

# Messdaten einlesen
n,v = np.genfromtxt('data/frequenz.csv',delimiter=',',unpack=True)

# Sinusfrequenz ermitteln
v_sin = ufloat(np.mean(n*v),stats.sem(n*v))

# Ergebnisse von verschiebung.py einlesen
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))

# Peek-to-Peek Sinus
p2p = 1.27 #cm

# Empfindlichkeit
Empfindlichkeit = ufloat_fromstr(Ergebnisse['Verschiebung']['p1[cm]'])

# Beschleunigungsspannung
U_B = 300 #V

# Scheitelwert / Amplitude (Spannung) 
A = (-1)*(p2p*U_B)/(2*Empfindlichkeit)


if not 'Frequenz' in Ergebnisse:
    Ergebnisse['Frequenz'] = {}
Ergebnisse['Frequenz']['v_sin[Hz]'] = '{}'.format(v_sin)
Ergebnisse['Frequenz']['Amplitude[V]'] = '{}'.format(A)
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)