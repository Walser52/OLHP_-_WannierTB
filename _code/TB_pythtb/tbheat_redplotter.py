# Create reduced heat map.
#Also saves npy files in the tbred folder as numpy array. These may be used to create a graph later.
from mpl_toolkits.axes_grid1.axes_divider import HBoxDivider, VBoxDivider
import mpl_toolkits.axes_grid1.axes_size as Size


# ============
import matplotlib.pyplot as plt
import numpy as np
import os

from jhr.plotters._base import annotate
from jhr.plotters.plots import tbHeat

from jhr.codes import W90
from jhr.codes.W90 import GetOneCell, GetHomePlusNeighbors, GetAllContributions
from jhr.codes.W90 import GetTBHam



datroot = '../../_data/wann_tbred_files/'
files = [#TSV files 
        "CsPbBr3.tsv" ,
        "CsPbBr2I.tsv",
        "CsPbBrI2.tsv",
        "CsPbI3.tsv"  ,
        ]
datfiles = [datroot+ f for f in files]
savefolder = '../../_plots/TB/HeatTBRed/'
num_basis = 12

symmetric = True
#________READ__________



H_all     = GetTBHam(datfiles, num_basis = 12, getfor = 'all', verbose = False)


lab = list(range(0,12))

for H, path in zip(H_all, datfiles):
  savefile, _ = os.path.splitext(os.path.basename(path))

  # make symmetric
  if symmetric:
    H = np.abs(H)
    H = np.maximum(H, H.transpose())

  logH = np.log(H)
  
  fig, ax1 = plt.subplots(1, 1, figsize=(6,6))

  tbHeat(logH, num_basis = num_basis, ax = ax1, cbar_kw = {'fraction': 0.025}, ticks = True)
  
  logH[np.isinf(logH)] = np.nan
#  print(logH)
  np.savetxt(f'{datroot}{savefile}.csv', logH, delimiter=',', fmt='%f', comments='')

  plt.savefig(f'{savefolder}{savefile}.png', format = 'png', dpi = 300)
  plt.savefig(f'{savefolder}{savefile}.svg', format = 'svg')
  
  # plt.show()
