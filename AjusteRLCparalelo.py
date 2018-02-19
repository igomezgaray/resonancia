'''
Se plotea la curva campana50khz.txt.
Se usa el modelo RLC con capacitor C2 paralelo.
Se plotea sobre los datos: el modelo teorico con todos los parametros fijos en funcion
del ancho de banda, el w resonancia, y la transferencia maxima.
Se busca obtener el valor de C2 logrando que el ajuste sea bueno, similar al RLC del 
modelo aproximado

FER: calculate el R**2 entre las dos curvas que se plotean al final
'''
import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
'''
Busco definir la funcion de Transferencia:

R: resistencia del piezo
L: inductancia del piezo
C1: capacitancia del piezo
C2: capacitancia de los bornes

R2: resistencia externa
fs: frecuencia de resonancia
Tmax: transferencia de resonancia
f1: f- de la campana
f2: f+ de la campana
'''
R2 = 10000
fs = 50097.900000000001
Tmax = 0.75360794533946895
f1 = 50096.099999999999
f2 = 50099.800000000003

def Transf(f, C2):
	w = f * 2*np.pi
	w1 = f1 * 2*np.pi
	w2 = f2 * 2*np.pi
	ws = fs * 2*np.pi
	R = R2 * (1 / Tmax - 1)
	L = R2 / (w2-w1) / Tmax
	C1 = Tmax * (w2 - w1) / R2 / ws ** 2
	Z1 = R + 1j*(w*L - 1/(w*C1))
	Z2 = -1j/(w*C2)
	Zeq = Z1 * Z2 / (Z1 + Z2)
	return (R2 / abs(R2 + Zeq))

Data = np.loadtxt('campana50khz.txt')
T = Data[:,2] / Data[:,1]
popt, pcov = curve_fit(Transf, Data[:,0], T, p0 = 10**-12)
print (popt)
plt.plot(Data[:,0], Transf(Data[:,0], popt))
plt.plot(Data[:,0], T, linestyle = '--', color = 'r')
plt.show()