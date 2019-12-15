import numpy as np
import json
from scipy import stats
from uncertainties import ufloat

# Ergebnisse laden
Ergebnisse = json.load(open('data/Ergebnisse.json','r'))

# D und I_D auslesen
D = ufloat(Ergebnisse['winkelrichtgroesse']['D'],Ergebnisse['winkelrichtgroesse']['D_err'])
I_D = ufloat(Ergebnisse['eigentraegheit']['I_D'],Ergebnisse['eigentraegheit']['I_D_err'])


#############################
# Puppe Allgemein
#############################

# Konstanten gemessen
L_Arm=13.7*10**(-2) #m
D_Arm=1.3*10**(-2) #m
L_Kopf=6.0*10**(-2) #m
D_Kopf=3.0*10**(-2) #m
D_Torso=4.0*10**(-2) #m
L_Torso=10.0*10**(-2) #m
L_Bein=14.5*10**(-2) #m
D_Bein=1.5*10**(-2) #m
Masse_mit_Stange=168.0*10**(-3) #kg

#Konstanten nicht gemessen
dichte = 430 #kg/m^2 Tannenholz?


# Theorie Massen
m_Kopf = (dichte*np.pi*(D_Kopf/2)**2*L_Kopf)
m_Torso = (dichte*np.pi*(D_Torso/2)**2*L_Torso)
m_Arm = (dichte*np.pi*(D_Arm/2)**2*L_Arm)
m_Bein = (dichte*np.pi*(D_Bein/2)**2*L_Bein)

# Theorie Trägheitsmomente im Schwerpunkt
I_Kopf = (1/2) * m_Kopf * (D_Kopf/2)**2
I_Torso = (1/2) * m_Torso * (D_Torso/2)**2
# Erste Stellung
I_Arm_1 = (1/2) * m_Arm * (D_Arm/2)**2
I_Bein_1 = (1/2) * m_Bein * (D_Bein/2)**2
# Zweite Stellung
I_Arm_2 = (1/4)*m_Arm*(D_Arm/2)**2 + (1/12)*m_Arm*L_Arm**2
I_Bein_2 = (1/4)*m_Bein*(D_Bein/2)**2 + (1/12)*m_Bein*L_Bein**2

# Daten speichern
if not 'puppe' in Ergebnisse:
    Ergebnisse['puppe'] = {}

if not 'allgemein' in Ergebnisse['puppe']:
    Ergebnisse['puppe']['allgemein'] = {}

Ergebnisse['puppe']['allgemein']['m_Kopf[kg]'] = m_Kopf
Ergebnisse['puppe']['allgemein']['m_Torso[kg]'] = m_Torso
Ergebnisse['puppe']['allgemein']['m_Arm[kg]'] = m_Arm
Ergebnisse['puppe']['allgemein']['m_Bein[kg]'] = m_Bein
Ergebnisse['puppe']['allgemein']['I_Kopf'] = I_Kopf
Ergebnisse['puppe']['allgemein']['I_Torso'] = I_Torso
Ergebnisse['puppe']['allgemein']['I_Arm_1'] = I_Arm_1
Ergebnisse['puppe']['allgemein']['I_Bein_1'] = I_Bein_1
Ergebnisse['puppe']['allgemein']['I_Arm_2'] = I_Arm_2
Ergebnisse['puppe']['allgemein']['I_Bein_2'] = I_Bein_2



#############################
# Erste Stellung
#############################


# Periodendauer auslesen und berechnen
T5_1 = np.genfromtxt('data/puppe_1_gemessen.csv',delimiter=',',unpack=True)
T5_mean_1 = ufloat(np.mean(T5_1),stats.sem(T5_1)) #s
T_mean_1 = T5_mean_1/5 #s


# Trägheitsmoment berechnen
I_gemessen_1 = ((T_mean_1**2)*D)/(2*np.pi)**2 - I_D

# Theoriewert
I_Theorie_1 = I_Torso + I_Kopf + 2*(I_Arm_1 + m_Arm*(D_Arm/2+D_Torso/2)**2) + 2*(I_Bein_1 + m_Bein*(D_Bein/2)**2)

DeltaI_1 = I_Theorie_1 - I_gemessen_1

# Daten speichern
if not 'stellung_1' in Ergebnisse['puppe']:
    Ergebnisse['puppe']['stellung_1'] = {}

Ergebnisse['puppe']['stellung_1']['T5_mean[s]'] = T5_mean_1.n
Ergebnisse['puppe']['stellung_1']['T5_mean_err[s]'] = T5_mean_1.s
Ergebnisse['puppe']['stellung_1']['T_mean[s]'] = T_mean_1.n
Ergebnisse['puppe']['stellung_1']['T_mean_err[s]'] = T_mean_1.s
Ergebnisse['puppe']['stellung_1']['I_gemessen'] = I_gemessen_1.n
Ergebnisse['puppe']['stellung_1']['I_gemessen_err'] = I_gemessen_1.s
Ergebnisse['puppe']['stellung_1']['I_Theorie'] = I_Theorie_1
Ergebnisse['puppe']['stellung_1']['DeltaI'] = DeltaI_1.n
Ergebnisse['puppe']['stellung_1']['DeltaI_err'] = DeltaI_1.s



#############################
# Zweite Stellung
#############################

# Periodendauer auslesen und berechnen
T2_2 = np.genfromtxt('data/puppe_2_gemessen.csv',delimiter=',',unpack=True)
T2_mean_2 = ufloat(np.mean(T2_2),stats.sem(T2_2)) #s
T_mean_2 = T2_mean_2/2 #s


# Trägheitsmoment berechnen
I_gemessen_2 = ((T_mean_2**2)*D)/(2*np.pi)**2 - I_D

# Theoriewert
I_Theorie_2 = I_Kopf + I_Torso + 2*(I_Arm_2 + m_Arm*((D_Torso/2)+(L_Arm/2))**2 ) + 2*(I_Bein_2 + m_Bein*( (D_Bein/2)**2 + (L_Bein/2)**2 ))

DeltaI_2 = I_Theorie_2 - I_gemessen_2


# Daten speichern
if not 'stellung_2' in Ergebnisse['puppe']:
    Ergebnisse['puppe']['stellung_2'] = {}

Ergebnisse['puppe']['stellung_2']['T2_mean[s]'] = T2_mean_2.n
Ergebnisse['puppe']['stellung_2']['T2_mean_err[s]'] = T2_mean_2.s
Ergebnisse['puppe']['stellung_2']['T_mean[s]'] = T_mean_2.n
Ergebnisse['puppe']['stellung_2']['T_mean_err[s]'] = T_mean_2.s
Ergebnisse['puppe']['stellung_2']['I_gemessen'] = I_gemessen_2.n
Ergebnisse['puppe']['stellung_2']['I_gemessen_err'] = I_gemessen_2.s
Ergebnisse['puppe']['stellung_2']['I_Theorie'] = I_Theorie_2
Ergebnisse['puppe']['stellung_2']['DeltaI'] = DeltaI_2.n
Ergebnisse['puppe']['stellung_2']['DeltaI_err'] = DeltaI_2.s



#######################
# Ergebnisse Speichern
#######################

json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)