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
tm1_master = TM1Service(**config['tm1srv01'])
tm1_other = TM1Service(**config['tm1srv02'])

# read process
p_master = tm1_master.processes.get('TM1py process')
p_other = tm1_other.processes.get('TM1py process')

print(p_master.prolog_procedure)

    # # modify process
    # p.datasource_type = 'None'
    # p.epilog_procedure = "nRevenue = 100000;\r\nsCostCenter = 'UK01';"
    # # p.remove_parameter('pCompanyCode')
    # # p.add_parameter('pBU', prompt='', value='UK02')

    # # update
    # tm1.processes.update(p)
