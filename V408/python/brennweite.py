####### Use /default/matplotlibrc and /default/header-matplotlib.tex
import os
import pathlib
os.environ['MATPLOTLIBRC'] = (pathlib.Path(__file__).absolute().parent.parent.parent / 'default' / 'matplotlibrc').__str__()
os.environ['TEXINPUTS'] =  (pathlib.Path(__file__).absolute().parent.parent.parent / 'default').__str__() + ':'
#######
import numpy as np
from uncertainties import ufloat
from scipy import stats
import json
import matplotlib.pyplot as plt

for linse in [50,100]:
    # Messwerte einlesen
    g,b = np.genfromtxt('data/brennweite{}.csv'.format(linse), delimiter=',', unpack=True)

    # Brennweite berechnen
    f = 1/(1/g+1/b)
    f_mean = ufloat(np.mean(f),stats.sem(f))

    # Schnittpunkte der Geraden (b_i,g_i verbunden)
    def Intersection(g1,b1,g2,b2):
        # Für die Rechnung siehe images/Schnittpunkte_Rechnung.pdf
        t = b2*(g1-g2)/(g1*b2-g2*b1)
        s_x = g1-t*g1
        s_y = t*b1
        return (s_x,s_y)

    s_x = np.array([])
    s_y = np.array([])
    n = g.size
    for i in range(0,n):
        # Alle Schnittpunkte der i-ten Linie mit allen nachfolgenden Linien
        s_x_i,s_y_i = Intersection(g[i+1:n],b[i+1:n],g[i],b[i])
        s_x = np.append(s_x,s_x_i)
        s_y = np.append(s_y,s_y_i)

    # Schwerpunkt der Schnittpunkte (Mittelwert)
    s_x_mean = ufloat(np.mean(s_x),stats.sem(s_x))
    s_y_mean = ufloat(np.mean(s_y),stats.sem(s_y))


    ####################################
    ## Ergebnisse speichern
    ####################################
    
    #Json
    Ergebnisse = json.load(open('data/Ergebnisse.json','r'))
    if not 'Brennweite{}'.format(linse) in Ergebnisse:
        Ergebnisse['Brennweite{}'.format(linse)] = {}
    Ergebnisse['Brennweite{}'.format(linse)]['f_mean[cm]'] = '{}'.format(f_mean)
    Ergebnisse['Brennweite{}'.format(linse)]['s_x_mean[cm]'] = '{}'.format(s_x_mean)
    Ergebnisse['Brennweite{}'.format(linse)]['s_y_mean[cm]'] = '{}'.format(s_y_mean)
    json.dump(Ergebnisse,open('data/Ergebnisse.json','w'),indent=4)

    # Tabelle
    data = list(zip(g,b,f))
    np.savetxt('data/brennweite{}_tabelle.csv'.format(linse), data, header='g[cm],b[cm],f[cm]', fmt='%i,%2.1f,%2.2f')


    ####################################
    ## Plot
    ####################################

    print("plot_brennweite",linse)

    # Plot der Verbindungslinien
    for i in range(0,g.size):
        plt.plot([g[i],0],[0,b[i]], 'k-', linewidth=0.5)

    # Plot der Daten
    plt.plot(g, g*0, 'co', markersize=3, label='Gegenstandsweiten $g$')
    plt.plot(b*0, b, 'yo', markersize=3, label='Bildweiten $b$')

    # Plot der Schnittpunkte
    plt.plot(s_x,s_y, 'r.', markersize=3.5, markeredgewidth=0, label="Schnittpunkte")

    # Achsenbeschriftung
    plt.xlabel(r'$g \:/\: \si{\centi\metre}$')
    plt.ylabel(r'$b \:/\: \si{\centi\metre}$')

    # in matplotlibrc leider (noch) nicht möglich
    plt.legend()
    plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

    # Speicherort
    plt.savefig('build/plot_brennweite{}.pdf'.format(linse))
    plt.clf()

    # Zoomed Plot
    print("plot_brennweite",linse,"_zoom")

    # Plot der Verbindungslinien
    for i in range(0,g.size):
        plt.plot([g[i],0],[0,b[i]], 'k-', linewidth=0.5)

    # Plot der Schnittpunkte
    plt.plot(s_x,s_y, 'r.', markersize=3.5, markeredgewidth=0, label="Schnittpunkte")

    # Schwerpunkt der Schnittpunkte plotten
    plt.errorbar(s_x_mean.n,s_y_mean.n, yerr=s_y_mean.s, xerr=s_x_mean.s, fmt='go', label="Schwerpunkt der Schnittpunkte")

    linse_cm = linse/10
    # Zoom zu den Schnittpunkten
    plt.xlim(linse_cm-1.5,linse_cm+1.5)
    plt.ylim(linse_cm-1.5,linse_cm+1.5)

    # in matplotlibrc leider (noch) nicht möglich
    plt.legend()
    plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

    # Zoom Plot Speicherort
    plt.savefig('build/plot_brennweite{}_zoom.pdf'.format(linse))
    plt.clf()
