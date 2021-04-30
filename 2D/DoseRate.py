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

xmin = 1291
xmax = 26890

ymin = -290
ymax = 220





points = ["ir1"] #["ir1", "ir5"]
cooldowns = ["1w", "1m"]# ["1h" , "1d", "1w", "1m", "2m" , "4m", "6m", "1y", "1.5y"]
cooldownLabels = ["1 week", "1 month"] #["1 hour", "1 day", "1 week", "1 month", "2 months", "4 months", "6 months", "1 year", "1.5 years"]



gs = gridspec.GridSpec(20, 1)

for point in points:
    for i, cd in enumerate(cooldowns):
        filename = point + "_" + cd

            
        fluka = USRBIN(filename, path_data, 0.0036)
        
        if point == "ir1":
            fluka.loadGeometryFile( "horizontal.dat", path_drawings)
        else:
            fluka.loadGeometryFile( "horizontal_ir5.dat", path_drawings)
        
        
        fig = plt.figure()
        ax = plt.subplot(gs[0:12, 0])

        
        image = fluka.cube[0:,y_beamaxis, 0:]
        plt.pcolor(fluka.X, fluka.Y,image, norm=LogNorm(vmin=vmin, vmax=vmax) ,cmap = cmap)
        fluka.drawGeo(ax, 0.15, 0.3)
        

        
        ax.set_xticks(xticks)
        ax.set_xticklabels(xlabels)
        ax.set_yticks(yticks)
        ax.set_yticklabels(ylabels)

        plt.ylabel("x [m]", fontsize = 16)
        
        plt.xlabel("z [m from IP]", fontsize = 16)
        plt.xlim(xmin,xmax)
        plt.ylim(ymin,ymax)

        plt.xticks(fontsize=18)
        plt.yticks(fontsize=18)

        yes = fluka.cube[x_1meter, y_beamaxis, 0:]
        

         
        plt.title("LSS{} after {} cool down after Run 3 p-p operations".format(point[2], cooldownLabels[i] ), fontsize = 25)
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
            plt.savefig(filename + ".pdf",  bbox_inches = 'tight', pad_inches = 0.1)
        except:
            pass;


