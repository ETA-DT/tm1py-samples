""" 
Get a Process from TM1. Update it. Push it back to TM1.
"""
import configparser
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
    # read process
    p = tm1.processes.get('tm1py_test')

    # modify process
    p.datasource_type = 'None'
    p.epilog_procedure = "nRevenue = 100000;\r\nsCostCenter = 'UK01';"
    # p.remove_parameter('pCompanyCode')
    # p.add_parameter('pBU', prompt='', value='UK02')

    # update
    tm1.processes.update(p)
