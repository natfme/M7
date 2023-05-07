import numpy as np    # Numeerical PYthon -> numpy
import matplotlib.pyplot as plt    # Plotting tool of Python
from astropy.io.votable import parse_single_table    # Read VOTables
import matplotlib   # To change some properties of the plots
from matplotlib.colors import LinearSegmentedColormap   # To create colors
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable 
# - Some times when reading data, there could be "Warnings" which can be
# - ignored via the warnings module
import warnings
warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------
# ----- Transformation functions -----


# - To get the magnitude
def Magnitude(V,d=780,E=0):
    M = V - 5*np.log10(d/10) - 3.2*E  # This is the absolute magnitude
    return M


# - To get the Johnson-Cousins color index from Gaia color index
def B_V(BP_RP):
    GG = np.ones(2000)*BP_RP
    a = 0.0981      # Coefficient a
    b = 1.4290      # Coefficient b                                 
    c = -0.0269     # Coefficient c
    d = 0.0061      # Coefficient d
    B_V = np.linspace(-3,5,2000)          # This includes spuriours stars 
    y = a + b*B_V + c*B_V**2 + d*B_V**3   # Transformation equation
    """
    The next line takes the difference of the sign function to evaluate the
    change in sign for the difference GG - y (right and left sides of the 
    equation). This return the index (or location) where the change in sign
    is present. With this location we calculate the value of B-V of the sign
    difference.
    """
    idx = np.argwhere(np.diff(np.sign(GG - y))).flatten() 
    return B_V[idx][0]   # This returns the actual float of the intersection


# - To get the magnitude
def V(B_V,RP):
    a = 0.1245      # Coefficient a
    b = 1.0147      # Coefficient b
    c = 0.1329      # Coefficient c
    d = -0.004      # Coefficient d4
    V_RP = a + b*B_V + c*B_V**2 + d*B_V**3 # Transformation equation
    V = V_RP + RP  # Value of the Visual magnitude!! :D
    return V

# ----- Table reading and function operations -----

name = 'messier7_r_1-5-result.vot'
data = parse_single_table(name).array

bp_rp = data['bp_rp']               # Gaia color index
G = data['phot_g_mean_mag']         # Gaia G magnitude
rp = data['phot_rp_mean_mag']       # Gaia RP filter 
temp = data['teff_val']             # Effective temperature
e = data['e_bp_min_rp_val']         # e
parallax =data['parallax']          # parallax 
parall_erri=data['parallax_error']  # parallax error (for statistical analy.)
                                    # include this for adding errorbars in
                                    # the magnitudes (because of the distance)
E = 0.103                          # This information is taken from WEBDA


d = 1000/parallax   # Take into account negative values of parallax
S = np.where(d>0) and np.where(temp >= 100) and np.where(e<1000)
# - The objects are not too far away (except for some saggitarius clusters)
# - so "d" can be taken positive for sure.    


"""
Empty ARRAYS are created in order to fill them with the information of the
Johnson-Cousins passband.
"""
b_v = np.zeros(len(G))   # Transformation
v   = np.zeros(len(G))   # Visual magnitude
MM  = np.zeros(len(G))   # Absolute magnitude
MG  = np.zeros(len(G))
brillo = data['lum_val']

for i in range(len(G)):
    """
    If data is indeed a float (decimal), then operate the functions, otherwise
    fill the arrays with Not-A-Number (NAN)
    """
    if isinstance(bp_rp[i],np.float32): # if data is a decimal point
        BP_RP  = bp_rp[i]
        RP     = rp[i]
        d      = 1000/parallax[i]        # Distance in parsec
        b_v[i] = B_V(BP_RP)              # Transformation
        v[i]   = V(b_v[i],RP)            # Visual magnitude
        MM[i]  = Magnitude(v[i],d,E=E)   # Absolute magnitude
        #MG[i]  = G[i]-5*np.log10(d/10)-3.2*e[i]
    else:       # If data is not present, do not operate an fill with NAN
        b_v[i] = np.nan
        v[i]   = np.nan
        MM[i]  = np.nan
        MG[i]  = np.nan    

"""
  Color-Magnitude diagram for the Transformed Johnson-Cousins passbands.
  Change "jet_r" in "cmap" for "new_color" (defined previously at the 
  beginning of the code) to get an approximate of the "color" of the stars.
  -- Why are there no green stars?
"""
# - This next lines creates a plot with a size of 6 and 7 "
fig, (ax1) = plt.subplots(figsize=(6,7), dpi=180)
# - Change the size of the labels and titles (bigger font sizes)
matplotlib.rcParams.update({'font.size': 12})
plt.rcParams.update({'font.size': 12})

# - Plot the stars. In this case we will not use plt.plot but plt.scatter
# - which is a function that make a scatter plot and has so many settings.

# s:  The marker size in points
im1 = ax1.scatter(b_v-E,MM,c=temp,s=temp/100, cmap='jet_r', vmax=10000,\
    edgecolors='k',lw=0.5)
# - To plot the Color-Magnitude diagram as of the GAIA colors
#im2 = ax1.scatter(bp_rp,MG,c=temp,cmap='rainbow_r',edgecolors='k')
fontsize = 12
plt.suptitle("Messier 7 Diagrama Color-Magnitud", fontsize=fontsize,x=0.5,y=0.92)

plt.xlabel('Índice de Color (B-V)',fontsize=12)
plt.ylabel('Magnitud absoluta (Mv)',fontsize=12)
plt.grid()
plt.gca().invert_yaxis()
#plt.xlim(-0.5,1.7)
#plt.ylim(16,-3)
# - The next lines create a colorbar on top of the figure
ax1_divider = make_axes_locatable(ax1)
cax1 = ax1_divider.append_axes("top", size="5%", pad="25%")
# - The next line creates the colorbar on top of the figure. The label of the 
# - colorbar includes a LaTeX notation (look the $ sign). 
cb = fig.colorbar(im1,cax=cax1,label=r'Temperatura efectiva $T_{eff}$ [K]', \
    orientation='horizontal')
#cax1.xaxis.set_ticks_position("top")   # To locate ticks on top
cb.ax.invert_xaxis()   # To invert the direction of the colorbar
plt.savefig('messier7-diagrama-HR.jpg',dpi=190)
plt.show()        