import numpy as np
import json

f,U_C,a_gemessen = np.genfromtxt('data/gemessen.csv',delimiter=',',unpack=True)

a = 1/(2*f) - a_gemessen*10**(-3)
a = a*10**(3)

data = list(zip(f,U_C,a_gemessen,a))

print(a_gemessen)
print(a)

np.savetxt('data/gemessen_und_a.csv',data,header='f[Hz],U_C[V],a_gemessen[ms],a[ms]',fmt='%i,%1.3f,%1.3f,%1.3f')

R = 15.058*10**3
R_err = 0.6*10**3
C = 93.2*10**-9

RC = R*C# s
RC_err = C*R_err #s

RC_Ergebnisse = json.load(open('data/RC_Ergebnisse.json','r'))
RC_Ergebnisse['theorie[s]'] = RC
RC_Ergebnisse['theorie_err[s]'] = RC_err
json.dump(RC_Ergebnisse,open('data/RC_Ergebnisse.json','w'))