import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as tck

def B(k):
    if(k==0):
        return 0
    else:
        return - (2*(-1)**k) / k

# A(k) = 0

N = 8
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

f,ax = plt.subplots(1)

ax.plot(x/np.pi,y/np.pi, label="x")

ax.xaxis.set_major_formatter(tck.FormatStrFormatter('%g $\pi$'))
ax.xaxis.set_major_locator(tck.MultipleLocator(base=1.0))

ax.yaxis.set_major_formatter(tck.FormatStrFormatter('%g $\pi$'))
ax.yaxis.set_major_locator(tck.MultipleLocator(base=0.5))

ax.legend(loc='best')

plt.show()

