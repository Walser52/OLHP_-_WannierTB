"""
Description: Gives distribution and KDE of hopping parameters for the reduced TB model.
Inputs: 
Outputs: 
  - HoppingParamDist.png in _plots/TB
  - Saves dataframe description in _data/wann_tbred_files/summary.csv
  
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# Load the data from the TSV file
import itertools
import pandas as pd
from jhr.plotters._aesthete import select_colors_lines_markers
from jhr.plotters._base import makeplot

files = ['CsPbBr3', 
         'CsPbBr2I', 
        'CsPbBrI2', 
        'CsPbI3'
        ]
#color = itertools.cycle(['red', 'orange', 'blue', 'lightgray'])

all_hops = []

df = pd.DataFrame()
for f in files:
  data = np.loadtxt(f'../../_data/wann_tbred_files/{f}.tsv', delimiter='\t')

  # Extract the last two columns (real and imaginary parts)
  real_part = data[:, -2]
  imaginary_part = data[:, -1]

  # Compute the absolute values
  absolute_values = np.sqrt(real_part**2 + imaginary_part**2)

  # If you want a 1D array
  absolute_values_1d = np.log(absolute_values.flatten())
  dftemp = pd.DataFrame(absolute_values_1d, columns = ['Value'])
  dftemp['Material'] = f


  df = pd.concat([df, dftemp], ignore_index=True)

df['Material'] = df['Material'].replace(r'(\d+)', r'$_\1$', regex=True)



colors, lines, markers = select_colors_lines_markers(number = 8, palette = 'Custom_1')
sns.set_palette(colors[0:])


settings = {'figure': {'figsize': [6,6]},
            'plot': dict(data = df, x = 'Value', bins=30, edgecolor = 'white', alpha =0.25,
                    line_kws={'lw': 2.5, 'ls':'-'}, #fill = None,
                    kde=True, hue = 'Material'),  
          }
makeplot(sns.histplot, settings)


plt.xlabel(r'$log |H\cdot eV^{-1}|$')
plt.ylabel('Frequency')
plt.savefig('../../_plots/TB/HoppingParamDist.png', format = 'png', dpi = 300)
plt.savefig('../../_plots/TB/HoppingParamDist.svg', format = 'svg')
# plt.show()


#------------------

print(df.groupby('Material').describe())
df.groupby('Material').describe().to_csv('../../_data/wann_tbred_files/summary.csv')


