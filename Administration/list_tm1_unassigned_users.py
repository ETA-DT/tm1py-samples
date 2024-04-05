"""
Find all security groups, that are not used
"""
import configparser
from TM1py.Services import TM1Service
import os
import csv
import sys
sys.path.insert(0, 'Functions')
from export_functions import *

def set_current_directory():
    abspath = os.path.abspath(__file__)         # file absolute path
    directory = os.path.dirname(abspath)        # current file parent directory
    os.chdir(directory)
    return directory

CURRENT_DIRECTORY = set_current_directory()

generate_output_file = input("Would you like to generate the results in an output csv file? (Y/N):")

config = configparser.ConfigParser()
config.read(r'..\config.ini')

with TM1Service(**config['tm1srv01']) as tm1:
    # Get all groups
    all_groups = tm1.security.get_all_groups()
    all_users = tm1.security.get_all_user_names()

    # Determine the used groups from }ClientGroups Cube
    mdx = "SELECT " \
          "NON EMPTY {TM1SUBSETALL( [}Clients] )} on ROWS, " \
          "NON EMPTY {TM1SUBSETALL( [}Groups] )} ON COLUMNS " \
          "FROM [}ClientGroups]"
    
    assigned_users = tm1.cubes.cells.execute_mdx_dataframe(mdx=mdx)['}Clients']
    
    all_groups = list(tm1.elements.get_all_leaf_element_identifiers(dimension_name='}Groups',hierarchy_name='}Groups'))
    
    # Determine the unused groups
    unassigned_users = set(all_users) - set(assigned_users)

    # Print out the unused groups
    print(unassigned_users)

    if generate_output_file == 'Y':
        with open('../Outputs/unassigned_users.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Unassigned users:"])
            write_elem_by_row(writer,list(unassigned_users))

