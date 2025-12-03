# Generates a tsv file for the reduced TB matrix.

from __future__ import print_function
from pythtb import * # import TB model class
from pythtb.pythtb import * # import TB model class
import matplotlib.pyplot as plt

from jhr.plotters._base import makeplot
from jhr.plotters._aesthete import select_colors_lines_markers

import itertools

root = '../../_data/wann_tb_files/'

folderfile = [ ("CsPbBr3_wan", "CsPbBr3"), ("MAPbI3_wan", "MAPbI3")] #foldername, prefix for Wannier90.
min_hopping_norm = [0.06,0.09,0.033,0.085]

lattice = [5.9, 6.3, 6.2 , 6.2]
efermi = [1.9671, 3.1106, 4.2752, 3.6711]

#===================================================

savefolder = '../../_data/wann_tbred_files/'

# 
folderfile = [(root + x , y) for (x,y) in folderfile]

def to_tsv(data_list, filename):
    with open(filename, 'w') as f:
        for data in data_list:
            output_values = []

            # Extract values in the required order
            output_values.extend(data[3].tolist())  # From the array
            output_values.append(data[1])            # Second element
            output_values.append(data[2])            # Third element

            # First element (complex number)
            real_part = data[0].real
            imag_part = data[0].imag
            output_values.append(real_part)
            output_values.append(imag_part)

            # Write the formatted string to the file
            f.write('\t'.join(map(str, output_values)) + '\n')

    print(f"Data saved to {filename}")



def saveTBred(folderfile, efermi, lattice, min_hopping_norm, lattice_scale = 1.5):
  """
  Save reduced TB to tsv file. 

  Args:
    folderfile: list of tuples in the form [("CsPbBr3_wan", "CsPbBr3"), ...]
    efermi: list of fermi levels
    lattice: avg lattice length
    min_hopping_norm: min hopping norm.
    lattice_scale: max distance in units of lattice length. Defaults to 1.5 if nothing is given.
  
  """
  lattice = [lattice_scale * l for l in lattice]

  for f, ef, md, mhn in zip(folderfile, efermi, lattice, min_hopping_norm):
    mat=w90(f[0], f[1]) #Read W90 output
    mod = mat.model(zero_energy=ef, min_hopping_norm=mhn, max_distance= md, ignorable_imaginary_part=None)

    print("# of hoppings + site energies = ", len(mod._hoppings) + len(mod._site_energies))

    #______Add site energies and save to tsv_______
    sen = []
    for (i,dt) in enumerate(mod._site_energies):
      sen.append([dt+0j, i+1, i+1, np.array([0, 0, 0])])
    
    ham = mod._hoppings + sen

    # ham = np.maximum( ham, ham.transpose() )
    to_tsv(ham, f'{savefolder}{f[1]}.tsv')

  return

saveTBred(folderfile, efermi, lattice, min_hopping_norm, lattice_scale = 1.5)
