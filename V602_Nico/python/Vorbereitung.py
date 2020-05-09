import numpy as np


# Kupfer:
K_a =  8048 #eV
K_b = 8905 #eV

# Naturkonstanten
eV = 1.602*10**(-19) #J
h_J = 6.626*10**(-34) #J s
h = 4.136*10**(-15) #eV s
c = 2.998*10**(8) #m/s
# Naturkonstanten 2
R_inf = 13.6 # eV
alpha = 7.297*10**(-3)

# Messkonstanten
d = 2.014*10**(-10) #m
n = 1

# Wellenlänge berechnen
lambda_a = h*c / K_a
lambda_b = h*c / K_b

# Braggwinkel
theta_a = np.degrees(np.arcsin(n*lambda_a/(2*d))) # °
theta_b = np.degrees(np.arcsin(n*lambda_b/(2*d))) # °

print("theta_a: ", theta_a)
print("theta_b: ", theta_b)

# 2)
#data = np.genfromtxt('data/Vorbereitung.csv',delimiter=',',unpack=True,dtype=['U8',np.int,np.float])
#print(data)
#print(type(data[5]))
#print(type(np.genfromtxt('data/Vorbereitung.csv',delimiter=',',unpack=True)[1][1]))
# Elem,Z,E = np.genfromtxt('data/Vorbereitung.csv',delimiter=',',unpack=True)
#Elem,Z,E = data

Elem = np.genfromtxt('data/Vorbereitung.csv',delimiter=',',unpack=True,usecols=0,dtype='<U2')
Z,E = np.genfromtxt('data/Vorbereitung.csv',delimiter=',',unpack=True,usecols=(1,2))

# Berechnungen
E = E*10**3 # eV
l = h*c / E # m Wellenlänge
theta = np.degrees(np.arcsin(n*l/(2*d))) # °


sigma_K = Z - np.sqrt(E/R_inf - alpha**2*Z**4/4)

# Ergebnisse Speichern
dtype = [('Material','<U2'),('Z',np.int32),('E',np.float64),('theta',np.float64),('sigma',np.float64)]
data = np.array(list(zip(Elem,Z,E*10**(-3),theta,sigma_K)),dtype=dtype)
np.savetxt('data/Vorbereitung_Ergebnis.csv', data, header='Material,Z,E_K[keV],theta[°],sigma_K', fmt='%s,%1.0f,%2.2f,%2.1f,%1.2f')