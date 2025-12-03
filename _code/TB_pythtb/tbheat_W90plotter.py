"""
Description:
  Creates ../_plots/TB/HeatTB/grid_image.png
  A grid of tight-binding heatmaps (not reduced)
Inputs:

Outputs:

"""

from mpl_toolkits.axes_grid1.axes_divider import HBoxDivider, VBoxDivider
import mpl_toolkits.axes_grid1.axes_size as Size


# ============
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd 

from jhr.plotters._base import annotate, ax_divider, createTag
from jhr.codes import W90
from jhr.plotters.plots import tbHeat
from jhr.codes.W90 import GetTBHam

from PIL import Image


# __________Material info files___________
mats = ['MAPbI3_info', 
#        'CsPbBr2I_info'
        ]
mats = ['../../_data/materials/' + m + '.py' for m in mats]



#___________Other info____________
datroot = '../../_data/wann_tb_files/'
spreadsroot = '../../_data/wann_tb_files/'
files = [#HR.dat for TB, Wout for spreads
        ( "MAPbI3_wan/MAPbI3_hr.dat"  ,'MAPbI3_wan/MAPbI3.wout' ),
#        ( "CsPbBr2I_wan/CsPbBr2I_hr.dat"  ,'CsPbBr2I_wan/CsPbBr2I.wout' ),
#        ( "CsPbBrI2_wan/CsPbBrI2_hr.dat"  ,'CsPbBrI2_wan/CsPbBrI2.wout' ),
#        ( "CsPbI3_wan/CsPbI3_hr.dat"  ,'CsPbI3_wan/CsPbI3.wout' ),
        ]

savefolder = '../../_plots/TB/HeatTB/'
num_basis = 130


#________READ__________
datfiles  = [datroot + dat for (dat, spreads) in files]
H_all     = GetTBHam(datfiles, num_basis = num_basis, getfor = 'all', verbose = False)

spreadsfiles = [spreadsroot + spreads for (dat, spreads) in files]
spreads_all = W90.readSpread(spreadsfiles)


done = []

for ind, (H, Spr, f, m)  in enumerate(zip(H_all, spreads_all, spreadsfiles, mats)):
  #Read info files
  with open(m) as f:
    exec(f.read())

  #Generate label to store on figure
#  label = chr(ord('a') + ind)

  fig, ax = plt.subplots(1, 1, figsize=(16,16))
  axs = ax_divider(ax, divisions = 2, direction = 'top', size = '25%')

  #Plot heatmap
  tbHeat(np.log(np.abs(H)), num_basis = num_basis, ax = axs[0], cbar_kw = {'fraction': 0.025}, ticks = False)

  #Plot Bars
  plt.sca(axs[1])
  for i, (spread, color) in enumerate(zip(Spr, hmap['barcolors'])): 
    plt.bar(i, spread, color = color, align='center', width=0.4)
  plt.ylabel(r"WF Spread ($\AA^2$)")
  createTag(name = plottag, pos = (0.01, 1.045), fontsize = 16, weight = 'bold', fontcolor = '#003030' ,  
            bboxsettings = dict(alpha = 0., facecolor = '#005d33', boxstyle = 'round'))
  
  #Save
  plt.savefig(f'{savefolder}{title}.png', format = 'png', dpi = 300)
  done.append(f'{savefolder}{title}.png')







# _____________MAKE A GRID____________
#img = []
#grid = (2,2)
#
#for ind, d in enumerate(done):
#  img.append(Image.open(d))
#
# Assuming all images are the same size
#width, height = img[0].size
#
#grid_image = Image.new('RGB', (width * grid[0], height * grid[1]))
#
#
#grid_image.paste(img[0], (0, 0))  # Top-left
#grid_image.paste(img[1], (width, 0))  # Top-right
#grid_image.paste(img[2], (0, height))  # Bottom-left
#grid_image.paste(img[3], (width, height))  # Bottom-right
#
# Save the resulting image
#saveto = savefolder + 'grid_image.png'
#grid_image.save(saveto)
#
#
#----ANNOTATE----------
#
#from PIL import Image
#from PIL import ImageFont
#from PIL import ImageDraw 
#
#image = Image.open(saveto)
# Create a Draw object
#draw = ImageDraw.Draw(image)
#w, h = image.size
#
# Define the text and position
#text = "a"
#l = 0.02
#r = 0.52
#u = 0.02
#d = 0.52
#
#
#pos1 = (l*w, u*h) 
#pos2 = (r*w, u*h) 
#pos3 = (l*w, d*h) 
#pos4 = (r*w, d*h) 
#
#font_size = 90  
#font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)  # Use a path to your font file
#
#col = 'black'
#
#draw.text(pos1, "a", fill=col, font=font)
#draw.text(pos2, "b", fill=col, font=font)
#draw.text(pos3, "c", fill=col, font=font)
#draw.text(pos4, "d", fill=col, font=font)
#
# Save the edited image
#image.save(saveto)

