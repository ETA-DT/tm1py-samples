"""
Get a dimension. Update it and push it back to TM1.

"""
import configparser
import uuid
import os
import TM1py
from TM1py.Services import TM1Service

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

dimension_name = '}DimensionProperties'
# Connection to TM1. Needs Address, Port, Credentials, and SSL
with TM1Service(**config['tm1srv01']) as tm1:
    # get dimension
    dimension = tm1.dimensions.get(dimension_name)

    # get the default hierarchy of the dimension
    h = dimension.hierarchies[0]

    # create new random element name
    element_name = 'TOUPDATE'

    # add elements to hierarchy
    if not(tm1.elements.exists(dimension_name=dimension_name,hierarchy_name=h.name,element_name=element_name)):
        h.add_element(element_name=element_name, element_type='String')
    else:
        print(f'Element {element_name} already exists')

    # add the picklist attribute
    h.add_element_attribute('Pick list','String')
    tm1.dimensions.update(dimension)

    if not(tm1.dimensions.exists('}Picklist')):
        picklist_dim = TM1py.Dimension('}Picklist')
        tm1.dimensions.create(picklist_dim)

    if not(tm1.cubes.exists('}PickList_}DimensionProperties')):
        option_list = 'static:'\
                        'Updated:'\
                        'Elements:'\
                        'Hierarchies/Attributes Values:'\
                        'Hierarchies/Subsets:'\
                        'Attributes Values:'\
                        'Elements/Hierarchies:'\
                        'Elements/Hierarchies/Subsets:'\
                        'Elements/Hierarchies/Attributes Values:'\
                        'Elements/Hierarchies/Subsets/Attributes Values:'\
                        'Elements/Subsets:'\
                        'Elements/Subsets/Attributes Values:'\
                        'Elements/Attributes Values'
        rules = "SKIPCHECK;\n"\
                "\n"\
                f"['TOUPDATE'] = S: IF(SCAN(':',!{'}'}Dimensions) =0,'{option_list}',''); \n"\
                "\n"\
                "FEEDERS;"
        picklist_cube = TM1py.Cube('}PickList_}DimensionProperties',['}Dimensions','}DimensionProperties','}Picklist'],rules=rules)
        tm1.cubes.create(picklist_cube)
    
    # for element in (element for element in tm1.elements.get_element_names(dimension_name='}Dimensions',hierarchy_name='}Dimensions') if (':' not in element)):              # exclure les hiérarchies
    #     tm1.cells.write_value(value='Updated',cube_name='}DimensionProperties',element_tuple=(element,'TOUPDATE'),dimensions=['}Dimensions','}DimensionProperties'])

    # write Hierarchy back to TM1
    tm1.dimensions.update(dimension)
