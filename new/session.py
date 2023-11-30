#!/usr/bin/env python

import netrc
import xnat

def get_credentials(host):
    auth = netrc.netrc().authenticators(host)
    if auth is not None:
        return auth[0], auth[2]  # Returns login and password
    else:
        raise Exception(f"Credentials for '{host}' not found in .netrc")

# Replace with your XNAT server's host
host = 'xnat1.beckman.illinois.edu'
username, password = get_credentials(host)

# Connect to the XNAT server
with xnat.connect(f'http://{host}', user=username, password=password) as session:
    # Your code here, e.g., list all projects
    projects = session.projects
    for project in projects:
        print(project)

