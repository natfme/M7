import numpy as np
import matplotlib.pyplot as plt
from astropy.io.votable import parse_single_table

# Se lee la tabla con el nombre del archivo
name = 'messier7_r_1-5-result.vot'
data = parse_single_table(name).array

bp_rp = data['bp_rp'] # Indice de color de Gaia
G = data['phot_g_mean_mag'] # Magnitud absoluta de Gaia
rp = data['phot_rp_mean_mag'] # Banda Grp de Gaia (797 nm)
temp = data['teff_val'] # Temperatura efectiva

# Se muestra el diagrama color-magnitud de Gaia
plt.plot(bp_rp,G,'.') # Para que muestre puntos

# Para que el label quede con notación de LATEX, se escribe:
plt.xlabel(r"Indice de color G$_{BP}$ - G$_{RP}$")
plt.ylabel(r"Magnitud absoluta G")
plt.title('Messier 7 Diagrama Color-Magnitud')
plt.grid()
plt.gca().invert_yaxis() # Para invertir el eje "y"
plt.savefig('datos_gaia_messier_7.jpg',dpi=190)
plt.show()