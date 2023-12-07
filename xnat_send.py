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
port = '8104'
#host2 = host+':'+port ##not working,  wrong  port number??
username, password = get_credentials(host)

# Connect to the XNAT server with login info in ~/.netrc file for security (No login info hard coded in script) 
with xnat.connect(f'http://{host}', user=username, password=password, debug=True) as session:
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
        
        session.services.import_(zip_full_path,project='CUPS', subject='test002')


#subject='XNAT03_New003' ##comment out for now since not knowing what to use, there are many choices
#session.services.import_(zip_path, project, subject)

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
