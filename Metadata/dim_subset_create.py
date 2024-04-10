"""
- Create new private Subset in TM1
- Read the subset and its elements
- Delete the subset in TM1
"""
import configparser
import os
import csv
from TM1py.Objects import Subset
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
dimension_name = input('Enter dimension name: ')
subset_name = input('Enter new subset name: ')
elements = []

with TM1Service(**config['tm1srv01']) as tm1:
    try:
        dimension = tm1.dimensions.get(dimension_name=dimension_name)
    except:
        raise SystemExit(f'No dimension named {dimension_name}')
    element_to_add = input('Enter element name to add (empty: end):')
    while element_to_add:
        if not(tm1.elements.exists(dimension_name=dimension_name,hierarchy_name=dimension_name,element_name=element_to_add)):
            print(f'{element_to_add} does not exist')
        else:
            elements.append(element_to_add)
        element_to_add = input('Enter element name to add (empty: end):')

    # create subset
    s = Subset(dimension_name=dimension_name, subset_name=subset_name, alias='', elements=elements)
    tm1.dimensions.subsets.create(subset=s, private=False)

    # get it and print out the elements
    s = tm1.dimensions.subsets.get(dimension_name=dimension_name, subset_name=subset_name, private=False)
    print(s.elements)

    # delete it
    tm1.dimensions.subsets.delete(dimension_name=dimension_name, subset_name=subset_name, private=False)
