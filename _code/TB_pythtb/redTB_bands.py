#!/usr/bin/env python
from pythtb import * # import TB model class
from pythtb.pythtb import *
import matplotlib.pyplot as plt


def plottb(evals,k_dist,k_node,k_label, color = 'k', label = None):
    ax = plt.gca()
    for i in range(evals.shape[0]):
        if i == 0: ax.plot(k_dist,evals[i],color = color, linestyle = '-', alpha = 1, lw = 2, label = label)
        else:      ax.plot(k_dist,evals[i],color = color, linestyle = '-', alpha = 1, lw = 2)

    for n in range(len(k_node)):
        ax.axvline(x=k_node[n],linewidth=0.5, color='k')

    ax.set_xlim(k_dist[0],k_dist[-1])
    ax.set_xticks(k_node)
    ax.set_xticklabels(k_label)
    # fig.tight_layout()    
    return

def modelcreate(mat, path, report, min_hopping_norm = 0.1, max_distance=None, zero_energy=0):
    my_model=mat.model(zero_energy=zero_energy, min_hopping_norm=min_hopping_norm, max_distance=max_distance);


    (k_vec,k_dist,k_node)=my_model.k_path(path,101, report = report);
    evals=my_model.solve_all(k_vec);
    return evals, k_dist, k_node

def tuneandplottb(mat, path, report, k_label, min_hopping_norm = 0.1, max_distance=None, color = 'k', label = None, zero_energy = 0):
    evals, k_dist, k_node = modelcreate(mat, path, report, min_hopping_norm = min_hopping_norm, max_distance=max_distance, zero_energy= zero_energy)
    plottb(evals,k_dist,k_node, k_label, color = color, label = label)    

    return


folderfile = ["CsPbBr3", "CsPbBr2I", "CsPbBrI2","CsPbI3"]

lattice = [5.9, 6.3, 6.2 , 6.2]
efermi  = [1.9671, 3.1106, 4.2752, 3.6711]

ind = 0
mhn_a = 0.001
mhn = [0.06, 0.09, 0.035, 0.085]

# -----------------

for ind, (ff, lat, ef, mhn_b) in enumerate(zip(folderfile, lattice, efermi, mhn)):
  mat=w90(rf"../../_data/wann_tb_files/{ff}_wan",f"{ff}");
  path=[[0,0,0], [0.0,0.5, 0.0],[0.5,0.5,0.0], [0.,0.,0.0], [0.5, 0.5, 0.5], [0,0.5,0], [0.5,0.5,0], [0.5,0.5,0.5]]
  report = False
  k_label=(r'$\Gamma$', r'X',r'M', r'$\Gamma$', r'R',r'X',r'M',r'R')

  fig, ax = plt.subplots(figsize = [6,6])
  tuneandplottb(mat, path, report, k_label, min_hopping_norm = mhn_a, max_distance=None, color = '#E19C24', label = mhn_a)
  tuneandplottb(mat, path, report, k_label, min_hopping_norm = mhn_b, max_distance=1.5*lat, color = '#5E81B5', label = mhn_b)

  plt.legend(frameon=True, loc = 'lower right', facecolor = '#FFFFFF', framealpha = 0.93, edgecolor = 'white', ncol = 2)
  # plt.legend()
  ax.yaxis.set_major_locator(plt.MaxNLocator(5))
  plt.xlabel('k points')
  plt.ylabel('Energy (eV)')


  plt.savefig(f'../../_plots/TB/RedTB_Bands/{ff}_RedTB_bands.png', format = 'png', dpi = 300)
  plt.savefig(f'../../_plots/TB/RedTB_Bands/{ff}_RedTB_bands.svg', format = 'svg')
  # plt.show()