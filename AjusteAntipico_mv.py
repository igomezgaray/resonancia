'''
Se fitean los datos de 'anti2mv.txt' y 'anti20uv.txt', y se plotean
Se usa el modelo RLC con capacitor C2 paralelo.
Se plotea sobre los datos: el modelo teorico con todos los parametros fijos en funcion
del ancho de banda, el w resonancia, y la transferencia maxima.
Se busca obtener el valor de C2 logrando que el ajuste sea bueno, y comparable al RLC 
del modelo aproximado

FER: calculate el R**2 entre las dos curvas que se plotean al final. Es más importante
este valor de C2 porque es más relevante para la antiresonancia.
'''
import numpy as np
from matplotlib import pyplot as plt
antipico1 = np.loadtxt('anti2mv.txt')
'''
antipico1: COLUMNA2 esta en escala de 2 milivolts
		   COLUMNA1 esta en escala de 1 volt
Paso todo a volts
'''
antipico1[:,2] *= 2 * 10**-3 / 10
antipico1[:,1] /= 10

from scipy.optimize import curve_fit
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

T = antipico1[:,2] / antipico1[:,1] #obtengo la transferencia
popt, pcov = curve_fit(Transf, antipico1[:,0], T, p0 = 10**-12)
print (popt)
dominio = np.arange(min(antipico1[:,0]),max(antipico1[:,0]),0.5) 
plt.plot(dominio, Transf(dominio, popt))
plt.plot(antipico1[:,0], T, marker = 'x', linestyle = 'none', color = 'r')
plt.show()

