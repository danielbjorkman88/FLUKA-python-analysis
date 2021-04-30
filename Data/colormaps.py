# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 15:28:33 2021

@author: dbjorkma
"""

import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.colors as mcolors
import numpy as np

# Default colormap for LHC studies between limits 1E-3 and 1E4
cmap = cm.get_cmap('jet', 21)   # 21 = 3 colors per decade times 7 decades  


# LL map works with vmin = 0.1 and vmax = 100000
colors1 = plt.cm.Blues(np.linspace(0., 1, 150))
colors2 = plt.cm.autumn(np.linspace(0., 1, 150*5))

colorIdx = 0
for rowIdx in range(len(colors2)):
    colors2[rowIdx, 0:] = colors2[colorIdx, 0:]
    if rowIdx % 150 == 0:
        colorIdx += 149
        
colors = np.vstack((colors1, colors2))
LL_cmap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)



#Ratio
ratio_cmap = "seismic" # vmax = 1/vmin








