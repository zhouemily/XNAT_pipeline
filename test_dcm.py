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
    #ds = pydicom.dcmread(dicom_file_path, force=False)
    ds = pydicom.dcmread(dicom_file_path, force=True)

    # Print the DICOM dataset
    print(ds)

    # Access the "Patient Comments" attribute
    patient_comments = ds.get((0x0010, 0x4000))
    patient_name = ds.PatientName
    study_date = ds.StudyDate

    if patient_comments:
        # Concatenate the individual elements into a single string
        patient_comment_string = "".join(patient_comments)
        print("Patient Comments:")
        print(patient_comment_string)
    else:
        print("Patient Comments not found or empty in the DICOM file.")
        # Access specific DICOM attributes (e.g., Patient's Name, Study Date)

    # Print specific attributes
    print(f"Patient's Name: {patient_name}")
    print(f"Study Date: {study_date}")

except Exception as e:
    print(f"Error reading the DICOM file: {str(e)}")
