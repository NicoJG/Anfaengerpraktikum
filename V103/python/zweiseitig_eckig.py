import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit

F = 4.7188 * 9.81 #Gewichtskraft
L = 0.555 #Meter
I= (0.010**4)/12 #Meter^4
E_vorher = (86.64)*10**9 #Pascal

# Funktion für Curve Fit:

def D_links_fit(x,E):
    return F/(48* E * I)* (3* L**(2)*x - (4*x**3))

def D_rechts_fit(x,E):
    return F/(48* E * I)* ((4*x**3) - (12* L * x**2) + (9* L**2 *x) - (L**3))

# def D_Theorie(x,F,E,I,L):
#     if x <= (L/2):
#         return F/(48* E * I)* (3* L**(2)*x - (4*x**3))
#     else:
#         return F/(48* E * I)* ((4*x**3) - (12* L * x**2) + (9* L**2 *x) - (L**3))

# def D_Theorie_Array(x,F,E,I,L):
#     result = np.array([0.0]*x.size)
#     for index,xValue in enumerate(x):
#         result[index] = D_Theorie(xValue,F,E,I,L)
#         #print(D_Theorie(x[index],F,E,I,L))
#     #print(result)
#     return result

# def D_fit(x,E):
#     #x = x - b
#     if isinstance(x, (np.ndarray, np.generic) ):
#         return D_Theorie_Array(x,F,E,I,L)
#     else:
#         return D_Theorie(x,F,E,I,L)

# Daten einlesen
x,D0,DM = np.genfromtxt('data/zweiseitig_eckig.csv',delimiter=',',unpack=True)

#Berechnungen
x = x*10**(-3) #m
D0 = D0*10**(-3) #m
DM = DM*10**(-3) #m
D= D0-DM #m

# Arrays splitten
x_split = np.split(x,2)
x_links = x_split[0]
x_rechts = x_split[1]
D_split = np.split(D,2)
D_links = D_split[0]
D_rechts = D_split[1]

# Ausgleichskurve berechnen
params_links,pcov_links = curve_fit(D_links_fit,x_links,D_links,p0=E_vorher)
E_links = params_links[0]
params_rechts,pcov_rechts = curve_fit(D_rechts_fit,x_rechts,D_rechts,p0=E_vorher)
E_rechts = params_rechts[0]

#Fehler berechnen
E_links_err = np.absolute(pcov_links[0][0])**0.5
E_rechts_err = np.absolute(pcov_rechts[0][0])**0.5


# Plot der Daten
plt.plot(x*10**(3), D*10**(3), 'ro', label='gemessene Auslenkung')

# Plot der Ausgleichskurve
#x_links_linspace = np.linspace(np.min(x_links),np.max(x_links),100)
x_links_linspace = np.linspace(0,np.max(x_links),100)
plt.plot(x_links_linspace*10**(3), D_links_fit(x_links_linspace,*params_links)*10**3, 'g-', label='Ausgleichskurve links')

x_rechts_linspace = np.linspace(np.min(x_rechts),np.max(x_rechts),100)
plt.plot(x_rechts_linspace*10**(3), D_rechts_fit(x_rechts_linspace,*params_rechts)*10**3, 'b-', label='Ausgleichskurve rechts')

# Theorie Plot mit dem E Wert aus der anderen Messung (keine Ahnung warum das direkt in mm berechnet wird, eigentlich müsste man ja das Ergebnis *10**3 rechnen...)
#plt.plot(x_linspace*10**(3), D_Theorie_Array(x_linspace,F,E_vorher,I,L)*10**3, 'b-', label='Theorie')


# Achsenbeschriftung
plt.xlabel(r'$x \:/\: \si{\milli\meter}$')
plt.ylabel(r'$D \:/\: \si{\milli\meter}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.grid(True,which="both", linestyle='--')

# Speicherort
plt.savefig('build/plot_zweiseitig_eckig.pdf')

print('E3 links[GP]:',E_links*10**(-9))
print('Fehler von E3_links[GP]',E_links_err*10**(-9))
print('E3 rechts[GP]:',E_rechts*10**(-9))
print('Fehler von E3_rechts[GP]',E_rechts_err*10**(-9))
#print('Verschiebung nach rechts[mm]: ',verschiebung*10**(3))