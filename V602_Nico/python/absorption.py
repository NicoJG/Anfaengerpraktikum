####### Use /default/matplotlibrc and /default/header-matplotlib.tex
import os
import pathlib
os.environ['MATPLOTLIBRC'] = (pathlib.Path(__file__).absolute().parent.parent.parent / 'default' / 'matplotlibrc').__str__()
os.environ['TEXINPUTS'] =  (pathlib.Path(__file__).absolute().parent.parent.parent / 'default').__str__() + ':'
#######
import math
import numpy as np
import matplotlib.pyplot as plt
import json

# Matrizen initialisieren var[Element][0:Element_size]
theta = np.zeros([6,21]) 
N = np.zeros([6,21]) 
name = ['Zink','Gallium','Brom','Rubidium','Strontium','Zirkonium']
kurz = ['Zn','Ga','Br','Rb','Sr','Zr']
size = [16,21,16,14,16,16] # Anzahl an Messwerte-Paaren
Z = np.array([30,31,35,37,38,40]) # Ordnungszahl

## Messwerte einlesen
for i in range(0,6):
    theta[i][0:size[i]], N[i][0:size[i]] = np.genfromtxt('data/'+name[i]+'.dat',delimiter=',',unpack=True)

# Naturkonstanten
h = 4.136*10**(-15) # eV s
c = 2.998*10**(8) # m/s
R_inf = 13.6 # eV Rydbergkonstante
alpha = 7.297*10**(-3) # Sommerfeldsche Feinstrukturkonstante

# Messkonstanten
d = 201.4 * 10**(-12) # m Gitterkonstante LiF
n = 1 # Beugungsordnung

## Absorptionskante bestimmen
# Indizes der Mitten der Kanten (abgelesen/abgeschätzt)
# .5 meint zwischen 2 Messwerten
i_K = [7, 3.5, 4.5, 6, 6, 5]
# K-Kante als Winkel
theta_K = np.zeros(6)
for i in range(0,6):
    if i_K[i] % 1 == 0:
        theta_K[i] = theta[i][i_K[i]]
    else:
        # die mitte zwischen den Punkten um den Index herum
        theta_K[i] = 0.5*(theta[i][math.ceil(i_K[i])] + theta[i][math.floor(i_K[i])])

# K-Kante als Wellenlänge
l_K = 2*d/n * np.sin(np.deg2rad(theta_K)) # m Wellenlänge

# K-Kante als Energie
E_K = h*c/l_K # eV Photonenenergie

# Abschirmkonstante
sigma_K = Z - np.sqrt(E_K/R_inf - alpha**2*Z**4/4)

###############################
## Ergebnisse speichern Tabelle
###############################
dtype = [('Element','<U2'),('Z',np.int32),('E_K',np.float64),('theta_K',np.float64),('sigma_K',np.float64)]
data = np.array(list(zip(kurz,Z,E_K*10**(-3),theta_K,sigma_K)),dtype=dtype)
np.savetxt('data/Absorption_Ergebnisse.csv', data, header='Element,Z,E_K[keV],theta[°],sigma_K', fmt='%s,%1.0f,%2.2f,%2.2f,%1.2f')


###############################
## Plots der Messwerte
###############################
for i in range(0,6):
    print('Plot: '+name[i])
    # Plot der Messwerte
    plt.plot(theta[i][0:size[i]],N[i][0:size[i]], 'ro', label='Messwerte')

    # Achsenbeschriftung
    plt.xlabel(r'$\theta \:/\: \si{\degree}$')
    plt.ylabel(r'$N \:/\: \si{\frac{Impulse}{\second}}$')

    # in matplotlibrc leider (noch) nicht möglich
    plt.legend()
    plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

    # Plot speichern
    plt.savefig('build/plot_'+name[i]+'.pdf')
    plt.clf()