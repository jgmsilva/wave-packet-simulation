import numpy as np
import scipy.sparse as sp
import matplotlib.pyplot as plt

J, dx, dt, steps = 800, 0.1, 5e-6, 16e6 #world parameters
bdist_pts, width_pts, V0 = 50, 10, 0.3 #semi-transparent barriers

N = 2*J+1
x = dx*np.arange(-J, J+1)
d, w = bdist_pts*dx, width_pts*dx

V = np.zeros(N)
V[(np.abs(x-d)<=w/2)|(np.abs(x+d)<=w/2)] = V0

main = -2*np.ones(N, complex)
off = np.ones(N-1, complex)
D2 = sp.diags([off, main, off], [-1,0,1], shape=(N,N))/dx**2
D2 = D2.tolil()
D2[0,:]=0; D2[-1,:]=0
D2 = D2.tocsr()
H = -0.5*D2 + sp.diags(V)

x0, s, k0 = 0.0, 1.0, 0.0 #gaussian packet
a = 2*s
A = (2.0/(np.pi*a*a))**0.25
psi = A * np.exp(-((x-x0)**2)/(a*a)) * np.exp(1j*k0*x)
psi[0] = psi[-1] = 0
psi /= np.sqrt(np.sum(np.abs(psi)**2)*dx)

inside = (x > (-d + w/2)) & (x < (d - w/2))
Pin = np.empty(steps)
Pin0 = np.sum(np.abs(psi[inside])**2)*dx

for n in range(steps):
    psi += -1j*dt*(H@psi)
    psi[0] = psi[-1] = 0
    Pin[n] = np.sum(np.abs(psi[inside])**2)*dx
    # print(f"Norm at {n} is {Pin[n]}")

t = dt*np.arange(steps)

plt.figure()
plt.plot(t, Pin)
plt.xlabel("time")
plt.ylabel("P_inside")
plt.title("Tunneling from inside double barrier")
plt.tight_layout()
plt.show()

print(f"final norm: {np.sum(np.abs(psi)**2)*dx}")

np.savetxt("base_pin16.csv",
           np.column_stack([t, Pin]),
           delimiter=",",
           header="t,Pin",
           comments="")
