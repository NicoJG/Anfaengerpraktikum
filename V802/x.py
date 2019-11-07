import matplotlib.pyplot as plt
import numpy as np

def B(k):
    if(k==0):
        return 0
    else:
        return - (2*(-1)**k) / k

# A(k) = 0

N = 1000
AnzahlX = 10000

b = []

for k in range(N+1):
    b.append(B(k))
    print("B(",k,") = ", b[k])

x = np.linspace(-3*np.pi,3*np.pi, AnzahlX)

y = (x/x)*b[0]
for k in range(N+1):
    if k > 0:
        y = y + b[k]*np.sin(k*x)

plt.plot(x,y, label="|sin(x)|")
plt.legend(loc='best')
plt.show()

