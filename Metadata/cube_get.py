"""
Get a Cube from TM1
"""
import configparser
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

cube_name = input('Enter cube name: ')

with TM1Service(**config['tm1srv01']) as tm1:
    try:
        c = tm1.cubes.get(cube_name)
    except:
        raise SystemExit(f'No cube named {cube_name}')
    print(c.name)
    print(c.dimensions)
    if c.has_rules:
        print(c.rules)
