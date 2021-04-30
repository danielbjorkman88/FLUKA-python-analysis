# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 15:40:13 2021

@author: dbjorkma
"""

# 1D example

import os, sys
from matplotlib.colors import LogNorm
import numpy as np
from matplotlib import cm
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
path = os.getcwd()
sys.path.insert(0, os.path.split(os.getcwd())[0] + "\\USRBIN")
path_data = os.path.split(os.getcwd())[0] + "\\Data"
sys.path.insert(0, path_data)
path_drawings = os.path.split(os.getcwd())[0] + "\\Data\\Drawings"
sys.path.insert(0, path_drawings)
from USRBIN import USRBIN
from LHC_constants import *


y_beamaxis = 15 # bin number y axis
x_1meter = 20 # bin number x axis corresponding 1 meter from beam axis


zmin = 1291/100 # m
zmax = 265

vmax, vmin = 10000, 1E-2

ratio_max, ratio_min = 4, 0.1

normfactor = 0.0036

ref = USRBIN("ir1_1w", path_data, normfactor)
ref.loadGeometryFile( "horizontal.dat", path_drawings)

mod = USRBIN("ir1_1m", path_data, normfactor)


xticks = list(range(0, 300, 25))
xlabels = [str(item) for item in xticks]


    

gs = gridspec.GridSpec(100, 1)

fig = plt.figure()
ax = plt.subplot(gs[0:70, 0])
    
plt.plot(ref.xcoordinates/100, ref.cube[x_1meter , y_beamaxis, 0:], label = "1 week")
plt.plot(mod.xcoordinates/100, mod.cube[x_1meter , y_beamaxis, 0:], label = "1 month")
    

ax.set_xticks(xticks)
ax.set_xticklabels(xlabels)

ax.set_xlim(zmin, zmax)
ax.set_ylim(vmin, vmax)
ax.set_yscale('log')
plt.ylabel(r"Residual $H^{*}(10)$ rates [uSv/h]", fontsize = 20)

plt.legend(prop={'size': 14}, loc = 3) 

plt.grid(linewidth = 0.1)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off


ax2 = ax.twinx()
ax2 = ref.drawGeo_inside_of(ax2 , 0.50, 260 , 100, 0.3, 0.3)
                                    #(self, ax , yCut, zCut , factor = 1 ,linewidth = 0.5, alpha = 1)
                                    #                           
                                
ax2.set_ylim(-3.50, 0.45)
ax2.set_xlim(zmin, zmax)
ax2.axes.yaxis.set_visible(False)

for key in machine_labels.keys():
    zpos = machine_labels[key][0]/100
    ax2.text(zpos, machine_labels[key][1]/100 , key,
            color='k', fontsize=12)



ax = plt.subplot(gs[72:, 0])


plt.plot(ref.xcoordinates/100, ref.cube[x_1meter , y_beamaxis, 0:]/mod.cube[x_1meter , y_beamaxis, 0:], label = "1 week/1 month")
plt.axhline(y=1, color='k', linestyle='-')

plt.xlabel("z [m from IP]", fontsize = 24)
plt.ylabel("Ratio", fontsize = 20)
plt.legend(prop={'size': 14}, loc = 3) 
plt.grid(linewidth = 0.1)

ax.set_xlim(zmin, zmax)
plt.ylim(ratio_min, ratio_max)

plt.suptitle("Example 1D plot", fontsize = 20)


xlength = 12
fig.set_size_inches(xlength, xlength/1.61803398875)
plt.show()
try:
    os.chdir(path)
    plt.savefig("example_1dplot.pdf",  bbox_inches = 'tight', pad_inches = 0.1)
except:
    pass;
























