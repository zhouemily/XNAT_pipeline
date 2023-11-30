#!/usr/bin/env python

import netrc
import xnat

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
username, password = get_credentials(host)

# Connect to the XNAT server with login info in ~/.netrc file for security (No login info hard coded in script) 
with xnat.connect(f'http://{host}', user=username, password=password) as session:
    # Your code here, e.g., list all projects
    projects = session.projects
    for project in projects:
        print(project)
    subjects = session.subjects
    for subject in subjects:
        print(subject)

##use xnatpy module, not netrc module to get user and passwd which is not safe, NOT use it
#server_host = "xnat1.beckman.illinois.edu"
#server_port = 8104
#session = xnat.connect(server_host+":"+server_port)
#session = xnat.connect('http://my.xnat.server', user='admin', password='secret')

#To add new data into XNAT it is possible to use the REST import service. 
#It allows you to upload a zip file containing an experiment and XNAT will automatically 
#try to store it in the correct place:

zip_path='./CUPS.DICOM.zip'
project='CUPS'
##subject='' ##comment out for now since not knowing what to use, there are many choices

session.services.import_(zip_path, project, subject)

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
