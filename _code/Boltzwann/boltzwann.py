from jhr.plotters._base import makeplot, annotate
from jhr.plotters._aesthete import select_colors_lines_markers

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from jhr._helpers import fileswith
from jhr.io.base import get_vars

import itertools

import glob


import pandas as pd


showplot = False


mats = ['CsPbBr3_info', 
        'CsPbI3_info', 
        'CsPbBr2I_info', 
        'CsPbBrI2_info' 
        ]
mats = ['../../_data/materials/' + m + '.py' for m in mats]


figsize = (10,10)

#_____________Generate Dictionary of DataFrames_________________


#Which line in data file contains column names?
header = {'elcond': 2, 'seebeck': 2, 'boltzdos': 4, 'kappa': 4, 'sigmas':2, 'tdf': 3}


data = {}

for m in mats:

  # with open(m) as f: exec(f.read())
  get = ['title', 'bzwann', 'plottag', 'efermi_wann', 'efermi']
  title, bzwann, plottag, efermi_wann, efermi = get_vars(m, get)


  parameters = bzwann['files'] #File paths for el_cond, seebeck etc.
  
  for param in parameters:
    #Find files matching criteria (e.g. containing seebeck) and use file stem as labels.
    files = fileswith(pattern = f'*{param}*', infolder = bzwann['base'] ) 
    labels = [os.path.basename(os.path.dirname(f)) for f in files]

    for (f, l) in zip(files, labels):
      dftemp = pd.read_csv(f, nrows = 10, header = header[param])
      columns = list(dftemp.columns)[0].split()[1:]
     
      df              = pd.read_csv(f, delim_whitespace=True, comment = '#', header=None)
      df.columns      = columns[0:df.shape[1]]
      df['Material']  = title
      df['Parameter'] = param
      df['Label']     = l
      df['Plottag']   = plottag

      if 'Mu(eV)' in df.columns:        #Shift by fermi level.
<<<<<<< HEAD
        df['Mu(eV)'] = df['Mu(eV)'] - efermi_wann 
=======
#        print(m, efermi, efermi_wann)
        df['Mu(eV)'] = df['Mu(eV)']  - efermi_wann
>>>>>>> 85fecd8b2ebaf43373d1c8be7731b66235cac1c8

      if param not in data.keys(): data[param] = df
      else:                        data[param] = pd.concat([data[param], df], ignore_index = True)
 


#-----------------Figure of Merit----------------

# ZT = sigma * seebeck^2*T/kappa


sb, el, ka = data['seebeck'], data['elcond'], data['kappa']

elsb = pd.merge(el, sb, on=['Mu(eV)', 'Temp(K)', 'Material', 'Label'], how='inner', suffixes=('_el', '_sb'))
elsbka = pd.merge(elsb, ka, on=['Mu(eV)', 'Temp(K)', 'Material', 'Label'], how='inner', suffixes=('_elsb', '_ka'))

elsbka['ZT'] = elsbka['ElCond_xx'] * elsbka['Seebeck_xx']**2*elsbka['Temp(K)']/elsbka['Kappa_xx']
#elsbka['ZT'] = elsbka['ZT'].replace("", np.nan)

elsbka.to_csv('tra.csv')

f1 = ((elsbka['Temp(K)'] == 300))
fil = elsbka[f1]

# _______________PLOT_________________
#--------Cyclers----------
colors, lines, markers = select_colors_lines_markers(number = 4, palette = 'Intense')
colors = ['#d8765b','#1f6096', '#f3b010', '#827f77']
sns.set_palette(colors)



fig, Axs = plt.subplots(2,2, figsize = figsize)
Axs = Axs.flatten()

# Parameter, limits, y_label
pms = [('ElCond_xx',  [-1,6.7], r'Electrical Conductivity ($\Omega^{-1} \cdot m^{-1}$)'), 
      ('Kappa_xx',    [-1,6.7], r'Thermal Conductivity ($W \cdot m^{-1}\cdot K^{-1}$)'),
      ('Seebeck_xx',  [-1,6.7], r'Seebeck Coefficient ($V \cdot K^{-1}$)'),
      ('ZT',          [-1,6.7], 'ZT')]

for ax, pm in zip(Axs, pms):
  plt.sca(ax)

<<<<<<< HEAD
  settings = {'plot': dict(data = fil, x = 'Mu(eV)', y = pm[0] , hue = 'Plottag', linewidth = 2.8),
=======
  settings = {'plot': dict(data = fil, x = 'Mu(eV)', y = pm[0] , hue = 'Plottag', linewidth = 2.4),
>>>>>>> 85fecd8b2ebaf43373d1c8be7731b66235cac1c8
              # 'legend': {'frameon': False},
              'xlabel': r'$\mu  - E_f\ (eV)$',
              'ylabel': pm[2],
<<<<<<< HEAD
              # 'xlim': pm[1]        
=======
#              'xlim': pm[1]        
              'xlim': [-3,3]
>>>>>>> 85fecd8b2ebaf43373d1c8be7731b66235cac1c8
             }
  # plt.axvline(0, color = 'gray', linestyle = '--')
#  sns.lineplot(data=fil, x='Mu(eV)', y=pm[0] , hue = 'Plottag')
#  makeplot(sns.lineplot, settings)
  if pm[0] =='ZT': 
    lw = settings['plot'].pop('linewidth')
    makeplot(sns.scatterplot, settings)
    settings['plot']['linewidth'] = lw
  else: makeplot(sns.lineplot, settings)

  # plt.axvspan(-2,0, facecolor = '#c8e3ae', alpha = 0.2)
  # plt.axvspan(0,2, facecolor = '#e5c9c6', alpha = 0.2)


  # plt.text(0.98, 0.97, "n-type", horizontalalignment='right', verticalalignment='top', transform=ax.transAxes, fontweight = 'bold', bbox=dict(facecolor='#f9f4f3', edgecolor = '#f9f4f3'))
  # plt.text(0.02, 0.97, "p-type", horizontalalignment='left', verticalalignment='top', transform=ax.transAxes, fontweight = 'bold',  bbox=dict(facecolor='#f4f9ee', edgecolor = '#f4f9ee'))
  ax.get_legend().remove()

#  plt.fill_between(fil['Mu(eV)'], fil[pm[0]], where=(fil['Mu(eV)'] < 0), color='green', alpha=0.3)

plt.sca(Axs[2])
plt.legend(frameon = False, loc='lower left')

annotate(size = 16)
plt.savefig('../../_plots/BoltzWann/ThermalProperties.png', format = 'png', dpi = 300)
plt.savefig('../../_plots/BoltzWann/ThermalProperties.svg', format = 'svg')

if showplot: plt.show()
