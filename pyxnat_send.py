#!/usr/bin/env python

import netrc
import pyxnat

##use pyxnat and netrc modules (DO NOT use xnatpy module, it is NOT working well so far)
#creat ~/.netrc to store "machine", user, and passwd for security purpose
##use encrytion (Not plain passwd) to be safer if needed

def get_credentials(host):
    auth = netrc.netrc().authenticators(host)
    if auth is not None:
        return auth[0], auth[2]  # Returns login and password
    else:
        raise Exception(f"Credentials for '{host}' not found in .netrc")

# Replace with your XNAT server's host
host = 'xnat1.beckman.illinois.edu'
username, password = get_credentials(host)


# Connect to XNAT instance
xnat = pyxnat.Interface(server=host, user=username, password=password)

# Specify the project, subject, and experiment
project_id = 'my_project_id'
subject_id = 'my_subject_id'
experiment_id = 'my_experiment_id'

# Check if the project exists, if not create it
if not xnat.select.project(project_id).exists():
    xnat.select.project(project_id).create()

# Check if the subject exists, if not create it
if not xnat.select.project(project_id).subject(subject_id).exists():
    xnat.select.project(project_id).subject(subject_id).create()

# Check if the experiment exists, if not create it
if not xnat.select.project(project_id).subject(subject_id).experiment(experiment_id).exists():
    xnat.select.project(project_id).subject(subject_id).experiment(experiment_id).create()

# Path to your ZIP file
zip_file_path = './CUPS.DICOM.zip'

# Upload the ZIP file
#xnat.select.project(project_id).subject(subject_id).experiment(experiment_id).resource('resource_name').file('file.zip').put(zip_file_path, format='zip', content='YOUR_CONTENT_TYPE')

xnat.select.project(project_id).subject(subject_id).experiment(experiment_id).resource('resource_name').file('file.zip').put(zip_file_path, format='zip', content='DICOM')

# Close the connection
xnat.disconnect()
