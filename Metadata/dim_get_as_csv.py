"""
Export a dimension as a csv file (to be imported)
"""
import configparser
import random
import os
import csv
import pandas as pd
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
hierarchy_name = input(f'Enter hierarchy name (default:{dimension_name}): ')
if not(hierarchy_name):
    hierarchy_name = dimension_name

# Connection to TM1. Needs Address, Port, Credentials, and SSL
with TM1Service(**config['tm1srv02']) as tm1:
    try:
        dimension = tm1.dimensions.get(dimension_name)
    except:
        raise SystemExit(f'No dimension named {dimension_name}')
    try:
        hierarchy = tm1.hierarchies.get(dimension_name,hierarchy_name=hierarchy_name)
    except:
        raise SystemExit(f'No hierarchy named {hierarchy_name}')
            
    dataframe = tm1.elements.get_elements_dataframe(dimension_name=dimension_name,hierarchy_name=dimension_name)
    level_names = tm1.elements.get_level_names(dimension_name=dimension_name,hierarchy_name=dimension_name)
    attribute_names = tm1.elements.get_element_attribute_names(dimension_name=dimension_name,hierarchy_name=dimension_name)
    attribute_names.reverse()
    reordered_col = attribute_names + [hierarchy_name] + level_names[1:]
    dataframe_to_export = dataframe.loc[:,reordered_col]
    dataframe_to_export.to_csv(f'../Outputs/{dimension_name}_info.csv',index=False)
