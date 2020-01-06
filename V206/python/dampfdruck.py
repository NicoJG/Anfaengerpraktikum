import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from uncertainties import ufloat
from scipy import stats

# Funktion für Curve Fit:
def p(T,L):
    return  np.exp(-L/8.314 * 1/T)

def p2(x,a,b):
    return a*x+b

def m(c_w, dichte_w, v_w, cm_k, dT2, L):
    return (v_w * c_w * dichte_w + cm_k) * dT2 * 1/L   

def dm(c_w, dichte_w, v_w, cm_k, dT2, ddT2, L, dL):
    return sqrt( ( (v_w * c_w * dichte_w + cm_k) * 1/L * ddT2)^2 + ((v_w * c_w * dichte_w + cm_k) * 1/L * ddT2)^2     )
def N(k, Pa, Pb, rho, Dm):
    return  1/(1-k) * (Pb*(Pa/Pb)**(1/k) - Pa) * 1/rho * Dm

# Daten einlesen
t,pa,pb,T1,T2,N = np.genfromtxt('data/waermepumpe.csv',delimiter=',',unpack=True)

#Berechnungen
t = t * 60 #in Sekunden
pa = (pa + 1) * 100000 #in Pascal
pb = (pb + 1) * 100000 #in Pascal
T1 = T1 + 273.15 #in Kelvin
T2 = T2 + 273.15 #in Kelvin
N = N
R=8.314 #in Joule durch Mol mal Kelvin
p0 = 1

k = 1.14
#Pa_4 = np.array([3.6,2.9,2.5,2.2]) 
#Pb_4 = np.array([7.0,8.5,10.0,11.5])
#rho0 = 5.51 #kilo pro meter^3
dm1 = ufloat(-0.00115,0.00005)
dm2 = ufloat(-0.00099,0.00005)
dm3 = ufloat(-0.00085,0.00005)
dm4 = ufloat(-0.00070,0.00005) #kilogram pro sekunde

print("N1: ", N(1.14, (3.6 + 1.0) * 100000, (7.0 + 1.0) * 100000, 5.51 * 273.15 * (3.6 + 1) * 100000 / ((17 + 273.15) * 100000), dm1)  )
#print("N2: ", N(k, (2.9 + 1.0) * 100000, (8,5 + 1.0) * 100000, 5.51 * 273.15 * (2.9 + 1) * 100000 / ((12.5 + 273.15) * 100000), dm2))
#print("N3: ", N(k, (2.5 + 1.0) * 100000, (10.0 + 1.0) * 100000, 5.51 * 273.15 * (2.5 + 1) * 100000 / ((8.2 + 273.15) * 100000), dm3))
#print("N4: ", (k, (2.2 + 1.0) * 100000, (11.5 + 1.0) * 100000, 5.51 * 273.15 * (2.2 + 1) * 100000 / ((4.8 + 273.15) * 100000), dm4))


# Ausgleichskurve berechnen
#params1,pcov = curve_fit(p2,1/T1,np.log(pb))
#a = params1[0]
#b = params1[1]


#Fehler berechnen
#a_err = np.absolute(pcov[0][0])**0.5
#b_err = np.absolute(pcov[1][1])**0.5

# Aufgabe c
# Ableitungen
#t_4 = np.array([5,10,15,20])
#t_4 = t_4 * 60 
#n_4 = np.array([125,125,130,116])
#dT2_4 = np.array([-0.0167 ,-0.0145,-0.0124,-0.0102])
#ddT1_4 = np.array([0.0003,0.0004,0.0004,0.0005])

#dT2_fehler1 = ufloat(-0.0167,0.0003)
#dT2_fehler2 = ufloat(-0.0145,0.0004)
#dT2_fehler3 = ufloat(-0.0124,0.0004)
#dT2_fehler4 = ufloat(-0.0102,0.0005)

#L_fehler = ufloat(23308.25,990.74)

#print("Fehler 1: ", m(c_w, dichte_w, v_w, cm_k, dT2_fehler1, L_fehler))
#print("Fehler 2: ", m(c_w, dichte_w, v_w, cm_k, dT2_fehler2, L_fehler))
#print("Fehler 3: ", m(c_w, dichte_w, v_w, cm_k, dT2_fehler3, L_fehler))
#print("Fehler 4: ", m(c_w, dichte_w, v_w, cm_k, dT2_fehler4, L_fehler))

#print("Die 4 Massendurchsätze: ", m(c_w, dichte_w, v_w, cm_k, dT2_4, L))

# Plot der Ausgleichskurve
t_linspace = np.linspace(np.min(1/T1),np.max(1/T1),100)
plt.plot(t_linspace, p2(t_linspace,a,b), 'r-', label='Dampfkurve')
# Plot der Daten
plt.plot(1/T1, np.log(pb), 'ro', label='Dampfdruckkurve')

# Achsenbeschriftung
plt.xlabel(r'$\frac{1}{T1} \:/\: \frac{1}{\si{\kelvin}}$')
plt.ylabel(r'$ln(pb/p0)$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Speicherort
plt.savefig('build/plot_dampfdruck.pdf')