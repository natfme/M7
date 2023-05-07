from astropy.io.votable import parse_single_table
import numpy as np
import matplotlib.pyplot as plt

# Se lee la tabla y los valores de temperatura y luminosidad
name = 'messier7_r_1-5-result.vot'
data = parse_single_table(name).array
temperature = data['teff_val']
luminosity  = data['lum_val']
temp        = data['teff_val'] 
plt.figure(dpi=150,figsize=(6,6))

# -- En la siguiente línea, “s” es el tamaño del punto -- #
plt.scatter(temperature, luminosity, c='royalblue', s=80, \
            edgecolors='k', linewidth=1.0, alpha=0.5)

# La siguiente línea lee los datos del archivo .iso
data = np.loadtxt('MIST_iso_64582378a945d100.iso', comments='#').T
LogL = data[7] # Dato del logaritmo10 de Luminosidad
LogT = data[10] # Dato del logaritmo10 de Temperatura

data_2 = np.loadtxt('MIST_iso_645823a4be953d200.iso', comments='#').T
LogL_2 = data_2[7] # Dato del logaritmo10 de Luminosidad
LogT_2 = data_2[10] # Dato del logaritmo10 de Temperatura

# La siguiente línea lee los datos del archivo .iso
data = np.loadtxt('MIST_iso_645823db1a53f220.iso', comments='#').T
LogL_3 = data[7] # Dato del logaritmo10 de Luminosidad
LogT_3 = data[10] # Dato del logaritmo10 de Temperatura

data_2 = np.loadtxt('MIST_iso_645823fd763fc250.iso', comments='#').T
LogL_4 = data_2[7] # Dato del logaritmo10 de Luminosidad
LogT_4 = data_2[10] # Dato del logaritmo10 de Temperatura

# Se grafica Luminosidad en función de la Temperatura
#data = np.loadtxt('MIST_iso_5f70ade1d61fb.iso', comments='#').T
#LogL1 = data[7] # Dato del logaritmo10 de Luminosidad
#LogT1 = data[10] # Dato del logaritmo10 de Temperatura
# Se grafica Luminosidad en función de la Temperatura
size=10
plt.title('Diagrama Hertzsprung-Russell Messier 7')
plt.plot(10**LogT  , 10**LogL    , label='100 Myr')
plt.plot(10**LogT_2, 10**LogL_2, label='200 Myr')
plt.plot(10**LogT_3 , 10**LogL_3    , label='220 Myr')
plt.plot(10**LogT_4, 10**LogL_4, label='250 Myr')
plt.xlabel(r'T$_{eff}$ [K]')
plt.ylabel(r'Luminosity [L$_*$/L$_\odot$]')
plt.yscale('log')
plt.legend()
plt.grid()
plt.gca().invert_xaxis()
plt.xlim(2000,12000)
plt.savefig('isocronas_messier_7.jpg',dpi=190)
plt.show()