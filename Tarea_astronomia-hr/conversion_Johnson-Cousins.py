import numpy as np
import matplotlib.pyplot as plt
from astropy.io.votable import parse_single_table # -- librería para leer VOT
#import warnings   # ------ librería que esconde los warnings
#warnings.filterwarnings("ignore")

def Magnitude(V,d,E):
    M = V - 5*np.log10(d) + 5 - 3.2*E
    return M

def B_V(BP_RP):
    GG = np.ones(2000)*BP_RP # Parte de la izquierda de (2)
    a = 0.0981 # Definición de coeficientes
    b = 1.4290
    c = -0.0269
    d = 0.0061
    B_V = np.linspace(-2,4,2000)
    right = a + b*(B_V) + c*(B_V)**2 + d*(B_V)**3 # Parte de la derecha de (2)
    # La siguiente función calcula cuando la resta cambia de signo. ¿Para qué?
    idx = np.argwhere(np.diff(np.sign(GG - right))).flatten()
    # idx da el valor del PIXEL para el cual GG y right son iguales. Para saber
    # qué valor de B-V corresponde el pixel, se llama de la siguiente manera:
    return B_V[idx][0]

def V(B_V,RP): # RP es el valor de G_RP (valor que ya se leyó)
    a = 0.1245 # Constantes según la ecuación (4)
    b = 1.0147
    c = 0.1329
    d = -0.0044
    V = RP + a + b*(B_V) + c*(B_V)**2 + d*(B_V)**3 # Ecuación (4)
    return V

# ---------------------------------------------------------------------

# -- Se lee la tabla con el nombre del archivo
name = 'messier7_r_1-5-result.vot'
data = parse_single_table(name).array
 
G     = data['phot_g_mean_mag']    # Magnitud absoluta de Gaia
bp_rp = data['bp_rp']              # Indice de color de Gaia
temp  = data['teff_val']           # Temperatura efectiva
rp    = data['phot_rp_mean_mag']   # G_RP: Indice centrado en 797 nm 
d     = 1000/data['parallax']      # Distancia en parsec (d=1/paralaje)
E     = 0.030                      # Valor del reddening (tomado de WEBDA)

b_v = np.zeros(len(G))  # Acá se pondrá el índice de color (B-V)
v   = np.zeros(len(G))  # Acá se pondrá el filtro en el visible (V)
Mv  = np.zeros(len(G))  # Acá se pondrá la Magnitud absoluta (Mv)


for i in range(len(G)):
    if isinstance(bp_rp[i],np.float32):  # Garantiza que bp_rp sea un número
        BP_RP  = bp_rp[i]
        RP     = rp[i]
        b_v[i] = B_V(BP_RP)         # Se ingresa cada número que está en bp_rp
        v[i]   = V(b_v[i],RP)              # Acá se va escribiendo el array v
        Mv[i]  = Magnitude(v[i],d[i],E)  # Acá se va escribiendo el array Mv
    else:
        b_v[i] = np.nan      # Si bp_rp no es un número, lo llena con NAN 
        v[i]   = np.nan
        Mv[i]  = np.nan

a=sum(b_v)
print (a)
# Ojo, en el eje 'x' se hace (B-V)-E, el cual es el índice de color intrínseco
plt.plot(b_v-E,Mv,'o',color='mediumblue',alpha=0.5) 
plt.gca().invert_yaxis()  # Para invertir la dirección del eje "y"
plt.title('Messier 7 Diagrama Color-Magnitud')
plt.grid()
plt.xlabel('Índice de Color (B-V)',fontsize=12)
plt.ylabel('Magnitud absoluta',fontsize=12)
plt.savefig('datos_johnson-cousins_messier_7.jpg',dpi=190)
plt.show()