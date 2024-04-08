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
config.read(r'..\config.ini')

tm1_master = TM1Service(**config['tm1srv01'])
tm1_other = TM1Service(**config['tm1srv02'])

# while True:
dimension_master = tm1_master.dimensions.get(dimension_name="dimension_test")
dimension_other = tm1_other.dimensions.get(dimension_name="dimension_test")

if dimension_master != dimension_other:
    print(f"Recognized changes. Updating dimension: '{dimension_master.name}'")
    tm1_other.dimensions.update(dimension_master)

subsets_names = tm1_master.subsets.get_all_names("dimension_test")
for subsets_name in subsets_names:
    subset_master = tm1_master.subsets.get(subsets_name, dimension_name="dimension_test")

    subset_other = tm1_other.subsets.get(subsets_name, dimension_name="dimension_test")
    if subset_master != subset_other:
        print(f"Recognized changes. Updating Subset: '{subsets_name}'")
        tm1_other.subsets.update(subset_master)

hierarchy_names = tm1_master.hierarchies.get_all_names(dimension_name="dimension_test")
for hierarchy_name in hierarchy_names:
    hierarchy_master = tm1_master.hierarchies.get(dimension_name="dimension_test",hierarchy_name=hierarchy_name)

    hierarchy_other = tm1_other.hierarchies.get(dimension_name="dimension_test",hierarchy_name=hierarchy_name)
    if hierarchy_master.element_attributes != hierarchy_other.element_attributes:
        print(f"Recognized changes. Updating Hierarchy: '{hierarchy_name}'")
        tm1_other.hierarchies.update(hierarchy_master)
    tm1_other.hierarchies.update_element_attributes(hierarchy_master,keep_existing_attributes=True)
    # time.sleep(2)
