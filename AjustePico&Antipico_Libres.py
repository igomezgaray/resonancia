'''
Se mergean los datos de 'campana50khz.txt', 'anti2mv.txt', 'anti20uv.txt' y se plotean
Se usa el modelo RLC con capacitor C2 paralelo.
Se plotea sobre los datos: el modelo teorico con todos los parametros fijos en funcion
del ancho de banda, el w resonancia, y la transferencia maxima.
Se busca obtener el valor de C2 logrando que el ajuste sea bueno, y comparable al RLC 
del modelo aproximado

FER: aca creo que con estimar el r**2 alcanza. creo que es mas importante el C2 que
impone la antiresonancia sola a que los puntos cambien un poquito en la campana
'''
import numpy as np
from matplotlib import pyplot as plt
pico = np.loadtxt('campana50khz.txt')
antipico1 = np.loadtxt('anti2mv.txt')
antipico2 = np.loadtxt('anti20uv.txt')
'''
antipico1: COLUMNA2 esta en escala de 2 milivolts
		   COLUMNA1 esta en escala de 1 volt
antipico2: COLUMNA2 esta en escala de 20 microvolts
		   COLUMNA1 esta en escala de 1 volt
pico: 	   Ambas columnas están en volts
Paso todo a volts
'''
antipico1[:,2] *= 2 * 10**-3 / 10
antipico1[:,1] /= 10
antipico2[:,2] *= 20 * 10**-5 / 10
antipico2[:,1] /= 10
#mergeo los datos
tabla = np.concatenate((pico, antipico1, antipico2), axis = 0)

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
R20 = 10000
fs0 = 50097.900000000001
Tmax0 = 0.75360794533946895
f10 = 50096.099999999999
f20 = 50099.800000000003
C20 = 2.3*10**-12
p0 = np.array([R20, fs0, Tmax0, f10, f20, C20])

def Transf(f, R2, fs, Tmax, f1, f2, C2):
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

T = tabla[:,2] / tabla[:,1] #obtengo la transferencia

popt, pcov = curve_fit(Transf, tabla[:,0], T, p0 = p0)
print (popt)
dominio = np.arange(min(tabla[:,0]),max(tabla[:,0]),0.5) 
#plt.plot(dominio, Transf(dominio, popt))
plt.plot(dominio, Transf(dominio, popt[0], popt[1],popt[2],popt[3],popt[4],popt[5]))
plt.plot(tabla[:,0], T, marker = '*', linestyle = 'none', color = 'r')
plt.xlabel('Frecuencia (Hz)')
plt.title('Transferencia vs Frecuencia')
plt.ylabel('Transferencia (-)')
y = T
x = tabla[:,0]
f = Transf
ey = y * 0.02
#R^2+Chi cuadrado
residuals = y- f(x, popt[0],popt[1],popt[2],popt[3],popt[4],popt[5])
ss_res = np.sum(residuals**2)
ss_tot = np.sum((y-np.mean(y))**2)
r_squared = 1 - (ss_res / ss_tot)
chi=np.sum(((residuals/(ey))**2)/len(y))
print(r_squared,chi)
print((popt-p0)/p0)
plt.show()

