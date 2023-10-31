#!/usr/bin/env python

import pydicom
import sys

# Check if the command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_dicom_file>")
    sys.exit(1)

# Specify the path to the DICOM file
dicom_file_path = sys.argv[1]

try:
    # Read the DICOM file with force=True
    ds = pydicom.dcmread(dicom_file_path, force=True)

    # Print the DICOM dataset
    print(ds)

    # Access specific DICOM attributes (e.g., Patient's Name, Study Date)
    patient_name = ds.PatientName
    study_date = ds.StudyDate

    # Print specific attributes
    print(f"Patient's Name: {patient_name}")
    print(f"Study Date: {study_date}")

except Exception as e:
    print(f"Error reading the DICOM file: {str(e)}")

