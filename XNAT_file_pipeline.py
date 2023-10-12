#!/usr/bin/env python

import os
import cairosvg
from PIL import Image, ImageDraw, ImageFont

# Convert SVG files to PNG
def svg_to_png(svg_file, png_file):
    with open(svg_file, 'rb') as svg:
        cairosvg.svg2png(file_obj=svg, write_to=png_file)


# File paths for the three input files
root_path = "/System/Volumes/Data/Volumes/CUPS/"
png_file_path = root_path + "PipelineOutputs/bids/derivatives/fsqc/screenshots/sub-CUPS003/sub-CUPS003.png"
svg_file_path1 = root_path + "PipelineOutputs/bids/derivatives/fmriprep/sub-CUPS003/figures/sub-CUPS003_ses-A_task-rest_dir-PA_run-1_desc-carpetplot_bold.svg"
svg_file_path2 = root_path + "PipelineOutputs/bids/derivatives/qsiprep/sub-CUPS003/figures/sub-CUPS003_ses-A_run-1_carpetplot.svg"

# Function to resize and convert SVG files to PNG 
def svg_to_png(svg_file, png_file, width, height):
    cairosvg.svg2png(file_obj=open(svg_file, 'rb'), write_to=png_file, output_width=width, output_height=height)

print("Program Started")
# Load the PNG and resized SVGs
png_image = Image.open(png_file_path)

# Define the new dimensions (width and height) you want for the resized image
new_width = int(0.8 * png_image.width)  # Adjust to your desired width
new_height = int(0.8 * png_image.height)  # Adjust to your desired height

# Resize the image
resized_image = png_image.resize((new_width, new_height))

# Save the resized image
resized_image.save('resized_image.png')

# Resize and convert the first SVG 
svg_to_png(svg_file_path1, 'temp1.png', png_image.width, png_image.height)
image1 = Image.open('temp1.png')

# Resize and convert the second SVG 
svg_to_png(svg_file_path2, 'temp2.png', png_image.width, png_image.height)
image2 = Image.open('temp2.png')

# Determine the size of the stacked image
width = png_image.width
height = png_image.height * 3  # Three times the height of the PNG image

# Create a new image with the determined size
stacked_image = Image.new('RGB', (width, height))

# Paste the PNG and SVG images onto the stacked image
#stacked_image.paste(png_image, (0, 0)) 
stacked_image.paste(resized_image, (300, 0)) 
stacked_image.paste(image1, (0, png_image.height+50))
stacked_image.paste(image2, (0, 2 * png_image.height+50))

#######################################################
# Create a drawing context to add text
draw = ImageDraw.Draw(stacked_image)
# Use a system font and specify the size
font_size = 36  # Adjust the font size as needed
#font = ImageFont.truetype("arial.ttf", font_size)  # Replace "arial.ttf" with your desired font and font path
font = ImageFont.truetype("/System/Library/Fonts/Geneva.ttf", font_size) 

# Specify the position and text to be added
#text_position = (500, png_image.height)  # Adjust the position as needed
text = "add needed text or check mark here"  # Replace with the desired text
#draw.text(text_position, text, fill="white", font=font)

# Calculate the position to center the text horizontally and vertically
text_width, text_height = draw.textsize(text, font)
x = (width - text_width) // 2
#y = (height - text_height) // 2
y = png_image.height

# Add text to the image at the calculated position
#draw.text((x, y), text, fill="white", font=font)
draw.text((x, y), text, fill="red", font=font) ##first text string
draw.text((x, y+png_image.height+50), text, fill="red", font=font) ##another text position
#################################################

# Save the stacked image
stacked_image.save('stacked_image.png')

# Clean up temporary PNG files
image1.close()
image2.close()

# Clean up temporary files
os.remove(image1)
os.remove(image2)

print("Stacked image saved as 'stacked_image.png'")
print("End of Program")
