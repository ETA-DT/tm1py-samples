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

    # Determine the used groups from }ClientGroups Cube
    mdx = "SELECT " \
          "NON EMPTY {TM1SUBSETALL( [}Clients] )} on ROWS, " \
          "NON EMPTY {TM1SUBSETALL( [}Groups] )} ON COLUMNS " \
          "FROM [}ClientGroups]"
    cube_content = tm1.cubes.cells.execute_mdx(mdx, ['Value'])

    used_groups = {cell['Value'] for cell in cube_content.values() if cell['Value'] != ''}

    # Determine the unused groups
    unused_groups = set(all_groups) - used_groups

    # Print out the unused groups
    print(unused_groups)

    if generate_output_file == 'Y':
        with open('../Outputs/unused_groups.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Unused security groups:"])
            write_elem_by_row(writer,list(unused_groups))

