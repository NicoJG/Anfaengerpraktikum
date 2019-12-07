import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit

F = 4718.8 * 9.81 #Gewichtskraft
L = 0.555 #Meter
I= (0.010**4)/12 #Meter^4
E_vorher = (86.64-1)*10**9 #Pascal

# Funktion für Curve Fit:

def D_Theorie(x,F,E,I,L):
    if x <= (L/2):
        return F/(48* E * I)* (3* L**(2)*x - (4*x**3))
    else:
        return F/(48* E * I)* ((4*x**3) - (12* L * x**2) + (9* L**2 *x) - (L**3))

def D_Theorie_Array(x,F,E,I,L):
    result = np.array([0.0]*x.size)
    for index,xValue in enumerate(x):
        result[index] = D_Theorie(xValue,F,E,I,L)
        #print(D_Theorie(x[index],F,E,I,L))
    #print(result)
    return result

def D_fit(x,E):
    if isinstance(x, (np.ndarray, np.generic) ):
        return D_Theorie_Array(x,F,E,I,L)
    else:
        return D_Theorie(x,F,E,I,L)

# Daten einlesen
x,D0,DM = np.genfromtxt('data/zweiseitig_eckig.csv',delimiter=',',unpack=True)

#Berechnungen
x = x*10**(-3) #m
D0 = D0*10**(-3) #m
DM = DM*10**(-3) #m
D= D0-DM #m

# Ausgleichskurve berechnen
params,pcov = curve_fit(D_fit,x,D,p0=E_vorher)
a = params[0]

#Fehler berechnen
E_err = np.absolute(pcov[0][0])**0.5


# Plot der Daten
plt.plot(x*10**(3), D*10**(3), 'rx', label='Auslenkung')
# Plot der Ausgleichskurve
x_linspace = np.linspace(np.min(x),np.max(x),100)
plt.plot(x_linspace*10**(3), D_fit(x_linspace,*params)*10**3, 'k-', label='Ausgleichskurve')
# Theorie Plot mit dem E Wert aus der anderen Messung (keine Ahnung warum das direkt in mm berechnet wird, eigentlich müsste man ja das Ergebnis *10**3 rechnen...)
plt.plot(x_linspace*10**(3), D_Theorie_Array(x_linspace,F,E_vorher,I,L), 'b-', label='Theorie')


# Achsenbeschriftung
plt.xlabel(r'$x \:/\: \si{\milli\meter}$')
plt.ylabel(r'$D \:/\: \si{\milli\meter}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.grid(True,which="both", linestyle='--')

# Speicherort
plt.savefig('build/plot_zweiseitig_eckig.pdf')

print('E3:',a*10**(-9))
print('Fehler von E3',E_err*10**(-9))