import matplotlib.pyplot as plt
from jhr.plotters._aesthete import select_colors_lines_markers
from jhr.plotters._base import useplotdefaults


#br3, br2i, bri2, i3
vol = [1454.62, 1553.49, 1652.66, 1623.29]
bg = [2.2216, 1.5053, 1.141, 1.1798 ]
lab = [r'CsPbBr$_3$',r'CsPbBr$_2$I',r'CsPbBrI$_2$',r'CsPbI$_3$']
mk = ['s', 'o', '^', '*']
col, _, _ = select_colors_lines_markers(number = 4)


plt.figure(figsize = [5,5])
useplotdefaults(fontsize = 12)
for v, b, m, l, c in zip(vol, bg, mk, lab, col):
  plt.scatter(v, b, marker= m, label = l, color = c, s = 90)

plt.legend(frameon = False)
plt.xlabel(r'Unit cell volume (a.u.$^3$)')
plt.ylabel(r'Bandgap (eV)')

plt.savefig('../../_data/bgvol.png', dpi = 300)
plt.savefig('../../_data/bgvol.svg')

plt.show()
