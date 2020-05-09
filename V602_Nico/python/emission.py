import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.signal import argrelextrema

# Daten einlesen
theta,N = np.genfromtxt('data/EmissionCu.dat',delimiter=',',unpack=True)

theta = np.radians(theta) # rad
N = N # Impulse / s

# Konstanten der Messung
t = 90 * 10**(-6) # s Totzeit des GM-Zählers
d = 201.4 * 10**(-12) # m Gitterkonstante LiF
n = 1 # Beugungsordnung
Z = 29 # Ordnungszahl Kupfer

# Naturkonstanten
h = 4.136*10**(-15) # eV s
c = 2.998*10**(8) # m/s
R_inf = 13.6 # eV
alpha = 7.297*10**(-3)

# Berechnungen
l = 2*d/n * np.sin(theta) # m Wellenlänge
E = h*c/l # eV Photonenenergie
I = N/(1-t*N) # Intensität

# Maxima finden
i_max = argrelextrema(N, np.greater, order=20)[0] # Indices der relativen Maxima von N

##############################################
# Halbwertsbreite berechnen
def f(x,a,b):
    return a*x+b

def g(y,a,b):
    return (y-b)/a

def ab(x1,y1,x2,y2):
    a = (y2-y1)/(x2-x1)
    b = y1-a*x1
    return (a,b)

# K_beta:
i1 = i_max[1]-2
i2 = i_max[1]-1
i3 = i_max[1]+3
i4 = i_max[1]+4
a1,b1 = ab(l[i1],N[i1],l[i2],N[i2])
a2,b2 = ab(l[i3],N[i3],l[i4],N[i4])

# K_alpha:
i5 = i_max[2]-2
i6 = i_max[2]-1
i7 = i_max[2]+3
i8 = i_max[2]+4
a3,b3 = ab(l[i5],N[i5],l[i6],N[i6])
a4,b4 = ab(l[i7],N[i7],l[i8],N[i8])

# Breite
hbreite_1 = np.abs(g(N[i_max[1]]/2,a1,b1) - g(N[i_max[1]]/2,a2,b2))
hbreite_2 = np.abs(g(N[i_max[2]]/2,a3,b3) - g(N[i_max[2]]/2,a4,b4))
##############################################

# Auflösungsvermögen berechnen
deltaE1 = h*c/hbreite_1
deltaE2 = h*c/hbreite_2
E1 = E[i_max[1]] # beta
E2 = E[i_max[2]] # alpha
A1 = E1/deltaE1
A2 = E2/deltaE2

# Absorbtionsenergie
E_abs = 8987 # eV

# Abschirmkonstanten
sigma_abs = Z - np.sqrt(E_abs/R_inf)
sigma_alpha = Z - np.sqrt(4*((Z-sigma_abs)**2-E2/R_inf))
sigma_beta = Z - np.sqrt(9*((Z-sigma_abs)**2-E1/R_inf))

# Ergebnisse Speichern
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
if not 'Emission' in Ergebnisse:
    Ergebnisse['Emission'] = {}
Ergebnisse['Emission']['K_alpha[eV]'] = E2
Ergebnisse['Emission']['K_beta[eV]'] = E1
Ergebnisse['Emission']['HBreite_alpha[m]'] = hbreite_2
Ergebnisse['Emission']['HBreite_beta[m]'] = hbreite_1
Ergebnisse['Emission']['A_alpha'] = deltaE2
Ergebnisse['Emission']['A_beta'] = deltaE1
Ergebnisse['Emission']['sigma_abs'] = sigma_abs
Ergebnisse['Emission']['sigma_alpha'] = sigma_alpha
Ergebnisse['Emission']['sigma_beta'] = sigma_beta
json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)

# Plot der K-Linien
plt.axvline(l[i_max[2]],-1000,6000, color='r', linestyle='--', linewidth=1, label=r'$K_\alpha$ Linie')
plt.axvline(l[i_max[1]],-1000,6000, color='r', linestyle=':', linewidth=1, label=r'$K_\beta$ Linie')
# Plot Bremsberg Kommentar
plt.annotate('Bremsberg', xy=(l[i_max[0]],500),xycoords='data',
                xytext=(-50, 30), textcoords='offset points',
                arrowprops=dict(arrowstyle="->"))
# Plot der Geraden für die Halbwärtsbreite
x1 = np.array([l[i1],l[i2]])
x2 = np.array([l[i3],l[i4]])
x3 = np.array([l[i5],l[i6]])
x4 = np.array([l[i7],l[i8]])
plt.plot(x1, f(x1,a1,b1), 'g-', linewidth=0.7, label='Hilfsgeraden')
plt.plot(x2, f(x2,a2,b2), 'g-', linewidth=0.7)
plt.plot(x3, f(x3,a3,b3), 'g-', linewidth=0.7)
plt.plot(x4, f(x4,a4,b4), 'g-', linewidth=0.7)
# Plot der horizontalen Geraden für die Halbwärtsbreite
y5 = np.array([N[i_max[1]]/2,N[i_max[1]]/2])
x5 = np.array([g(y5[0],a1,b1),g(y5[0],a2,b2)])
y6 = np.array([N[i_max[2]]/2,N[i_max[2]]/2])
x6 = np.array([g(y6[0],a3,b3),g(y6[0],a4,b4)])
plt.plot(x5, y5, 'b:', linewidth=1, label='Halbwertsbreiten')
plt.plot(x6, y6, 'b:', linewidth=1)
# Plot der Daten
plt.plot(l, N, 'k.', label='Messdaten')

# Achsenbeschriftung
plt.xlabel(r'$\lambda \:/\: \si{\metre}$')
plt.ylabel(r'$N \:/\: \si{Impulse\per\second}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.grid(False)
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_emission.pdf')