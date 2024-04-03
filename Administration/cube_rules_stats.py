"""
Read rules from all cubes and sort cubes by some metrics (Number rows, Number feeders,... )
"""

import os
import csv
import configparser
from TM1py.Services import TM1Service
import sys
sys.path.insert(0, 'Functions')
from export_functions import *
# from directory_functions import *

def set_current_directory():
    abspath = os.path.abspath(__file__)         # file absolute path
    directory = os.path.dirname(abspath)        # current file parent directory
    os.chdir(directory)
    return directory

CURRENT_DIRECTORY = set_current_directory()     # redirecting to the current file's directory

config = configparser.ConfigParser()
# storing the credentials in a file is not recommended for purposes other than testing.
# it's better to setup CAM with SSO or use keyring to store credentials in the windows credential manager. Sample:
# Samples/credentials_best_practice.py
config.read(r'..\config.ini')

# Connect to TM1
with TM1Service(**config['tm1srv01']) as tm1:
    cubes = tm1.cubes.get_all()
    with open('..\Outputs\cube_rules_info.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        # cubes with SKIPCHECK
        cubes_with_skipcheck = [cube.name for cube in cubes if cube.skipcheck]
        print("Cubes with SKIPCHECK:")
        print(cubes_with_skipcheck)
        writer.writerow(["Cubes with SKIPCHECK:"])
        write_elem_by_row(writer,cubes_with_skipcheck)


        # cubes with UNDEFVALS
        cubes_with_undefvals = [cube.name for cube in cubes if cube.undefvals]
        print("Cubes with UNDEFVALS:")
        print(cubes_with_undefvals)
        writer.writerow(["Cubes with UNDEFVALS:"])
        write_elem_by_row(writer,cubes_with_undefvals)

        # cubes ordered by the number of rule statements
        cubes.sort(key=lambda cube: len(cube.rules.rule_statements) if cube.has_rules else 0, reverse=True)
        cubes_sorted_rule_statements = [cube.name for cube in cubes]
        print("Cubes sorted by number of Rule Statements:")
        print(cubes_sorted_rule_statements)
        writer.writerow(["Cubes sorted by number of Rule Statements:"])
        write_elem_by_row(writer,cubes_sorted_rule_statements)

        # cubes ordered by the number of feeder statements
        cubes.sort(key=lambda cube: len(cube.rules.feeder_statements) if cube.has_rules else 0, reverse=True)
        cubes_sorted_feeder_statements = [cube.name for cube in cubes]
        print("Cubes sorted by number of Feeder Statements:")
        print(cubes_sorted_feeder_statements)
        writer.writerow(["Cubes sorted by number of Feeder Statements:"])
        write_elem_by_row(writer,cubes_sorted_feeder_statements)