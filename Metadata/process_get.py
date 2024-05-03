"""
Query a Process from the TM1 model
"""
import configparser

from TM1py.Services import TM1Service
import os
from TM1py.Services import TM1Service

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
with TM1Service(**config['tm1srv01']) as tm1:
    # read Process
    p = tm1.processes.get('tm1py_test')

    # print variables, parameters, ...
    print('Parameters: \r\n' + str(p.parameters))
    print('Variables: \r\n' + str(p.variables))
    print('Prolog: \r\n' + str(p.prolog_procedure))
    print('Metadata: \r\n' + str(p.metadata_procedure))
    print('Data: \r\n' + str(p.data_procedure))
    print('Epilog: \r\n' + str(p.epilog_procedure))
