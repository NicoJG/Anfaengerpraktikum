####### Use /default/matplotlibrc and /default/header-matplotlib.tex
import os
import pathlib
os.environ['MATPLOTLIBRC'] = (pathlib.Path(__file__).absolute().parent.parent.parent / 'default' / 'matplotlibrc').__str__()
os.environ['TEXINPUTS'] =  (pathlib.Path(__file__).absolute().parent.parent.parent / 'default').__str__() + ':'
#######
import numpy as np
import matplotlib.pyplot as plt

# Rohdaten einlesen
dx,dy = np.genfromtxt('data/elektronen_rohdaten.csv', delimiter=',', unpack=True)

# Konstanten der Messung
U_B = 11 # V
T = 25 # °C
x0 = 0.6 # V
xSkalaKaestchen = 236 # Kästchen
xSkalaSpannung = 9.4 # V
xSkala = xSkalaSpannung/xSkalaKaestchen
y0 = 105 # nA
ySkalaKaestchen = 145 # Kästchen
ySkalaStrom = 60 # nA
ySkala = ySkalaStrom/ySkalaKaestchen

# Messwerte berechnen
U_A = np.zeros(dx.size+1)
U_A[0] = x0
dU_A = dx*xSkala
for i in range(0,dU_A.size):
    U_A[i+1] = U_A[i] + dU_A[i]

I_A = np.zeros(dy.size+1)
I_A[0] = y0
dI_A = dy*ySkala
for i in range(0,dI_A.size):
    I_A[i+1] = I_A[i] - dI_A[i]


# Plot der Integralen Energieverteilung
print("Plot der Integralen Energieverteilung")
plt.plot(U_A, I_A, 'ro', label='Messwerte')
# Achsenbeschriftung
plt.xlabel(r'$U_A \:/\: \si{\volt}$')
plt.ylabel(r'$I_A \:/\: \si{\nano\ampere}$')
# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
# Speicherort
plt.savefig('build/plot_elektronen.pdf')


# Veräbnderung der Messwerte berechnen
# also I(U)-I(U+dU)
#dI_A = I_A[:I_A.size-1] - I_A[1:]

# Plot der Änderung der Energieverteilung
plt.clf()
print("Plot der Änderung der Energieverteilung")
# Plot der Integralen Energieverteilung
plt.plot(U_A[:U_A.size-1], dI_A, 'ro', label='Messwerte')
# Achsenbeschriftung
plt.xlabel(r'$U_A \:/\: \si{\volt}$')
plt.ylabel(r'$\Delta I_A \:/\: \si{\nano\ampere}$')
# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
# Speicherort
plt.savefig('build/plot_elektronen_diff.pdf')


# Werte in Tabelle speichern
dU_A = np.append(dU_A,0)
dI_A = np.append(dI_A,0)
data = list(zip(U_A,dU_A,I_A,dI_A))
np.savetxt('data/elektronen.csv', data, header='U_A[V],dU_A[V],I_A[nA],dI_A[nA]', fmt='%1.2f,%1.2f,%1.2f,%1.2f')