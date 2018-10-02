"""
BASICS

Contains a set of functions that are called accross the other APIs
"""

import os
from pathlib import Path
from influxdb import InfluxDBClient



# Checks if the provided user key is valid
def valid_key(ukey):

    if ukey == os.environ['greyfish_key']:
        return True
    return False


# Creates a new key (new dir) in the dictionary
# fpl (arr) (str): Contains the list of subsequent directories
# exdic (dict)
def create_new_dirtag(fpl, exdic):

    # New working dictionary
    nwd = exdic

    for qq in range(0, len(fpl)-1):
        nwd = nwd[fpl[qq]]

    # Adds one at the end
    nwd[fpl[-1]] = {"files":[]}

    return exdic


# Returns a dictionary showing all the files in a directory (defaults to working directory)
def structure_in_json(PATH = '.'):

    FSJ = {PATH.split('/')[-1]:{"files":[]}}

    # Includes the current directory
    # Replaces everything before the user
    unpart = '/'.join(PATH.split('/')[:-1])+'/'

    for ff in [str(x).replace(unpart, '').split('/') for x in Path(PATH).glob('**/*')]:

        if os.path.isdir(unpart+'/'.join(ff)):
            create_new_dirtag(ff, FSJ)
            continue

        # Files get added to the list, files
        # Loops through the dict
        nwd = FSJ
        for hh in range(0, len(ff)-1):
            nwd = nwd[ff[hh]]

        nwd["files"].append(ff[-1])

    return FSJ


# Returns a administrative client 
# Default refers to the basic grey server
def idb_admin(db='greyfish'):

    return InfluxDBClient(host = os.environ['URL_BASE'], port = 8086, username = os.environ['INFLUXDB_ADMIN_USER'], 
        password = os.environ['INFLUXDB_ADMIN_PASSWORD'], database = db)


# Returns an incfluxdb client with read-only access
def idb_reader(db='greyfish'):

    return InfluxDBClient(host = os.environ['URL_BASE'], port = 8086, username = os.environ['INFLUXDB_READ_USER'], 
        password = os.environ['INFLUXDB_READ_USER_PASSWORD'], database = db)


# Returns an incfluxdb client with write privileges
def idb_reader(db='greyfish'):

    return InfluxDBClient(host = os.environ['URL_BASE'], port = 8086, username = os.environ['INFLUXDB_WRITE_USER'], 
        password = os.environ['INFLUXDB_WRITE_USER_PASSWORD'], database = db)

