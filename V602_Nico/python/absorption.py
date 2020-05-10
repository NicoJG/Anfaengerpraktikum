####### Use /default/matplotlibrc and /default/header-matplotlib.tex
import os
import pathlib
os.environ['MATPLOTLIBRC'] = (pathlib.Path(__file__).absolute().parent.parent.parent / 'default' / 'matplotlibrc').__str__()
os.environ['TEXINPUTS'] =  (pathlib.Path(__file__).absolute().parent.parent.parent / 'default').__str__() + ':'
#######
import sys
import numpy as np
import matplotlib.pyplot as plt
import json

# Print the full matrix
np.set_printoptions(threshold=sys.maxsize)

# Matrizen initialisieren var[Element][0:Element_size]
theta = np.zeros([6,21]) 
N = np.zeros([6,21]) 

##############################
## Messwerte einlesen
##############################
# Messwerte Zink einlesen
Zn = 0
Zn_size = 16
theta[Zn][0:Zn_size],N[Zn][0:Zn_size] = np.genfromtxt('data/Zink.dat',delimiter=',',unpack=True)

# Messwerte Gallium einlesen
Ga = 1
Ga_size = 21
theta[Ga][0:Ga_size],N[Ga][0:Ga_size] = np.genfromtxt('data/Gallium.dat',delimiter=',',unpack=True)

# Messwerte Brom einlesen
Br = 2
Br_size = 16
theta[Br][0:Br_size],N[Br][0:Br_size] = np.genfromtxt('data/Brom.dat',delimiter=',',unpack=True)

# Messwerte Rubidium einlesen
Rb = 3
Rb_size = 14
theta[Rb][0:Rb_size],N[Rb][0:Rb_size] = np.genfromtxt('data/Rubidium.dat',delimiter=',',unpack=True)

# Messwerte Strontium einlesen
Sr = 4
Sr_size = 16
theta[Sr][0:Sr_size],N[Sr][0:Sr_size] = np.genfromtxt('data/Strontium.dat',delimiter=',',unpack=True)

# Messwerte Zirkonium einlesen
Zr = 5
Zr_size = 16
theta[Zr][0:Zr_size],N[Zr][0:Zr_size] = np.genfromtxt('data/Zirkonium.dat',delimiter=',',unpack=True)

###############################
## Plots
###############################
##Zink
# Plot der Messwerte
plt.plot(theta[Zn][0:Zn_size],N[Zn][0:Zn_size], 'ro', label='Messwerte')

# Achsenbeschriftung
plt.xlabel(r'$\theta \:/\: \si{\degree}$')
plt.ylabel(r'$N \:/\: \si{\frac{Impulse}{\second}}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Plot speichern
plt.savefig('build/plot_zink.pdf')