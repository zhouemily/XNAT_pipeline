#!/usr/bin/env python
from PIL import Image
import os
import cairosvg

# File paths for the three input files
root_path = "/System/Volumes/Data/Volumes/CUPS/"
png_file_path = root_path + "PipelineOutputs/bids/derivatives/fsqc/screenshots/sub-CUPS003/sub-CUPS003.png"
svg_file_path1 = root_path + "PipelineOutputs/bids/derivatives/fmriprep/sub-CUPS003/figures/sub-CUPS003_ses-A_task-rest_dir-PA_run-1_desc-carpetplot_bold.svg"
svg_file_path2 = root_path + "PipelineOutputs/bids/derivatives/qsiprep/sub-CUPS003/figures/sub-CUPS003_ses-A_run-1_carpetplot.svg"

# Open the PNG image
image_png = Image.open(png_file_path)

# Create temporary filenames for the converted SVG files
png_file_path1 = svg_file_path1.replace(".svg", "_converted.png")
png_file_path2 = svg_file_path2.replace(".svg", "_converted.png")

# Convert SVG files to PNG using CairoSVG
cairosvg.svg2png(url=svg_file_path1, write_to=png_file_path1)
cairosvg.svg2png(url=svg_file_path2, write_to=png_file_path2)

# Open the PNG images converted from SVG
image_svg1 = Image.open(png_file_path1)
image_svg2 = Image.open(png_file_path2)

# Create a new image to stack the PNG and SVG images
width, height = image_png.size
stacked_image = Image.new("RGB", (width, height * 3), (255, 255, 255))

# Paste the PNG image onto the stacked image
stacked_image.paste(image_png, (0, 0))

# Paste the converted SVG images onto the stacked image
stacked_image.paste(image_svg1, (0, height))
stacked_image.paste(image_svg2, (0, height * 2))

# Save the stacked image
stacked_image.save("stacked_image.png")

# Clean up temporary files
os.remove(png_file_path1)
os.remove(png_file_path2)

print("Files have been stacked and saved as 'stacked_image.png'")