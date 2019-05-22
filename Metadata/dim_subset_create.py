"""
- Create new private Subset in TM1
- Read the subset and its elements
- Delete the subset in TM1
"""
import configparser
config = configparser.ConfigParser()
config.read('..\config.ini')

from TM1py.Objects import Subset
from TM1py.Services import TM1Service

dimension_name = "Region"
subset_name = "TM1py Subset"
elements = ['1', '2', '3']

with TM1Service(**config['tm1srv01']) as tm1:

    # create subset
    s = Subset(dimension_name=dimension_name, subset_name=subset_name, alias='', elements=elements)
    tm1.dimensions.subsets.create(subset=s, private=True)

    # get it and print out the elements
    s = tm1.dimensions.subsets.get(dimension_name=dimension_name, subset_name=subset_name, private=True)
    print(s.elements)

    # delete it
    tm1.dimensions.subsets.delete(dimension_name=dimension_name, subset_name=subset_name, private=True)

