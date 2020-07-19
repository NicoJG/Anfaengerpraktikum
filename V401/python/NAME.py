####### Use /default/matplotlibrc and /default/header-matplotlib.tex
import os
import pathlib
os.environ['MATPLOTLIBRC'] = (pathlib.Path(__file__).absolute().parent.parent.parent / 'default' / 'matplotlibrc').__str__()
os.environ['TEXINPUTS'] =  (pathlib.Path(__file__).absolute().parent.parent.parent / 'default').__str__() + ':'
#######
import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from uncertainties import ufloat
from scipy import stats

# Funktion für Curve Fit:
def l(z):
    return 2*0.005/(z * 5.017)

def n(z,p):
    return 1 + (z*lam)/(2*b) * (T)/(T0) * (p0)/(p0 - p)
# Daten einlesen
z = np.genfromtxt('data/wegunterschied.csv',delimiter=',',unpack=True)
p_minus, z_luft = np.genfromtxt('data/luft.csv',delimiter=',',unpack=True)

lam = 693.16 * 10**-9
T0 = 273.15
p0 = 1.0132
b = 0.050
T = 293.15
p = 1 + p_minus

#print(np.mean(n(z_luft, p)))