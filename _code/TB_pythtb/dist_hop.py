"""
Description: 
Inputs: 
Outputs: dist_hop.png in _plots/TB
"""

from __future__ import print_function
from pythtb import * # import TB model class
from pythtb.pythtb import * # import TB model class
import matplotlib.pyplot as plt

from jhr.plotters._base import makeplot
from jhr.plotters._aesthete import select_colors_lines_markers

import itertools

root = '../../_data/wann_tb_files/'

folderfile = [ ("CsPbBr3_wan", "CsPbBr3"), ("CsPbBr2I_wan", "CsPbBr2I"), ("CsPbBrI2_wan", "CsPbBrI2"), ("CsPbI3_wan","CsPbI3")]
folderfile = [(root + x , y) for (x,y) in folderfile]

label = ["CsPbBr$_3$","CsPbBr$_2$I", "CsPbBrI$_2$", "CsPbI$_3$"]
lattice = [5.9, 6.3, 6.2 , 6.2]


fig, ax = plt.subplots(figsize = (6,6))

#--------Cyclers----------
colors, lines, markers = select_colors_lines_markers(number = 4)
colors[3] = colors[0]
colors[0] = '#edae49'
lines =  itertools.cycle(lines)
colors = itertools.cycle(colors)
markers = itertools.cycle(markers)

alpha = [0.8, 0.7, 0.7, 0.7]
alpha = itertools.cycle(alpha)


alldistham = []

for f, lab, lat, in zip(folderfile, label, lattice):
  mat=w90(f[0], f[1]) #Read W90 output
  (dist,ham) = mat.dist_hop()

  alldistham.append(mat.dist_hop)

  sample_size = 10000
  dist = np.random.choice(dist, size=sample_size, replace=False)
  ham = np.random.choice(ham, size=sample_size, replace=False)

  cutoffind = np.where(dist < 1.5 * lat)[0]
  # cutoffind = np.where(np.log(np.abs(ham)) > -4)
  # cutoffind = np.where((np.log(np.abs(ham)) > -4) & (dist < 2 * lat))
  dist2 = dist[cutoffind]
  ham2 = ham[cutoffind]
  dist2 = dist2/lat

    
  ax.scatter(dist2,np.log(np.abs(ham2)), 
            alpha = next(alpha), label = lab, marker = next(markers), color = next(colors))
  makeplot(plt.plot, {})


  ax.set_xlabel("Distance (in avg. lattice parameters)")
  ax.set_ylabel(r"$\log |H\cdot eV^{-1}|$ ")
  plt.legend(frameon = False)

plt.savefig('../../_plots/TB/dist_hop.png', format = 'png', dpi = 300)
plt.savefig('../../_plots/TB/dist_hop.svg', format = 'svg')
#plt.show()
