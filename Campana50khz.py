import numpy as np
from matplotlib import pyplot as plt
data = np.loadtxt('campana50khz.txt')
plt.plot(data[:,0],data[:,2]/data[:,1])
transf = data[:,2] / data[:,1]
np.where(abs(transf -  max(transf) / 2) < 0.009 )
# devuelve (array([ 60, 97], dtype=int32),)
Q = data[78,0]/(data[97,0] - data[60,0])
print(Q)
plt.plot(data[:,0],data[:,2]/data[:,1], color = 'b')
plt.xlabel('Frecuencia (Hz)')
plt.title('Transferencia vs Frecuencia')
plt.ylabel('Transferencia (-)')
plt.axvline(x = data[97,0], color = 'r', linestyle = '--', ymax = 0.64, linewidth = 0.5)
plt.axvline(x = data[60,0], color = 'r', linestyle = '--', ymax = 0.64, linewidth = 0.5)
plt.axvline(x = data[78,0], color = 'g', label = 'Ws', linestyle = '--', ymax = 0.95, linewidth = 0.5)
plt.axhline(y = max(transf), color = 'g', linestyle = '--', linewidth = 0.5)
plt.axhline(y = (transf[60] + transf[97])/2, color = 'r', linestyle = '--', linewidth = 0.5)
plt.show()