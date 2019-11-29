import numpy as np

f,U_C,a_gemessen = np.genfromtxt('data/gemessen.csv',delimiter=',',unpack=True)

a = 1/(2*f) - a_gemessen*10**(-3)
a = a*10**(3)

data = list(zip(f,U_C,a_gemessen,a))

print(a_gemessen)
print(a)

np.savetxt('data/gemessen_und_a.csv',data,header='f[Hz],U_C[V],a_gemessen[ms],a[ms]',fmt='%i,%1.3f,%1.3f,%1.3f')