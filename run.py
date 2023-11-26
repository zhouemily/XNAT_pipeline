#!/usr/bin/env python
"""         
Author: Emily Rong Zhou
Release Version: 1.0
""" 
import os
import sys
import csv
import argparse
import subprocess as sp
import numpy as np
import inspect
import cairosvg
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import pydicom
from pydicom.datadict import tag_for_keyword

class myRun:
    def __init__(self,list=None,debug=None,verbose=None,path=None):
        self.list=list
        self.debug=debug
        self.verbose=verbose
        self.path=path  ##set path in command line like "./run.py -d path"

    def run_it(self):
        if not list:
            if self.debug:
                Util().debug_print("list is empty")
            sys.exit(1)
        for e in self.list:
            e=e.replace("sub-","")
            if self.path==None: 
                cmd="./XNAT_file_pipeline.py -L -id "+e
            else:
                cmd="./XNAT_file_pipeline.py -id "+e

            out,err,ret=Util().run_cmd(cmd)
            if ret:
                Util().tprint("excute command::Not OK: "+cmd)
                Util().debug_print("run_cmd failed")
            else:
                Util().tprint("excute command::OK: "+cmd)

class Util:
    def __int__(self, debug=None,verbose=None,local=None):
        self.name=''
        self.data=[]
        self.debug=debug
        self.verbose=verbose
        self.local=local

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

    def tprint(self, *args):
        tempa = ' '.join(str(a) for a in args)
        print(str(datetime.now().strftime('%Y-%m-%d %H:%M%S')) + " " + tempa)    

    def debug_print(self, message):
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

#################################################################################
def get_id_in_file(file_path, keyword, debug=None):
    filter='PipelineOutputs/bids'
    cup_id_list=[]
    try:
        with open(file_path, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                if keyword in line and filter in line:
                    # Split the line (in file)
                    #line is a file path format: ./PipelineOutputs/bids/sub-CUPS003/ses-A
                    drive, path = os.path.splitdrive(line)
                    # Split the path into parts
                    path_parts = path.split(os.sep)
                    # Include the drive as the first element if it exists
                    if drive:
                        path_parts.insert(0, drive)
                    elem=path_parts[3].strip("\n")
                    if keyword in elem and elem not in cup_id_list:
                            cup_id_list.append(elem)
                    if debug:
                        print(f"Line {line_number}: {line.strip()}")
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    cup_id_list.sort()
    if debug:
        #printf 10 items per line from the list
        for i, a in enumerate(cup_id_list):
            print (a,) 
            if i % 10 == 9: 
                print ("\n")
        #print(cup_id_list) ##this will print whole list in one line
        print("total number of cups_ids: "+ str(len(cup_id_list)))
    return cup_id_list

def main():
    parser = argparse.ArgumentParser(description="Script to process user arguments")
    
    # Define command-line arguments
    parser.add_argument('-i', '--input', help='Input file', required=False)
    parser.add_argument('-o', '--outdir', help='Output dir path', required=False)
    parser.add_argument('-d', '--directory', help='Directory path', required=False)
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity (up to 3 levels).")
    parser.add_argument("-D", "--debug", action="store_true", help="Enable debug mode.")
    
    args = parser.parse_args()
    
    # Access the parsed arguments, # Add your processing logic here
    input_file = args.input
    out_dir = args.outdir
    input_directory = args.directory
    verbosity = args.verbose
    debug_mode = args.debug

    #output directory:
    if not args.outdir:
        out_dir='./dcm_dir'
        
    if debug_mode:
        print("Debug mode is enabled.")
        print(f"Input file: {args.input}")
        print(f"Output dir path: {out_dir}")
        print(f"Directory: {args.directory}")
        print(f"Verbose: {'Yes' if args.verbose else 'No'}")
        print(f"Debug: {'Yes' if args.debug else 'No'}")
    
    if verbosity >= 1:
        print("This is a verbose message.")
    
    if verbosity >= 2:
        print("This is an even more verbose message.")
    
    if verbosity >= 3:
        print("You really like to see a lot of messages!")

    #get CUP list from CUPS list log file passed from command line:
    
    
    #id_list=["CUPS003","CUPS004"]
    keyword='sub-CUPS'
    id_list=get_id_in_file(input_file,keyword,debug_mode)

    myrun=myRun(id_list,debug_mode,verbosity,input_directory)
    myrun.run_it()

if __name__ == "__main__":
    main()

