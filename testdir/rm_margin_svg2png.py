
import cairosvg
from PIL import Image  # Import the Image class from Pillow

def convert_svg_to_png(input_svg, output_png, width=None, height=None, remove_margins=False):
    # Define the options for rendering
    options = {}
    
    if width and height:
        options['output_width'] = width
        options['output_height'] = height

    # Convert the SVG to PNG
    cairosvg.svg2png(url=input_svg, write_to=output_png, **options)

    # Optionally remove margins
    if remove_margins:
        # Open the PNG and remove transparent margins
        img = Image.open(output_png)
        img = img.crop(img.getbbox())
        img.save(output_png)

# Example usage:
input_svg = './sub-CUPS003_ses-A_run-1_carpetplot.svg'
output_png = 'output.png'
width = 800
height = 600
remove_margins = True

convert_svg_to_png(input_svg, output_png, width, height, remove_margins)
