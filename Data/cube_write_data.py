"""
Write data to TM1
"""
import configparser
import time
import os

from TM1py import TM1Service

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

with TM1Service(**config['tm1srv01']) as tm1:
    cube_name = '}ElementAttributes_dimension_test'
    cube_dimensions_names = tm1.cubes.get_dimension_names(cube_name=cube_name)
    # # cellset to store the new data
    # cellset = {}
    # # Populate cellset with coordinates and value pairs
    # cellset[('FY 2004 Budget', 'UK', 'Finance', 'Utilities', 'local', 'input', 'Apr-2005')] = 2312
    # cellset[('FY 2004 Budget', 'UK', 'Finance', 'Utilities', 'local', 'input', 'May-2005')] = 2214
    # cellset[('FY 2004 Budget', 'UK', 'Finance', 'Utilities', 'local', 'input', 'Jun-2005')] = 2451
    # cellset[('FY 2004 Budget', 'UK', 'Finance', 'Utilities', 'local', 'input', 'Jul-2005')] = 2141
    # cellset[('FY 2004 Budget', 'UK', 'Finance', 'Utilities', 'local', 'input', 'Aug-2005')] = 2621
    # # send the cellset to TM1
    # tm1.cubes.cells.write_values('Plan_BudgetPlan', cellset)

    cells = dict()
    elements = []
    for dimension_name in cube_dimensions_names:
        elems = []
        hierarchies = tm1.hierarchies.get_all_names(dimension_name=dimension_name)
        elems += tm1.elements.get_element_names(dimension_name=dimension_name,hierarchy_name=hierarchies[0])
        elements += [elems]
    print(elements)

    for element_name_2 in elements[1]:
        for element_name_1 in elements[0]:
            cells[tuple([element_name_1,element_name_2])] = 2
            tm1.cells.write_values(
                cube_name=cube_name,
                cellset_as_dict=cells,
                dimensions=cube_dimensions_names,
                deactivate_transaction_log=True,
                reactivate_transaction_log=True)
