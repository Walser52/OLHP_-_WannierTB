import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from jhr.io.base import get_vars
from pathlib import Path
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# Example matrix with NaN values
savefolder = '/home/fes33/Documents/GIK - R&D/Personal - Papers and Reports/--Libraries/abinit/Abinitio-Codes/work/perovskites/_plots/Graph/'

tbred_root = '/home/fes33/Documents/GIK - R&D/Personal - Papers and Reports/--Libraries/abinit/Abinitio-Codes/work/perovskites/_data/wann_tbred_files/'

materials = ['CsPbBr3', 'CsPbI3', 'CsPbBr2I', 'CsPbBrI2']
csvfiles = [mat+'.csv' for mat in materials]
mats =  [mat+'_info' for mat in materials]

paths = [tbred_root+file for file in csvfiles]



#Materials info files
mats = ['CsPbBr3_info', 'CsPbI3_info', 'CsPbBr2I_info', 'CsPbBrI2_info']
mats = ['../../_data/materials/' + m + '.py' for m in mats]


for path, m in zip(paths, mats):
  get = ['hmap', 'Pb', 'Br', 'I']
  hmap, Pb, Br, I = get_vars(m, get)

  node_colors = hmap['barcolors']
  color_mapping = {
      Pb: 'Pb',  # dark green
      Br: 'Br',  # green
      I : 'I'    # light green (if it exists in the list)
  }

  node_labels = [color_mapping.get(color, color) for color in node_colors]
#  print(labels)
  arr = np.loadtxt(path, delimiter = ',')

  # Create an empty graph
  G = nx.Graph()

  # Create nodes
  num_nodes = arr.shape[0]
  G.add_nodes_from(range(num_nodes))

  # Add edges where values are not NaN, rounding weights to two decimal places
  for i in range(num_nodes):
      for j in range(i + 1, num_nodes):  # Only check the upper triangle to avoid duplicate edges
          if not np.isnan(arr[i, j]):
              # Round the weight to two decimal places before adding it to the edge
              weight = round(arr[i, j], 2)
              G.add_edge(i, j, weight=weight)
  for i, label in enumerate(node_labels):
      G.nodes[i]['label'] = label

  # Plot the graph
  plt.figure(figsize=(8, 8))

  # pos = nx.spring_layout(G, k=0.5, iterations=50)  # Layout for positioning nodes
  pos = nx.shell_layout(G)
#  pos = nx.circular_layout(G)
#  pos = nx.spectral_layout(G)

  #Edge colors
  edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
  norm = mcolors.Normalize(vmin=min(edge_weights), vmax=max(edge_weights))
  cmap = cm.get_cmap('coolwarm')  # You can choose any colormap like 'coolwarm', 'RdBu', etc.
  edge_colors = [cmap(norm(weight)) for weight in edge_weights]

  nx.draw(G, pos, node_color=node_colors, node_size=2000, font_size=12, font_weight='bold', edge_color=edge_colors, width = 3)

  labels = nx.get_edge_attributes(G, 'weight')
  nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=11)
  node_label_pos = {i: (pos[i][0], pos[i][1]) for i in range(num_nodes)}  # Slight offset for readability
  nx.draw_networkx_labels(G, node_label_pos, labels={i: node_labels[i] for i in range(num_nodes)}, font_size=18, font_weight='bold')


  # Show colorbar to indicate edge weights
#  sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
#  sm.set_array([])  # Empty array for colorbar
#  plt.colorbar(sm)
#
  # Show the plot
  plt.title("Network Graph from Matrix (Weights Rounded to 2 Decimals)")

  stem = Path(path).stem
  plt.savefig(f'{savefolder}{stem}.png', format = 'png', dpi = 300)
  plt.savefig(f'{savefolder}{stem}.svg', format = 'svg')
  # plt.show()

