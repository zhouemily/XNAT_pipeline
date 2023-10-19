#!/usr/bin/env python

import os
import sys
import csv
import subprocess as sp
import cairosvg
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
DEBUG=1

class Pipeline:
    def __init__(self):
        self.name=''
        self.data=[] 

    def svg_to_png(self, svg_file, png_file):
        # Convert SVG files to PNG
        with open(svg_file, 'rb') as svg:
            cairosvg.svg2png(file_obj=svg, write_to=png_file)

    def svg_to_png(self, svg_file, png_file, width, height):
        # Function to resize and convert SVG files to PNG 
        cairosvg.svg2png(file_obj=open(svg_file, 'rb'), write_to=png_file, output_width=width, output_height=height)

    def check_file_exist(self, file_path):
        """
        Check if a file exists and print the result.
        Args:
            file_path (str): The path to the file to be checked.
        """
        if os.path.exists(file_path):
            print(f"The file '{file_path}' exists.")
            msg="The file " + file_path + " exists."
            return msg
        else:
            print(f"The file '{file_path}' does not exist.")
            msg="The file " + file_path + " does NOT exists."
            return msg

    def get_keyValue(self, key,file_path):
        if DEBUG:
            print('DEBUG: csv_file_path='+file_path)

        # Initialize an empty dictionary to store the key-value pairs
        data_dict = {}

        # Check if the CSV file exists
        try:
            with open(file_path, 'r') as csvfile:
                lines = csvfile.readlines()
                if DEBUG:
                    print("DEBUG: print out csv file content\n")
                    for line in lines:
                        print(line)
        
                # Check if there are at least two lines in the file
                if len(lines) >= 2:
                    # Extract the keys (line 1) and values (line 2)
                    k = lines[0].strip().split(',')
                    v = lines[1].strip().split(',')
            
                    # Create key-value pairs and store them in the dictionary
                    data_dict = dict(zip(k, v))
                else:
                    print("The CSV file does not contain enough data.")
        
        except FileNotFoundError:
            print(f"The CSV file '{file_path}' does not exist.")

        # Print the extracted key-value pairs
        if DEBUG:
            for k, v in data_dict.items():
                print(f"Key: {k}, Value: {v}")

            print(key+"="+data_dict[key]+"\n")
        return data_dict[key]

class Util:
    def __init__(self):
        self.data=[]
        self.root_path=""
        self.cups_id=""
        self.png_fname=''
        self.svg_fname1=''
        self.svg_fname2=''
        self.csv_fname=''
        self.keys=["motionDVCorrInit", "motionDVCorrFinal", "estimatedLostTemporalDOF"]
        self.file_check1=''
        self.file_check2=''
        self.debug=0
        self.help=0
        self.verbose=0

    def process_args(self):
        """
        This function process user inputs and set object attributes
        Input:  None (process global variable: sys.argv[1])
        Output: None (assign values to attributes: root path, cups_id, etc)
        Return:   None
        """
        x=sys.argv[1:]
        zlist=["-h","-d","-id","-f","-D","-v"]
        if len(x)==0:
            self.print_help()
            exit(1)
        else:
            if "-id" in x:
                i=x.index("-id")
                self.cups_id=x[i+1]
            else:
                tprint("cups id is needed:\n")
                print("example: ./Xnat_file_pipeline.py -id sub-CUPS003\n")
                self.print_help()
                exit(1)
            
            if "-D" in x:
                self.verbose=1
                self.debug=1
            if "-d" in x:
                i=x.index("-d")
                self.root_path=x[i+1]
            else:
                self.root_path="/System/Volumes/Data/Volumes/CUPS/PipelineOutputs/bids/derivatives/"

            if "-fpng" in x:
                i=x.index("-fpng")
                self.png_fname=x[i+1]
            else:
                self.png_fname=self.root_path+"fsqc/screenshots/"+self.cups_id+"/"+self.cups_id+'.png'

            if "-fsvg1" in x:
                i=x.index("-fsvg1")
                self.svg_fname1=x[i+1]
            else:
                self.svg_fname1=self.root_path+"fmriprep/"+self.cups_id+"/figures/"+self.cups_id+'_ses-A_task-rest_dir-PA_run-1_desc-carpetplot_bold.svg'
            if "-fsvg2" in x:
                i=x.index("-fsvg2")
                self.svg_fname2=x[i+1]
            else:
                self.svg_fname2=self.root_path+"qsiprep/"+self.cups_id+"/figures/"+self.cups_id+'_ses-A_run-1_carpetplot.svg'
      
            #set default:
            self.file_check1=self.root_path+"fmriprep/"+self.cups_id+"/figures/"+self.cups_id+"_ses-A_task-rest_dir-PA_run-1_desc-sdc_bold.svg"
            self.file_check2=self.root_path+"qsiprep/"+self.cups_id+"/figures/"+self.cups_id+"_ses-A_run-1_desc-sdc_b0.svg"
            self.csv_fname=self.root_path+ 'xcp/ses-A/xcp_minimal_aroma/'+self.cups_id+"/"+self.cups_id+'_ses-A_quality_aroma.csv'
            if self.debug:
                print(self.cups_id+"\n")
                print(self.png_fname+"\n")
                print(self.svg_fname1+"\n")
                print(self.svg_fname2+"\n")
                print(self.csv_fname+"\n")
                print(self.fname_check1+"\n")
                print(self.fname_check2+"\n")

    def print_help(self):
        msg="""
            Usage: ./XNAT_file_pipeline.py -id cups_id [-h] [-D] [-v] [-fpng png_fname] [-fsvg1 svg_fname1] [-fsvg2 svg_fname2]
            -h			print help menu
            -id [cups_id]       input cups_id
            -D                  run debug mode
            -v                  enable verbose
            -d                  input root path directory
            """
        print(msg)

    def run_cmd(self, cmd):
        """
        This is a function wrapper using python subprocess module
        Input: cmd => command line input
        Output: None
        Return: out, err, proc.returncode
        """
        proc=sp.Popen(cmd, stdout=sp.PIPE,stderr=sp.PIPE,shell=True)
        out, err=proc.communicate()
        out=out.decode("utf8")
        err=err.decode("utf8")
        return out, err, proc.returncode
           
###############################################################
global tprint

def tprint(*args):
    tempa = ' '.join(str(a) for a in args)
    print(str(datetime.now().strftime('%Y-%m-%d %H:%M%S')) + " " + tempa)        

def main():
    print("Program Started")
    # Load the PNG and resized SVGs
   
    pl=Pipeline()             #create instance from Pipeline class
    ut=Util()                 #create instance from Util class
    ut.process_args()
    if ut.help:
        ut.print_help()
        exit(1)
    kv1 = pl.get_keyValue(ut.keys[0],ut.csv_fname)
    kv2 = pl.get_keyValue(ut.keys[1],ut.csv_fname)
    kv3 = pl.get_keyValue(ut.keys[2],ut.csv_fname)

    png_image = Image.open(ut.png_fname)
    # Define the new dimensions (width and height) you want for the resized image
    new_width = int(0.8 * png_image.width)  # Adjust to your desired width
    new_height = int(0.8 * png_image.height)  # Adjust to your desired height

    # Resize the image
    resized_image = png_image.resize((new_width, new_height))

    # Save the resized image
    resized_image.save('resized_image.png')

    # Resize and convert the first SVG 
    pl.svg_to_png(ut.svg_fname1, 'temp1.png', png_image.width *1.5, png_image.height*1.5)
    # Resize and convert the second SVG 
    pl.svg_to_png(ut.svg_fname2, 'temp2.png', png_image.width *1.5, png_image.height *1.5)
    image1 = Image.open('temp1.png')
    image2 = Image.open('temp2.png')

    # Determine the size of the stacked image
    width = png_image.width
    height = png_image.height * 5  # five times the height of the PNG image

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
    font = ImageFont.truetype("/System/Library/Fonts/Geneva.ttf", font_size) #full path to fond is needed here 

    # Specify the position and text to be added
    #text_position = (500, png_image.height)  # Adjust the position as needed
    #text = "add needed text or check mark here"  # Replace with the desired text
    #draw.text(text_position, text, fill="white", font=font)
    text1 = pl.check_file_exist(ut.file_check1) # check if the required file is exist
    text2 = pl.check_file_exist(ut.file_check2)

    # Calculate the position to center the text horizontally and vertically
    ##text_width, text_height = draw.textsize(text, font)
    x = width / 2
    #y = (height - text_height) // 2
    y = png_image.height

    # Add text to the image at the calculated position
    draw.text((x, y), text1, fill="red", font=font) ##first text string from file_check1
    draw.text((x, y+png_image.height+50), text2, fill="red", font=font) ##another text position
    draw.text((0,y+100), ut.keys[0]+"="+kv1, fill="blue", font=font)
    draw.text((0,y+200), ut.keys[1]+"="+kv2, fill="blue", font=font)
    draw.text((0,y+300), ut.keys[2]+"="+kv3, fill="blue", font=font)
    #################################################

    # Save the stacked image
    stacked_image.save(ut.cups_id+'stacked_image.png')

    # Clean up temporary PNG files
    image1.close()
    image2.close()

    # Clean up temporary files
    #os.remove(image1)
    #os.remove(image2)
    #os.remove('resized_image.png')

    print("Stacked image saved as "+ut.cups_id+ 'stacked_image.png')
    print("End of Program")

if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nexception detected, exit now...")
        exit(1)