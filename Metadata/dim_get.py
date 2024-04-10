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
        dimension = tm1.dimensions.get(dimension_name=dimension_name)
    except:
        raise SystemExit(f'No dimension named {dimension_name}')

    with open(f'../Outputs/{dimension_name}_info.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        # iterate through hierarchies
        for hierarchy in dimension:
            writer.writerow(['Hierarchy Name: {}'.format(hierarchy.name)])
            # iterate through Elements in hierarchy
            for element in hierarchy:
                writer.writerow(['Element Name: {} Index: {} Type: {}'.format(element.name, str(element.index), element.element_type)])

            # iterate through Subsets
            for subset in hierarchy.subsets:
                writer.writerow(['Subset Name: {}'.format(subset)])

            # iterate through Edges
            for parent, child in hierarchy.edges:
                writer.writerow([".Parent Name: {}, Component Name: {}".format(parent, child)])
                parent_child = {}
            
            # print the default member
            writer.writerow(['Default Member: {}'.format(hierarchy.default_member)])
        
        writer.writerow([])
        writer.writerow([f'Cubes containing {dimension_name} dimension:'])
        for cube in tm1.cubes.search_for_dimension(dimension_name):
            writer.writerow([cube])
