import numpy as np
import json
from uncertainties import ufloat

#Maße
R_i = ufloat(10,1) #cm
R_a = ufloat(15,1) #cm
h = ufloat(20,1) #cm

#Berechnungen
V = np.pi * h * (R_a**2 - R_i**2)
V_err_selbst = np.pi * np.sqrt( 
    (R_a.n**2 - R_i.n**2)**2 * h.s**2 
    + 4 * h.n**2 * R_a.n**2 * R_a.s**2 
    + 4 * h.n**2 * R_i.n**2 * R_i.s**2 
    )

# Einzelne Daten Speichern
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))

if not 'hohlzylinder' in Ergebnisse:
    Ergebnisse['hohlzylinder'] = {}

Ergebnisse['hohlzylinder']['V'] = V.n
Ergebnisse['hohlzylinder']['V_err'] = V.s
Ergebnisse['hohlzylinder']['V_err_selbst'] = V_err_selbst
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)