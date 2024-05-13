""" 
Get a Process from TM1. Update it. Push it back to TM1.
"""
import configparser
import os
from TM1py.Services import TM1Service
from operator import itemgetter

def set_current_directory():
    abspath = os.path.abspath(__file__)         # file absolute path
    directory = os.path.dirname(abspath)        # current file parent directory
    os.chdir(directory)
    return directory

CURRENT_DIRECTORY = set_current_directory()
config = configparser.ConfigParser()
# storing the credentials in a file is not recommended for purposes other than testing.
# it's better to setup CAM with SSO or use keyring to store credentials in the windows credential manager. Sample:
# Samples/credentials_best_practice.py
config.read(r'..\config.ini')

# connection to TM1 Server
tm1_master = TM1Service(**config['tm1srv01'])
tm1_other = TM1Service(**config['tm1srv02'])

try:
    process_name = input('Which process to synchronize ? ')
except:
    raise SystemExit(f'No process named {process_name}') 

# read process
p_master = tm1_master.processes.get(process_name)
p_other = tm1_other.processes.get(process_name)

tm1_other.processes.delete(process_name)
tm1_other.processes.create(p_master)

