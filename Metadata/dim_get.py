"""
Get a random dimension from the TM1 model and print out its details
"""
import configparser
import random
import os
import csv
from TM1py.Services import TM1Service

def set_current_directory():
    abspath = os.path.abspath(__file__)         # file absolute path
    directory = os.path.dirname(abspath)        # current file parent directory
    os.chdir(directory)
    return directory

CURRENT_DIRECTORY = set_current_directory()

config = configparser.ConfigParser()
config.read(r'..\config.ini')

dimension_name = input('Enter dimension name: ')

# Connection to TM1. Needs Address, Port, Credentials, and SSL
with TM1Service(**config['tm1srv01']) as tm1:
    try:
        c = tm1.dimensions.get(dimension_name)
    except:
        raise SystemExit(f'No dimension named {dimension_name}')
    dimension = tm1.dimensions.get(dimension_name=dimension_name)

    # iterate through hierarchies
    for hierarchy in dimension:
        print('Hierarchy Name: {}'.format(hierarchy.name))
        # iterate through Elements in hierarchy
        for element in hierarchy:
            print('Element Name: {} Index: {} Type: {}'.format(element.name, str(element.index), element.element_type))
        # iterate through Subsets
        for subset in hierarchy.subsets:
            print('Subset Name: {}'.format(subset))
        # iterate through Edges
        for parent, child in hierarchy.edges:
            print("Parent Name: {}, Component Name: {}".format(parent, child))

        # print the default member
        print('Default Member: {}'.format(hierarchy.default_member))
