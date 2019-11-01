import numpy as np

x,F = np.genfromtxt('data.csv',delimiter=',',unpack=True)

print("Mittelwertsbildung:")
print("<F/x> ",np.mean(F/x))

print("Ausgleichsrechnung:")
Fx = np.mean(F*x)
print("F*x",Fx)
Fmean = np.mean(F)
print("F",Fmean)
xmean = np.mean(x)
print("x",xmean)
x2mean = np.mean(x**2)
print("x²",x2mean)
xmean2 = np.mean(x)**2
print("<x>²",xmean2)

print("D=",(Fx-Fmean*xmean)/(x2mean-xmean2))