import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as tck

def A(k):
    if(k==0):
        return 2/np.pi
    else:
        return -4/(np.pi * (4 * k**2 -1))

# B(k) = 0

N = 10000
AnzahlX = 10000

a = []

for k in range(N+1):
    a.append(A(k))
    print("A(",k,") = ", a[k])

x = np.linspace(-3*np.pi,3*np.pi, AnzahlX)

y = (x/x)*a[0]
for k in range(N+1):
    if k > 0:
        y = y + a[k]*np.cos(2*k*x)

f,ax = plt.subplots(1)

ax.plot(x/np.pi,y, label="|sin(x)|")

ax.xaxis.set_major_formatter(tck.FormatStrFormatter('%g$\pi$'))
ax.xaxis.set_major_locator(tck.MultipleLocator(base=1.0))
ax.legend(loc='best')

plt.show()