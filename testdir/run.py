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
        self.path=path

    def run_it(self):
        if not list:
            if self.debug:
                Util().debug_print("list is empty")
            sys.exit(1)
        for e in self.list:
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
def main():
    parser = argparse.ArgumentParser(description="Script to process user arguments")
    
    # Define command-line arguments
    parser.add_argument("-f", "--file", type=str, help="Path to the input file.")
    parser.add_argument("-d", "--directory", type=str, help="Path to the input directory.")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity (up to 3 levels).")
    parser.add_argument("-D", "--debug", action="store_true", help="Enable debug mode.")
    
    args = parser.parse_args()
    
    # Access the parsed arguments
    input_file = args.file
    input_directory = args.directory
    verbosity = args.verbose
    debug_mode = args.debug
    
    if debug_mode:
        print("Debug mode is enabled.")
    
    if input_file:
        print(f"Input file: {input_file}")
    
    if input_directory:
        print(f"Input directory: {input_directory}")
    
    print(f"Verbosity level: {verbosity}")
    
    if verbosity >= 1:
        print("This is a verbose message.")
    
    if verbosity >= 2:
        print("This is an even more verbose message.")
    
    if verbosity >= 3:
        print("You really like to see a lot of messages!")

    id_list=["CUPS003","CUPS004"]
    myrun=myRun(id_list,debug_mode,verbosity,input_directory)
    myrun.run_it()

if __name__ == "__main__":
    main()

