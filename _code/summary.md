## bandDOS

Plot the bandstructure and density of states calcuated from DFT in QE.
### banderDOS.py
Input:
### banderDOSGrid.py
Description: Loop over all the provided materials and generate grid of bands and DOS.
Input: Materials_info files from "_data/materials/mat_info" which contians the dft bands and DOS path.
Output: Save plot in "_plots/BandsDOS/title"


## bandsWannier
Complete code to plot DFT Bands, Wannier Bands and DOS depends on its handling. Enable the option which you want to plot. It contains the following file:

### banderWanniergrid.py
Description: Loop over all the provided materials, superimpose W90 bands on DFT bands and generate grid.
Input: Materials_info files from "_data/materials/mat_info" which contians the dft and w90 bands path.
Output: Save plot in "_plots/BandsWannier/title"


## BoltzWwnn
### boltzwann.py
Description: Plots all the thermoelectric properties (botzdos, elcond, kappa, seebeck, sigmas, tdf) calculated using Boltzwann module of w90. 
Input: Materials_info files from "_data/materials/mat_info" which contains the boltzwann files path.
Output: Save grid of plots in "_plots/BoltzWann/ThermalProperties"

## pythtb
It contains the following files:

### tbheat_W90plotter
Description: Generate heatmap grid for nxn basis of w90 which contains the hopping strength
Input: Read mat_hr.dat and mat.wout file from "_data/wann_tb_files/mat_wan"
Output: Save grids for each mat and grid of grid of mats m in "_plots/TB/HeatTB"

### redTB_bands.py
Description: Plot bands with minimum hopping norm and superimpose them on w90 bands
Input:
Output:

### redTB_tsvGenerator
Description: Generate tsv files for mats m to further utilize them in
Format of tsv files: 
    First 3 columns: Translated unit cell vectors
    4 and 5 column: Wannier basis
    6 and 7 column: Real and imaginary parts of energies
Input: "_data/wann_tb_files/mat_wan/mat"
Output: Save tsv files in "_data/wann_tbred_files/"

### tbheat_redplotter
Description: Read tsv files and generate grid of reduced tight binding scheme for all mats.
Input: "_data/wann_tberd_files/mat.tsv"
Output: Save plot of separate as well as the grid of reduced tb grids of mats m in "_plots/TB/HeatTbRed/"

### hopdensity.py
Description: It generates histplot and density plot (frequency vs hopping strength)
Input: Reads tsv files from "_data/wann_tbred_files/mat.tsv"
Output: Save plot in "_plots/

### dist_hop.py
Description: Plots log of hopping strength vs distance (in terms of avg unit cell length).
Input: wannier tightbinding files from "_data/wann_tb_files/mat_wan/mat"
Output: Save plot in "_plots/TB/dist_hop.png"

## TB_pythtb

