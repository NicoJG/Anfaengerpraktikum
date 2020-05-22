import numpy as np
import json
from uncertainties import ufloat

# Konstanten der Messung
t = 120 #s Integrationszeit
N1 = 96041 #Imp/t
N12 = 158479 #Imp/t
N2 = 76518 #Imp/t

# In Ufloats
N1 = ufloat(N1,np.sqrt(N1))
N12 = ufloat(N12,np.sqrt(N12))
N2 = ufloat(N2,np.sqrt(N2))

# Umrechnungen in Imp/s
N1 /= t
N12 /= t
N2 /= t

# Totzeit
T = (N1+N2-N12)/(2*N1*N2)

###############################
## Ergebnisse Speichern JSON
###############################
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
if not 'Totzeit' in Ergebnisse:
    Ergebnisse['Totzeit'] = {}
Ergebnisse['Totzeit']['T'] = '{:1.7f}'.format(T)
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)