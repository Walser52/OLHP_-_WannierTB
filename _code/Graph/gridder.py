"""
Description: Make a grid
"""

from jhr.plotters._base import gridder

files = [
  '../../_plots/Graph/CsPbBr3.png',
#  '../../_plots/Graph/CsPbBr2I.png',
  '../../_plots/Graph/CsPbBrI2.png',
#  '../../_plots/Graph/CsPbI3.png',
]

saveto = '../../_plots/Graph/GraphGrid.png'

gridder(files, saveto = saveto, grid = (1,2))


from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

image = Image.open(saveto)
# Create a Draw object
draw = ImageDraw.Draw(image)
w, h = image.size

# Define the text and position
#text = "a"
l = 0.02
r = 0.52
u = 0.02
d = 0.52


pos1 = (l*w, u*h) 
#pos2 = (r*w, u*h) 
pos3 = (l*w, d*h) 
#pos4 = (r*w, d*h) 

font_size = 60  
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)  # Use a path to your font file

col = 'black'

draw.text(pos1, "a", fill=col, font=font)
#draw.text(pos2, "b", fill=col, font=font)
draw.text(pos3, "b", fill=col, font=font)
#draw.text(pos4, "d", fill=col, font=font)

# Save the edited image
image.save(saveto)
