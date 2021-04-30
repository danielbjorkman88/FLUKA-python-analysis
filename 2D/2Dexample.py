
# 2D example

import os, sys
from matplotlib.colors import LogNorm
import numpy as np 
from matplotlib import cm
import matplotlib.gridspec as gridspec
import math
import matplotlib.pyplot as plt
path = os.getcwd()
sys.path.insert(0, os.path.split(os.getcwd())[0] + "\\USRBIN")
path_data = os.path.split(os.getcwd())[0] + "\\Data"
sys.path.insert(0, path_data)
path_drawings = os.path.split(os.getcwd())[0] + "\\Data\\Drawings"
sys.path.insert(0, path_drawings)
from USRBIN import USRBIN
from LHC_constants import *
from colormaps import *






xticks = list(range(0, 26000 + 10000,1000))
xlabels = [str(item/100)[:-2] for item in xticks]

yticks = list(range(-300, 300,100))
ylabels = [str(item/100)[:-2] for item in yticks]



vmin = 1E-3
vmax = 1E4





normfactor = 0.0036


    
fluka = USRBIN("ir1_1w", path_data, normfactor)
fluka.loadGeometryFile( "horizontal.dat", path_drawings)


zmin = int(fluka.info["zmin"][0])
zmax = 26890

xmin = -290
xmax = 220




gs = gridspec.GridSpec(20, 1)


fig = plt.figure()
ax = plt.subplot(gs[0:12, 0])


image = fluka.cube[0:,y_beamaxis, 0:]
plt.pcolor(fluka.X, fluka.Y,image, norm=LogNorm(vmin=vmin, vmax=vmax) ,cmap = cmap)
fluka.drawGeo(ax, 0.15, 0.7) #numbers are related to alpha and line thickness



ax.set_xticks(xticks)
ax.set_xticklabels(xlabels)
ax.set_yticks(yticks)
ax.set_yticklabels(ylabels)
plt.ylabel("x [m]", fontsize = 16)

plt.xlabel("z [m from IP]", fontsize = 16)
plt.xlim(zmin,zmax)
plt.ylim(xmin,xmax)

plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
 
plt.title("Example 2D plot" , fontsize = 25)
plt.gcf().subplots_adjust(bottom=0.1)

ax = plt.subplot(gs[18:, 0])

img = plt.pcolor(fluka.X, fluka.Y,image,  shading='auto' ,norm=LogNorm(vmin=vmin, vmax=vmax) ,cmap = cmap)
img.set_visible(False)
plt.colorbar(orientation="horizontal", cax=ax)

plt.gcf().subplots_adjust(bottom=0.3)
plt.xlabel(r"Residual $H^{*}(10)$ rates [uSv/h]", fontsize = 20)
plt.xticks(fontsize=20)        

xlength = 18
fig.set_size_inches(xlength, xlength/5)
plt.show()
try:
    os.chdir(path)
    plt.savefig("2Dexample_plot.pdf",  bbox_inches = 'tight', pad_inches = 0.1)
except:
    pass;


