import matplotlib.pyplot as plt
import numpy as np

from jhr.plotters.express import DOSExpress
from jhr.plotters.express import bandsExpress

from jhr.plotters._base import createTag, annotate, ax_divider

from cycler import cycler


showplot = True

mats = ['CsPbBr3_info', 'CsPbI3_info', 'CsPbBr2I_info', 'CsPbBrI2_info' ]
mats = ['../../_data/materials/' + m + '.py' for m in mats]

printBG = True #Whether to print BG and Homolumo info to the terminal.
title = 'grid'

savefile = f'../../_plots/BandsWannier/{title}'
high_symmetry_points = {#Define High Symmetry Points
    '$\Gamma$'   : 0,
    'X'          : 30,
    'M'          : 60,
    '$\Gamma$ '  : 90,
    'R'          : 120,
    'X|M'        : 150,
    'R '         : 180
}

figsize = (8,8)



#======================================================
fig, Axs =  plt.subplots(2, 2, figsize=(8, 8))  
if len(Axs) > 1: Axs = Axs.flatten()
else: Axs = [Axs]

# plt.subplots_adjust(left=0.1,
#                     bottom=0.05, 
#                     right=0.95, 
#                     top=0.95, 
#                     wspace=0.2, 
#                     hspace=0.3)


DOS_cycler = cycler(color=['#003049', '#f77f00', '#B028C6', '#f2542d', '#562c2c'])




for m, ax in zip(mats, Axs):
  print(m)
  with open(m) as f:
    exec(f.read())

  #_________Plot settings__________
  #DOS Plot settings
  plotsettingsDOS = {
      'plot':{'x':[], 'y': [], 'label': [], 'alpha': 1, 'lw':0.9}, 
      'xlabel': 'DOS (states/eV)', 
      'set_prop_cycle': DOS_cycler,
      'xlim': xlimDOS,      
      'ylim': ylimDOS,
      'legend': {'frameon': False, 'ncol':2, 'fontsize': 9}}

  #Bands Plot settings
  
  plotsettingsBands = {
      'plot':{'x':[], 'y': [], 'alpha': 0.8, 'color': '#1C829C', 'lw': 0.9}, 
      'yaxis.set_minor_locator': {'AutoMinorLocator': 2},
      'xlabel': 'k points', 
      'ylabel': 'Energy (eV)',
      'ylim': ylimBands,
      # 'legend': {'frameon': False, },
  }
  
  plotsettingsW90Bands = {
      'plot':{'x':[], 'y': [], 'alpha': 0.8, 'color': 'green'}, 
      'ylim': ylimBands, 
  }



  #Create dictionary
  mat = {'DOS': dict(pdos_folder = pdos_folder, totaldosfile = totaldosfile, 
                    toskip = toskipDOS, efermi = efermi, plotTDOS = plotTDOS, plotsettings = plotsettingsDOS),

        'bands': dict(data_file = bandsQEFile, plotsettings = plotsettingsBands, toskip = toskipbands, code = 'QE',
                      symmPoints = high_symmetry_points , efermi = efermi, printAll = False,
                      showhomolumo = showhomolumo, homolumosettings = {'fontsize': 8},
                      bandgapDict = dict(printall = printBG)
                      
                      ),

        'w90bands': dict(data_file = (dat_file_wann, gnu_file_wann), 
                        plotsettings= plotsettingsW90Bands, efermi = efermi_wann,
                        bandgapDict = dict(printall = printBG),
                        scale_k = scale_k, toskip = [], code = 'W90')
  }


  plt.sca(ax)
  bandsExpress(**mat['w90bands'])
  bandsExpress(**mat['bands'])

  createTag(name = plottag, pos = (0.02, 1.02), weight = 'bold', fontcolor = '#003030' ,  bboxsettings = dict(alpha = 0))

  


annotate(labels = 'abcd    ',append = '')
plt.savefig(savefile+'.png', format = 'png', dpi = 350, transparent = True)
plt.savefig(savefile+'.svg', format = 'svg', transparent = True)

if showplot: plt.show()


