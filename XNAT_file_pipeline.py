#!/usr/bin/env python
"""
Author: Emily Rong Zhou 
Release Version: 1.0
"""
import os
import sys
import csv
import subprocess as sp
import cairosvg
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import pydicom
from pydicom.datadict import tag_for_keyword
import numpy as np
import inspect

class Pipeline:
    def __init__(self, debug=None,verbose=None,local=None):
        self.debug=debug
        self.verbose=verbose 
        self.local=local 
        self.png=''
        self.jpeg=''
        self.dicom=''

    def svg_to_png(self,svg_file, png_file, width=None, height=None, remove_margins=False):
        # Define the options for rendering
        options = {}
        if width and height:
            options['output_width'] = width
            options['output_height'] = height

        if self.debug:
            print("svg2png::png_file="+png_file+" width="+str(width)+" height="+str(height)+" remove_margins="+str(remove_margins))
        # Convert the SVG to PNG 
        cairosvg.svg2png(url=svg_file, write_to=png_file, **options)

        # Optionally remove margins
        if remove_margins:
            # Open the PNG and remove transparent margins
            img = Image.open(png_file)
            img = img.crop(img.getbbox())
            img.save(png_file)
        if self.debug:
            print(png_file+ " size::width="+ str(img.width)+" height="+str(img.height))

    def check_file_exist(self, file_path):
        """
        Check if a file exists and print the result.
        Args:
            file_path (str): The path to the file to be checked.
        """
        if os.path.exists(file_path):
            print(f"The file '{file_path}' exists.")
            msg="Susceptibility distortion correction: Applied"
            return msg
        else:
            print(f"The file '{file_path}' does not exist.")
            msg="Susceptibility distortion correction: Not Applied"
            return msg

    def get_keyValue(self, key,file_path):
        # Initialize an empty dictionary to store the key-value pairs
        data_dict = {}
        if self.debug:
            print('self.debug: csv_file_path='+file_path)
            if len(file_path)==0:
                return "csv_file not found"
             
        # Check if the CSV file exists
        try:
            with open(file_path, 'r') as csvfile:
                lines = csvfile.readlines()
                if self.debug:
                    print("self.debug: print out csv file content\n")
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
                    if self.local:
                        return "CSV file does not contian enough data"
        
        except FileNotFoundError:
            print(f"The CSV file '{file_path}' does not exist.")
            if self.local:
                return "CSV file Not Exist"

        # Print the extracted key-value pairs
        if self.debug:
            for k, v in data_dict.items():
                print(f"Key: {k}, Value: {v}")

            print(key+"="+data_dict[key]+"\n")
        return data_dict[key]

    def png2jpg(self,png_file):
        #convert an png_file to jpeg file which can be convertered to dicom with img2dcm from dcmtk tool set    
        #img2dcm tool does not support png to dcm directly, see reference documentation for more details
        #https://support.dcmtk.org/docs/img2dcm.html
        if self.local:
            print("input png_file is: "+png_file)
        im = Image.open('./'+png_file)
        rgb_im = im.convert('RGB')
        self.jpg=png_file.replace('png','jpg')
        rgb_im.save(self.jpg)
        return self.jpg

    def jpg2dcm(self,jpg_file):
        #input with dicom dataSet object, and jpg image, return with dicom file
        #https://support.dcmtk.org/docs/img2dcm.html
        #img2dcm [options] imgfile-in... dcmfile-out
        #put dicom file in out_directory: ./dcm_dir directory(default directory)
        self.dicom='./dcm_dir/'+jpg_file.replace('jpg','dcm')
        cmd='/usr/local/bin/img2dcm ./'+self.jpg+' '+self.dicom
        proc=sp.Popen(cmd, stdout=sp.PIPE,stderr=sp.PIPE,shell=True)
        out, err=proc.communicate()
        out=out.decode("utf8")
        err=err.decode("utf8")
        if proc.returncode:
            print("jpg2dcm is NOT successful")
        else:
            print("jpg2dcm is successful: dcm="+self.dicom)
        return  proc.returncode
  
    def dcmodify(self,dcm_file, util_obj):
        #use dcmodify from dcmtk toolkit to modify dcm file
        #https://support.dcmtk.org/docs/dcmodify.html
        #dcmodify -i "(0010,0010)=A Name" file.dcm 
        #https://dicom.innolitics.com/ciods/cr-image/general-series/00080060 (tag)

        full_path = os.path.abspath(dcm_file)
        if self.verbose:
            print(full_path)

        meta_info=["(0010,0010)="+util_obj.cups_id+"_A","(0010, 0020)="+util_obj.cups_id,
                   "(0008,1030)=CUPS",
                   "(0008,103e)=Sample Series",
                   "(0008,0020)=20211203",
                   "(0008,0021)=20211203",
                   "(0008,0060)=MR"]
        for e in meta_info:
            cmd="/usr/local/bin/dcmodify -i "+ "\""+e +"\" "+ full_path
            out,err,ret=Util().run_cmd(cmd)	
            if ret!=0:
                print("dcmodify is NOT successful, cmd ="+cmd)
            if self.verbose:
                print("cmd is: "+cmd)
                if ret==0:
                    print("dcmodify is successful\n")
                else:
                    print("dcmodify is NOT successful\n")
       
    ##def dcmodify(self, dcm_file, patient_comment):
    def dcmodify2(self,dcm_file, util_obj):
        #add patient commant which is List Type 
        patient_comment=[]
        #(0010,4000)=patient_comment
        subject_value=util_obj.cups_id.replace("CUPS","CUPS_")
        session_value=subject_value+"_A"
        # Assign the "Patient Comments" attribute
        p_comment="Project:CUPS;Subject:"+subject_value+";Session:"+session_value
        patient_comment.append(p_comment)

        # Convert the list of comments into a single formatted comment string
        formatted_comment = "\\\\n".join(patient_comment)  # Use double backslashes for line breaks

        # Construct the dcmodify command
        cmd = [
            "/usr/local/bin/dcmodify",
            "-i", f"(0010,4000)={formatted_comment}",
            dcm_file
        ]

        try:
            # Run the dcmodify command
            sp.run(cmd, check=True)
            print("Patient Comments modified successfully.")
        except sp.CalledProcessError as e:
            print(f"Error: {e}")

    def modify_dcm(self, dcm_file, util_obj):
        #it works to modify dcm file, but cant NOT be viewed by Weasis tool
        #pass util class obj for cups_id, etc parameters
        if len(dcm_file)==0:
            print("Error: dcm_file is NULL")
            sys.exit(1)
        else:
            dicom_file_path='./'+dcm_file
            if len(dicom_file_path)==0:
                print("Error: dcm_file path is NULL")
                sys.exit(1)

            ds = pydicom.dcmread(dicom_file_path, force=True)

            # Set other mandatory DICOM attributes
            patient_comment=[]
            subject_value=util_obj.cups_id.replace("CUPS","CUPS_")
            session_value=subject_value+"_A"
            # Assign the "Patient Comments" attribute
            p_comment="Project:CUPS;Subject:"+subject_value+";Session:"+session_value
            patient_comment.append(p_comment)
            # Create a DataElement for "Patient Comments"
            patient_comment_element = pydicom.DataElement(0x00104000, "LT", patient_comment)
            # Assign the DataElement to the DICOM dataset
            ds.add(patient_comment_element)
            ds.save_as('out.dcm', write_like_original=False)

            print("final file is: out.dcm")
            
    def png2dcm(self, cups_id, dicom_file_path, png_file_path):
        # Specify the path to your DICOM file and PNG file
        #this method does not work 100%, more work is needed for view it with Weasis tool
        try:
            # Read the existing DICOM file
            ds = pydicom.dcmread(dicom_file_path, force=True)

            # Open the PNG file for replacement
            im_frame = Image.open(png_file_path)

            if im_frame.mode == 'L':
                # (8-bit pixels, black and white)
                np_frame = np.array(im_frame.getdata(), dtype=np.uint16)
                ds.Rows = im_frame.height
                ds.Columns = im_frame.width
                ds.PhotometricInterpretation = "MONOCHROME1"
                ds.SamplesPerPixel = 1
                ds.BitsStored = 16
                ds.BitsAllocated = 16
                ds.HighBit = 15
                ds.PixelRepresentation = 0
                #ds.PixelData = np_frame.tobytes()
                ds.PixelData = np.array(im_frame.getdata(), dtype=np.uint8)
                ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRBigEndian
                vr = 'OB'  # Other Byte String
                ds[0x7FE0, 0x0010].VR = vr  # Explicitly set VR for Pixel Data
                ds.save_as(cups_id+'_bw.dcm')
            elif im_frame.mode == 'RGBA':
                # Check if the image is 'RGBA'
                np_frame = np.array(im_frame.convert('RGB'), dtype=np.uint16)
                ds.Rows = im_frame.height
                ds.Columns = im_frame.width
                ds.PhotometricInterpretation = "RGB"
                ds.SamplesPerPixel = 3
                ds.BitsStored = 16
                ds.BitsAllocated = 16
                ds.HighBit = 15
                ds.PixelRepresentation = 0
                #ds.PixelData = np_frame.tobytes()
                pixel_data = np.array(im_frame.getdata(), dtype=np.uint8).tobytes()
                vr = 'OW'  # Other Word String
                ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRBigEndian
                # Update the DICOM dataset with pixel data and VR
                ds.PixelData = pixel_data
                ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian  # Use appropriate transfer syntax
                ds[0x7FE0, 0x0010].VR = vr  # Explicitly set VR for Pixel Data
                # Save the updated DICOM file
                dcm_file=cups_id+'_rgb.dcm'
                ds.save_as(dcm_file)
                print("DICOM file saved as: "+dcm_file)
            else:
                raise ValueError("Unsupported image mode")
        except Exception as e:
            print(f"Error: {str(e)}")

class Util:
    def __init__(self):
        self.data=[]
        self.root_path=""
        self.cups_id=""
        self.sub_cups_id=""
        self.png_fname=''
        self.svg_fname1=''
        self.svg_fname2=''
        self.csv_fname1=''
        self.csv_fname2=''
        self.keys1=["motionDVCorrInit", "motionDVCorrFinal", "estimatedLostTemporalDOF"]
        self.keys2=["raw_coherence_index","t1_coherence_index"] 
        self.file_check1=''
        self.file_check2=''
        self.debug=0
        self.help=0
        self.verbose=0
        self.local=0
        self.dicom_metadata = {} # Load the provided sample DICOM metadata

    def process_args(self):
        """
        This function process user inputs and set object attributes
        Input:  None (process global variable: sys.argv[1])
        Output: None (assign values to attributes: root path, cups_id, etc)
        Return:   None
        """
        x=sys.argv[1:]
        zlist=["-h","-d","-id","-f","-D","-v","-L"]
        if len(x)==0:
            self.print_help()
            exit(1)
        else:
            if "-id" in x:
                i=x.index("-id")
                self.cups_id=x[i+1]
                self.sub_cups_id="sub-"+x[i+1]
            else:
                tprint("cups id is needed:\n")
                print("example: ./Xnat_file_pipeline.py -id CUPS003\n")
                self.print_help()
                exit(1)
            
            if "-D" in x:
                self.verbose=1
                self.debug=1
            if "-L" in x:
                self.local=True
            if "-v" in x:
                self.verbose=True
            if "-d" in x:
                i=x.index("-d")
                self.root_path=x[i+1]
            else:
                if self.local:
                    self.root_path="/Users/zhou/uc/mri/xnat/XNAT_pipeline-main/testdir/"
                else:
                    self.root_path="/System/Volumes/Data/Volumes/CUPS/PipelineOutputs/bids/derivatives/"
                print("root_path is set to: "+self.root_path)
            if "-fpng" in x:
                i=x.index("-fpng")
                self.png_fname=x[i+1]
            else:
                if self.local:
                    self.png_fname=self.root_path+"/"+self.sub_cups_id+'.png'
                else:
                    self.png_fname=self.root_path+"fsqc/screenshots/"+self.sub_cups_id+"/"+self.sub_cups_id+'.png'

            if "-fsvg1" in x:
                i=x.index("-fsvg1")
                self.svg_fname1=x[i+1]
            else:
                if self.local:
                    self.svg_fname1=self.root_path+"/"+self.sub_cups_id+'_ses-A_task-rest_dir-PA_run-1_desc-carpetplot_bold.svg'
                else:
                    self.svg_fname1=self.root_path+"fmriprep/"+self.sub_cups_id+"/figures/"+self.sub_cups_id+'_ses-A_task-rest_dir-PA_run-1_desc-carpetplot_bold.svg'
            if "-fsvg2" in x:
                i=x.index("-fsvg2")
                self.svg_fname2=x[i+1]
            else:
                if self.local:
                    self.svg_fname2=self.root_path+"/"+self.sub_cups_id+'_ses-A_run-1_carpetplot.svg'
                else:
                    self.svg_fname2=self.root_path+"qsiprep/"+self.sub_cups_id+"/figures/"+self.sub_cups_id+'_ses-A_run-1_carpetplot.svg'
      
            #set default:
            if self.local:
                #self.file_check1=self.root_path+self.sub_cups_id+"_ses-A_task-rest_dir-PA_run-1_desc-sdc_bold.svg"
                self.file_check1=self.root_path+self.sub_cups_id+"_ses-A_task-rest_dir-PA_run-1_desc-carpetplot_bold.svg"
                #self.file_check2=self.root_path+self.sub_cups_id+"_ses-A_run-1_desc-sdc_b0.svg"
                self.file_check2=self.root_path+self.sub_cups_id+"_ses-A_run-1_carpetplot.svg"
                self.csv_fname1=self.root_path+self.sub_cups_id+'_ses-A_quality_aroma.csv'
                self.csv_fname2=self.root_path+self.sub_cups_id+'_ses-A_run-1_desc-ImageQC_dwi.csv'
            else:
                self.file_check1=self.root_path+"fmriprep/"+self.sub_cups_id+"/figures/"+self.sub_cups_id+"_ses-A_task-rest_dir-PA_run-1_desc-sdc_bold.svg"
                self.file_check2=self.root_path+"qsiprep/"+self.sub_cups_id+"/figures/"+self.sub_cups_id+"_ses-A_run-1_desc-sdc_b0.svg"
                self.csv_fname1=self.root_path+ 'xcp/ses-A/xcp_minimal_aroma/'+self.sub_cups_id+"/"+self.sub_cups_id+'_ses-A_quality_aroma.csv'
                self.csv_fname2=self.root_path+ 'qsiprep/'+self.sub_cups_id+'/ses-A/dwi/'+self.sub_cups_id+'_ses-A_run-1_desc-ImageQC_dwi.csv'
            if self.debug:
                print(self.sub_cups_id+"\n")
                print(self.png_fname+"\n")
                print(self.svg_fname1+"\n")
                print(self.svg_fname2+"\n")
                print(self.csv_fname1+"\n")
                print(self.csv_fname2+"\n")
                print(self.file_check1+"\n")
                print(self.file_check2+"\n")

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
###############################################################global
global tprint

def tprint(*args):
    tempa = ' '.join(str(a) for a in args)
    print(str(datetime.now().strftime('%Y-%m-%d %H:%M%S')) + " " + tempa)        

def debug_print(message):
    # Get the current frame in the call stack
    frame = inspect.currentframe()
    if frame is not None:
        try:
            # Get the caller's function or method name
            caller_name = inspect.getframeinfo(frame.f_back).function
            
            # Get the line number where this function is called
            line_number = frame.f_back.f_lineno
            
            # Print the debug information
            print(f"DEBUG [{caller_name}:{line_number}]: {message}")
        finally:
            # Always release the frame to prevent resource leaks
            del frame
#################################################################main
def main():
    print("Program Started")
    # Load the PNG and resized SVGs
    debug_print("This is a debug message from debug_print function")
   
    ut=Util()                 #create instance from Util class, process user arguments
    ut.process_args()
    if ut.help:
        ut.print_help()
        exit(1)

    pl=Pipeline(ut.debug,ut.verbose,ut.local)             #create instance from Pipeline class with flags passed
    if pl.debug:
        print("run debugging...")
    if pl.verbose:
        print("run with verbose mode...")
    if pl.local:
        print("run with local files...")
        

    # Load the provided sample DICOM metadata
    print("Input is: "+ut.cups_id)
    p_name=ut.cups_id.replace("CUPS","CUPS_")
    p_id=p_name+"_A"
    ut.dicom_metadata = {
            (0x0010, 0x0010): p_name,  # Patient's Name
            (0x0010, 0x0020): p_id,  # Patient ID
            (0x0008, 0x1030): "CUPS",  # Study Description
            (0x0008, 0x0020): "20211203",  # Study Date
            (0x0008, 0x0021): "20211203",  # Series Date
            (0x0020, 0x000D): "1.3.12.2.1107.5.2.0.79030.30000021120314124240800000013",  # Study Instance UID
            (0x0008, 0x0016): "1.2.840.10008.5.1.4.1.1.4",  # SOP Class UID
    }
    if ut.debug:
        print("dicom_metadata:\n")
        print(ut.dicom_metadata)

    png_image = Image.open(ut.png_fname)
    # Define the new dimensions (width and height) you want for the resized image
    #new_width = int(0.8 * png_image.width)  # Adjust to your desired width
    #new_height = int(0.8 * png_image.height)  # Adjust to your desired height
    # Resize the image
    # Save the resized image
    #resized_image = png_image.resize((new_width, new_height))
    #resized_image.save('resized_image.png')

    # Resize and convert the first SVG  to PNG
    pl.svg_to_png(ut.svg_fname1, 'temp1.png', width=png_image.width*2, height=png_image.height*1.5, remove_margins=True)
    pl.svg_to_png(ut.svg_fname2, 'temp2.png', width=png_image.width*2, height=png_image.height*1.5, remove_margins=True)
    if pl.debug:
        print("svg2png_image.width="+str(png_image.width*2))
        print("svg2png_image.height="+str(png_image.height*1.5))

    image1 = Image.open('temp1.png')
    new_width = png_image.width
    factor = float(png_image.width / image1.width)
    new_height = int(image1.height*factor)

    # Save the resized image
    r_image1 = image1.resize((new_width, new_height))
    r_image1.save('r_image1.png')

    image2 = Image.open('temp2.png')
    new_width = png_image.width
    factor = float(png_image.width / image2.width)
    new_height = int(image2.height*factor)

    # Save the resized image
    r_image2 = image2.resize((new_width, new_height))
    r_image2.save('r_image2.png')

    # Determine the size of the stacked image
    width = png_image.width
    ##height = png_image.height * 5  # five times the height of the PNG image
    #height = png_image.height * 10  # ten times the height of the PNG image
    height = png_image.height * 8  # eight times the height of the PNG image

    if ut.debug:
        print("stacked image width="+str(width)+"\n")
        print("stacked image height="+str(height)+"\n")
    # Create a new image with the determined size
    #stacked_image = Image.new('RGB', (width, height))
    stacked_image = Image.new('RGBA', (width, height))

    # Paste the PNG and SVG images onto the stacked image
    stacked_image.paste(png_image, (0, 0)) 
    stacked_image.paste(r_image1, (0, png_image.height)) #svg1_2_png paste

    # Create a drawing context to add text
    draw = ImageDraw.Draw(stacked_image)
    # Use a system font and specify the size
    font_size = 36  # Adjust the font size as needed
    font_path = "/System/Library/Fonts/Geneva.ttf"
    font = ImageFont.truetype(font_path, font_size) #full path to fond is needed here 

    kv1 = pl.get_keyValue(ut.keys1[0],ut.csv_fname1)
    if len(kv1)==0:
        kv1=" not found"
    kv2 = pl.get_keyValue(ut.keys1[1],ut.csv_fname1)
    if len(kv2)==0:
        kv2=" not found"
    kv3 = pl.get_keyValue(ut.keys1[2],ut.csv_fname1)
    if len(kv3)==0:
        kv3=" not found"

    x=0
    color="yellow"
    y1 = png_image.height+r_image1.height+50
    draw.text((0,y1), ut.keys1[0]+"="+kv1, fill=color, font=font)
    draw.text((0,y1+50), ut.keys1[1]+"="+kv2, fill=color, font=font)
    draw.text((0,y1+100), ut.keys1[2]+"="+kv3, fill=color, font=font)
    text1 = pl.check_file_exist(ut.file_check1) # check if the required file is exist
    # Add text to the image at the calculated position
    y2=y1+150
    draw.text((x, y2), text1, fill="red", font=font) ##first text string from file_check1

    y3=y2+100
    stacked_image.paste(r_image2, (0, y3)) #svg2_2_png paste

    y4=y3+r_image2.height+50
    kv_1 = pl.get_keyValue(ut.keys2[0],ut.csv_fname2)
    if len(kv_1)==0:
        kv_1=" not found"
    kv_2 = pl.get_keyValue(ut.keys2[1],ut.csv_fname2)
    if len(kv_2)==0:
        kv_2=" not found"
    draw.text((0,y4), ut.keys2[0]+"="+kv_1, fill=color, font=font)
    draw.text((0,y4+50), ut.keys2[1]+"="+kv_2, fill=color, font=font)

    y5=y4+100
    text2 = pl.check_file_exist(ut.file_check2)
    draw.text((x, y5), text2, fill="red", font=font) ##another text position
    #################################################

    # Save the stacked image
    pl.png=ut.cups_id+'stacked_image.png'
    if len(pl.png)==0:
        print("pl.png file name is NULL")
        sys.exit(1)
    stacked_image.save(pl.png)
    print("Stacked image saved as "+pl.png)

    stacked_image.save(ut.sub_cups_id+'stacked_image.png')
    print("Stacked image saved as "+ut.sub_cups_id+ 'stacked_image.png')

    # Close and Clean up temporary PNG files
    image1.close()
    image2.close()
    r_image1.close()
    r_image2.close()
    os.remove("./temp1.png")
    os.remove("./temp2.png")
    os.remove("./r_image1.png")
    os.remove("./r_image2.png")

    # Create a new DICOM dataset with sample metadata===============
    if len(pl.png)==0:
        sys.exit(0)
    pl.png2jpg(pl.png)

    if len(pl.jpg)==0:
        sys.exit(0)
    pl.jpg2dcm(pl.jpg)
    print("Final DICOM file created: "+pl.dicom)

    ##add all missing meta data tag or elements, etc
    pl.dcmodify(pl.dicom, ut)
    pl.dcmodify2(pl.dicom, ut)
    #pl.modify_dcm(pl.dicom,ut)
    print("End of Program")

if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nexception detected, exit now...")
        exit(1)

"""
# sources of sample dcm in each session

AAHead_Scout_32ch-head-coil_MPR_sag 
fmap_task-rest_acq-7TfMRI_dir-AP 

# maintain from sample dcm
(0010,0010) 	Patient’s Name 	CUPS_008
(0010,0020) 	Patient ID 	CUPS_008_A
(0008,1030) 	Study Description 	CUPS
(0008,0020) 	Study Date 	20211203
(0008,0021) 	Series Date 	20211203
(0020,000D) 	Study Instance UID 	1.3.12.2.1107.5.2.0.79030.30000021120314124240800000013
(0008,0016) 	SOP Class UID 	1.2.840.10008.5.1.4.1.1.4

# to change for PNG QC file:
(0008,0008) 	Image Type 	DERIVED
(0028,0004) 	Photometric Interpretation 	"RGB"
(0028,0002) 	Samples per Pixel 	1
(0028,0004) 	Photometric Interpretation 	MONOCHROME2
(0028,0010) 	Rows 	300
(0028,0011) 	Columns 	306
(0028,0030) 	Pixel Spacing 	0.74666666984558\0.74666666984558
(0028,0100) 	Bits Allocated 	16
(0028,0101) 	Bits Stored 	12
(0028,0102) 	High Bit 	11
(0028,0103) 	Pixel Representation 	0
(0028,0106) 	Smallest Image Pixel Value 	0
(0028,0107) 	Largest Image Pixel Value 	4078
(0028,1050) 	Window Center 	1918
(0028,1051) 	Window Width 	2784
(0028,1055) 	Window Center & Width Explanation 	

# link to code
https://github.com/pydicom/pydicom/issues/939#issuecomment-532475747

   ## example code to create instance with arguments 
class MyClass:
    def __init__(self, arg1, arg2=None, arg3=None):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3

# Creating instances with different argument combinations
obj1 = MyClass("Value1")
obj2 = MyClass("Value1", "Value2")
obj3 = MyClass("Value1", "Value2", "Value3")
"""
