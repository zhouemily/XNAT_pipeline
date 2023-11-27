#!/usr/bin/env python

import xnat

##use xnatpy module
server_host = "xnat1.beckman.illinois.edu"
server_port = 8104
session = xnat.connect(server_host+":"+server_port)
session = xnat.connect('http://my.xnat.server', user='admin', password='secret')

with xnat.connect('http://my.xnat.server') as session:
    print session.projects

#To add new data into XNAT it is possible to use the REST import service. 
#It allows you to upload a zip file containing an experiment and XNAT will automatically 
#try to store it in the correct place:
zip_path='./dcm_dir/CUPS.DICOM.zip'
project='CUPS'
subject='cpus003'
session.services.import_(zip_path, project, subject)

#Import via prearchive:
prearchive_session = session.services.import_('/home/hachterberg/temp/ANONYMIZ.zip', project='brainimages', destination='/prearchive')
print(prearchive_session)
session.prearchive.sessions()
prearchive_session = session.prearchive.sessions()[0]
experiment = prearchive_session.archive(subject='ANONYMIZ3', experiment='ANONYMIZ3')
print(experiment)

##When working with a session it is always important to disconnect when done:
session.disconnect()
