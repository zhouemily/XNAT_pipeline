#!/usr/bin/env python

import netrc
import xnat
import os

##use xnatpy and netrc modules
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
#port = '8104'
username, password = get_credentials(host)

# Connect to the XNAT server with login info in ~/.netrc file for security (No login info hard coded in script) 
with xnat.connect(f'http://{host}', user=username, password=password, debug=False) as session:
    if session.connect:
        projects = session.projects
        # Iterate through the projects and print their IDs
        for project_id in projects:
            print(f"Project ID: {project_id}")

        subjects = session.subjects
        for subject_id in subjects:
            print(subject_id)

        project_id='CUPS'    #select this only one
        try:
            project = session.projects[project_id]
            # Retrieve the XNAT project object corresponding to the project ID
            print(">>>project_id: "+project_id)
        except KeyError:
            project = None
            print("project is None")

        zip_path='./CUPS.DCM.zip'
        zip_full_path = os.path.abspath(zip_path)
        print("zip_file: "+zip_full_path)
        
        #session.services.import_(zip_full_path,project='CUPS')  ##try to upload to prearchive to be safe
        #session.services.import_(zip_full_path,project='CUPS', subject='test002') ## should not use subject here since it is unknown here

        prearchive_session = session.services.import_(zip_full_path, project='CUPS', destination='/prearchive')
        print("zip file uploaded to prearchive: "+zip_path)
        #print(prearchive_session)
        #session.prearchive.sessions()
        #prearchive_session = session.prearchive.sessions()[0]
        #experiment = prearchive_session.archive(subject='ANONYMIZ3', experiment='ANONYMIZ3')
        #print(experiment)


##When working with a session it is always important to disconnect when done:
session.disconnect()

"""
#sample code for import via prearchive:
prearchive_session = session.services.import_('/home/hachterberg/temp/ANONYMIZ.zip', project='brainimages', destination='/prearchive')
print(prearchive_session)
session.prearchive.sessions()
prearchive_session = session.prearchive.sessions()[0]
experiment = prearchive_session.archive(subject='ANONYMIZ3', experiment='ANONYMIZ3')
print(experiment)
"""
