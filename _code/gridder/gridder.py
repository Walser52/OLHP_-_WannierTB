# """
# Description: Make a grid
# """

# from jhr.plotters._base import gridder

# files = [
#   '../../_data/WannOrbs/Pb_xsf.png',
#   '../../_data/WannOrbs/px_xsf.png',
  
#   '../../_data/WannOrbs/py_xsf.png',
#   '../../_data/WannOrbs/pz_xsf.png']

# saveto = '../../_plots/WannOrbs/WannOrbsgrid.png'

# gridder(files, saveto = saveto)


# from PIL import Image
# from PIL import ImageFont
# from PIL import ImageDraw 

# # desired_size = (300, 300)  # Set desired image size for each image in the grid
# # resized_files = []

# # for file in files:
# #     img = Image.open(file)
# #     img = img.resize(desired_size)
# #     resized_files.append(img)
    
# # gridder(resized_files, saveto=saveto)

# # Open the saved image for annotation
# image = Image.open(saveto)
# draw = ImageDraw.Draw(image)
# w, h = image.size

# # Define the text and position
# text = "a"
# l = 0.01
# r = 0.52
# u = 0.02
# d = 0.52


# pos1 = (l*w, u*h) 
# pos2 = (r*w, u*h) 
# pos3 = (l*w, d*h) 
# pos4 = (r*w, d*h) 

# font_size = 60  
# font = ImageFont.truetype(r"C:\Users\HP\Downloads\dejavu-sans\DejaVuSans-Bold.ttf", font_size)  # Use a path to your font file

# col = 'black'

# draw.text(pos1, "a", fill=col, font=font)
# draw.text(pos2, "b", fill=col, font=font)
# draw.text(pos3, "c", fill=col, font=font)
# draw.text(pos4, "d", fill=col, font=font)

# # Save the edited image
# image.save(saveto)

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from jhr.plotters._base import makeplot, annotate
# Paths to your 4 images
images = [
    '../../_data/WannOrbs/Pb_xsf.png',
    '../../_data/WannOrbs/px_xsf.png',
    '../../_data/WannOrbs/py_xsf.png',
    '../../_data/WannOrbs/pz_xsf.png'
]



# Create a figure and 2x2 grid
fig, axes = plt.subplots(2, 2, figsize=(8.5, 8))  # Adjust figsize for size control

plt.subplots_adjust(wspace=0.25, hspace=0.4)

# Loop through each image, annotation, and corresponding subplot
for ax, img_path in zip(axes.ravel(), images):
    img = mpimg.imread(img_path)  # Read image
    ax.imshow(img)  # Display image in the subplot
    ax.axis('off')  # Turn off axes for better aesthetics
    # Add annotation in the top-left corner
    # ax.text(0.05, 0.9, annotation, transform=ax.transAxes, fontsize=14, 
            # color='black', 
            # bbox=dict(facecolor='black', alpha=0.7, boxstyle="round")
            # )
annotate(loc = (-0.05, 1.0), size=18)
# ax.text(0.05, 0.9, transform=ax.transAxes, fontsize=14, 
#             color='black')
            
# Save the grid to a file
plt.tight_layout()
plt.savefig('../../_plots/WannOrbs/WannOrbsgrid_annotated.png', dpi=300)

# Show the grid
plt.show()
