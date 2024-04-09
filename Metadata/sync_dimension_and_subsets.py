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

dimension_name = "dimension_test"
dimension_master = tm1_master.dimensions.get(dimension_name=dimension_name)                 # main dimension
dimension_other = tm1_other.dimensions.get(dimension_name=dimension_name)                   # dimension to sync

if dimension_master != dimension_other:                                                     # sync dimension
    print(f"Recognized changes. Updating dimension: '{dimension_master.name}'")         
    tm1_other.dimensions.update(dimension_master)

hierarchy_names = tm1_master.hierarchies.get_all_names(dimension_name=dimension_name)
for hierarchy_name in hierarchy_names:
    hierarchy_master = tm1_master.hierarchies.get(dimension_name=dimension_name,hierarchy_name=hierarchy_name)
    hierarchy_other = tm1_other.hierarchies.get(dimension_name=dimension_name,hierarchy_name=hierarchy_name)
    if hierarchy_master.element_attributes != hierarchy_other.element_attributes:
        print(f"Recognized changes. Updating Hierarchy: '{hierarchy_name}'")
        tm1_other.hierarchies.update(hierarchy_master)

subsets_names = tm1_master.subsets.get_all_names(dimension_name)                                # sync subsets
for subsets_name in subsets_names:
    subset_master = tm1_master.subsets.get(subsets_name, dimension_name=dimension_name)         # main subsets
    if not(tm1_other.subsets.exists(subset_name=subsets_name, dimension_name=dimension_name)):
        print(f"Recognized changes. Creating Subset: '{subsets_name}'")
        tm1_other.subsets.create(subset=subset_master)
    subset_other = tm1_other.subsets.get(subsets_name, dimension_name=dimension_name)           # subsets to sync
    if subset_master != subset_other:
        print(f"Recognized changes. Updating Subset: '{subsets_name}'")
        tm1_other.subsets.update(subset_master)

cube_name = '}'+f'ElementAttributes_{dimension_name}'
cube_attribute_master = tm1_master.cubes.get(cube_name=cube_name)
cube_attribute_other  = tm1_other.cubes.get(cube_name=cube_name)
cube_dimensions_names = tm1_master.cubes.get_dimension_names(cube_name=cube_name)

cells_dict = dict()
all_elements = []
for dimension_name in cube_dimensions_names:
    element_by_dim = []
    hierarchies = tm1_master.hierarchies.get_all_names(dimension_name=dimension_name)
    element_by_dim += tm1_master.elements.get_element_names(dimension_name=dimension_name,hierarchy_name=hierarchies[0])
    all_elements += [element_by_dim]

for element_name_2 in all_elements[1]:
    for element_name_1 in all_elements[0]:
        cell = [element_name_1,element_name_2]
        cells_dict[tuple(cell)] = tm1_master.cells.get_value(cube_name=cube_name,elements=','.join(cell))

tm1_other.cells.write_values(
    cube_name=cube_name,
    cellset_as_dict=cells_dict,
    dimensions=cube_dimensions_names,
    deactivate_transaction_log=True,
    reactivate_transaction_log=True)

    # time.sleep(2)
