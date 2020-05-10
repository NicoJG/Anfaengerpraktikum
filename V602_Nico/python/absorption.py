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
name = ['Zink','Gallium','Brom','Rubidium','Strontium','Zirkonium']
size = [16,21,16,14,16,16]

## Messwerte einlesen
for i in range(0,6):
    theta[i][0:size[i]],N[i][0:size[i]] = np.genfromtxt('data/'+name[i]+'.dat',delimiter=',',unpack=True)

###############################
## Plots
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