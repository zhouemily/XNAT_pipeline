#!/usr/bin/env python
import xnat

# Connect to XNAT instance
with xnat.connect('http://your.xnat.server', use_netrc=True) as session:
    # Your code here, for example, list all projects
    projects = session.projects
    for project in projects:
        print(project)

# The connection will be automatically closed when exiting the 'with' block

