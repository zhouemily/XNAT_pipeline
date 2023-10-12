#!/usr/bin/env python

from PIL import Image
import cairosvg

# Convert SVG files to PNG
def svg_to_png(svg_file, png_file):
    with open(svg_file, 'rb') as svg:
        cairosvg.svg2png(file_obj=svg, write_to=png_file)

# Load the PNG and converted SVGs
f1_png="sub-CUPS003.png"
f2_svg="sub-CUPS003_ses-A_run-1_carpetplot.svg"
f3_svg="sub-CUPS003_ses-A_task-rest_dir-PA_run-1_desc-carpetplot_bold.svg"

# Function to resize and convert SVG files to PNG 
def svg_to_png(svg_file, png_file, width, height):
    cairosvg.svg2png(file_obj=open(svg_file, 'rb'), write_to=png_file, output_width=width, output_height=height)

# Load the PNG and resized SVGs
png_image = Image.open(f1_png)

# Resize and convert the first SVG 
svg_to_png(f2_svg, 'temp1.png', png_image.width, png_image.height)
image1 = Image.open('temp1.png')

# Resize and convert the second SVG 
svg_to_png(f3_svg, 'temp2.png', png_image.width, png_image.height)
image2 = Image.open('temp2.png')

# Determine the size of the stacked image
width = png_image.width
height = png_image.height * 3  # Three times the height of the PNG image

# Create a new image with the determined size
stacked_image = Image.new('RGB', (width, height))

# Paste the PNG and SVG images onto the stacked image
stacked_image.paste(png_image, (0, 0)) 
stacked_image.paste(image1, (0, png_image.height))
stacked_image.paste(image2, (0, 2 * png_image.height))

# Save the stacked image
stacked_image.save('stacked_image.png')

# Clean up temporary PNG files
image1.close()
image2.close()

print("Stacked image saved as 'stacked_image.png'")
