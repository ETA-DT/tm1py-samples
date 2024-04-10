"""
Get a chore from TM1
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

chore_name = input('Enter chore name:')

# Connection to TM1 Server
with TM1Service(**config['tm1srv01']) as tm1:
    # Read Chore:
    try:
        c = tm1.chores.get(chore_name)
    except:
        raise SystemExit(f'No chore named {chore_name}')
    print(f'StartTime: {c.start_time}')
    print(f'Frequency: {c.frequency}')
    # Print out the tasks
    for task in c.tasks:
        print("Process: {} Parameters: {}".format(task, task.parameters))
        
